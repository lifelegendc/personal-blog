from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import markdown
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')

# 检查是否在 Vercel 环境中
if os.getenv('VERCEL_ENV'):
    # 在 Vercel 环境中使用 SQLite 内存数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # 本地开发环境使用文件数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256:600000')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 文章模型
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 首页路由
@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

# 文章详情页
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    content = markdown.markdown(post.content)
    return render_template('post.html', post=post, content=content)

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin'))
        flash('Invalid username or password')
    return render_template('login.html')

# 管理后台
@app.route('/admin')
@login_required
def admin():
    posts = Post.query.filter_by(author=current_user).order_by(Post.created_at.desc()).all()
    return render_template('admin.html', posts=posts)

# 创建新文章
@app.route('/admin/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_post.html')

# 编辑文章
@app.route('/admin/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_post.html', post=post)

# 删除文章
@app.route('/admin/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('admin'))

# 退出登录
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8080)