"""
HTTP/2 服务器启动命令
使用方法：
    python manage.py runserver2                    # 启动 HTTP/2 服务器 (默认 127.0.0.1:8000)
    python manage.py runserver2 8080               # 指定端口
    python manage.py runserver2 127.0.0.1:8080     # 指定地址和端口
    python manage.py runserver2 --http1            # 降级为 HTTP/1.1（不使用证书）
"""
import os
import sys
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = '启动支持 HTTP/2 的开发服务器 (使用 Hypercorn)'

    def add_arguments(self, parser):
        parser.add_argument(
            'addrport',
            nargs='?',
            default='127.0.0.1:8000',
            help='地址和端口，格式: [address:]port (默认 127.0.0.1:8000)'
        )
        parser.add_argument(
            '--http1',
            action='store_true',
            help='使用 HTTP/1.1 模式（不需要证书）'
        )
        parser.add_argument(
            '--reload',
            action='store_true',
            default=True,
            help='启用自动重载（默认启用）'
        )
        parser.add_argument(
            '--no-reload',
            action='store_true',
            help='禁用自动重载'
        )
        parser.add_argument(
            '--workers', '-w',
            type=int,
            default=1,
            help='工作进程数（默认 1）'
        )

    def handle(self, *args, **options):
        # 检查 hypercorn 是否安装
        try:
            import hypercorn
        except ImportError:
            self.stdout.write(self.style.ERROR('Hypercorn 未安装！'))
            self.stdout.write('请运行: pip install hypercorn')
            return

        # 解析地址和端口
        addrport = options['addrport']
        if ':' in addrport:
            addr, port = addrport.rsplit(':', 1)
        else:
            addr = '127.0.0.1'
            port = addrport

        # 证书路径
        base_dir = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        cert_dir = os.path.join(base_dir, 'certs')
        cert_file = os.path.join(cert_dir, 'cert.pem')
        key_file = os.path.join(cert_dir, 'key.pem')

        # 构建命令 - 日志格式模仿 Django runserver
        cmd = [
            sys.executable, '-m', 'hypercorn',
            'JobRecommend.asgi:application',
            '--bind', f'{addr}:{port}',
            '--workers', str(options['workers']),
            '--access-logformat', '"%(m)s %(U)s HTTP/%(H)s" %(s)s %(b)s',
            '--access-logfile', '-',
            '--error-logfile', '-',
        ]

        # HTTP/2 模式需要证书
        if not options['http1']:
            if not os.path.exists(cert_file) or not os.path.exists(key_file):
                self.stdout.write(self.style.ERROR('证书文件不存在！'))
                self.stdout.write('请先运行: python manage.py cert --generate')
                self.stdout.write('或使用 --http1 参数以 HTTP/1.1 模式启动')
                return
            
            cmd.extend(['--certfile', cert_file, '--keyfile', key_file])
            protocol = 'HTTP/2 (HTTPS)'
            url_prefix = 'https'
        else:
            protocol = 'HTTP/1.1'
            url_prefix = 'http'

        # 自动重载
        if options['reload'] and not options['no_reload']:
            cmd.append('--reload')

        # 显示启动信息
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'=== {protocol} 开发服务器 ==='))
        self.stdout.write(f'监听地址: {url_prefix}://{addr}:{port}/')
        if not options['http1']:
            self.stdout.write(self.style.WARNING('提示: 自签名证书可能触发浏览器安全警告；使用本地可信证书可消除警告'))
        self.stdout.write('')
        self.stdout.write('按 Ctrl+C 停止服务器')
        self.stdout.write('')

        # 启动服务器
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('服务器已停止'))
