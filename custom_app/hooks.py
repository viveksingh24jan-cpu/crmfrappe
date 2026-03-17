import frappe
from frappe.custom.custom_field import create_custom_field
from frappe.boot import get_bootinfo

def after_install():
    create_insurance_custom_fields()
    create_email_templates()
    create_property_setter()
    print("Insurance CRM Enterprise installed successfully!")

def after_app_install(app):
    if app == "insurance_crm":
        create_insurance_custom_fields()
        print("Insurance custom fields created!")

def create_property_setter():
    """Set list view columns for better UX"""
    # Set list view columns for CRM Lead
    if not frappe.db.exists("Property Setter", {"doc_type": "CRM Lead", "property": "title_field"}):
        frappe.get_doc({
            "doctype": "Property Setter",
            "doc_type": "CRM Lead",
            "property": "title_field",
            "value": "lead_name"
        }).insert(ignore_permissions=True)

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
        }
    ]

    all_fields = lead_fields + deal_fields + contact_fields

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
<p>Thank you for your interest in our insurance services. We have received your inquiry for {{ doc.policy_type }} insurance.</p>
<p>Our team will contact you within 24 hours.</p>
<p>Best regards,<br>{{ doc.company_name }}</p>
"""
        },
        {
            "name": "Quote Follow-up",
            "subject": "Your Insurance Quote - {{ doc.company_name }}",
            "content": """
<p>Dear {{ doc.customer_name }},</p>
<p>Please find attached the quote for your {{ doc.policy_type }} insurance.</p>
<p>Premium: {{ doc.premium_amount }}<br>Coverage: {{ doc.coverage_amount }}</p>
<p>Contact us for any questions.</p>
<p>Best regards,<br>{{ doc.company_name }}</p>
"""
        },
        {
            "name": "Policy Renewal Reminder",
            "subject": "Your {{ doc.policy_type }} Insurance is due for renewal",
            "content": """
<p>Dear {{ doc.customer_name }},</p>
<p>Your {{ doc.policy_type }} insurance policy is due for renewal on {{ doc.renewal_date }}.</p>
<p>Contact us for renewal quote and continue your coverage without interruption.</p>
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
