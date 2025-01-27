from app import app

# Vercel serverless function handler
def handler(request):
    """处理所有 HTTP 请求"""
    return app(request.environ, request.start_response)
