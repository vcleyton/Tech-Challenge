"""
Script para gerar chaves seguras para SECRET_KEY e JWT_SECRET_KEY
Execute: python generate_keys.py
"""

import secrets

def generate_secure_key(length=32):
    """Gera uma chave hexadecimal segura"""
    return secrets.token_hex(length)

if __name__ == "__main__":
    print("=" * 60)
    print("GERADOR DE CHAVES SEGURAS")
    print("=" * 60)
    
    secret_key = generate_secure_key()
    jwt_secret_key = generate_secure_key()
    
    print("\n📌 SECRET_KEY (para Flask):")
    print(f"   {secret_key}")
    
    print("\n📌 JWT_SECRET_KEY (para autenticação JWT):")
    print(f"   {jwt_secret_key}")
    
    print("\n" + "=" * 60)
    print("Adicione estas chaves no seu arquivo .env:")
    print("=" * 60)
    print(f'\nSECRET_KEY="{secret_key}"')
    print(f'JWT_SECRET_KEY="{jwt_secret_key}"')
    
    print("\n✅ Copie as chaves acima e cole no seu arquivo .env")
