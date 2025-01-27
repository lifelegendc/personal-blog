#!/bin/bash

# 更新系统并安装必要的软件
echo "正在更新系统..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx git supervisor

# 创建应用目录
echo "创建应用目录..."
sudo mkdir -p /var/www/personal-blog
sudo chown -R $USER:$USER /var/www/personal-blog

# 创建虚拟环境
echo "设置Python虚拟环境..."
cd /var/www/personal-blog
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 配置Supervisor
echo "配置Supervisor..."
sudo tee /etc/supervisor/conf.d/personal-blog.conf << EOF
[program:personal-blog]
directory=/var/www/personal-blog
command=/var/www/personal-blog/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
user=$USER
autostart=true
autorestart=true
stderr_logfile=/var/log/personal-blog/err.log
stdout_logfile=/var/log/personal-blog/out.log
EOF

# 创建日志目录
sudo mkdir -p /var/log/personal-blog
sudo chown -R $USER:$USER /var/log/personal-blog

# 配置Nginx
echo "配置Nginx..."
sudo tee /etc/nginx/sites-available/personal-blog << EOF
server {
    listen 80;
    server_name your-domain.com;  # 需要替换为您的域名

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /var/www/personal-blog/static;
    }
}
EOF

# 启用网站配置
sudo ln -s /etc/nginx/sites-available/personal-blog /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 重启服务
echo "重启服务..."
sudo systemctl restart supervisor
sudo systemctl restart nginx

# 安装SSL证书（如果需要）
echo "是否安装SSL证书？(y/n)"
read install_ssl
if [ "$install_ssl" = "y" ]; then
    sudo apt install -y certbot python3-certbot-nginx
    sudo certbot --nginx -d your-domain.com  # 需要替换为您的域名
fi

echo "部署脚本执行完成！"
