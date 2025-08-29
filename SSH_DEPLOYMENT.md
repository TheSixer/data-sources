# 🔧 SSH手动部署指南

## 📋 部署信息

- **服务器**: 47.116.221.184
- **用户名**: Administrator
- **密码**: Longjia@3713
- **SSH端口**: 22

## 🚀 部署步骤

### 1. 连接到服务器

```bash
ssh Administrator@47.116.221.184
```

### 2. 检查Python安装

```cmd
python --version
```

如果Python未安装，执行以下命令安装Python 3.11：

```cmd
# 下载Python安装程序
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'C:\python-3.11.8-amd64.exe'"

# 安装Python
C:\python-3.11.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1

# 清理安装文件
del C:\python-3.11.8-amd64.exe
```

### 3. 创建部署目录

```cmd
mkdir C:\mt5-api
mkdir C:\mt5-api\logs
mkdir C:\mt5-api\backup
```

### 4. 克隆代码仓库

```cmd
cd C:\mt5-api
git clone https://github.com/TheSixer/data-source.git .
```

### 5. 安装Python依赖

```cmd
cd C:\mt5-api
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. 配置防火墙

```cmd
netsh advfirewall firewall add rule name="MT5 Data API" dir=in action=allow protocol=TCP localport=3020
```

### 7. 创建环境变量文件

创建 `.env` 文件：

```cmd
cd C:\mt5-api
echo # API Configuration > .env
echo API_KEY=your_api_key_here >> .env
echo. >> .env
echo # MT5 Configuration >> .env
echo MT5_LOGIN=your_mt5_login >> .env
echo MT5_PASSWORD=your_mt5_password >> .env
echo MT5_SERVER=your_mt5_server >> .env
echo MT5_TIMEOUT=60000 >> .env
```

### 8. 启动服务

```cmd
cd C:\mt5-api
python -m app.main
```

### 9. 测试服务

在新的SSH会话中测试：

```cmd
curl http://localhost:3020/
```

## 🔍 验证部署

### 检查服务状态

```cmd
# 检查端口监听
netstat -an | findstr :3020

# 检查进程
tasklist | findstr python
```

### 访问API

- **API地址**: http://47.116.221.184:3020
- **API文档**: http://47.116.221.184:3020/docs
- **ReDoc文档**: http://47.116.221.184:3020/redoc

## 🛠️ 服务管理

### 启动服务

```cmd
cd C:\mt5-api
python -m app.main
```

### 停止服务

```cmd
# 查找Python进程
tasklist | findstr python

# 停止进程
taskkill /PID <进程ID> /F
```

### 查看日志

```cmd
cd C:\mt5-api\logs
dir
```

## 🔧 故障排除

### 常见问题

1. **Python未找到**
   ```cmd
   where python
   echo %PATH%
   ```

2. **依赖安装失败**
   ```cmd
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

3. **端口被占用**
   ```cmd
   netstat -ano | findstr :3020
   taskkill /PID <进程ID> /F
   ```

4. **防火墙问题**
   ```cmd
   netsh advfirewall firewall show rule name="MT5 Data API"
   ```

## 📞 技术支持

如果遇到问题，请检查：

1. Python版本是否为3.11+
2. 所有依赖是否正确安装
3. 防火墙是否配置正确
4. 端口3020是否可用

---

💡 **提示**: 建议使用Windows服务管理器来管理API服务，确保服务在系统重启后自动启动。
