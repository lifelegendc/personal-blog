from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import or_
import markdown
import os
from dotenv import load_dotenv
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 基本配置
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-key-please-change'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///blog.db').replace('postgres://', 'postgresql://')
)

# 初始化扩展
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # 显式指定表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'posts'  # 显式指定表名
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    """初始化数据库"""
    try:
        # 创建所有表
        db.create_all()
        logger.info("数据库表创建成功")

        # 检查是否存在管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin')
            admin.set_password('casfoq-zavqy1-zUzxan')
            db.session.add(admin)
            db.session.commit()
            logger.info("管理员用户创建成功")
        else:
            logger.info("管理员用户已存在")
    except Exception as e:
        logger.error(f"数据库初始化错误: {str(e)}")
        db.session.rollback()
        raise

# 添加数据库连接池配置
engine_options = {
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 1800
}

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = engine_options

# 在应用启动时初始化数据库
init_db()

# 首页路由
@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    footer_text = ' 2025 '
    return render_template('index.html', posts=posts, footer_text=footer_text)

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
    if not current_user.username == 'admin':
        flash('只有管理员可以访问后台！', 'error')
        return redirect(url_for('index'))
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/index.html', posts=posts)

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
@app.route('/admin/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('文章已成功删除！', 'success')
    return redirect(url_for('admin'))

# 修改博客创建时间
@app.route('/admin/edit_time/<int:post_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_time(post_id):
    if not current_user.username == 'admin':
        flash('只有管理员可以修改博客时间！', 'error')
        return redirect(url_for('index'))
        
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        try:
            new_time = datetime.strptime(request.form['created_at'], '%Y-%m-%d %H:%M:%S')
            post.created_at = new_time
            db.session.commit()
            flash('博客创建时间已更新！', 'success')
            return redirect(url_for('admin'))
        except ValueError:
            flash('时间格式不正确，请使用 YYYY-MM-DD HH:MM:SS 格式', 'error')
    return render_template('admin/edit_time.html', post=post)

# 退出登录
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if query:
        # 使用 SQLAlchemy 的 or_ 和 like 进行模糊搜索
        search_results = Post.query.filter(
            or_(
                Post.title.like(f'%{query}%'),
                Post.content.like(f'%{query}%')
            )
        ).order_by(Post.created_at.desc()).all()
    else:
        # 如果查询为空，返回所有文章
        search_results = Post.query.order_by(Post.created_at.desc()).all()
    
    return render_template('search.html', posts=search_results, query=query)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)