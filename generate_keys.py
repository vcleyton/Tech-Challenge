"""
Script para gerar chaves seguras para SECRET_KEY e JWT_SECRET_KEY
Execute: python generate_keys.py

Este script cria automaticamente um arquivo .env com as chaves geradas.
"""

import secrets
import os

def generate_secure_key(length=32):
    """Gera uma chave hexadecimal segura"""
    return secrets.token_hex(length)

def create_env_file():
    """Cria arquivo .env com as chaves geradas"""
    
    env_file = ".env"
    
    # Verifica se arquivo .env já existe
    if os.path.exists(env_file):
        print(f"⚠️  Arquivo {env_file} já existe!")
        response = input("Deseja sobrescrever? (s/n): ").strip().lower()
        if response != 's':
            print("❌ Operação cancelada. Usando arquivo .env existente.")
            return False
    
    # Gera chaves
    secret_key = generate_secure_key()
    jwt_secret_key = generate_secure_key()
    
    # Conteúdo do arquivo .env
    env_content = f"""# Configurações de Segurança da Aplicação
# Este arquivo foi gerado automaticamente. NÃO commitar em git!
# Adicione .env ao .gitignore

SECRET_KEY={secret_key}
JWT_SECRET_KEY={jwt_secret_key}
DATABASE_URI=sqlite:///user.db
"""
    
    # Escreve arquivo .env
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        return True
    except Exception as e:
        print(f"❌ Erro ao criar arquivo .env: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("GERADOR DE CHAVES SEGURAS E ARQUIVO .ENV")
    print("=" * 70)
    
    if create_env_file():
        print("\n✅ Arquivo .env criado com sucesso!")
        print("\n📍 Conteúdo do arquivo .env:")
        print("-" * 70)
        with open(".env", 'r') as f:
            content = f.read()
            # Ocultar chaves por segurança ao exibir
            for line in content.split('\n'):
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    print(f"{key}={'*' * min(16, len(value))}")
                else:
                    print(line)
        print("-" * 70)
        print("\n⚠️  IMPORTANTE:")
        print("   1. Adicione .env ao .gitignore")
        print("   2. Nunca commite este arquivo no repositório")
        print("   3. Copie .env.example para controle de versão (sem valores)")
        print("\n✅ A aplicação está pronta para iniciar!")
    else:
        print("\n⚠️  Arquivo .env não foi criado. Faça manualmente:")
        
        secret_key = generate_secure_key()
        jwt_secret_key = generate_secure_key()
        
        print("\nCrie um arquivo chamado '.env' na raiz do projeto com:")
        print("-" * 70)
        print(f'SECRET_KEY={secret_key}')
        print(f'JWT_SECRET_KEY={jwt_secret_key}')
        print(f'DATABASE_URI=sqlite:///user.db')
        print("-" * 70)
