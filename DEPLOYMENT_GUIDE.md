# MT5 Data Source API 自动化部署指南

## 🌟 概述

本指南将帮助你使用GitHub Actions自动化部署MT5 Data Source API到Windows Server。

## 📋 前置要求

### 1. GitHub仓库设置
- 确保项目已推送到GitHub仓库
- 仓库名称: `data-source`
- 仓库所有者: `TheSixer`

### 2. GitHub Personal Access Token
1. 访问 [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. 生成新的token，选择以下权限:
   - `repo` (完整仓库访问权限)
   - `workflow` (工作流权限)
   - `admin:org` (组织管理权限，如果需要)

### 3. 服务器信息
- **IP地址**: 47.116.221.184
- **用户名**: root
- **密码**: Longjia@3713
- **端口**: 22

## 🚀 部署步骤

### 步骤1: 设置GitHub Secrets

#### 方法1: 使用自动化脚本 (推荐)

1. 安装依赖:
```bash
pip install requests cryptography python-dotenv
```

2. 运行Secrets设置脚本:
```bash
python scripts/setup_github_secrets.py TheSixer data-source YOUR_GITHUB_TOKEN
```

#### 方法2: 手动设置

在GitHub仓库页面:
1. 进入 `Settings` > `Secrets and variables` > `Actions`
2. 点击 `New repository secret`
3. 添加以下secrets:

| Secret名称 | 值 | 说明 |
|-----------|----|------|
| `API_KEY` | your_api_key_here | API密钥 |
| `MT5_LOGIN` | your_mt5_login | MT5登录账号 |
| `MT5_PASSWORD` | your_mt5_password | MT5密码 |
| `MT5_SERVER` | your_mt5_server | MT5服务器地址 |
| `MT5_TIMEOUT` | 60000 | MT5超时时间 |
| `SERVER_HOST` | 47.116.221.184 | 服务器IP |
| `SERVER_USERNAME` | root | 服务器用户名 |
| `SERVER_PASSWORD` | Longjia@3713 | 服务器密码 |
| `SERVER_PORT` | 22 | 服务器SSH端口 |

### 步骤2: 服务器初始化

#### 方法1: 使用自动化脚本 (推荐)

1. 安装依赖:
```bash
pip install paramiko
```

2. 运行服务器初始化脚本:
```bash
python scripts/server_setup.py 47.116.221.184 root Longjia@3713
```

#### 方法2: 手动初始化

如果自动化脚本失败，可以手动执行以下步骤:

1. **安装Python 3.11**
```powershell
# 下载Python安装程序
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe" -OutFile "C:\python-3.11.8-amd64.exe"

# 安装Python
C:\python-3.11.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1

# 清理安装文件
del C:\python-3.11.8-amd64.exe
```

2. **安装NSSM**
```powershell
# 创建NSSM目录
mkdir C:\nssm

# 下载NSSM
Invoke-WebRequest -Uri "https://nssm.cc/release/nssm-2.24.zip" -OutFile "C:\nssm\nssm.zip"

# 解压NSSM
Expand-Archive -Path "C:\nssm\nssm.zip" -DestinationPath "C:\nssm" -Force

# 复制nssm.exe
copy C:\nssm\nssm-2.24\win64\nssm.exe C:\nssm\

# 清理临时文件
rmdir /s /q C:\nssm\nssm-2.24
del C:\nssm\nssm.zip

# 添加到PATH
setx PATH "%PATH%;C:\nssm" /M
```

3. **创建部署目录**
```cmd
mkdir C:\mt5-api
mkdir C:\mt5-api\logs
mkdir C:\mt5-api\backup
```

4. **配置防火墙**
```cmd
netsh advfirewall firewall add rule name="MT5 Data API" dir=in action=allow protocol=TCP localport=3020
```

### 步骤3: 触发部署

#### 方法1: 推送代码 (自动触发)
```bash
git add .
git commit -m "feat: 添加自动化部署配置"
git push origin main
```

#### 方法2: 手动触发
1. 在GitHub仓库页面，进入 `Actions` 标签
2. 选择 `Deploy MT5 Data Source API to Windows Server` 工作流
3. 点击 `Run workflow`
4. 选择分支并点击 `Run workflow`

### 步骤4: 监控部署进度

#### 方法1: 使用监控脚本
```bash
python scripts/deploy_monitor.py TheSixer data-source
```

#### 方法2: 在GitHub Actions页面监控
1. 进入 `Actions` 标签
2. 点击正在运行的工作流
3. 查看详细日志

## 🔍 部署验证

### 1. 检查服务状态
```cmd
# 在服务器上执行
nssm status "MT5DataAPI"
```

### 2. 测试API端点
```bash
# 测试根路径
curl http://47.116.221.184:3020/

# 测试API文档
curl http://47.116.221.184:3020/docs
```

### 3. 查看服务日志
```cmd
# 在服务器上执行
nssm dump "MT5DataAPI"
```

## 🛠️ 故障排除

### 常见问题

#### 1. 连接服务器失败
- 检查服务器IP和端口是否正确
- 确认SSH服务正在运行
- 检查防火墙设置

#### 2. Python安装失败
- 确保有足够的磁盘空间
- 检查网络连接
- 尝试手动下载安装

#### 3. 服务启动失败
- 检查Python路径是否正确
- 确认所有依赖已安装
- 查看详细错误日志

#### 4. API无法访问
- 检查防火墙设置
- 确认服务正在运行
- 验证端口3020是否开放

### 日志查看

#### GitHub Actions日志
1. 进入 `Actions` 标签
2. 点击失败的工作流
3. 查看具体步骤的日志

#### 服务器日志
```cmd
# 查看服务状态
nssm status "MT5DataAPI"

# 查看服务配置
nssm dump "MT5DataAPI"

# 查看Windows事件日志
eventvwr.msc
```

## 📞 支持

如果遇到问题，请:

1. 检查GitHub Actions日志
2. 查看服务器上的服务状态
3. 确认所有Secrets设置正确
4. 验证服务器网络连接

## 🔄 更新部署

### 自动更新
推送代码到main分支会自动触发重新部署

### 手动更新
1. 在GitHub Actions页面手动触发工作流
2. 或使用以下命令:
```bash
git push origin main
```

## 📊 监控和维护

### 服务管理命令
```cmd
# 启动服务
nssm start "MT5DataAPI"

# 停止服务
nssm stop "MT5DataAPI"

# 重启服务
nssm restart "MT5DataAPI"

# 删除服务
nssm remove "MT5DataAPI" confirm
```

### 备份和恢复
```cmd
# 备份当前版本
xcopy /s /e C:\mt5-api\app C:\mt5-api\backup\app\

# 恢复备份
xcopy /s /e C:\mt5-api\backup\app\ C:\mt5-api\app\
```

---

🎉 **恭喜!** 你的MT5 Data Source API已成功部署到Windows Server!
