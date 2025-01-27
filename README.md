# 个人博客系统

这是一个使用 Flask 开发的简单个人博客系统，支持文章的创建、编辑、删除和展示功能。

## 功能特点

- 用户认证系统（登录/登出）
- 文章管理（创建、编辑、删除）
- Markdown 支持
- 响应式设计
- 简洁美观的界面

## 安装说明

1. 克隆项目到本地：
```bash
git clone <repository-url>
cd personal-blog
```

2. 创建虚拟环境并激活：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 初始化数据库：
```python
python
>>> from app import app, db, User
>>> with app.app_context():
...     db.create_all()
...     # 创建管理员账户
...     admin = User(username='admin', password_hash='<your-password-hash>')
...     db.session.add(admin)
...     db.session.commit()
```

5. 运行应用：
```bash
python app.py
```

访问 http://localhost:5000 即可看到博客首页。

## 使用说明

1. 访问 `/login` 登录管理后台
2. 在管理后台可以进行以下操作：
   - 创建新文章
   - 编辑现有文章
   - 删除文章
3. 文章支持 Markdown 格式
4. 首页会显示所有文章的列表
5. 点击文章标题可以查看文章详情

## 技术栈

- Flask
- SQLAlchemy
- Flask-Login
- Bootstrap 5
- Markdown

## 注意事项

- 请修改 `app.py` 中的 `SECRET_KEY`
- 在生产环境中使用时，请确保正确配置数据库和安全设置
- 建议使用环境变量来存储敏感信息
