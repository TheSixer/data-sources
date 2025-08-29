# 🚀 MT5 Data Source API 快速开始

## 📋 概述

本指南将帮助你在5分钟内完成MT5 Data Source API的自动化部署。

## ⚡ 超快速部署 (2分钟)

### 1. 获取GitHub Token
访问 [GitHub Token生成页面](https://github.com/settings/tokens) 并创建新的Personal Access Token，选择权限：
- ✅ `repo` (完整仓库访问权限)
- ✅ `workflow` (工作流权限)

### 2. 运行一键部署
```bash
python deploy.py YOUR_GITHUB_TOKEN
```

### 3. 等待部署完成
部署过程大约需要5-10分钟，包括：
- 设置GitHub Secrets
- 初始化Windows Server
- 安装Python和依赖
- 配置服务
- 启动API服务

### 4. 验证部署
```bash
python scripts/test_deployment.py
```

## 🌐 访问API

部署完成后，你可以通过以下地址访问：

- **API服务**: http://47.116.221.184:3020
- **API文档**: http://47.116.221.184:3020/docs
- **ReDoc文档**: http://47.116.221.184:3020/redoc

## 📊 监控部署

### GitHub Actions监控
访问: https://github.com/TheSixer/data-source/actions

### 本地监控
```bash
python scripts/deploy_monitor.py TheSixer data-source
```

## 🔧 常用命令

### 服务管理
```cmd
# 在服务器上执行
nssm start "MT5DataAPI"    # 启动服务
nssm stop "MT5DataAPI"     # 停止服务
nssm restart "MT5DataAPI"  # 重启服务
nssm status "MT5DataAPI"   # 查看状态
```

### 更新部署
```bash
# 推送代码自动触发重新部署
git push origin main

# 或手动触发GitHub Actions
```

### 测试API
```bash
# 健康检查
curl http://47.116.221.184:3020/

# 获取API文档
curl http://47.116.221.184:3020/docs
```

## 🛠️ 故障排除

### 常见问题

1. **部署失败**
   - 检查GitHub Token权限
   - 确认服务器连接正常
   - 查看GitHub Actions日志

2. **API无法访问**
   - 检查防火墙设置
   - 确认服务正在运行
   - 验证端口3020是否开放

3. **MT5连接失败**
   - 检查MT5凭据配置
   - 确认MT5服务器可访问
   - 验证网络连接

### 获取帮助

- 📖 详细文档: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- 🐛 问题反馈: GitHub Issues
- 📧 技术支持: longjia3713@163.com

## 🎯 下一步

1. **配置MT5凭据**: 在GitHub Secrets中设置正确的MT5登录信息
2. **测试API接口**: 使用API文档测试各种功能
3. **集成到应用**: 将API集成到你的交易系统中
4. **监控和维护**: 设置监控和告警机制

---

🎉 **恭喜!** 你的MT5 Data Source API已经成功部署并运行!
