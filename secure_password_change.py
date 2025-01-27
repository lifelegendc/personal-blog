from app import app, db, User
import getpass
import os

def change_admin_password():
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            db.session.add(admin)
        
        # 从环境变量获取密码（如果存在）
        password = os.environ.get('ADMIN_PASSWORD')
        if not password:
            # 如果环境变量中没有密码，则从命令行安全输入
            password = getpass.getpass('Enter new admin password: ')
            confirm_password = getpass.getpass('Confirm new admin password: ')
            if password != confirm_password:
                print("Passwords do not match!")
                return
        
        admin.set_password(password)
        db.session.commit()
        print("Admin password has been updated successfully!")
        print("Please delete any files containing plain text passwords.")

if __name__ == '__main__':
    change_admin_password()
