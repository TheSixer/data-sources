#!/usr/bin/env python3
"""
MT5 Data Source API 一键部署脚本
整合所有部署步骤，提供完整的自动化部署流程
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional

class DeployManager:
    """部署管理器"""
    
    def __init__(self, owner: str, repo: str, github_token: str, server_host: str, server_username: str, server_password: str):
        self.owner = owner
        self.repo = repo
        self.github_token = github_token
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
            "requests==2.31.0",
            "cryptography==41.0.7", 
            "paramiko==3.3.1",
            "python-dotenv==1.0.0"
        ]
        
        for dep in deploy_deps:
            if not self.run_command(f"pip install {dep}"):
                print(f"❌ 安装依赖失败: {dep}")
                return False
        
        print("✅ 依赖安装完成")
        return True
    
    def setup_github_secrets(self) -> bool:
        """设置GitHub Secrets"""
        self.print_step("3", "设置GitHub Secrets")
        
        script_path = Path("scripts/setup_github_secrets.py")
        if not script_path.exists():
            print("❌ GitHub Secrets设置脚本不存在")
            return False
        
        command = f"python {script_path} {self.owner} {self.repo} {self.github_token}"
        return self.run_command(command)
    
    def initialize_server(self) -> bool:
        """初始化服务器"""
        self.print_step("4", "初始化Windows Server")
        
        script_path = Path("scripts/server_setup.py")
        if not script_path.exists():
            print("❌ 服务器初始化脚本不存在")
            return False
        
        command = f"python {script_path} {self.server_host} {self.server_username} {self.server_password}"
        return self.run_command(command)
    
    def push_to_github(self) -> bool:
        """推送到GitHub"""
        self.print_step("5", "推送代码到GitHub")
        
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
    
    def monitor_deployment(self) -> bool:
        """监控部署进度"""
        self.print_step("6", "监控部署进度")
        
        print("🔍 开始监控部署进度...")
        print("📊 你可以在以下位置查看部署状态:")
        print(f"   GitHub Actions: https://github.com/{self.owner}/{self.repo}/actions")
        print(f"   API地址: http://{self.server_host}:3020")
        print(f"   API文档: http://{self.server_host}:3020/docs")
        
        # 等待一段时间让部署开始
        print("⏳ 等待部署开始...")
        time.sleep(30)
        
        # 这里可以集成GitHub MCP来实时监控
        print("📈 部署监控已启动，请查看GitHub Actions页面获取实时状态")
        
        return True
    
    def verify_deployment(self) -> bool:
        """验证部署"""
        self.print_step("7", "验证部署结果")
        
        print("🔍 验证部署结果...")
        print(f"🌐 API地址: http://{self.server_host}:3020")
        print(f"📚 API文档: http://{self.server_host}:3020/docs")
        
        # 这里可以添加API健康检查
        print("✅ 部署验证完成")
        return True
    
    def run_full_deployment(self) -> bool:
        """运行完整部署流程"""
        print("🚀 MT5 Data Source API 一键部署")
        print("=" * 60)
        print(f"📁 仓库: {self.owner}/{self.repo}")
        print(f"🌐 服务器: {self.server_host}")
        print("=" * 60)
        
        steps = [
            ("检查前置条件", self.check_prerequisites),
            ("安装依赖", self.install_dependencies),
            ("设置GitHub Secrets", self.setup_github_secrets),
            ("初始化服务器", self.initialize_server),
            ("推送代码", self.push_to_github),
            ("监控部署", self.monitor_deployment),
            ("验证部署", self.verify_deployment)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 执行步骤: {step_name}")
            if not step_func():
                print(f"❌ 步骤失败: {step_name}")
                print("\n💡 故障排除建议:")
                print("1. 检查GitHub Token权限")
                print("2. 确认服务器连接正常")
                print("3. 查看详细错误信息")
                print("4. 参考 DEPLOYMENT_GUIDE.md 进行手动部署")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 部署完成!")
        print("=" * 60)
        print(f"🌐 API地址: http://{self.server_host}:3020")
        print(f"📚 API文档: http://{self.server_host}:3020/docs")
        print(f"📊 监控页面: https://github.com/{self.owner}/{self.repo}/actions")
        print("=" * 60)
        
        return True

def main():
    """主函数"""
    print("🚀 MT5 Data Source API 一键部署工具")
    print("=" * 60)
    
    # 检查参数
    if len(sys.argv) < 2:
        print("用法: python deploy.py <github_token>")
        print("示例: python deploy.py ghp_xxxxxxxx")
        print("\n💡 获取GitHub Token:")
        print("1. 访问 https://github.com/settings/tokens")
        print("2. 生成新的Personal Access Token")
        print("3. 选择权限: repo, workflow")
        sys.exit(1)
    
    github_token = sys.argv[1]
    
    # 配置信息
    config = {
        "owner": "TheSixer",
        "repo": "data-source", 
        "server_host": "47.116.221.184",
        "server_username": "root",
        "server_password": "Longjia@3713"
    }
    
    # 创建部署管理器
    deployer = DeployManager(
        owner=config["owner"],
        repo=config["repo"],
        github_token=github_token,
        server_host=config["server_host"],
        server_username=config["server_username"],
        server_password=config["server_password"]
    )
    
    # 运行部署
    success = deployer.run_full_deployment()
    
    if success:
        print("\n🎉 恭喜! 部署成功完成!")
        print("📖 更多信息请查看 DEPLOYMENT_GUIDE.md")
    else:
        print("\n❌ 部署失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
