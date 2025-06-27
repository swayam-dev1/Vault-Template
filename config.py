import os
import hvac

def load_secrets():
    client = hvac.Client(
        url=os.getenv("VAULT_ADDR"),
        token=os.getenv("VAULT_TOKEN")
    )
    
    try:
        response = client.secrets.kv.v2.read_secret_version(
            mount_point="secret",
            path="app/config"
        )
        return response["data"]["data"]
    except Exception as e:
        print(f"Error loading secrets: {e}")
        return {}
