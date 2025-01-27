from app import app

# Vercel 需要这个变量名
application = app

# 确保在应用启动时创建数据库表
with app.app_context():
    from app import db
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")

def handler(event, context):
    return app(event, context)
