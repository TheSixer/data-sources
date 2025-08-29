#!/usr/bin/env python3
"""
MT5 Data Source API 简化部署脚本
跳过GitHub Secrets设置，直接进行服务器初始化和代码推送
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional

class SimpleDeployManager:
    """简化部署管理器"""
    
    def __init__(self, owner: str, repo: str, server_host: str, server_username: str, server_password: str):
        self.owner = owner
        self.repo = repo
        self.server_host = server_host
        self.server_username = server_username
        self.server_password = server_password
        
    def print_step(self, step: str, message: str):
        """打印步骤信息"""
        print(f"\n{'='*60}")
        print(f"🔧 步骤 {step}: {message}")
        print(f"{'='*60}")
    
    def run_command(self, command: str, cwd: Optional[str] = None) -> bool:
        """运行命令"""
        try:
            print(f"执行命令: {command}")
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'  # 忽略编码错误
            )
            
            if result.stdout:
                print(f"输出: {result.stdout}")
            if result.stderr:
                print(f"错误: {result.stderr}")
            
            if result.returncode == 0:
                print("✅ 命令执行成功")
                return True
            else:
                print(f"❌ 命令执行失败，返回码: {result.returncode}")
                return False
                
        except Exception as e:
            print(f"❌ 执行命令时发生错误: {e}")
            return False
    
    def check_prerequisites(self) -> bool:
        """检查前置条件"""
        self.print_step("1", "检查前置条件")
        
        # 检查Python版本
        if not self.run_command("python --version"):
            print("❌ Python未安装或不在PATH中")
            return False
        
        # 检查Git
        if not self.run_command("git --version"):
            print("❌ Git未安装或不在PATH中")
            return False
        
        # 检查是否在Git仓库中
        if not Path(".git").exists():
            print("❌ 当前目录不是Git仓库")
            return False
        
        # 检查远程仓库
        if not self.run_command("git remote -v"):
            print("❌ 未配置远程仓库")
            return False
        
        print("✅ 前置条件检查通过")
        return True
    
    def install_dependencies(self) -> bool:
        """安装依赖"""
        self.print_step("2", "安装Python依赖")
        
        # 升级pip
        if not self.run_command("python -m pip install --upgrade pip"):
            return False
        
        # 安装部署脚本依赖
        deploy_deps = [
            "paramiko==3.3.1",
            "python-dotenv==1.0.0"
        ]
        
        for dep in deploy_deps:
            if not self.run_command(f"pip install {dep}"):
                print(f"❌ 安装依赖失败: {dep}")
                return False
        
        print("✅ 依赖安装完成")
        return True
    
    def initialize_server(self) -> bool:
        """初始化服务器"""
        self.print_step("3", "初始化Windows Server")
        
        script_path = Path("scripts/server_setup_no_emoji.py")
        if not script_path.exists():
            print("❌ 服务器初始化脚本不存在")
            return False
        
        command = f"python {script_path} {self.server_host} {self.server_username} {self.server_password}"
        return self.run_command(command)
    
    def push_to_github(self) -> bool:
        """推送到GitHub"""
        self.print_step("4", "推送代码到GitHub")
        
        commands = [
            "git add .",
            "git commit -m \"feat: 添加自动化部署配置\"",
            f"git push origin main"
        ]
        
        for command in commands:
            if not self.run_command(command):
                return False
        
        print("✅ 代码推送成功")
        return True
    
    def show_next_steps(self) -> bool:
        """显示后续步骤"""
        self.print_step("5", "显示后续步骤")
        
        print("🔍 部署流程已启动，请按以下步骤完成部署:")
        print()
        print("📋 手动设置GitHub Secrets:")
        print("1. 访问: https://github.com/TheSixer/data-source/settings/secrets/actions")
        print("2. 点击 'New repository secret'")
        print("3. 添加以下Secrets:")
        print()
        print("   | Secret名称 | 值 | 说明 |")
        print("   |-----------|----|------|")
        print("   | API_KEY | your_api_key_here | API密钥 |")
        print("   | MT5_LOGIN | your_mt5_login | MT5登录账号 |")
        print("   | MT5_PASSWORD | your_mt5_password | MT5密码 |")
        print("   | MT5_SERVER | your_mt5_server | MT5服务器地址 |")
        print("   | MT5_TIMEOUT | 60000 | MT5超时时间 |")
        print("   | SERVER_HOST | 47.116.221.184 | 服务器IP |")
        print("   | SERVER_USERNAME | root | 服务器用户名 |")
        print("   | SERVER_PASSWORD | Longjia@3713 | 服务器密码 |")
        print("   | SERVER_PORT | 22 | 服务器SSH端口 |")
        print()
        print("🚀 触发部署:")
        print("1. 访问: https://github.com/TheSixer/data-source/actions")
        print("2. 选择 'Deploy MT5 Data Source API to Windows Server'")
        print("3. 点击 'Run workflow'")
        print("4. 选择分支 'main' 并点击 'Run workflow'")
        print()
        print("📊 监控部署:")
        print("- GitHub Actions: https://github.com/TheSixer/data-source/actions")
        print("- API地址: http://47.116.221.184:3020")
        print("- API文档: http://47.116.221.184:3020/docs")
        print()
        print("🧪 测试部署:")
        print("python scripts/test_deployment.py")
        
        return True
    
    def run_simple_deployment(self) -> bool:
        """运行简化部署流程"""
        print("🚀 MT5 Data Source API 简化部署")
        print("=" * 60)
        print(f"📁 仓库: {self.owner}/{self.repo}")
        print(f"🌐 服务器: {self.server_host}")
        print("=" * 60)
        
        steps = [
            ("检查前置条件", self.check_prerequisites),
            ("安装依赖", self.install_dependencies),
            ("初始化服务器", self.initialize_server),
            ("推送代码", self.push_to_github),
            ("显示后续步骤", self.show_next_steps)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 执行步骤: {step_name}")
            if not step_func():
                print(f"❌ 步骤失败: {step_name}")
                print("\n💡 故障排除建议:")
                print("1. 检查Git配置")
                print("2. 确认服务器连接正常")
                print("3. 查看详细错误信息")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 简化部署完成!")
        print("=" * 60)
        print("📋 请按照上述步骤手动设置GitHub Secrets并触发部署")
        print("📖 详细指南: DEPLOYMENT_GUIDE.md")
        print("=" * 60)
        
        return True

def main():
    """主函数"""
    print("🚀 MT5 Data Source API 简化部署工具")
    print("=" * 60)
    
    # 配置信息
    config = {
        "owner": "TheSixer",
        "repo": "data-source", 
        "server_host": "47.116.221.184",
        "server_username": "root",
        "server_password": "Longjia@3713"
    }
    
    # 创建部署管理器
    deployer = SimpleDeployManager(
        owner=config["owner"],
        repo=config["repo"],
        server_host=config["server_host"],
        server_username=config["server_username"],
        server_password=config["server_password"]
    )
    
    # 运行部署
    success = deployer.run_simple_deployment()
    
    if success:
        print("\n🎉 简化部署流程完成!")
        print("📖 请按照提示完成GitHub Secrets设置")
    else:
        print("\n❌ 简化部署失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
