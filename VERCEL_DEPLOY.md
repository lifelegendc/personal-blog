# Vercel 部署指南

## 准备工作

1. 创建 GitHub 账号（如果没有）
2. 创建 Vercel 账号（https://vercel.com）

## 部署步骤

### 1. 准备代码仓库

1. 在 GitHub 上创建新仓库
2. 将代码推送到 GitHub：
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <你的GitHub仓库地址>
git push -u origin main
```

### 2. Vercel 部署

1. 登录 Vercel（https://vercel.com）
2. 点击 "New Project"
3. 导入你的 GitHub 仓库
4. 配置项目：
   - Framework Preset: 选择 "Other"
   - Build and Output Settings: 保持默认
   - Environment Variables: 添加以下变量
     - `SECRET_KEY`: 你的密钥
     - `DATABASE_URL`: 数据库连接 URL

5. 点击 "Deploy"

### 3. 环境变量设置

在 Vercel 项目设置中添加以下环境变量：
- `SECRET_KEY`: 设置为一个安全的随机字符串
- `DATABASE_URL`: 设置数据库连接（可以使用 SQLite 或其他数据库服务）

### 4. 域名设置（可选）

1. 在 Vercel 项目设置中找到 "Domains"
2. 添加你的自定义域名
3. 按照指示配置 DNS 记录

### 5. 验证部署

1. 访问 Vercel 提供的域名（形如 your-project.vercel.app）
2. 测试网站功能是否正常：
   - 登录功能
   - 文章发布
   - 文章编辑
   - 图片上传等

### 6. 常见问题解决

1. 如果部署失败：
   - 检查 build 日志
   - 确认所有依赖都在 requirements.txt 中
   - 验证环境变量是否正确设置

2. 如果网站加载出错：
   - 检查应用日志
   - 确认数据库连接是否正常
   - 验证静态文件是否正确加载

### 7. 更新网站

1. 本地修改代码
2. 提交到 GitHub：
```bash
git add .
git commit -m "Update description"
git push
```
3. Vercel 将自动重新部署

### 8. 注意事项

1. 数据持久化：
   - Vercel 的文件系统是临时的
   - 建议使用外部数据库服务
   - 不要在本地存储上传的文件

2. 环境变量：
   - 不要在代码中硬编码敏感信息
   - 使用 Vercel 的环境变量功能

3. 性能优化：
   - 使用缓存机制
   - 优化静态资源
   - 考虑使用 CDN
