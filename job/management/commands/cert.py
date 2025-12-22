"""
证书管理命令（跨平台：Windows / Linux / macOS）

使用方法：
    python manage.py cert --generate    # 生成自签名证书
    python manage.py cert --renew       # 续签证书（重新生成）
    python manage.py cert --info        # 查看证书信息
    python manage.py cert --days 730    # 指定有效期（天）

说明：
    - 如果系统存在 openssl，会优先使用 openssl 生成（保持原逻辑）
    - 如果没有 openssl（Windows 常见），则使用 Python 的 cryptography 生成/读取证书
"""

import ipaddress
import os
import shutil
import subprocess
from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

try:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    _HAS_CRYPTOGRAPHY = True
except Exception:  # pragma: no cover
    _HAS_CRYPTOGRAPHY = False


class Command(BaseCommand):
    help = 'SSL 证书管理：生成、续签、查看证书信息'

    def add_arguments(self, parser):
        parser.add_argument(
            '--generate', '-g',
            action='store_true',
            help='生成新的自签名证书'
        )
        parser.add_argument(
            '--renew', '-r',
            action='store_true',
            help='续签证书（重新生成）'
        )
        parser.add_argument(
            '--info', '-i',
            action='store_true',
            help='查看证书信息'
        )
        parser.add_argument(
            '--days', '-d',
            type=int,
            default=365,
            help='证书有效期（天），默认 365'
        )
        parser.add_argument(
            '--cn',
            type=str,
            default='localhost',
            help='证书 Common Name，默认 localhost'
        )
        parser.add_argument(
            '--no-openssl',
            action='store_true',
            help='强制不使用 openssl（即使存在），改用 Python 生成证书（便于 Windows 环境）'
        )
        parser.add_argument(
            '--trusted',
            action='store_true',
            help='生成本地可信证书（需要安装 mkcert）'
        )

    def handle(self, *args, **options):
        # 证书目录
        base_dir = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        cert_dir = os.path.join(base_dir, 'certs')
        cert_file = os.path.join(cert_dir, 'cert.pem')
        key_file = os.path.join(cert_dir, 'key.pem')

        if options['generate']:
            self.generate_cert(cert_dir, cert_file, key_file, options['days'], options['cn'], options['no_openssl'], options['trusted'])
        elif options['renew']:
            self.renew_cert(cert_dir, cert_file, key_file, options['days'], options['cn'], options['no_openssl'], options['trusted'])
        elif options['info']:
            self.show_info(cert_file, options['no_openssl'])
        else:
            self.stdout.write(self.style.WARNING('请指定操作：--generate, --renew 或 --info'))
            self.stdout.write('使用 python manage.py cert --help 查看帮助')

    def generate_cert(self, cert_dir, cert_file, key_file, days, cn, no_openssl=False, trusted=False):
        """生成自签名证书"""
        # 检查是否已存在
        if os.path.exists(cert_file) or os.path.exists(key_file):
            self.stdout.write(self.style.WARNING('证书已存在！如需重新生成，请使用 --renew'))
            return

        self._create_cert(cert_dir, cert_file, key_file, days, cn, no_openssl=no_openssl, trusted=trusted)

    def renew_cert(self, cert_dir, cert_file, key_file, days, cn, no_openssl=False, trusted=False):
        """续签（重新生成）证书"""
        # 备份旧证书
        if os.path.exists(cert_file):
            backup_name = f"cert.pem.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
            os.rename(cert_file, os.path.join(cert_dir, backup_name))
            self.stdout.write(f'已备份旧证书: {backup_name}')
        if os.path.exists(key_file):
            backup_name = f"key.pem.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
            os.rename(key_file, os.path.join(cert_dir, backup_name))
            self.stdout.write(f'已备份旧私钥: {backup_name}')

        self._create_cert(cert_dir, cert_file, key_file, days, cn, no_openssl=no_openssl, trusted=trusted)

    def _openssl_available(self) -> bool:
        try:
            subprocess.run(['openssl', 'version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _find_mkcert(self):
        exe = 'mkcert.exe' if os.name == 'nt' else 'mkcert'
        p = shutil.which('mkcert')
        if p:
            return p
        candidates = []
        if os.name == 'nt':
            la = os.environ.get('LOCALAPPDATA', '')
            up = os.environ.get('USERPROFILE', '')
            candidates.extend([
                os.path.join(la, 'Microsoft', 'WinGet', 'Links', 'mkcert.exe'),
                os.path.join(la, 'Programs', 'mkcert', 'mkcert.exe'),
                os.path.join(up, 'scoop', 'apps', 'mkcert', 'current', 'mkcert.exe'),
                'C:\\Program Files\\mkcert\\mkcert.exe',
            ])
            pkg_dir = os.path.join(la, 'Microsoft', 'WinGet', 'Packages')
            if os.path.isdir(pkg_dir):
                try:
                    for n in os.listdir(pkg_dir):
                        p2 = os.path.join(pkg_dir, n, 'mkcert.exe')
                        if os.path.exists(p2):
                            return p2
                except Exception:
                    pass
        for c in candidates:
            if c and os.path.exists(c):
                return c
        return None

    def _mkcert_available(self) -> bool:
        path = self._find_mkcert()
        if not path:
            return False
        try:
            subprocess.run([path, '-CAROOT'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _create_cert(self, cert_dir, cert_file, key_file, days, cn, no_openssl=False, trusted=False):
        """创建证书的核心逻辑"""
        # 创建目录
        os.makedirs(cert_dir, exist_ok=True)

        # 生成证书
        self.stdout.write(f'正在生成证书 (有效期: {days} 天, CN: {cn})...')

        if trusted:
            if not self._mkcert_available():
                raise CommandError('未检测到 mkcert。请安装 mkcert 后重试：参见 https://github.com/FiloSottile/mkcert')
            try:
                mk = self._find_mkcert()
                if not mk:
                    raise CommandError('未检测到 mkcert。请安装 mkcert 后重试：参见 https://github.com/FiloSottile/mkcert')
                subprocess.run([mk, '-install'], capture_output=True, text=True, encoding='utf-8', errors='ignore', check=True)
                names = ['localhost', '127.0.0.1', '::1']
                if cn and cn not in names:
                    names.append(cn)
                cmd = [mk, '-key-file', key_file, '-cert-file', cert_file] + names
                subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', check=True)
                self._print_success(cert_file, key_file, provider='mkcert', trusted=True)
                return
            except subprocess.CalledProcessError as e:
                raise CommandError(f'证书生成失败(mkcert): {e.stderr}')

        use_openssl = (not no_openssl) and self._openssl_available()

        if use_openssl:
            cmd = [
                'openssl', 'req', '-x509',
                '-newkey', 'rsa:4096',
                '-keyout', key_file,
                '-out', cert_file,
                '-days', str(days),
                '-nodes',
                '-subj', f'/CN={cn}'
            ]
            try:
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                self._print_success(cert_file, key_file, provider='OpenSSL', trusted=False)
                return
            except subprocess.CalledProcessError as e:
                msg = (e.stderr or '').lower()
                if 'openssl.cnf' in msg or 'no such file or directory' in msg:
                    self.stdout.write(self.style.WARNING('OpenSSL 配置不可用，自动切换为 Python 方式生成证书'))
                else:
                    raise CommandError(f'证书生成失败(OpenSSL): {e.stderr}')

        # Python 生成（Windows 友好）
        if not _HAS_CRYPTOGRAPHY:
            raise CommandError('未安装 cryptography，无法在无 openssl 环境生成证书。请运行: pip install cryptography')

        self._create_cert_with_python(cert_file, key_file, days, cn)
        self._print_success(cert_file, key_file, provider='cryptography(Python)', trusted=False)

    def _print_success(self, cert_file, key_file, provider: str, trusted: bool):
        self.stdout.write(self.style.SUCCESS('[OK] 证书生成成功！'))
        self.stdout.write(f'  生成方式: {provider}')
        self.stdout.write(f'  证书文件: {cert_file}')
        self.stdout.write(f'  私钥文件: {key_file}')
        printed_days = False
        if _HAS_CRYPTOGRAPHY:
            try:
                with open(cert_file, 'rb') as f:
                    cert_data = f.read()
                c = x509.load_pem_x509_certificate(cert_data)
                nb = c.not_valid_before
                na = c.not_valid_after
                days = (na - nb).days
                self.stdout.write(f'  有效期: {days} 天')
                printed_days = True
            except Exception:
                pass
        if not printed_days:
            self.stdout.write('  有效期: 未读取')
        self.stdout.write('')
        if not trusted:
            self.stdout.write(self.style.WARNING('提示: 自签名证书在浏览器中会显示"不安全"警告，这是正常的'))

    def _create_cert_with_python(self, cert_file, key_file, days, cn):
        # 私钥
        key = rsa.generate_private_key(public_exponent=65537, key_size=4096)

        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn)])
        issuer = subject

        now = datetime.now(timezone.utc)
        not_before = now - timedelta(minutes=1)
        not_after = now + timedelta(days=int(days))

        # SAN：尽量覆盖开发常用地址
        alt_names = [
            x509.DNSName('localhost'),
            x509.DNSName(cn),
            x509.IPAddress(ipaddress.ip_address('127.0.0.1')),
            x509.IPAddress(ipaddress.ip_address('::1')),
        ]
        # cn 如果是 IP，也加入 SAN
        try:
            alt_names.append(x509.IPAddress(ipaddress.ip_address(cn)))
        except Exception:
            pass

        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(not_before)
            .not_valid_after(not_after)
            .add_extension(x509.SubjectAlternativeName(alt_names), critical=False)
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(private_key=key, algorithm=hashes.SHA256())
        )

        with open(key_file, 'wb') as f:
            f.write(
                key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        with open(cert_file, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

    def show_info(self, cert_file, no_openssl=False):
        """显示证书信息"""
        if not os.path.exists(cert_file):
            self.stdout.write(self.style.ERROR('证书文件不存在，请先使用 --generate 生成'))
            return

        use_openssl = (not no_openssl) and self._openssl_available()

        self.stdout.write(self.style.SUCCESS('=== 证书信息 ==='))

        if use_openssl:
            try:
                result = subprocess.run(
                    ['openssl', 'x509', '-in', cert_file, '-noout', '-text', '-dates'],
                    capture_output=True, text=True, check=True
                )

                lines = result.stdout.split('\n')
                for line in lines:
                    line = line.strip()
                    if 'Not Before' in line or 'Not After' in line:
                        self.stdout.write(f'  {line}')
                    elif 'Subject:' in line:
                        self.stdout.write(f'  {line}')
                    elif 'Issuer:' in line:
                        self.stdout.write(f'  {line}')
                return
            except subprocess.CalledProcessError as e:
                raise CommandError(f'读取证书失败(OpenSSL): {e.stderr}')

        if not _HAS_CRYPTOGRAPHY:
            raise CommandError('未安装 cryptography，无法在无 openssl 环境读取证书信息。请运行: pip install cryptography')

        try:
            with open(cert_file, 'rb') as f:
                cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data)

            self.stdout.write(f'  Subject: {cert.subject.rfc4514_string()}')
            self.stdout.write(f'  Issuer: {cert.issuer.rfc4514_string()}')
            self.stdout.write(f'  Not Before: {cert.not_valid_before}')
            self.stdout.write(f'  Not After : {cert.not_valid_after}')

            try:
                san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
                self.stdout.write('  Subject Alternative Name:')
                for item in san:
                    self.stdout.write(f'    - {item.value}')
            except Exception:
                pass
        except Exception as e:
            raise CommandError(f'读取证书失败(Python): {e}')
