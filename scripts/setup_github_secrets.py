#!/usr/bin/env python3
"""
GitHub Secrets 设置脚本
用于将本地 .env 文件中的配置同步到 GitHub Secrets
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

def load_env_file(env_path):
    """加载环境变量文件"""
    if not os.path.exists(env_path):
        print(f"错误: 环境变量文件 {env_path} 不存在")
        return None
    
    load_dotenv(env_path)
    return {
        'API_KEY': os.getenv('API_KEY'),
        'MT5_LOGIN': os.getenv('MT5_LOGIN'),
        'MT5_PASSWORD': os.getenv('MT5_PASSWORD'),
        'MT5_SERVER': os.getenv('MT5_SERVER'),
        'MT5_TIMEOUT': os.getenv('MT5_TIMEOUT'),
        'SERVER_HOST': '47.116.221.184',
        'SERVER_USERNAME': 'root',
        'SERVER_PASSWORD': 'Longjia@3713',
        'SERVER_PORT': '22'
    }

def create_github_secret(owner, repo, secret_name, secret_value, token):
    """创建GitHub Secret"""
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # 获取公钥
    public_key_url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key"
    response = requests.get(public_key_url, headers=headers)
    
    if response.status_code != 200:
        print(f"错误: 无法获取公钥 - {response.status_code}")
        return False
    
    public_key_data = response.json()
    public_key = public_key_data['key']
    key_id = public_key_data['key_id']
    
    # 加密secret值
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    import base64
    
    try:
        public_key_obj = load_pem_public_key(public_key.encode())
        encrypted_value = public_key_obj.encrypt(
            secret_value.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encrypted_value_b64 = base64.b64encode(encrypted_value).decode()
    except Exception as e:
        print(f"错误: 加密失败 - {e}")
        return False
    
    # 创建secret
    data = {
        'encrypted_value': encrypted_value_b64,
        'key_id': key_id
    }
    
    response = requests.put(f"{url}/{secret_name}", headers=headers, json=data)
    
    if response.status_code in [201, 204]:
        print(f"✅ 成功创建 Secret: {secret_name}")
        return True
    else:
        print(f"❌ 创建 Secret 失败: {secret_name} - {response.status_code}")
        print(f"响应: {response.text}")
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
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        env_path = Path(__file__).parent.parent / 'env.example'
    
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
    
    success_count = 0
    total_count = len(secrets_to_set)
    
    for secret_name, secret_value in secrets_to_set.items():
        if not secret_value:
            print(f"⚠️  跳过空值 Secret: {secret_name}")
            continue
            
        print(f"正在设置 {secret_name}...")
        try:
            if create_github_secret(owner, repo, secret_name, secret_value, github_token):
                success_count += 1
        except Exception as e:
            print(f"❌ 设置 {secret_name} 时发生错误: {e}")
        print()
    
    print("=" * 50)
    print(f"✅ 完成! 成功设置 {success_count}/{total_count} 个 Secrets")
    
    if success_count == total_count:
        print("🎉 所有 Secrets 设置成功，可以开始部署了!")
    else:
        print("⚠️  部分 Secrets 设置失败，请检查错误信息")
        print("\n💡 建议手动设置剩余的Secrets:")
        for secret_name, secret_value in secrets_to_set.items():
            if not secret_value:
                print(f"   {secret_name}: [需要手动设置]")

if __name__ == "__main__":
    main()
