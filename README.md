## Vault Configuration

### Default Credentials
- **Vault Address**: `http://localhost:8200`
- **Root Token**: `root-token`

### Getting Started

1. **Start Vault**
   ```bash
   docker-compose up -d vault
   ```
   
   Vault will be available at http://localhost:8200

2. **Insert secrets** (loads from .env file)
   ```bash
   docker-compose run --rm app python insert.py
   ```

3. **Run the application**
   ```bash
   docker-compose up app
   ```

   This will automatically load secrets from Vault and start the application.

### Accessing Secrets in Your Application

Secrets from Vault are automatically loaded into your Python environment. Access them in your code like this:

```python
from config import load_secrets

secrets = load_secrets()
db_user = secrets.get('DB_USER')
db_pass = secrets.get('DB_PASS')
```