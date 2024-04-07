import os

# Database configurations
PATH_TO_DB_FILE = os.getenv('PATH_TO_DB_FILE')
DB_PASSPHRASE = os.getenv('DB_PASSPHRASE')
DB_PASSPHRASE_SALT = os.getenv('DB_PASSPHRASE_SALT')

# Client configurations
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
PARTNER_ID = os.getenv('PARTNER_ID')

# Server configurations
AUTH_URL = os.getenv('AUTH_URL')
SERVER_HOST = os.getenv('SERVER_HOST')
SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_SCHEME = os.getenv('SERVER_SCHEME')

# UI configurations
PARTNER_NAME = os.getenv('PARTNER_NAME')
PARTNER_LOGO = os.getenv('PARTNER_LOGO')

# Scope configuration
DEFAULT_SCOPE = os.getenv('DEFAULT_SCOPE')

# Deep Link Expiration configuration (in seconds)
DEFAULT_EXPIRATION_TIME = int(os.getenv('DEFAULT_EXPIRATION_TIME'))