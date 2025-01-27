from app import app, db, User

def show_users():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"用户名: {user.username}")
            print(f"密码哈希: {user.password_hash}")
            print("-" * 50)

if __name__ == '__main__':
    show_users()
