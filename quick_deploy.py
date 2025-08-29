#!/usr/bin/env python3
"""
MT5 Data Source API 快速部署脚本
使用SSH命令直接部署到Windows Server
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class QuickDeploy:
    """快速部署类"""
    
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password
        
    def run_ssh_command(self, command: str) -> bool:
        """运行SSH命令"""
        try:
            print(f"执行SSH命令: {command}")
            
            # 使用sshpass或expect来处理密码
            # 在Windows上，我们可以使用PowerShell的ssh命令
            ssh_cmd = f'ssh {self.username}@{self.host} "{command}"'
            
            result = subprocess.run(
                ssh_cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.stdout:
                print(f"输出: {result.stdout}")
            if result.stderr:
                print(f"错误: {result.stderr}")
            
            if result.returncode == 0:
                print("命令执行成功")
                return True
            else:
                print(f"命令执行失败，返回码: {result.returncode}")
                return False
                
        except Exception as e:
            print(f"执行SSH命令时发生错误: {e}")
            return False
    
    def check_server_python(self) -> bool:
        """检查服务器Python安装"""
        print("检查服务器Python安装...")
        return self.run_ssh_command("python --version")
    
    def install_python_on_server(self) -> bool:
        """在服务器上安装Python"""
        print("在服务器上安装Python 3.11...")
        
        commands = [
            # 下载Python安装程序
            "powershell -Command \"Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' -OutFile 'C:\\python-3.11.8-amd64.exe'\"",
            
            # 安装Python
            "C:\\python-3.11.8-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1",
            
            # 清理安装文件
            "del C:\\python-3.11.8-amd64.exe"
        ]
        
        for cmd in commands:
            if not self.run_ssh_command(cmd):
                return False
        
        return True
    
    def create_deployment_dir(self) -> bool:
        """创建部署目录"""
        print("创建部署目录...")
        
        commands = [
            "mkdir C:\\mt5-api",
            "mkdir C:\\mt5-api\\logs",
            "mkdir C:\\mt5-api\\backup"
        ]
        
        for cmd in commands:
            if not self.run_ssh_command(cmd):
                return False
        
        return True
    
    def clone_repository(self) -> bool:
        """克隆代码仓库"""
        print("克隆代码仓库...")
        
        commands = [
            "cd C:\\mt5-api",
            "git clone https://github.com/TheSixer/data-source.git ."
        ]
        
        for cmd in commands:
            if not self.run_ssh_command(cmd):
                return False
        
        return True
    
    def install_dependencies(self) -> bool:
        """安装Python依赖"""
        print("安装Python依赖...")
        
        commands = [
            "cd C:\\mt5-api",
            "python -m pip install --upgrade pip",
            "pip install -r requirements.txt"
        ]
        
        for cmd in commands:
            if not self.run_ssh_command(cmd):
                return False
        
        return True
    
    def configure_firewall(self) -> bool:
        """配置防火墙"""
        print("配置防火墙...")
        
        firewall_cmd = (
            "netsh advfirewall firewall add rule "
            "name=\"MT5 Data API\" "
            "dir=in action=allow protocol=TCP localport=3020"
        )
        
        return self.run_ssh_command(firewall_cmd)
    
    def create_env_file(self) -> bool:
        """创建环境变量文件"""
        print("创建环境变量文件...")
        
        env_content = """# API Configuration
API_KEY=your_api_key_here

# MT5 Configuration
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
MT5_SERVER=your_mt5_server
MT5_TIMEOUT=60000
"""
        
        # 创建.env文件
        create_env_cmd = f'echo "{env_content}" > C:\\mt5-api\\.env'
        return self.run_ssh_command(create_env_cmd)
    
    def start_service(self) -> bool:
        """启动服务"""
        print("启动MT5 Data API服务...")
        
        commands = [
            "cd C:\\mt5-api",
            "python -m app.main"
        ]
        
        # 在后台启动服务
        start_cmd = "start /B python -m app.main"
        return self.run_ssh_command(start_cmd)
    
    def test_service(self) -> bool:
        """测试服务"""
        print("测试API服务...")
        
        # 等待服务启动
        time.sleep(10)
        
        test_cmd = "curl http://localhost:3020/"
        return self.run_ssh_command(test_cmd)
    
    def run_deployment(self) -> bool:
        """运行完整部署"""
        print("开始MT5 Data Source API部署...")
        print("=" * 60)
        print(f"目标服务器: {self.username}@{self.host}")
        print("=" * 60)
        
        steps = [
            ("检查Python安装", self.check_server_python),
            ("安装Python", self.install_python_on_server),
            ("创建部署目录", self.create_deployment_dir),
            ("克隆代码仓库", self.clone_repository),
            ("安装依赖", self.install_dependencies),
            ("配置防火墙", self.configure_firewall),
            ("创建环境文件", self.create_env_file),
            ("启动服务", self.start_service),
            ("测试服务", self.test_service)
        ]
        
        for step_name, step_func in steps:
            print(f"\n执行步骤: {step_name}")
            if not step_func():
                print(f"步骤失败: {step_name}")
                return False
        
        print("\n" + "=" * 60)
        print("部署完成!")
        print("=" * 60)
        print(f"API地址: http://{self.host}:3020")
        print(f"API文档: http://{self.host}:3020/docs")
        print("=" * 60)
        
        return True

def main():
    """主函数"""
    print("MT5 Data Source API 快速部署工具")
    print("=" * 60)
    
    # 配置信息
    host = "47.116.221.184"
    username = "Administrator"
    password = "Longjia@3713"
    
    # 创建部署器
    deployer = QuickDeploy(host, username, password)
    
    # 运行部署
    success = deployer.run_deployment()
    
    if success:
        print("\n部署成功完成!")
    else:
        print("\n部署失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
