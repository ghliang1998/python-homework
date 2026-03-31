# Docker 容器化部署指南

## 📋 前置要求

- 已安装 Docker Desktop（Windows/Mac）或 Docker Engine（Linux）
- 已安装 Docker Compose

## 🚀 快速开始

### 1. 配置环境变量
```bash
# 复制模板文件
cp .env.example .env

# 编辑.env文件，填入实际的数据库配置
# 如果有真实数据库，更新DB_HOST、DB_USER、DB_PASSWORD等
```

### 2. 启动容器（方式一：使用docker-compose）
```bash
# 启动所有容器（MySQL + Python应用）
docker-compose up -d

# 查看容器日志
docker-compose logs -f python_app

# 停止容器
docker-compose down

# 保留数据卷重启
docker-compose down -v  # 会删除数据卷
```

### 3. 启动容器（方式二：仅使用Docker）
```bash
# 构建镜像
docker build -t python-homework:latest .

# 运行容器（需先启动MySQL或修改数据库连接）
docker run -d \
  --name python_homework_app \
  -e DB_HOST=host.docker.internal \
  -e DB_PORT=3306 \
  -e DB_USER=student \
  -e DB_PASSWORD=mlbb2026 \
  -e DB_NAME=homework_db \
  -v $(pwd):/app \
  python-homework:latest
```

## 📊 查看日志和监控

```bash
# 查看python应用日志
docker-compose logs python_app

# 实时查看日志
docker-compose logs -f python_app

# 查看MySQL日志
docker-compose logs mysql

# 查看容器状态
docker-compose ps
```

## 🛠️ 常用命令

| 命令 | 说明 |
|------|------|
| `docker-compose up -d` | 后台启动所有容器 |
| `docker-compose down` | 停止并删除所有容器 |
| `docker-compose restart python_app` | 重启应用容器 |
| `docker-compose exec python_app bash` | 进入容器内部执行命令 |
| `docker-compose logs -f` | 实时查看所有日志 |
| `docker ps` | 查看正在运行的容器 |
| `docker images` | 查看已构建的镜像 |

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `Dockerfile` | 定义Python应用镜像如何构建 |
| `docker-compose.yaml` | 定义多个容器（MySQL+App）的协作方式 |
| `.env` | 环境变量配置（敏感信息，不上传Git） |
| `.env.example` | 环境变量模板（可上传Git，供他人参考） |

## 🔒 安全建议

1. **不提交.env文件** - 已在.gitignore中配置
2. **使用强密码** - 修改.env中的数据库密码
3. **生产环境** - 使用Docker Secrets或密钥管理工具
4. **限制资源** - docker-compose.yaml中已配置CPU和内存限制

## 🐛 故障排查

### 问题1：容器无法连接MySQL
```bash
# 确保MySQL容器正常运行
docker-compose ps

# 查看MySQL日志
docker-compose logs mysql

# 检查网络连接
docker-compose exec python_app ping mysql
```

### 问题2：Python依赖缺失
```bash
# 重新构建镜像（不使用缓存）
docker-compose build --no-cache

# 重启容器
docker-compose restart python_app
```

### 问题3：需要进入容器调试
```bash
# 进入python应用容器
docker-compose exec python_app bash

# 进入MySQL容器
docker-compose exec mysql bash
```

## 📝 环境变量参考

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DB_HOST` | 数据库主机地址 | 127.0.0.1 |
| `DB_PORT` | 数据库端口 | 3306 |
| `DB_USER` | 数据库用户名 | student |
| `DB_PASSWORD` | 数据库密码 | mlbb2026 |
| `DB_NAME` | 数据库名称 | homework_db |
| `LOG_LEVEL` | 日志级别 | INFO |
| `TIMEZONE` | 时区 | Asia/Shanghai |
