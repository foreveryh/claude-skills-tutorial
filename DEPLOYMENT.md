# Deployment Guide

本项目使用 **GitHub Actions + Dokploy** 的混合部署方案：
- GitHub Actions 负责构建 Docker 镜像（利用免费构建资源）
- Dokploy 负责部署和运行（节省 VPS 资源）

## 🚀 部署流程

### 1. GitHub 配置

#### 1.1 创建 Docker Hub 账号
1. 访问 https://hub.docker.com/ 注册账号
2. 创建访问令牌（Access Token）：
   - 进入 Account Settings > Security > New Access Token
   - 权限选择 "Read, Write, Delete"
   - 保存生成的 token

#### 1.2 配置 GitHub Secrets
在仓库设置中添加以下 Secrets：

1. 进入 GitHub 仓库 > Settings > Secrets and variables > Actions
2. 添加以下 secrets：
   - `DOCKERHUB_USERNAME`: 你的 Docker Hub 用户名
   - `DOCKERHUB_TOKEN`: 刚创建的 Access Token

### 2. Dokploy 配置

#### 2.1 创建新应用
1. 登录 Dokploy 控制面板
2. 点击 "Create Application"
3. 选择 **"Docker Image"** 作为部署方式

#### 2.2 配置 Docker 镜像
填写以下信息：

```
Application Name: claude-skills
Image: <DOCKERHUB_USERNAME>/claude-skills:latest
Port: 3000
```

#### 2.3 配置自动部署（可选但推荐）
**方法 1: Docker Hub Webhook**
1. 在 Dokploy 应用设置中找到 Webhook URL
2. 在 Docker Hub > Repository > Webhooks 添加：
   - Webhook name: `dokploy-auto-deploy`
   - Webhook URL: 从 Dokploy 复制的 URL

**方法 2: 定期拉取**
- 在 Dokploy 中启用 "Auto Deploy"
- 设置检查间隔（例如 5 分钟）

### 3. 域名绑定

#### 3.1 在 Dokploy 中添加域名
1. 进入应用的 "Domains" 标签
2. 添加域名：`skills.deeptoai.com`
3. 启用 SSL（Let's Encrypt 自动配置）

#### 3.2 配置 DNS
在你的域名 DNS 管理中添加 A 记录：

```
Type: A
Name: skills
Value: <你的 VPS IP 地址>
TTL: 自动或 3600
```

等待 DNS 传播（通常 5-30 分钟）

### 4. 首次部署

#### 4.1 推送代码触发构建
```bash
git add .
git commit -m "feat: add docker deployment config"
git push origin main
```

#### 4.2 查看构建状态
1. GitHub Actions 页面查看构建进度
2. 构建完成后，Docker Hub 应该有新镜像

#### 4.3 在 Dokploy 部署
1. 点击 Dokploy 应用的 "Deploy" 按钮
2. 等待部署完成（2-3 分钟）
3. 访问 `https://skills.deeptoai.com` 验证

## 🔄 后续部署流程

每次代码推送到 `main` 分支后：

1. ✅ GitHub Actions 自动构建新镜像
2. ✅ 推送到 Docker Hub
3. ✅ Dokploy 自动拉取并部署（如果配置了 webhook）
   - 或手动点击 "Deploy" 按钮

## ⚙️ 环境变量（如需要）

如果项目需要环境变量，在 Dokploy 中配置：

1. 进入应用 > Environment Variables
2. 添加所需变量（例如 API keys）

## 🐛 故障排查

### 构建失败
- 检查 GitHub Actions logs
- 验证 Docker Hub credentials

### 部署失败
- 检查 Dokploy logs
- 验证镜像名称是否正确
- 确认端口配置（3000）

### 域名无法访问
- 验证 DNS 配置
- 检查 Dokploy SSL 证书状态
- 确认防火墙开放 80/443 端口

## 📊 优势

✅ **节省 VPS 资源** - 构建在 GitHub Actions 完成
✅ **加快部署速度** - 直接拉取预构建镜像
✅ **免费构建** - 公开仓库无限使用
✅ **自动化流程** - Push 即部署
✅ **版本控制** - 每次构建都有唯一标签

## 🔗 相关链接

- Docker Hub: https://hub.docker.com/
- Dokploy 文档: https://docs.dokploy.com/
- GitHub Actions: https://docs.github.com/actions
