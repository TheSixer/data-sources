#!/usr/bin/env python3
"""
MT5 Data Source API 一键自动化部署脚本
包含GitHub Secrets设置和代码推送，触发GitHub Actions自动部署
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional

class AutoDeploy:
    """自动化部署类"""
    
    def __init__(self, owner: str, repo: str, github_token: str):
        self.owner = owner
        self.repo = repo
        self.github_token = github_token
        
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
                encoding='utf-8'
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
    
    def setup_github_secrets(self) -> bool:
        """设置GitHub Secrets"""
        self.print_step("1", "设置GitHub Secrets")
        
        # 检查依赖
        try:
            import requests
            import nacl
        except ImportError:
            print("安装GitHub Secrets设置依赖...")
            if not self.run_command("pip install requests PyNaCl"):
                return False
        
        # 运行GitHub Secrets设置脚本
        script_path = Path("setup_github_secrets.py")
        if not script_path.exists():
            print("❌ GitHub Secrets设置脚本不存在")
            return False
        
        command = f"python setup_github_secrets.py {self.owner} {self.repo} {self.github_token}"
        return self.run_command(command)
    
    def commit_and_push(self) -> bool:
        """提交并推送代码"""
        self.print_step("2", "提交并推送代码到GitHub")
        
        # 检查git状态
        if not self.run_command("git status"):
            return False
        
        # 添加所有文件
        if not self.run_command("git add ."):
            return False
        
        # 提交更改
        commit_message = f"feat: 自动部署更新 - {time.strftime('%Y-%m-%d %H:%M:%S')}"
        if not self.run_command(f'git commit -m "{commit_message}"'):
            return False
        
        # 推送到main分支
        if not self.run_command("git push origin main"):
            return False
        
        return True
    
    def monitor_deployment(self) -> bool:
        """监控部署进度"""
        self.print_step("3", "监控GitHub Actions部署进度")
        
        print("🔍 监控部署进度...")
        print(f"📁 仓库: {self.owner}/{self.repo}")
        print(f"🚀 GitHub Actions: https://github.com/{self.owner}/{self.repo}/actions")
        print()
        
        # 这里可以集成GitHub MCP来获取实时状态
        # 由于MCP工具的限制，我们提供监控指南
        
        print("📋 部署监控指南:")
        print("1. 访问GitHub Actions页面查看部署进度")
        print("2. 等待所有步骤完成（测试 -> 部署 -> 健康检查）")
        print("3. 检查部署日志确认成功")
        print("4. 测试API端点: http://47.116.221.184:3020/")
        print()
        
        return True
    
    def test_deployment(self) -> bool:
        """测试部署结果"""
        self.print_step("4", "测试部署结果")
        
        print("🧪 测试API服务...")
        
        # 等待服务启动
        print("⏳ 等待服务启动（30秒）...")
        time.sleep(30)
        
        # 测试API端点
        test_url = "http://47.116.221.184:3020/"
        try:
            import requests
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200:
                print(f"✅ API服务测试成功: {response.json()}")
                return True
            else:
                print(f"❌ API服务测试失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API服务测试失败: {e}")
            return False
    
    def deploy(self):
        """执行完整部署流程"""
        print("🚀 MT5 Data Source API 一键自动化部署")
        print("=" * 60)
        print(f"📁 仓库: {self.owner}/{self.repo}")
        print(f"🔑 GitHub Token: {self.github_token[:8]}...")
        print("=" * 60)
        
        # 步骤1: 设置GitHub Secrets
        if not self.setup_github_secrets():
            print("❌ GitHub Secrets设置失败")
            return False
        
        # 步骤2: 提交并推送代码
        if not self.commit_and_push():
            print("❌ 代码推送失败")
            return False
        
        # 步骤3: 监控部署进度
        if not self.monitor_deployment():
            print("❌ 部署监控失败")
            return False
        
        # 步骤4: 测试部署结果
        if not self.test_deployment():
            print("❌ 部署测试失败")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 自动化部署完成!")
        print("=" * 60)
        print("📊 API地址: http://47.116.221.184:3020")
        print("📚 API文档: http://47.116.221.184:3020/docs")
        print("🔍 GitHub Actions: https://github.com/TheSixer/data-source/actions")
        print("=" * 60)
        
        return True

def main():
    """主函数"""
    print("MT5 Data Source API 一键自动化部署工具")
    print("=" * 50)
    
    # 检查参数
    if len(sys.argv) < 2:
        print("用法: python auto_deploy.py <github_token>")
        print("示例: python auto_deploy.py ghp_xxxxxxxx")
        print("\n获取GitHub Token:")
        print("1. 访问 https://github.com/settings/tokens")
        print("2. 生成新的Personal Access Token")
        print("3. 选择权限: repo, workflow")
        sys.exit(1)
    
    github_token = sys.argv[1]
    owner = "TheSixer"
    repo = "data-source"
    
    # 创建部署实例
    deployer = AutoDeploy(owner, repo, github_token)
    
    # 执行部署
    if deployer.deploy():
        print("✅ 部署成功完成!")
        sys.exit(0)
    else:
        print("❌ 部署失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()
