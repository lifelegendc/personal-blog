from app import app, init_db
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vercel serverless function handler
def handler(request):
    """处理所有 HTTP 请求"""
    try:
        with app.app_context():
            init_db()
        return app(request.environ, request.start_response)
    except Exception as e:
        logger.error(f"Error handling request: {str(e)}")
        raise
