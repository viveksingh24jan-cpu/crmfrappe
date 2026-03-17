import frappe
from frappe.custom.custom_field import create_custom_field

def after_install():
    create_insurance_custom_fields()
    create_email_templates()
    create_workspace()
    print("Insurance CRM Enterprise v2.0 installed successfully!")

def after_app_install(app):
    if app == "insurance_crm":
        create_insurance_custom_fields()
        print("Insurance custom fields created!")

def create_insurance_custom_fields():
    """Create all insurance-related custom fields"""
    
    # Lead Custom Fields
    lead_fields = [
        {
            "dt": "CRM Lead",
            "fieldname": "policy_type",
            "label": "Policy Type",
            "fieldtype": "Select",
            "options": "Motor\nHealth\nLife\nTravel\nHome\nFire\nMarine\nOther",
            "insert_after": "company",
            "in_list_view": 1,
            "in_filter": 1
        },
        {
            "dt": "CRM Lead",
            "fieldname": "vehicle_details",
            "label": "Vehicle Details",
            "fieldtype": "Small Text",
            "insert_after": "policy_type"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "vehicle_number",
            "label": "Vehicle Number",
            "fieldtype": "Data",
            "insert_after": "vehicle_details",
            "depends_on": "eval:doc.policy_type == 'Motor'"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "coverage_amount",
            "label": "Coverage Amount",
            "fieldtype": "Currency",
            "insert_after": "vehicle_number",
            "in_list_view": 1
        },
        {
            "dt": "CRM Lead",
            "fieldname": "preferred_insurer",
            "label": "Preferred Insurer",
            "fieldtype": "Data",
            "insert_after": "coverage_amount"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "insurance_requirement",
            "label": "Insurance Requirement",
            "fieldtype": "Text Editor",
            "insert_after": "preferred_insurer"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "lead_source_detail",
            "label": "Lead Source Detail",
            "fieldtype": "Data",
            "insert_after": "source"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "lead_rating",
            "label": "Lead Rating",
            "fieldtype": "Select",
            "options": "Hot\nWarm\nCold",
            "insert_after": "lead_source_detail",
            "in_list_view": 1,
            "in_filter": 1,
            "default": "Warm"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "follow_up_date",
            "label": "Follow-up Date",
            "fieldtype": "Date",
            "insert_after": "lead_rating"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "last_contact_date",
            "label": "Last Contact Date",
            "fieldtype": "Date",
            "insert_after": "follow_up_date",
            "read_only": 1
        },
        {
            "dt": "CRM Lead",
            "fieldname": "whatsapp_opted_in",
            "label": "WhatsApp Opted In",
            "fieldtype": "Check",
            "insert_after": "last_contact_date",
            "description": "Customer has opted in for WhatsApp updates"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "utm_campaign",
            "label": "UTM Campaign",
            "fieldtype": "Data",
            "insert_after": "whatsapp_opted_in"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "utm_source",
            "label": "UTM Source",
            "fieldtype": "Data",
            "insert_after": "utm_campaign"
        }
    ]

    # Deal Custom Fields
    deal_fields = [
        {
            "dt": "CRM Deal",
            "fieldname": "policy_type",
            "label": "Policy Type",
            "fieldtype": "Select",
            "options": "Motor\nHealth\nLife\nTravel\nHome\nFire\nMarine\nOther",
            "insert_after": "organization",
            "in_list_view": 1,
            "in_filter": 1
        },
        {
            "dt": "CRM Deal",
            "fieldname": "premium_amount",
            "label": "Premium Amount",
            "fieldtype": "Currency",
            "insert_after": "policy_type",
            "in_list_view": 1
        },
        {
            "dt": "CRM Deal",
            "fieldname": "coverage_amount",
            "label": "Coverage Amount",
            "fieldtype": "Currency",
            "insert_after": "premium_amount",
            "in_list_view": 1
        },
        {
            "dt": "CRM Deal",
            "fieldname": "policy_tenure",
            "label": "Policy Tenure (Years)",
            "fieldtype": "Int",
            "insert_after": "coverage_amount"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "selected_insurer",
            "label": "Selected Insurer",
            "fieldtype": "Data",
            "insert_after": "policy_tenure",
            "in_list_view": 1
        },
        {
            "dt": "CRM Deal",
            "fieldname": "vehicle_details",
            "label": "Vehicle Details",
            "fieldtype": "Small Text",
            "insert_after": "selected_insurer"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "vehicle_number",
            "label": "Vehicle Number",
            "fieldtype": "Data",
            "insert_after": "vehicle_details",
            "depends_on": "eval:doc.policy_type == 'Motor'"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "deal_probability",
            "label": "Probability (%)",
            "fieldtype": "Percent",
            "insert_after": "vehicle_number",
            "in_list_view": 1,
            "default": "50"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "expected_close_date",
            "label": "Expected Close Date",
            "fieldtype": "Date",
            "insert_after": "deal_probability"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "lost_reason",
            "label": "Lost Reason",
            "fieldtype": "Small Text",
            "insert_after": "expected_close_date"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "quote_validity",
            "label": "Quote Validity (Days)",
            "fieldtype": "Int",
            "insert_after": "lost_reason",
            "default": "30"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "payment_link",
            "label": "Payment Link",
            "fieldtype": "Data",
            "read_only": 1,
            "insert_after": "quote_validity"
        }
    ]

    # Contact Fields
    contact_fields = [
        {
            "dt": "Contact",
            "fieldname": "date_of_birth",
            "label": "Date of Birth",
            "fieldtype": "Date",
            "insert_after": "phone"
        },
        {
            "dt": "Contact",
            "fieldname": "occupation",
            "label": "Occupation",
            "fieldtype": "Data",
            "insert_after": "date_of_birth"
        },
        {
            "dt": "Contact",
            "fieldname": "is_primary_insured",
            "label": "Is Primary Insured",
            "fieldtype": "Check",
            "insert_after": "occupation"
        },
        {
            "dt": "Contact",
            "fieldname": "whatsapp_number",
            "label": "WhatsApp Number",
            "fieldtype": "Data",
            "insert_after": "is_primary_insured"
        }
    ]

    # Activity Fields
    activity_fields = [
        {
            "dt": "CRM Activity",
            "fieldname": "call_duration",
            "label": "Call Duration (Minutes)",
            "fieldtype": "Int",
            "insert_after": "status"
        },
        {
            "dt": "CRM Activity",
            "fieldname": "call_recording_url",
            "label": "Call Recording URL",
            "fieldtype": "Data",
            "insert_after": "call_duration"
        }
    ]

    all_fields = lead_fields + deal_fields + contact_fields + activity_fields

    for field in all_fields:
        fieldname = field["fieldname"]
        dt = field["dt"]
        
        if not frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fieldname}):
            create_custom_field(dt, field)
            print(f"Created: {fieldname} in {dt}")

    frappe.db.commit()
    print("All custom fields created!")

def create_email_templates():
    """Create email templates for insurance communications"""
    templates = [
        {
            "name": "Lead Acknowledgment",
            "subject": "Thank you for your interest in {{ doc.company_name }}",
            "content": """
<p>Dear {{ doc.customer_name }},</p>
<p>Thank you for your interest in our insurance services. We have received your inquiry for <strong>{{ doc.policy_type }} insurance</strong>.</p>
<p>Our team will contact you within 24 hours.</p>
<h3>What happens next?</h3>
<ul>
<li>We'll understand your insurance needs</li>
<li>Compare quotes from top insurers</li>
<li>Help you choose the best coverage</li>
</ul>
<p>Best regards,<br>{{ doc.company_name }}</p>
"""
        },
        {
            "name": "Quote Follow-up",
            "subject": "Your Insurance Quote - {{ doc.company_name }}",
            "content": """
<p>Dear {{ doc.customer_name }},</p>
<p>Please find attached the quote for your <strong>{{ doc.policy_type }} insurance</strong>.</p>
<h3>Quote Summary:</h3>
<table>
<tr><td>Premium:</td><td>{{ doc.premium_amount }}</td></tr>
<tr><td>Coverage:</td><td>{{ doc.coverage_amount }}</td></tr>
<tr><td>Tenure:</td><td>{{ doc.policy_tenure }} Years</td></tr>
</table>
<p>This quote is valid for {{ doc.quote_validity }} days.</p>
<p>Contact us for any questions or to proceed.</p>
<p>Best regards,<br>{{ doc.company_name }}</p>
"""
        },
        {
            "name": "Policy Renewal Reminder",
            "subject": "Your {{ doc.policy_type }} Insurance is due for renewal",
            "content": """
<p>Dear {{ doc.customer_name }},</p>
<p>Your <strong>{{ doc.policy_type }} insurance</strong> policy is due for renewal on <strong>{{ doc.renewal_date }}</strong>.</p>
<p>Don't let your coverage lapse! Contact us for:</p>
<ul>
<li>Renewal quote with best offers</li>
<li>Policy comparison</li>
<li>Free expert consultation</li>
</ul>
<p>Best regards,<br>{{ doc.company_name }}</p>
"""
        },
        {
            "name": "Lead Follow-up",
            "subject": "Following up on your insurance inquiry",
            "content": """
<p>Dear {{ doc.customer_name }},</p>
<p>I wanted to follow up on your inquiry for <strong>{{ doc.policy_type }} insurance</strong>.</p>
<p>Have you had a chance to review our proposal? I'm here to answer any questions you may have.</p>
<p>Feel free to reach out anytime!</p>
<p>Best regards,<br>{{ doc.company_name }}</p>
"""
        }
    ]
    
    for template in templates:
        if not frappe.db.exists("Email Template", template["name"]):
            doc = frappe.get_doc({
                "doctype": "Email Template",
                "name": template["name"],
                "subject": template["subject"],
                "content": template["content"]
            })
            doc.insert(ignore_permissions=True)
            print(f"Created email template: {template['name']}")
    
    frappe.db.commit()

def create_workspace():
    """Create custom workspace for Insurance CRM"""
    if not frappe.db.exists("Workspace", "Insurance CRM"):
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "name": "Insurance CRM",
            "title": "Insurance CRM",
            "icon": "fa fa-shield",
            "content": json.dumps([
                {"type": "card", "data": {"title": "Leads", "items": [
                    {"type": "doc", "data": {"doc_type": "CRM Lead", "label": "All Leads", "icon": "fa fa-user"}},
                    {"type": "doc", "data": {"doc_type": "CRM Lead", "label": "Hot Leads", "filters": "{\"lead_rating\":\"Hot\"}", "icon": "fa fa-fire"}},
                    {"type": "doc", "data": {"doc_type": "CRM Lead", "label": "Today's Follow-ups", "filters": "{\"follow_up_date\":\"Today\"}", "icon": "fa fa-calendar"}}
                ]}},
                {"type": "card", "data": {"title": "Deals", "items": [
                    {"type": "doc", "data": {"doc_type": "CRM Deal", "label": "All Deals", "icon": "fa fa-handshake-o"}},
                    {"type": "doc", "data": {"doc_type": "CRM Deal", "label": "Open Pipeline", "filters": "{\"status\":\"Open\"}", "icon": "fa fa-filter"}}
                ]}},
                {"type": "card", "data": {"title": "Quick Actions", "items": [
                    {"type": "action", "data": {"action": "New Lead", "doc_type": "CRM Lead", "icon": "fa fa-plus"}},
                    {"type": "action", "data": {"action": "New Deal", "doc_type": "CRM Deal", "icon": "fa fa-plus"}},
                    {"type": "action", "data": {"action": "Schedule Call", "doc_type": "CRM Activity", "icon": "fa fa-phone"}}
                ]}}
            ])
        })
        workspace.insert(ignore_permissions=True)
        print("Created Insurance CRM workspace!")

import json
