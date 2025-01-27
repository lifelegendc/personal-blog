# 部署指南

本文档提供了在不同平台上部署个人博客的详细说明。

## 准备工作

1. 确保您已经有以下文件：
   - `requirements.txt`：包含所有依赖
   - `wsgi.py`：Web服务器网关接口文件
   - `gunicorn_config.py`：Gunicorn配置文件
   - `.env`：环境变量配置文件（注意不要提交到代码仓库）

2. 在部署之前，请确保：
   - 已经设置了安全的 SECRET_KEY
   - 已经配置了正确的数据库 URL
   - 已经创建了管理员账户

## 部署选项

### 1. 使用云服务器（推荐）

1. 登录您的云服务器
2. 安装必要的软件：
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

3. 克隆代码并设置环境：
   ```bash
   git clone <您的代码仓库URL>
   cd personal-blog
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. 配置 Nginx：
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. 启动应用：
   ```bash
   gunicorn -c gunicorn_config.py wsgi:app
   ```

6. 设置 SSL 证书（推荐使用 Let's Encrypt）：
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### 2. 使用 PythonAnywhere（简单方案）

1. 注册 PythonAnywhere 账户
2. 上传代码或通过 Git 克隆
3. 创建虚拟环境并安装依赖
4. 配置 Web 应用：
   - 选择 Manual Configuration
   - 选择 Python 版本
   - 设置虚拟环境路径
   - 配置 WSGI 文件
   - 设置环境变量

### 3. 使用 Docker（适合团队协作）

1. 创建 Dockerfile：
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]
   ```

2. 构建并运行：
   ```bash
   docker build -t personal-blog .
   docker run -p 8000:8000 personal-blog
   ```

## 安全注意事项

1. 环境变量：
   - 确保 `.env` 文件不被提交到代码仓库
   - 在生产环境中使用强密钥
   - 定期更换 SECRET_KEY

2. 数据库：
   - 在生产环境使用强密码
   - 定期备份数据
   - 限制数据库访问IP

3. 服务器安全：
   - 启用防火墙
   - 只开放必要端口
   - 定期更新系统和依赖包

## 维护建议

1. 监控：
   - 设置服务器监控
   - 监控应用日志
   - 设置错误告警

2. 备份：
   - 定期备份数据库
   - 备份配置文件
   - 保存多个版本的备份

3. 更新：
   - 定期更新依赖包
   - 检查安全漏洞
   - 及时应用安全补丁

## 故障排除

如果遇到问题，请检查：
1. 日志文件
2. 环境变量配置
3. 数据库连接
4. 防火墙设置
5. 域名解析

需要帮助时，可以查看错误日志或联系技术支持。
