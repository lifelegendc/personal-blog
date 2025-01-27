from app import app

# Vercel 需要这个变量名
application = app

# 确保在应用启动时创建数据库表
with app.app_context():
    from app import db
    db.create_all()

if __name__ == "__main__":
    app.run()
