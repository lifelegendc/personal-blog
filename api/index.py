from app import app as application

# Vercel serverless function handler
def handler(event, context):
    return application(event, context)
