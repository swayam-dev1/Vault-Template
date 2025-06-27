import os
from dotenv import load_dotenv
import hvac

def load_env_file():
    """Load environment variables from .env file."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    return load_dotenv(env_path, override=True)

def get_vault_client():
    """Initialize and return a Vault client."""
    vault_addr = os.getenv("VAULT_ADDR", "http://vault:8200")
    vault_token = os.getenv("VAULT_TOKEN", "root-token")
    
    print(f"Connecting to Vault at {vault_addr}")
    
    try:
        client = hvac.Client(
            url=vault_addr,
            token=vault_token,
            timeout=10
        )
        
        # Test the connection
        if not client.sys.is_initialized():
            raise Exception("Vault is not initialized")
            
        if not client.is_authenticated():
            raise Exception("Failed to authenticate with Vault. Check your VAULT_TOKEN.")
            
        print("Successfully connected to Vault")
        return client
        
    except Exception as e:
        print(f"Error connecting to Vault: {str(e)}")
        raise

def setup_kv_v2(client):
    """Set up KV v2 secrets engine if not already enabled."""
    if "secret/" not in client.sys.list_mounted_secrets_engines():
        client.sys.enable_secrets_engine("kv", path="secret", options={"version": "2"})

def get_secrets_from_env():
    """Extract non-VAULT_* environment variables as secrets."""
    return {
        k: v for k, v in os.environ.items()
        if not k.startswith('VAULT_') and not k.startswith('_')
    }

def main():
    # Load .env file
    if not load_env_file():
        print("⚠️  No .env file found or it's empty")

    # Initialize Vault client
    client = get_vault_client()
    
    # Set up KV v2
    setup_kv_v2(client)
    
    # Get secrets from .env
    secrets = get_secrets_from_env()
    
    if not secrets:
        print("⚠️  No secrets found in .env file")
        return
    
    # Store secrets in Vault
    client.secrets.kv.v2.create_or_update_secret(
        mount_point="secret",
        path="app/config",
        secret=secrets
    )
    
    print("✅ Successfully stored secrets in Vault at secret/app/config")
    print(f"   Loaded {len(secrets)} variables from .env")
    print("\nStored variables:")
    for key in sorted(secrets.keys()):
        print(f"   - {key}")

if __name__ == "__main__":
    main()
