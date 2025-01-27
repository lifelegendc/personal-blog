# 阿里云部署检查清单

## 1. 准备工作

### 阿里云控制台操作
- [ ] 购买ECS服务器（建议选择Ubuntu系统）
- [ ] 设置安全组，开放以下端口：
  - 22 (SSH)
  - 80 (HTTP)
  - 443 (HTTPS)
- [ ] 绑定弹性IP（如果需要）
- [ ] 设置域名解析（如果有域名）

### 本地准备
- [ ] 保存好ECS服务器的公网IP
- [ ] 准备好服务器的root密码或SSH密钥
- [ ] 确保所有代码已提交到Git仓库

## 2. 部署步骤

### 连接服务器
```bash
ssh root@your-server-ip
```

### 创建普通用户（安全考虑）
```bash
adduser deploy
usermod -aG sudo deploy
su - deploy
```

### 克隆代码
```bash
cd /var/www
git clone <您的代码仓库URL> personal-blog
cd personal-blog
```

### 配置环境变量
```bash
cd /var/www/personal-blog
cp .env.example .env
# 编辑.env文件，设置正确的配置
nano .env
```

### 运行部署脚本
```bash
chmod +x deploy_scripts/setup_server.sh
./deploy_scripts/setup_server.sh
```

## 3. 验证部署

### 检查服务状态
- [ ] 检查Supervisor状态：
  ```bash
  sudo supervisorctl status
  ```
- [ ] 检查Nginx状态：
  ```bash
  sudo systemctl status nginx
  ```
- [ ] 检查应用日志：
  ```bash
  tail -f /var/log/personal-blog/err.log
  tail -f /var/log/personal-blog/out.log
  ```

### 检查网站访问
- [ ] 通过IP地址访问网站
- [ ] 通过域名访问网站（如果已配置）
- [ ] 测试HTTPS访问（如果已配置SSL）

## 4. 安全检查

- [ ] 确保.env文件权限正确：
  ```bash
  chmod 600 .env
  ```
- [ ] 检查防火墙状态：
  ```bash
  sudo ufw status
  ```
- [ ] 确保日志文件权限正确：
  ```bash
  sudo chown -R deploy:deploy /var/log/personal-blog
  chmod -R 644 /var/log/personal-blog
  ```

## 5. 备份策略

- [ ] 设置数据库备份：
  ```bash
  # 创建备份脚本
  mkdir -p /var/www/personal-blog/backups
  chmod 700 /var/www/personal-blog/backups
  ```

## 6. 监控设置

- [ ] 设置服务器监控（可选）：
  - 阿里云监控服务
  - 自定义监控脚本

## 7. 维护命令

### 重启服务
```bash
# 重启应用
sudo supervisorctl restart personal-blog

# 重启Nginx
sudo systemctl restart nginx
```

### 查看日志
```bash
# 应用日志
tail -f /var/log/personal-blog/out.log
tail -f /var/log/personal-blog/err.log

# Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 更新代码
```bash
cd /var/www/personal-blog
git pull
sudo supervisorctl restart personal-blog
```
