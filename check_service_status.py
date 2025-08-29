#!/usr/bin/env python3
"""
检查MT5 Data Source API服务状态的脚本
"""

import paramiko
import time
import sys

def check_service_status():
    """检查服务器上的服务状态"""
    
    # 服务器配置
    host = "47.116.221.184"
    username = "Administrator"
    password = "Longjia@3713"
    port = 22
    
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("正在连接到服务器...")
        ssh.connect(host, port, username, password, timeout=10)
        print("✅ 连接成功")
        
        # 检查服务状态
        print("\n=== 检查Windows服务状态 ===")
        stdin, stdout, stderr = ssh.exec_command('nssm status "MT5DataAPI"')
        service_status = stdout.read().decode().strip()
        print(f"服务状态: {service_status}")
        
        # 检查进程
        print("\n=== 检查Python进程 ===")
        stdin, stdout, stderr = ssh.exec_command('tasklist /FI "IMAGENAME eq python.exe" /FO TABLE')
        python_processes = stdout.read().decode().strip()
        print(f"Python进程:\n{python_processes}")
        
        # 检查端口监听
        print("\n=== 检查端口3020监听状态 ===")
        stdin, stdout, stderr = ssh.exec_command('netstat -an | findstr :3020')
        port_status = stdout.read().decode().strip()
        print(f"端口3020状态:\n{port_status}")
        
        # 检查部署目录
        print("\n=== 检查部署目录 ===")
        stdin, stdout, stderr = ssh.exec_command('dir C:\\mt5-api')
        dir_content = stdout.read().decode().strip()
        print(f"部署目录内容:\n{dir_content}")
        
        # 检查环境变量文件
        print("\n=== 检查环境变量文件 ===")
        stdin, stdout, stderr = ssh.exec_command('type C:\\mt5-api\\.env')
        env_content = stdout.read().decode().strip()
        print(f"环境变量文件内容:\n{env_content}")
        
        # 尝试启动服务
        print("\n=== 尝试启动服务 ===")
        stdin, stdout, stderr = ssh.exec_command('nssm start "MT5DataAPI"')
        start_result = stdout.read().decode().strip()
        print(f"启动结果: {start_result}")
        
        # 等待几秒钟
        time.sleep(5)
        
        # 再次检查服务状态
        print("\n=== 重新检查服务状态 ===")
        stdin, stdout, stderr = ssh.exec_command('nssm status "MT5DataAPI"')
        service_status_after = stdout.read().decode().strip()
        print(f"服务状态: {service_status_after}")
        
        # 测试API端点
        print("\n=== 测试API端点 ===")
        stdin, stdout, stderr = ssh.exec_command('curl -f http://localhost:3020/')
        api_response = stdout.read().decode().strip()
        print(f"API响应: {api_response}")
        
        # 检查服务日志
        print("\n=== 检查服务日志 ===")
        stdin, stdout, stderr = ssh.exec_command('nssm dump "MT5DataAPI"')
        service_dump = stdout.read().decode().strip()
        print(f"服务配置:\n{service_dump}")
        
        ssh.close()
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔍 开始检查MT5 Data Source API服务状态...")
    success = check_service_status()
    if success:
        print("\n✅ 检查完成")
    else:
        print("\n❌ 检查失败")
        sys.exit(1)
