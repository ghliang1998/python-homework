# ============================================================
# Dockerfile - Python项目容器化配置
# ============================================================

# 1. 基础镜像：使用Python 3.10官方镜像
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 设置环境变量
#    PYTHONUNBUFFERED=1: 使Python输出实时显示（不缓存）
#    PYTHONDONTWRITEBYTECODE=1: 不生成.pyc文件
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# 4. 安装系统依赖
#    必要库用于构建Python包和MySQL连接
RUN apt-get update && apt-get install -y \
    gcc \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. 复制requirements.txt到容器
COPY requirements.txt .

# 6. 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 7. 复制项目代码到容器
COPY . .

# 8. 设置容器启动时运行的命令
#    启动write_analysis_log.py（定时任务脚本）
CMD ["python", "write_analysis_log.py"]
