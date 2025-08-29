# 🔧 MT5 Data Source API 手动部署指南

由于服务器SSH连接问题，我们提供手动部署方案。

## 📋 问题诊断

### 当前状态
- ✅ 服务器可以ping通 (47.116.221.184)
- ❌ SSH端口22连接失败
- ❌ 无法通过SSH自动化部署

### 可能原因
1. 服务器SSH服务未启动
2. 防火墙阻止22端口
3. 服务器配置问题
4. 网络策略限制

## 🚀 手动部署方案

### 方案1: 修复服务器SSH (推荐)

#### 1. 联系服务器管理员
- 确认SSH服务状态
- 检查防火墙设置
- 验证用户权限

#### 2. 手动启动SSH服务
如果可以直接访问服务器，执行以下命令：

```cmd
# 检查SSH服务状态
sc query sshd

# 启动SSH服务
net start sshd

# 或者使用OpenSSH
net start OpenSSHSSHD
```

#### 3. 配置防火墙
```cmd
# 开放22端口
netsh advfirewall firewall add rule name="SSH" dir=in action=allow protocol=TCP localport=22
```

### 方案2: 手动部署到服务器

#### 1. 直接访问服务器
- 通过远程桌面连接 (RDP)
- 或通过控制台访问

#### 2. 手动安装Python 3.11
```cmd
# 下载Python安装程序
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'C:\python-3.11.8-amd64.exe'"

# 安装Python
C:\python-3.11.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1

# 清理安装文件
del C:\python-3.11.8-amd64.exe
```

#### 3. 安装NSSM
```cmd
# 创建NSSM目录
mkdir C:\nssm

# 下载NSSM
powershell -Command "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'C:\nssm\nssm.zip'"

# 解压NSSM
powershell -Command "Expand-Archive -Path 'C:\nssm\nssm.zip' -DestinationPath 'C:\nssm' -Force"

# 复制nssm.exe
copy C:\nssm\nssm-2.24\win64\nssm.exe C:\nssm\

# 清理临时文件
rmdir /s /q C:\nssm\nssm-2.24
del C:\nssm\nssm.zip

# 添加到PATH
setx PATH "%PATH%;C:\nssm" /M
```

#### 4. 创建部署目录
```cmd
mkdir C:\mt5-api
mkdir C:\mt5-api\logs
mkdir C:\mt5-api\backup
```

#### 5. 配置防火墙
```cmd
netsh advfirewall firewall add rule name="MT5 Data API" dir=in action=allow protocol=TCP localport=3020
```

#### 6. 下载项目代码
```cmd
cd C:\mt5-api

# 使用Git下载
git clone https://github.com/TheSixer/data-source.git .

# 或者手动下载ZIP文件并解压
```

#### 7. 安装Python依赖
```cmd
cd C:\mt5-api
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 8. 配置环境变量
创建 `.env` 文件：
```env
# API Configuration
API_KEY=your_api_key_here

# MT5 Configuration
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server
MT5_TIMEOUT=60000
```

#### 9. 安装Windows服务
```cmd
cd C:\mt5-api

# 安装服务
nssm install "MT5DataAPI" "C:\Python311\python.exe" "-m app.main"
nssm set "MT5DataAPI" AppDirectory "C:\mt5-api"
nssm set "MT5DataAPI" Description "MT5 Data Source API Service"
nssm set "MT5DataAPI" Start SERVICE_AUTO_START

# 启动服务
nssm start "MT5DataAPI"
```

#### 10. 验证部署
```cmd
# 检查服务状态
nssm status "MT5DataAPI"

# 测试API
curl http://localhost:3020/
```

### 方案3: 使用其他部署方式

#### 1. 使用Docker (如果服务器支持)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 3020

CMD ["python", "-m", "app.main"]
```

#### 2. 使用IIS + FastCGI
- 配置IIS服务器
- 安装Python FastCGI模块
- 配置应用程序池

## 🔍 故障排除

### SSH连接问题
1. **检查SSH服务**
   ```cmd
   sc query sshd
   sc query OpenSSHSSHD
   ```

2. **检查端口监听**
   ```cmd
   netstat -an | findstr :22
   ```

3. **检查防火墙**
   ```cmd
   netsh advfirewall firewall show rule name="SSH"
   ```

### 服务启动问题
1. **检查Python路径**
   ```cmd
   where python
   python --version
   ```

2. **检查依赖安装**
   ```cmd
   pip list
   ```

3. **查看服务日志**
   ```cmd
   nssm dump "MT5DataAPI"
   eventvwr.msc
   ```

## 📞 技术支持

### 联系信息
- **邮箱**: longjia3713@163.com
- **GitHub**: https://github.com/TheSixer
- **项目地址**: https://github.com/TheSixer/data-source

### 获取帮助
1. 检查服务器SSH配置
2. 确认网络连接正常
3. 验证用户权限
4. 查看系统日志

## 🎯 下一步

1. **修复SSH连接** (推荐)
   - 联系服务器管理员
   - 配置SSH服务
   - 测试连接

2. **手动部署**
   - 按照上述步骤手动安装
   - 配置服务
   - 验证部署

3. **使用替代方案**
   - Docker部署
   - IIS部署
   - 其他部署方式

---

💡 **建议**: 优先修复SSH连接问题，这样可以继续使用自动化部署流程。
