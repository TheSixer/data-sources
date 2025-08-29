#!/usr/bin/env python3
"""
Windows Server 初始化脚本 (无emoji版本)
用于在目标服务器上安装必要的软件和配置环境
"""

import paramiko
import time
import sys
from typing import Optional

class WindowsServerSetup:
    """Windows服务器设置类"""
    
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = None
    
    def connect(self) -> bool:
        """连接到服务器"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                timeout=30
            )
            print(f"成功连接到服务器: {self.host}")
            return True
        except Exception as e:
            print(f"连接服务器失败: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.client:
            self.client.close()
            print("已断开服务器连接")
    
    def execute_command(self, command: str, timeout: int = 300) -> tuple:
        """执行命令"""
        try:
            print(f"执行命令: {command}")
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            
            # 获取输出
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            exit_code = stdout.channel.recv_exit_status()
            
            if output:
                print(f"输出: {output}")
            if error:
                print(f"错误: {error}")
            
            return exit_code, output, error
        except Exception as e:
            print(f"执行命令失败: {e}")
            return -1, "", str(e)
    
    def check_python_installation(self) -> bool:
        """检查Python安装"""
        print("检查Python安装...")
        exit_code, output, error = self.execute_command("python --version")
        
        if exit_code == 0 and "Python 3" in output:
            print("Python已安装")
            return True
        else:
            print("Python未安装或版本不符合要求")
            return False
    
    def install_python(self) -> bool:
        """安装Python 3.11"""
        print("安装Python 3.11...")
        
        # 下载Python安装程序
        download_cmd = (
            "powershell -Command \""
            "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe' "
            "-OutFile 'C:\\python-3.11.8-amd64.exe'"
            "\""
        )
        exit_code, output, error = self.execute_command(download_cmd, timeout=600)
        
        if exit_code != 0:
            print("下载Python安装程序失败")
            return False
        
        # 安装Python
        install_cmd = (
            "C:\\python-3.11.8-amd64.exe /quiet "
            "InstallAllUsers=1 PrependPath=1 "
            "Include_test=0 Include_pip=1"
        )
        exit_code, output, error = self.execute_command(install_cmd, timeout=600)
        
        if exit_code == 0:
            print("Python安装成功")
            # 清理安装文件
            self.execute_command("del C:\\python-3.11.8-amd64.exe")
            return True
        else:
            print("Python安装失败")
            return False
    
    def install_nssm(self) -> bool:
        """安装NSSM (Non-Sucking Service Manager)"""
        print("安装NSSM...")
        
        # 创建NSSM目录
        self.execute_command("mkdir C:\\nssm")
        
        # 下载NSSM
        download_cmd = (
            "powershell -Command \""
            "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' "
            "-OutFile 'C:\\nssm\\nssm.zip'"
            "\""
        )
        exit_code, output, error = self.execute_command(download_cmd, timeout=300)
        
        if exit_code != 0:
            print("下载NSSM失败")
            return False
        
        # 解压NSSM
        extract_cmd = (
            "powershell -Command \""
            "Expand-Archive -Path 'C:\\nssm\\nssm.zip' -DestinationPath 'C:\\nssm' -Force"
            "\""
        )
        exit_code, output, error = self.execute_command(extract_cmd)
        
        if exit_code != 0:
            print("解压NSSM失败")
            return False
        
        # 复制nssm.exe到根目录
        copy_cmd = "copy C:\\nssm\\nssm-2.24\\win64\\nssm.exe C:\\nssm\\"
        exit_code, output, error = self.execute_command(copy_cmd)
        
        if exit_code == 0:
            # 清理临时文件
            self.execute_command("rmdir /s /q C:\\nssm\\nssm-2.24")
            self.execute_command("del C:\\nssm\\nssm.zip")
            
            # 添加到PATH
            self.execute_command("setx PATH \"%PATH%;C:\\nssm\" /M")
            print("NSSM安装成功")
            return True
        else:
            print("NSSM安装失败")
            return False
    
    def create_deployment_directory(self) -> bool:
        """创建部署目录"""
        print("创建部署目录...")
        
        commands = [
            "mkdir C:\\mt5-api",
            "mkdir C:\\mt5-api\\logs",
            "mkdir C:\\mt5-api\\backup"
        ]
        
        for cmd in commands:
            exit_code, output, error = self.execute_command(cmd)
            if exit_code != 0:
                print(f"创建目录失败: {cmd}")
                return False
        
        print("部署目录创建成功")
        return True
    
    def configure_firewall(self) -> bool:
        """配置防火墙"""
        print("配置防火墙...")
        
        # 开放3020端口
        firewall_cmd = (
            "netsh advfirewall firewall add rule "
            "name=\"MT5 Data API\" "
            "dir=in action=allow protocol=TCP localport=3020"
        )
        exit_code, output, error = self.execute_command(firewall_cmd)
        
        if exit_code == 0:
            print("防火墙配置成功")
            return True
        else:
            print("防火墙配置失败")
            return False
    
    def setup_environment(self) -> bool:
        """设置环境变量"""
        print("设置环境变量...")
        
        # 设置Python路径
        python_path_cmd = "setx PYTHONPATH \"C:\\mt5-api\" /M"
        exit_code, output, error = self.execute_command(python_path_cmd)
        
        if exit_code == 0:
            print("环境变量设置成功")
            return True
        else:
            print("环境变量设置失败")
            return False
    
    def run_full_setup(self) -> bool:
        """运行完整设置"""
        print("开始Windows Server初始化...")
        print("=" * 60)
        
        try:
            # 连接服务器
            if not self.connect():
                return False
            
            # 检查并安装Python
            if not self.check_python_installation():
                if not self.install_python():
                    return False
            
            # 安装NSSM
            if not self.install_nssm():
                return False
            
            # 创建部署目录
            if not self.create_deployment_directory():
                return False
            
            # 配置防火墙
            if not self.configure_firewall():
                return False
            
            # 设置环境变量
            if not self.setup_environment():
                return False
            
            print("=" * 60)
            print("Windows Server初始化完成!")
            print("部署目录: C:\\mt5-api")
            print("NSSM路径: C:\\nssm\\nssm.exe")
            print("API端口: 3020")
            return True
            
        except Exception as e:
            print(f"初始化过程中发生错误: {e}")
            return False
        finally:
            self.disconnect()

def main():
    """主函数"""
    if len(sys.argv) < 4:
        print("用法: python server_setup_no_emoji.py <host> <username> <password> [port]")
        print("示例: python server_setup_no_emoji.py 47.116.221.184 root Longjia@3713")
        sys.exit(1)
    
    host = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 22
    
    print("MT5 Data Source API - Windows Server 初始化")
    print("=" * 60)
    
    setup = WindowsServerSetup(host, username, password, port)
    success = setup.run_full_setup()
    
    if success:
        print("\n服务器初始化成功，可以开始部署了!")
    else:
        print("\n服务器初始化失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
