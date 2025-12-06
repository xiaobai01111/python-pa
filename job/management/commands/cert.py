"""
证书管理命令
使用方法：
    python manage.py cert --generate    # 生成自签名证书
    python manage.py cert --renew       # 续签证书
    python manage.py cert --info        # 查看证书信息
    python manage.py cert --days 730    # 指定有效期（天）
"""
import os
import subprocess
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


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

    def handle(self, *args, **options):
        # 证书目录
        base_dir = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        cert_dir = os.path.join(base_dir, 'certs')
        cert_file = os.path.join(cert_dir, 'cert.pem')
        key_file = os.path.join(cert_dir, 'key.pem')

        if options['generate']:
            self.generate_cert(cert_dir, cert_file, key_file, options['days'], options['cn'])
        elif options['renew']:
            self.renew_cert(cert_dir, cert_file, key_file, options['days'], options['cn'])
        elif options['info']:
            self.show_info(cert_file)
        else:
            self.stdout.write(self.style.WARNING('请指定操作：--generate, --renew 或 --info'))
            self.stdout.write('使用 python manage.py cert --help 查看帮助')

    def generate_cert(self, cert_dir, cert_file, key_file, days, cn):
        """生成自签名证书"""
        # 检查是否已存在
        if os.path.exists(cert_file) or os.path.exists(key_file):
            self.stdout.write(self.style.WARNING('证书已存在！如需重新生成，请使用 --renew'))
            return

        self._create_cert(cert_dir, cert_file, key_file, days, cn)

    def renew_cert(self, cert_dir, cert_file, key_file, days, cn):
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

        self._create_cert(cert_dir, cert_file, key_file, days, cn)

    def _create_cert(self, cert_dir, cert_file, key_file, days, cn):
        """创建证书的核心逻辑"""
        # 创建目录
        os.makedirs(cert_dir, exist_ok=True)

        # 检查 openssl 是否可用
        try:
            subprocess.run(['openssl', 'version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise CommandError('未找到 openssl 命令，请先安装 OpenSSL')

        # 生成证书
        self.stdout.write(f'正在生成证书 (有效期: {days} 天, CN: {cn})...')
        
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
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.stdout.write(self.style.SUCCESS(f'✓ 证书生成成功！'))
            self.stdout.write(f'  证书文件: {cert_file}')
            self.stdout.write(f'  私钥文件: {key_file}')
            self.stdout.write(f'  有效期: {days} 天')
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('提示: 自签名证书在浏览器中会显示"不安全"警告，这是正常的'))
        except subprocess.CalledProcessError as e:
            raise CommandError(f'证书生成失败: {e.stderr}')

    def show_info(self, cert_file):
        """显示证书信息"""
        if not os.path.exists(cert_file):
            self.stdout.write(self.style.ERROR('证书文件不存在，请先使用 --generate 生成'))
            return

        try:
            # 获取证书信息
            result = subprocess.run(
                ['openssl', 'x509', '-in', cert_file, '-noout', '-text', '-dates'],
                capture_output=True, text=True, check=True
            )
            
            self.stdout.write(self.style.SUCCESS('=== 证书信息 ==='))
            
            # 解析关键信息
            lines = result.stdout.split('\n')
            for line in lines:
                line = line.strip()
                if 'Not Before' in line or 'Not After' in line:
                    self.stdout.write(f'  {line}')
                elif 'Subject:' in line:
                    self.stdout.write(f'  {line}')
                elif 'Issuer:' in line:
                    self.stdout.write(f'  {line}')
                    
        except subprocess.CalledProcessError as e:
            raise CommandError(f'读取证书失败: {e.stderr}')
