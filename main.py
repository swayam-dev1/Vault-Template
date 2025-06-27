from config import load_secrets
import os

def main():
    # Load secrets from Vault
    secrets = load_secrets()

    # Access specific variables
    db_username = secrets.get('POSTGRES_USER')
    db_password = secrets.get('POSTGRES_PASSWORD')
    api_key = secrets.get('API_KEY')

    # Example usage
    print("\n📋 Database Connection:")
    print(f"Username: {db_username}")
    print(f"Password: {(db_password) if db_password else 'Not set'}")
    print(f"Key: {'*' * 8}{api_key[-4:] if api_key else ''}")

    # You can also access them directly in your code
    # For example, to connect to a database:
    # connection = connect(
    #     user=secrets['db_username'],
    #     password=secrets['db_password'],
    #     host=secrets.get('db_host', 'localhost')
    # )

    print("\nApplication started successfully!")

if __name__ == "__main__":
    main()
