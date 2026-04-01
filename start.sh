#!/bin/bash
# 启动 FPA 音频网站

cd "$(dirname "$0")"

echo "🚀 启动功能点审核培训音频系统..."
echo "=================================="

# 检查依赖
python3 -c "import flask; import flask_sqlalchemy; import flask_login" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装依赖..."
    pip install flask flask-sqlalchemy flask-login requests --break-system-packages -q
fi

echo "🌐 启动服务..."
echo "访问地址: http://localhost:5000"
echo "登录账号: Admin / Admin123"
echo "=================================="
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py
