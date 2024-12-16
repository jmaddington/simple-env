# Server Configuration Editor

A simple flask-driven web interface for managing server configuration files, specifically designed for:
- Writing to .env files
- Adding SSH public keys to authorized_keys

## Features

### ENV File Editor
- Write-only interface for managing .env files
- Secure - never displays existing contents
- Clear success/error messages
- Simple, clean interface

### SSH Key Manager
- Two methods to add SSH keys:
  1. Paste SSH public keys directly
  2. Upload public key files (.pub)
- Automatically manages proper permissions
  - Sets 700 permissions on .ssh directory
  - Sets 600 permissions on authorized_keys file
- Appends new keys (doesn't overwrite existing)
- Basic SSH key format validation

## Security Features
- Password protection via HTTP Basic Auth
- Write-only operations (no reading of sensitive files)
- Proper file permissions handling
- No display of existing contents
- Environment variable based configuration

## Setup

1. Install requirements:
```bash
pip install flask
```

2. Set the password environment variable:
```bash
export ENV_PASSWORD="your_secure_password"
```

3. Run the server:
```bash
python debug_server.py
```

The server will run on port 8081 by default.

## Usage

1. Access the web interface at `http://localhost:8081`
2. Enter the configured password when prompted
3. Use either the ENV editor or SSH key manager as needed

## File Locations
- ENV file: `/home/app/.env`
- SSH authorized_keys: `/home/app/.ssh/authorized_keys`

## Development

To run in debug mode:
```bash
export FLASK_DEBUG=1
python debug_server.py
```

## Security Notes
- Always use HTTPS in production
- Set a strong password
- Run with appropriate system permissions