@echo off
echo ============================================================
echo MT5 Data Source API 服务器部署脚本
echo ============================================================
echo.

echo 步骤1: 检查Python安装...
python --version
if %errorlevel% neq 0 (
    echo Python未安装，开始安装Python 3.11...
    echo 下载Python安装程序...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'C:\python-3.11.8-amd64.exe'"
    
    echo 安装Python...
    C:\python-3.11.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1
    
    echo 清理安装文件...
    del C:\python-3.11.8-amd64.exe
    
    echo 刷新环境变量...
    call refreshenv
) else (
    echo Python已安装
)

echo.
echo 步骤2: 创建部署目录...
if not exist "C:\mt5-api" mkdir C:\mt5-api
if not exist "C:\mt5-api\logs" mkdir C:\mt5-api\logs
if not exist "C:\mt5-api\backup" mkdir C:\mt5-api\backup

echo.
echo 步骤3: 克隆代码仓库...
cd /d C:\mt5-api
if exist ".git" (
    echo 代码已存在，更新代码...
    git pull origin main
) else (
    echo 克隆代码仓库...
    git clone https://github.com/TheSixer/data-source.git .
)

echo.
echo 步骤4: 安装Python依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 步骤5: 配置防火墙...
netsh advfirewall firewall add rule name="MT5 Data API" dir=in action=allow protocol=TCP localport=3020

echo.
echo 步骤6: 创建环境变量文件...
echo # API Configuration > .env
echo API_KEY=your_api_key_here >> .env
echo. >> .env
echo # MT5 Configuration >> .env
echo MT5_LOGIN=your_mt5_login >> .env
echo MT5_PASSWORD=your_mt5_password >> .env
echo MT5_SERVER=your_mt5_server >> .env
echo MT5_TIMEOUT=60000 >> .env

echo.
echo 步骤7: 启动服务...
echo 启动MT5 Data API服务...
start /B python -m app.main

echo.
echo 步骤8: 等待服务启动...
timeout /t 15 /nobreak

echo.
echo 步骤9: 测试服务...
curl http://localhost:3020/

echo.
echo ============================================================
echo 部署完成!
echo ============================================================
echo API地址: http://47.116.221.184:3020
echo API文档: http://47.116.221.184:3020/docs
echo ============================================================

pause
