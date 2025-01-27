from http.server import BaseHTTPRequestHandler
from app import app, init_db
import logging
from urllib.parse import parse_qs
from io import BytesIO

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def _handle_request(self):
        try:
            # 初始化数据库
            with app.app_context():
                init_db()

            # 准备 WSGI 环境
            environ = {
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'https',
                'wsgi.input': BytesIO(self.rfile.read(int(self.headers.get('content-length', 0)))),
                'wsgi.errors': BytesIO(),
                'wsgi.multithread': True,
                'wsgi.multiprocess': False,
                'wsgi.run_once': False,
                'REQUEST_METHOD': self.command,
                'PATH_INFO': self.path,
                'QUERY_STRING': self.path.split('?', 1)[1] if '?' in self.path else '',
                'SERVER_NAME': self.server.server_name,
                'SERVER_PORT': str(self.server.server_port),
                'SERVER_PROTOCOL': self.request_version,
            }

            # 添加 HTTP 头
            for key, value in self.headers.items():
                key = key.upper().replace('-', '_')
                if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                    key = 'HTTP_' + key
                environ[key] = value

            # 处理响应
            response_body = []
            def start_response(status, headers):
                self.send_response(int(status.split()[0]))
                for header, value in headers:
                    self.send_header(header, value)
                self.end_headers()

            # 调用 Flask 应用
            response = app(environ, start_response)
            for data in response:
                self.wfile.write(data)

        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            self.send_error(500, str(e))

handler = Handler
