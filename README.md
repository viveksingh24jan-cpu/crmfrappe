# Insurance CRM - Enterprise Edition v2.0

A production-ready, enterprise-grade Frappe CRM customization for insurance lead generation in India. Built with IRDAI compliance in mind.

## Features

### Core CRM Features
- **Lead Management** - Full lifecycle lead tracking
- **Deal Pipeline** - Visual sales funnel with probabilities
- **Contact Management** - Customer database with insurance-specific fields
- **Activity Tracking** - Calls, emails, meetings, tasks

### Integrations (Open Source)
- **WhatsApp Business API** - Send quotes, reminders, notifications
- **SMS (Twilio/Nexmo)** - SMS alerts and updates
- **Razorpay** - Payment link generation for premium collection
- **Jitsi Meet** - Video calling for consultations
- **Chatwoot** - Live chat widget integration
- **AI Lead Scoring** - Automatic lead scoring based on multiple factors

### Analytics & Reporting
- Lead funnel visualization
- Conversion rate tracking
- Drop-off analysis by stage
- Policy type performance
- Team performance metrics
- Revenue tracking
- Real-time dashboard

### Automation
- Auto follow-up reminders
- Lead rating updates
- Activity logging
- Email/WhatsApp notifications
- Status change workflows

## Quick Setup

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
Add to hosts file:
```
127.0.0.1 crm.localhost
```

Visit: http://crm.localhost:8000
- Username: Administrator
- Password: admin

## Integration Setup

### WhatsApp Business API
1. Create WhatsApp Business Account
2. Get API credentials from Meta Developer Portal
3. Create "WhatsApp Settings" doctype with:
   - API URL
   - API Token
   - Enable WhatsApp: 1

### SMS (Twilio)
1. Create Twilio account
2. Get Account SID, Auth Token, and phone number
3. Create "SMS Settings" doctype

### Razorpay (India)
1. Create Razorpay account
2. Get Key ID and Key Secret
3. Create "Razorpay Settings" doctype

### Jitsi Meet
1. Use default meet.jit.si or host your own
2. Create "Jitsi Settings" doctype

### Chatwoot
1. Create Chatwoot account
2. Get Account ID and API Token
3. Create "Chatwoot Settings" doctype

## Using Integrations

### Send WhatsApp Message
```javascript
frappe.call({
    method: "insurance_crm.integrations.send_whatsapp",
    args: { phone: "9999999999", message: "Your quote is ready!" }
});
```

### Create Payment Link
```javascript
frappe.call({
    method: "insurance_crm.integrations.create_payment_link",
    args: { 
        amount: 5000,
        customer: { name: "John", email: "john@example.com", phone: "9999999999" },
        description: "Insurance Premium"
    }
});
```

### Create Video Meeting
```javascript
frappe.call({
    method: "insurance_crm.integrations.create_video_meeting",
    args: { topic: "Policy Discussion" }
});
```

### AI Lead Scoring
```javascript
frappe.call({
    method: "insurance_crm.integrations.calculate_lead_score",
    args: { lead: { lead_rating: "Hot", phone: "9999999999", ... } },
    callback: function(r) {
        console.log("Score:", r.message.score); // 0-100
    }
});

// Refresh all lead scores
frappe.call({
    method: "insurance_crm.integrations.refresh_lead_scores"
});
```

## Dashboard API

### Get All Dashboard Data
```javascript
frappe.call({
    method: "insurance_crm.dashboard.get_dashboard_data",
    callback: function(r) {
        console.log(r.message);
    }
});
```

### Get Kanban Data
```javascript
frappe.call({
    method: "insurance_crm.dashboard.get_kanban_data",
    args: { doctype: "CRM Lead" },
    callback: function(r) {
        console.log(r.message);
    }
});
```

## Custom Fields

| DocType | Field | Type | Description |
|---------|-------|------|-------------|
| CRM Lead | policy_type | Select | Motor/Health/Life/Travel/Home/Fire/Marine |
| CRM Lead | vehicle_details | Small Text | Vehicle information |
| CRM Lead | vehicle_number | Data | Registration number |
| CRM Lead | coverage_amount | Currency | Sum insured |
| CRM Lead | lead_rating | Select | Hot/Warm/Cold |
| CRM Lead | follow_up_date | Date | Next follow-up |
| CRM Lead | whatsapp_opted_in | Check | WhatsApp consent |
| CRM Deal | premium_amount | Currency | Premium value |
| CRM Deal | policy_tenure | Int | Years |
| CRM Deal | deal_probability | Percent | Win probability |
| CRM Deal | payment_link | Data | Razorpay link |
| Contact | whatsapp_number | Data | WhatsApp contact |

## Project Structure

```
crmfrappe/
├── custom_app/
│   ├── hooks.py                    # Custom fields, templates, workspace
│   ├── insurance_crm/
│   │   ├── analytics.py           # Analytics API
│   │   ├── automation.py          # Workflow automations
│   │   ├── integrations.py        # WhatsApp, SMS, Payment, Video, AI
│   │   └── dashboard.py           # Dashboard widgets
│   └── apps.txt
├── frappe-bench/                   # Local dev (not in git)
└── README.md
```

## Automation Features

1. **Lead Status Changes**
   - Auto-create activities on conversion
   - Send notification emails/WhatsApp
   - Create follow-up tasks

2. **Deal Status Changes**
   - Auto-create policy creation tasks on win
   - Log lost reasons

3. **Scheduled Tasks**
   - Follow-up reminders (daily)
   - Overdue lead tracking
   - Auto-assignment

## Enterprise v2.0 New Features

- WhatsApp Business integration
- SMS notifications
- Razorpay payment links
- Video calling with Jitsi
- AI-powered lead scoring
- Chatwoot live chat
- Dashboard widgets
- Custom workspace
- UTM tracking fields
- Quote validity tracking

## License
MIT

## Author
Vivek Singh
