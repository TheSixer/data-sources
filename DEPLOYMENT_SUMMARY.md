# 📋 MT5 Data Source API 部署配置总结

## 🎯 项目概述

本项目已配置完整的GitHub Actions自动化部署流程，支持一键部署到Windows Server。

## 📁 项目结构

```
data-source/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions部署工作流
├── scripts/
│   ├── setup_github_secrets.py     # GitHub Secrets设置脚本
│   ├── server_setup.py             # 服务器初始化脚本
│   ├── deploy_monitor.py           # 部署监控脚本
│   └── test_deployment.py          # 部署测试脚本
├── deploy.py                       # 一键部署脚本
├── DEPLOYMENT_GUIDE.md             # 详细部署指南
├── QUICK_START.md                  # 快速开始指南
├── DEPLOYMENT_SUMMARY.md           # 部署配置总结
└── requirements.txt                # 项目依赖
```

## 🔧 部署配置

### 目标服务器
- **IP地址**: 47.116.221.184
- **操作系统**: Windows Server
- **用户名**: root
- **密码**: Longjia@3713
- **SSH端口**: 22

### GitHub仓库
- **所有者**: TheSixer
- **仓库名**: data-source
- **分支**: main

### 服务配置
- **服务名称**: MT5DataAPI
- **端口**: 3020
- **Python版本**: 3.11
- **部署目录**: C:\mt5-api

## 🚀 部署流程

### 1. GitHub Secrets配置
自动设置以下Secrets：
- `API_KEY`: API密钥
- `MT5_LOGIN`: MT5登录账号
- `MT5_PASSWORD`: MT5密码
- `MT5_SERVER`: MT5服务器地址
- `MT5_TIMEOUT`: MT5超时时间
- `SERVER_HOST`: 服务器IP
- `SERVER_USERNAME`: 服务器用户名
- `SERVER_PASSWORD`: 服务器密码
- `SERVER_PORT`: 服务器端口

### 2. 服务器初始化
- 安装Python 3.11
- 安装NSSM (Non-Sucking Service Manager)
- 创建部署目录
- 配置防火墙规则
- 设置环境变量

### 3. 应用部署
- 备份现有部署
- 上传新版本代码
- 安装Python依赖
- 配置Windows服务
- 启动API服务

### 4. 健康检查
- 验证服务状态
- 测试API端点
- 检查MT5连接

## 📊 监控和维护

### GitHub Actions监控
- **工作流名称**: Deploy MT5 Data Source API to Windows Server
- **触发条件**: 推送到main分支或手动触发
- **监控地址**: https://github.com/TheSixer/data-source/actions

### 服务管理命令
```cmd
# 查看服务状态
nssm status "MT5DataAPI"

# 启动服务
nssm start "MT5DataAPI"

# 停止服务
nssm stop "MT5DataAPI"

# 重启服务
nssm restart "MT5DataAPI"

# 查看服务配置
nssm dump "MT5DataAPI"
```

### 日志查看
- **GitHub Actions日志**: Actions页面查看
- **Windows事件日志**: eventvwr.msc
- **服务日志**: nssm dump命令

## 🔄 更新流程

### 自动更新
推送代码到main分支自动触发重新部署：
```bash
git add .
git commit -m "feat: 更新功能"
git push origin main
```

### 手动更新
1. 在GitHub Actions页面手动触发工作流
2. 或使用部署脚本重新部署

## 🛡️ 安全配置

### 防火墙规则
- 开放端口3020用于API访问
- 限制SSH访问来源

### 服务安全
- 使用Windows服务运行
- 配置适当的用户权限
- 定期更新依赖包

### 数据安全
- 敏感信息通过GitHub Secrets管理
- 环境变量加密存储
- 定期备份配置

## 📈 性能优化

### 服务配置
- 使用NSSM管理服务生命周期
- 配置自动重启机制
- 优化Python进程管理

### 监控指标
- 服务运行状态
- API响应时间
- 错误率统计
- 资源使用情况

## 🚨 故障排除

### 常见问题
1. **连接失败**: 检查网络和防火墙
2. **服务启动失败**: 检查Python路径和依赖
3. **API无响应**: 检查服务状态和端口
4. **MT5连接错误**: 检查凭据和网络

### 恢复流程
1. 检查GitHub Actions日志
2. 验证服务器连接
3. 重启服务
4. 回滚到备份版本

## 📞 支持信息

### 联系方式
- **邮箱**: longjia3713@163.com
- **GitHub**: https://github.com/TheSixer
- **项目地址**: https://github.com/TheSixer/data-source

### 文档链接
- **部署指南**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **快速开始**: [QUICK_START.md](QUICK_START.md)
- **API文档**: http://47.116.221.184:3020/docs

## 🎉 部署完成

### 访问地址
- **API服务**: http://47.116.221.184:3020
- **API文档**: http://47.116.221.184:3020/docs
- **ReDoc文档**: http://47.116.221.184:3020/redoc

### 验证命令
```bash
# 健康检查
curl http://47.116.221.184:3020/

# 运行测试脚本
python scripts/test_deployment.py
```

---

✅ **部署配置完成!** 你的MT5 Data Source API已准备好自动化部署。
