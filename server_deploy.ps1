# MT5 Data Source API PowerShell部署脚本
# 在Windows Server上直接运行

Write-Host "============================================================" -ForegroundColor Green
Write-Host "MT5 Data Source API 服务器部署脚本" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# 步骤1: 检查Python安装
Write-Host "步骤1: 检查Python安装..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python未安装，开始安装Python 3.11..." -ForegroundColor Yellow
    
    # 下载Python安装程序
    Write-Host "下载Python安装程序..." -ForegroundColor Cyan
    $pythonUrl = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
    $pythonInstaller = "C:\python-3.11.8-amd64.exe"
    
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    
    # 安装Python
    Write-Host "安装Python..." -ForegroundColor Cyan
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0", "Include_pip=1" -Wait
    
    # 清理安装文件
    Remove-Item $pythonInstaller -Force
    
    # 刷新环境变量
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "Python安装完成" -ForegroundColor Green
}

# 步骤2: 创建部署目录
Write-Host "步骤2: 创建部署目录..." -ForegroundColor Yellow
$deployPath = "C:\mt5-api"
$logsPath = "C:\mt5-api\logs"
$backupPath = "C:\mt5-api\backup"

if (!(Test-Path $deployPath)) { New-Item -ItemType Directory -Path $deployPath -Force }
if (!(Test-Path $logsPath)) { New-Item -ItemType Directory -Path $logsPath -Force }
if (!(Test-Path $backupPath)) { New-Item -ItemType Directory -Path $backupPath -Force }

Write-Host "部署目录创建完成" -ForegroundColor Green

# 步骤3: 克隆代码仓库
Write-Host "步骤3: 克隆代码仓库..." -ForegroundColor Yellow
Set-Location $deployPath

if (Test-Path ".git") {
    Write-Host "代码已存在，更新代码..." -ForegroundColor Cyan
    git pull origin main
} else {
    Write-Host "克隆代码仓库..." -ForegroundColor Cyan
    git clone https://github.com/TheSixer/data-source.git .
}

# 步骤4: 安装Python依赖
Write-Host "步骤4: 安装Python依赖..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

# 步骤5: 配置防火墙
Write-Host "步骤5: 配置防火墙..." -ForegroundColor Yellow
netsh advfirewall firewall add rule name="MT5 Data API" dir=in action=allow protocol=TCP localport=3020

# 步骤6: 创建环境变量文件
Write-Host "步骤6: 创建环境变量文件..." -ForegroundColor Yellow
$envContent = @"
# API Configuration
API_KEY=your_api_key_here

# MT5 Configuration
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server
MT5_TIMEOUT=60000
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8

# 步骤7: 启动服务
Write-Host "步骤7: 启动服务..." -ForegroundColor Yellow
Write-Host "启动MT5 Data API服务..." -ForegroundColor Cyan

# 检查是否有Python进程在运行
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "停止现有Python进程..." -ForegroundColor Yellow
    Stop-Process -Name "python" -Force
}

# 启动服务
Start-Process -FilePath "python" -ArgumentList "-m", "app.main" -WorkingDirectory $deployPath -WindowStyle Hidden

# 步骤8: 等待服务启动
Write-Host "步骤8: 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# 步骤9: 测试服务
Write-Host "步骤9: 测试服务..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3020/" -TimeoutSec 10
    Write-Host "API服务测试成功: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "响应内容: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "API服务测试失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 显示部署结果
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "部署完成!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "API地址: http://47.116.221.184:3020" -ForegroundColor Cyan
Write-Host "API文档: http://47.116.221.184:3020/docs" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Green

# 显示服务状态
Write-Host ""
Write-Host "服务状态检查:" -ForegroundColor Yellow
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "Python进程正在运行: $($pythonProcesses.Count) 个进程" -ForegroundColor Green
} else {
    Write-Host "未找到Python进程" -ForegroundColor Red
}

# 检查端口监听
$portCheck = netstat -an | Select-String ":3020"
if ($portCheck) {
    Write-Host "端口3020正在监听" -ForegroundColor Green
} else {
    Write-Host "端口3020未监听" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意键继续..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
