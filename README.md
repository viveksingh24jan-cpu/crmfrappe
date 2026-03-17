# Insurance CRM - Frappe CRM Customization

A customized Frappe CRM setup for insurance lead generation in India.

## Features

- **Lead Management** - Track insurance leads with custom fields:
  - Policy Type (Motor, Health, Life, Travel, Home, Fire, Marine)
  - Vehicle Details & Number
  - Coverage Amount
  - Preferred Insurer
  - Insurance Requirement

- **Deal Pipeline** - Track opportunities through funnel:
  - Policy Type
  - Premium Amount
  - Coverage Amount
  - Policy Tenure
  - Selected Insurer
  - Vehicle Details

## Quick Setup on New Device

### Prerequisites
```bash
# Install Homebrew (macOS)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install redis mariadb node yarn nvm

# Setup Node.js 24
export NVM_DIR="$HOME/.nvm"
source "/opt/homebrew/opt/nvm/nvm.sh"
nvm install 24
nvm alias default 24
```

### Initialize Frappe Bench
```bash
# Install frappe-bench
pipx install frappe-bench

# Initialize bench (skip assets initially)
bench init frappe-bench --skip-assets

cd frappe-bench

# Get CRM app
bench get-app crm https://github.com/frappe/crm.git

# Start services
brew services start redis
brew services start mariadb

# Create site
bench new-site crm.localhost --mariadb-root-username root --mariadb-root-password root --admin-password admin

# Install CRM
bench --site crm.localhost install-app crm
```

### Install Custom Fields
```bash
# Navigate to custom app
cd ../custom_app

# Install as bench app
bench get-app custom_app --path ..

# Or copy to apps and install
cp -r . ../frappe-bench/apps/insurance_crm
bench --site crm.localhost install-app insurance_crm
```

### Start Server
```bash
cd frappe-bench
bench start
```

### Access CRM
Add to hosts file:
```
127.0.0.1 crm.localhost
```

Visit: http://crm.localhost:8000
- Username: Administrator
- Password: admin

CRM: http://crm.localhost:8000/app/crm

## Project Structure

```
crmfrappe/
├── custom_app/          # Your customizations (push to git)
│   ├── __init__.py
│   ├── hooks.py         # Custom fields definition
│   └── apps.txt
├── frappe-bench/        # Local dev environment (not pushed)
├── crm/                # CRM app (git submodule or cloned)
└── README.md
```

## Troubleshooting

### MariaDB Connection Issues
```bash
# Start MariaDB
brew services start mariadb

# Set root password
mariadb -u root -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root'); FLUSH PRIVILEGES;"
```

### Redis Issues
```bash
brew services start redis
```

### Node Version
```bash
export NVM_DIR="$HOME/.nvm"
source "/opt/homebrew/opt/nvm/nvm.sh"
nvm use 24
```

## License
MIT
