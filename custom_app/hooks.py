import frappe
from frappe.custom.custom_field import create_custom_field

def after_install():
    create_insurance_custom_fields()
    print("Insurance CRM custom fields installed!")

def create_insurance_custom_fields():
    # Lead Custom Fields
    lead_fields = [
        {
            "dt": "CRM Lead",
            "fieldname": "policy_type",
            "label": "Policy Type",
            "fieldtype": "Select",
            "options": "Motor\nHealth\nLife\nTravel\nHome\nFire\nMarine\nOther",
            "insert_after": "company"
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
            "insert_after": "vehicle_details"
        },
        {
            "dt": "CRM Lead",
            "fieldname": "coverage_amount",
            "label": "Coverage Amount",
            "fieldtype": "Currency",
            "insert_after": "vehicle_number"
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
            "insert_after": "organization"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "premium_amount",
            "label": "Premium Amount",
            "fieldtype": "Currency",
            "insert_after": "policy_type"
        },
        {
            "dt": "CRM Deal",
            "fieldname": "coverage_amount",
            "label": "Coverage Amount",
            "fieldtype": "Currency",
            "insert_after": "premium_amount"
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
            "insert_after": "policy_tenure"
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
            "insert_after": "vehicle_details"
        }
    ]

    all_fields = lead_fields + deal_fields

    for field in all_fields:
        fieldname = field["fieldname"]
        dt = field["dt"]
        
        if not frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fieldname}):
            create_custom_field(dt, field)
            print(f"Created: {fieldname} in {dt}")

    frappe.db.commit()
    print("All insurance CRM custom fields created!")
