from flask import Flask, request
from app import app as flask_app

# Vercel serverless function handler
def handler(request):
    """Handle the request and return the response."""
    with flask_app.request_context(request):
        return flask_app.full_dispatch_request()
