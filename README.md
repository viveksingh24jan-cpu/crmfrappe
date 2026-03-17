# Insurance CRM - Enterprise Edition

A production-ready, enterprise-grade Frappe CRM customization for insurance lead generation in India. Built with IRDAI compliance in mind.

## Features

### Core CRM Features
- **Lead Management** - Full lifecycle lead tracking
- **Deal Pipeline** - Visual sales funnel with probabilities
- **Contact Management** - Customer database with insurance-specific fields
- **Activity Tracking** - Calls, emails, meetings, tasks
- **Email Integration** - Built-in email templates

### Custom Fields (Insurance-Specific)
- **Policy Types**: Motor, Health, Life, Travel, Home, Fire, Marine
- **Lead Fields**: Vehicle Details, Coverage Amount, Preferred Insurer, Lead Rating
- **Deal Fields**: Premium Amount, Policy Tenure, Probability %, Expected Close Date

### Enterprise Features

#### Analytics & Reporting
- Lead funnel visualization
- Conversion rate tracking
- Drop-off analysis by stage
- Policy type performance
- Team performance metrics
- Revenue tracking

#### Automation
- Auto follow-up reminders
- Lead rating updates
- Activity logging
- Email notifications
- Status change workflows

#### Integrations
- Email templates ready
- WhatsApp integration ready
- SMS gateway ready
- Document generation

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

# Install frappe-bench
pipx install frappe-bench
```

### Initialize Project
```bash
# Clone this repository
git clone https://github.com/viveksingh24jan-cpu/crmfrappe.git
cd crmfrappe

# Initialize bench
bench init frappe-bench --skip-assets
cd frappe-bench

# Get CRM app
bench get-app crm https://github.com/frappe/crm.git

# Start services
brew services start redis
brew services start mariadb

# Setup MariaDB root (first time only)
mariadb -u root -e "SET PASSWORD FOR 'root'@'localhost' = PASSWORD('root'); FLUSH PRIVILEGES;"

# Create site
bench new-site crm.localhost --mariadb-root-username root --mariadb-root-password root --admin-password admin

# Install CRM
bench --site crm.localhost install-app crm

# Install custom app
cp -r ../custom_app apps/insurance_crm
bench --site crm.localhost install-app insurance_crm

# Start server
bench start
```

### Access
Add to hosts file (`sudo nano /etc/hosts`):
```
127.0.0.1 crm.localhost
```

Visit: http://crm.localhost:8000
- Username: Administrator
- Password: admin
- CRM: http://crm.localhost:8000/app/crm

## Using Analytics API

### Get Lead Funnel
```javascript
// In browser console or via API
frappe.call({
    method: "insurance_crm.analytics.get_lead_funnel_data",
    callback: function(r) {
        console.log(r.message);
    }
});
```

### Get Deal Pipeline
```javascript
frappe.call({
    method: "insurance_crm.analytics.get_deal_pipeline_data",
    callback: function(r) {
        console.log(r.message);
    }
});
```

### Get Performance Metrics
```javascript
frappe.call({
    method: "insurance_crm.analytics.get_performance_metrics",
    args: { days: 30 },
    callback: function(r) {
        console.log(r.message);
    }
});
```

## Project Structure

```
crmfrappe/
├── custom_app/                    # Your enterprise customizations
│   ├── __init__.py
│   ├── hooks.py                   # App hooks (custom fields, templates)
│   ├── insurance_crm/
│   │   ├── __init__.py
│   │   ├── analytics.py           # Analytics API endpoints
│   │   └── automation.py          # Workflow automations
│   ├── apps.txt
│   └── pyproject.toml
├── frappe-bench/                  # Local dev (not in git)
└── README.md
```

## Automation Features

1. **Lead Status Changes**
   - Auto-create activities on conversion
   - Send notification emails
   - Create follow-up tasks

2. **Deal Status Changes**
   - Auto-create policy creation tasks on win
   - Log lost reasons

3. **Scheduled Tasks**
   - Follow-up reminders (daily)
   - Overdue lead tracking
   - Auto-assignment (round-robin)

## Enterprise Enhancements Made

| Feature | Status | Description |
|---------|--------|-------------|
| Custom Fields | Done | Insurance-specific fields for leads/deals |
| Analytics | Done | Funnel, conversion, dropoff, team metrics |
| Automation | Done | Status changes, reminders, notifications |
| Email Templates | Done | 3 ready-to-use templates |
| Contact Fields | Done | DOB, occupation, primary insured |
| Deal Probability | Done | Win probability tracking |
| Follow-up Tracking | Done | Date-based reminders |

## License
MIT

## Author
Vivek Singh
