from http.server import BaseHTTPRequestHandler
from app import app
import logging
from urllib.parse import parse_qs, urlparse
from io import BytesIO

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 在应用启动时初始化数据库
with app.app_context():
    from app import init_db
    init_db()

# 导出 Flask 应用实例
app = app

class Handler(BaseHTTPRequestHandler):
    def _handle_request(self):
        try:
            # 解析请求路径
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_params = parse_qs(parsed_path.query)

            # 设置环境变量
            environ = {
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'https',
                'wsgi.input': BytesIO(self.rfile.read(int(self.headers.get('content-length', 0)))),
                'wsgi.errors': BytesIO(),
                'wsgi.multithread': True,
                'wsgi.multiprocess': False,
                'wsgi.run_once': False,
                'SERVER_SOFTWARE': self.server_version,
                'REQUEST_METHOD': self.command,
                'SCRIPT_NAME': '',
                'PATH_INFO': path,
                'QUERY_STRING': parsed_path.query,
                'SERVER_NAME': self.server.server_name,
                'SERVER_PORT': str(self.server.server_port),
                'SERVER_PROTOCOL': self.protocol_version
            }

            # 添加 HTTP 头
            for key, value in self.headers.items():
                key = key.upper().replace('-', '_')
                if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                    key = 'HTTP_' + key
                environ[key] = value

            # 处理请求
            response_body = []
            def start_response(status, headers):
                self.send_response(int(status.split()[0]))
                for header, value in headers:
                    self.send_header(header, value)
                self.end_headers()

            # 调用 Flask 应用处理请求
            response = app(environ, start_response)
            
            # 发送响应
            for data in response:
                self.wfile.write(data)

        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            self.send_error(500, "Internal Server Error")

    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

handler = Handler
