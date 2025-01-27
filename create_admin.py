from app import app, db, User

def create_admin(username, password):
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        # 检查用户是否已存在
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"用户 {username} 已存在")
            return
        
        # 创建新管理员用户
        admin = User(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"管理员用户 {username} 创建成功！")
