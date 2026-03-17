"""
Insurance CRM Automation Module
Automated workflows and actions for lead management
"""

import frappe
from frappe import _
from frappe.utils import now_datetime, today, add_days
from datetime import datetime, timedelta

def setup_automation_hooks():
    """Setup automation hooks for CRM Lead"""
    
    # Lead status change automation
    frappe.register_doc_method(
        "CRM Lead",
        "on_status_change",
        "insurance_crm.automation.on_status_change"
    )
    
    # Deal status change automation
    frappe.register_doc_method(
        "CRM Deal", 
        "on_status_change",
        "insurance_crm.automation.on_deal_status_change"
    )

# ============================================
# LEAD AUTOMATIONS
# ============================================

def on_status_change(self, method):
    """Handle lead status changes"""
    if self.status == "Converted":
        on_lead_converted(self)
    elif self.status == "Lost":
        on_lead_lost(self)
    elif self.status == "Qualified":
        on_lead_qualified(self)

def on_lead_converted(self):
    """Actions when lead is converted"""
    # Create a celebration activity
    activity = frappe.get_doc({
        "doctype": "CRM Activity",
        "activity_type": "Call",
        "lead": self.name,
        "status": "Completed",
        "description": f"Lead converted to customer - {self.company or self.lead_name}"
    })
    activity.insert(ignore_permissions=True)
    
    # Send welcome email (if email template exists)
    send_conversion_notification(self)

def on_lead_lost(self):
    """Actions when lead is lost"""
    # Log the loss reason if not set
    if not self.get("lost_reason"):
        frappe.flags.ignore_permissions = True
        
    # Create follow-up task for review after 30 days
    # This helps in re-activating old leads

def on_lead_qualified(self):
    """Actions when lead is qualified"""
    # Create a reminder to create proposal
    frappe.get_doc({
        "doctype": "CRM Activity",
        "activity_type": "Task",
        "lead": self.name,
        "status": "Pending",
        "description": "Create proposal for qualified lead",
        "due_date": add_days(today(), 2)
    }).insert(ignore_permissions=True)

def send_conversion_notification(lead):
    """Send notification on lead conversion"""
    # Get email template
    template = frappe.db.get_value("Email Template", "Lead Converted")
    if template:
        try:
            email_template = frappe.get_doc("Email Template", template)
            content = frappe.render_template(email_template.content, {"lead": lead})
            
            frappe.sendmail(
                recipients=lead.email_id,
                subject=email_template.subject,
                content=content
            )
        except Exception as e:
            frappe.log_error(f"Error sending conversion email: {e}")

# ============================================
# DEAL AUTOMATIONS  
# ============================================

def on_deal_status_change(self, method):
    """Handle deal status changes"""
    if self.status == "Won":
        on_deal_won(self)
    elif self.status == "Lost":
        on_deal_lost(self)

def on_deal_won(deal):
    """Actions when deal is won"""
    # Create policy creation task
    frappe.get_doc({
        "doctype": "CRM Activity",
        "activity_type": "Task",
        "deal": deal.name,
        "status": "Pending",
        "description": f"Create policy for {deal.organization or 'customer'}",
        "due_date": add_days(today(), 3)
    }).insert(ignore_permissions=True)
    
    # Log celebration
    frappe.get_doc({
        "doctype": "CRM Activity",
        "activity_type": "Call",
        "deal": deal.name,
        "status": "Completed",
        "description": f"Deal won! Premium: {deal.premium_amount}"
    }).insert(ignore_permissions=True)

def on_deal_lost(deal):
    """Actions when deal is lost"""
    # Log reason if not set
    frappe.get_doc({
        "doctype": "CRM Activity",
        "activity_type": "Call",
        "deal": deal.name,
        "status": "Completed",
        "description": f"Deal lost. Reason: {deal.lost_reason or 'Not specified'}"
    }).insert(ignore_permissions=True)

# ============================================
# AUTOMATED REMINDERS
# ============================================

def send_follow_up_reminders():
    """Send reminders for leads due for follow-up"""
    due_leads = frappe.get_all(
        "CRM Lead",
        filters={
            "follow_up_date": today(),
            "status": ["in", ["New", "Contacted", "Qualified"]]
        },
        fields=["name", "lead_name", "email_id", "phone", "owner"]
    )
    
    for lead in due_leads:
        # Create activity
        frappe.get_doc({
            "doctype": "CRM Activity",
            "activity_type": "Call",
            "lead": lead.name,
            "status": "Pending",
            "description": f"Follow-up reminder - due today"
        }).insert(ignore_permissions=True)

def check_overdue_followups():
    """Check for overdue follow-ups"""
    overdue = frappe.get_all(
        "CRM Lead",
        filters={
            "follow_up_date": ["<", today()],
            "status": ["in", ["New", "Contacted", "Qualified"]],
            "lead_rating": ["!=", "Cold"]
        },
        fields=["name", "lead_name", "follow_up_date"]
    )
    
    # Mark as cold if overdue by more than 3 days
    for lead in overdue:
        if lead.follow_up_date:
            days_overdue = (datetime.strptime(today(), "%Y-%m-%d") - 
                          datetime.strptime(lead.follow_up_date, "%Y-%m-%d")).days
            if days_overdue > 3:
                frappe.db.set_value("CRM Lead", lead.name, "lead_rating", "Cold")

# ============================================
# ASSIGNMENT AUTOMATION
# ============================================

def auto_assign_leads():
    """Automatically assign leads to agents using round-robin"""
    # Get active agents
    agents = frappe.get_all(
        "User",
        filters={"enabled": 1, "user_type": "Website User"},
        fields=["name"]
    )
    
    if not agents:
        return
    
    # Get unassigned leads
    unassigned = frappe.get_all(
        "CRM Lead",
        filters={"owner": ["=", "Administrator"]},
        fields=["name"],
        limit=5
    )
    
    # Simple round-robin assignment
    for i, lead in enumerate(unassigned):
        agent = agents[i % len(agents)]
        frappe.db.set_value("CRM Lead", lead.name, "owner", agent.name)

# ============================================
# EMAIL AUTOMATIONS
# ============================================

def send_lead_acknowledgment(lead):
    """Send acknowledgment email to new lead"""
    try:
        template = frappe.get_doc("Email Template", "Lead Acknowledgment")
        content = frappe.render_template(template.content, {
            "customer_name": lead.lead_name,
            "company_name": "Your Insurance Company",
            "policy_type": lead.policy_type
        })
        
        frappe.sendmail(
            recipients=lead.email_id,
            subject=template.subject,
            content=content
        )
        return True
    except Exception as e:
        frappe.log_error(f"Error sending acknowledgment: {e}")
        return False

def send_quote_followup(deal):
    """Send quote follow-up email"""
    try:
        template = frappe.get_doc("Email Template", "Quote Follow-up")
        content = frappe.render_template(template.content, {
            "customer_name": deal.organization,
            "company_name": "Your Insurance Company",
            "policy_type": deal.policy_type,
            "premium_amount": deal.premium_amount,
            "coverage_amount": deal.coverage_amount
        })
        
        frappe.sendmail(
            recipients=deal.contact_email,
            subject=template.subject,
            content=content
        )
        return True
    except Exception as e:
        frappe.log_error(f"Error sending quote followup: {e}")
        return False
