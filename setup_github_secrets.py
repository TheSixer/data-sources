#!/usr/bin/env python3
"""
GitHub Secrets 自动设置脚本
用于将本地 .env 文件中的配置同步到 GitHub Secrets
"""

import os
import sys
import requests
import base64
from pathlib import Path
from dotenv import load_dotenv
from nacl import encoding, public

def load_env_file(env_path):
    """加载环境变量文件"""
    if not os.path.exists(env_path):
        print(f"错误: 环境变量文件 {env_path} 不存在")
        return None
    
    load_dotenv(env_path)
    return {
        'API_KEY': os.getenv('API_KEY', 'your_api_key_here'),
        'MT5_LOGIN': os.getenv('MT5_LOGIN', 'your_mt5_login'),
        'MT5_PASSWORD': os.getenv('MT5_PASSWORD', 'your_mt5_password'),
        'MT5_SERVER': os.getenv('MT5_SERVER', 'your_mt5_server'),
        'MT5_TIMEOUT': os.getenv('MT5_TIMEOUT', '60000'),
        'SERVER_HOST': '47.116.221.184',
        'SERVER_USERNAME': 'Administrator',
        'SERVER_PASSWORD': 'Longjia@3713',
        'SERVER_PORT': '22'
    }

def get_public_key(owner, repo, token):
    """获取仓库的公钥"""
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取公钥失败: {response.status_code} - {response.text}")
        return None

def encrypt_secret(public_key, secret_value):
    """加密secret值"""
    public_key_bytes = base64.b64decode(public_key)
    box = public.SealedBox(public_key_bytes)
    encrypted_bytes = box.encrypt(secret_value.encode('utf-8'))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def create_github_secret(owner, repo, secret_name, secret_value, token):
    """创建GitHub Secret"""
    # 获取公钥
    public_key_data = get_public_key(owner, repo, token)
    if not public_key_data:
        return False
    
    # 加密secret
    encrypted_value = encrypt_secret(public_key_data['key'], secret_value)
    
    # 创建secret
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret_name}"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'encrypted_value': encrypted_value,
        'key_id': public_key_data['key_id']
    }
    
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [201, 204]:
        print(f"✅ 成功创建/更新secret: {secret_name}")
        return True
    else:
        print(f"❌ 创建secret失败 {secret_name}: {response.status_code} - {response.text}")
        return False

def main():
    """主函数"""
    print("🚀 GitHub Secrets 设置工具")
    print("=" * 50)
    
    # 检查参数
    if len(sys.argv) < 4:
        print("用法: python setup_github_secrets.py <owner> <repo> <github_token>")
        print("示例: python setup_github_secrets.py TheSixer data-source ghp_xxxxxxxx")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    github_token = sys.argv[3]
    
    # 加载环境变量
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        env_path = Path(__file__).parent / 'env.example'
    
    env_vars = load_env_file(env_path)
    if not env_vars:
        sys.exit(1)
    
    print(f"📁 仓库: {owner}/{repo}")
    print(f"🔑 环境文件: {env_path}")
    print()
    
    # 需要设置的secrets
    secrets_to_set = {
        'API_KEY': env_vars['API_KEY'],
        'MT5_LOGIN': env_vars['MT5_LOGIN'],
        'MT5_PASSWORD': env_vars['MT5_PASSWORD'],
        'MT5_SERVER': env_vars['MT5_SERVER'],
        'MT5_TIMEOUT': env_vars['MT5_TIMEOUT'],
        'SERVER_HOST': env_vars['SERVER_HOST'],
        'SERVER_USERNAME': env_vars['SERVER_USERNAME'],
        'SERVER_PASSWORD': env_vars['SERVER_PASSWORD'],
        'SERVER_PORT': env_vars['SERVER_PORT']
    }
    
    # 设置secrets
    success_count = 0
    total_count = len(secrets_to_set)
    
    for secret_name, secret_value in secrets_to_set.items():
        if create_github_secret(owner, repo, secret_name, secret_value, github_token):
            success_count += 1
    
    print()
    print("=" * 50)
    print(f"设置完成: {success_count}/{total_count} 个secrets成功设置")
    
    if success_count == total_count:
        print("✅ 所有secrets设置成功！")
        print("🚀 现在可以推送代码到main分支触发自动部署")
    else:
        print("⚠️ 部分secrets设置失败，请检查GitHub Token权限")
        sys.exit(1)

if __name__ == "__main__":
    main()
