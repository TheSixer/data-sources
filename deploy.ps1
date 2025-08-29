# MT5 Data Source API PowerShell部署脚本

param(
    [string]$Host = "47.116.221.184",
    [string]$Username = "Administrator",
    [string]$Password = "Longjia@3713"
)

Write-Host "开始MT5 Data Source API部署..." -ForegroundColor Green
Write-Host "目标服务器: $Username@$Host" -ForegroundColor Yellow
Write-Host "=" * 60

# 定义SSH命令函数
function Invoke-SSHCommand {
    param([string]$Command)
    
    Write-Host "执行SSH命令: $Command" -ForegroundColor Cyan
    
    try {
        $sshCmd = "ssh $Username@$Host `"$Command`""
        $result = Invoke-Expression $sshCmd
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "命令执行成功" -ForegroundColor Green
            return $true
        } else {
            Write-Host "命令执行失败" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "SSH命令执行错误: $_" -ForegroundColor Red
        return $false
    }
}

# 步骤1: 检查Python安装
Write-Host "步骤1: 检查Python安装" -ForegroundColor Yellow
if (-not (Invoke-SSHCommand "python --version")) {
    Write-Host "Python未安装，开始安装Python 3.11..." -ForegroundColor Yellow
    
    # 下载Python
    Invoke-SSHCommand "powershell -Command `"Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'C:\python-3.11.8-amd64.exe'`""
    
    # 安装Python
    Invoke-SSHCommand "C:\python-3.11.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1"
    
    # 清理安装文件
    Invoke-SSHCommand "del C:\python-3.11.8-amd64.exe"
}

# 步骤2: 创建部署目录
Write-Host "步骤2: 创建部署目录" -ForegroundColor Yellow
Invoke-SSHCommand "mkdir C:\mt5-api"
Invoke-SSHCommand "mkdir C:\mt5-api\logs"
Invoke-SSHCommand "mkdir C:\mt5-api\backup"

# 步骤3: 克隆代码仓库
Write-Host "步骤3: 克隆代码仓库" -ForegroundColor Yellow
Invoke-SSHCommand "cd C:\mt5-api && git clone https://github.com/TheSixer/data-source.git ."

# 步骤4: 安装Python依赖
Write-Host "步骤4: 安装Python依赖" -ForegroundColor Yellow
Invoke-SSHCommand "cd C:\mt5-api && python -m pip install --upgrade pip"
Invoke-SSHCommand "cd C:\mt5-api && pip install -r requirements.txt"

# 步骤5: 配置防火墙
Write-Host "步骤5: 配置防火墙" -ForegroundColor Yellow
Invoke-SSHCommand "netsh advfirewall firewall add rule name=`"MT5 Data API`" dir=in action=allow protocol=TCP localport=3020"

# 步骤6: 创建环境变量文件
Write-Host "步骤6: 创建环境变量文件" -ForegroundColor Yellow
$envContent = @"
# API Configuration
API_KEY=your_api_key_here

# MT5 Configuration
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server
MT5_TIMEOUT=60000
"@

Invoke-SSHCommand "echo '$envContent' > C:\mt5-api\.env"

# 步骤7: 启动服务
Write-Host "步骤7: 启动服务" -ForegroundColor Yellow
Invoke-SSHCommand "cd C:\mt5-api && start /B python -m app.main"

# 步骤8: 等待服务启动并测试
Write-Host "步骤8: 等待服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host "测试API服务..." -ForegroundColor Yellow
Invoke-SSHCommand "curl http://localhost:3020/"

Write-Host "=" * 60
Write-Host "部署完成!" -ForegroundColor Green
Write-Host "API地址: http://$Host`:3020" -ForegroundColor Cyan
Write-Host "API文档: http://$Host`:3020/docs" -ForegroundColor Cyan
Write-Host "=" * 60
