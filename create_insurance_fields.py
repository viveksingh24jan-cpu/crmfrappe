import frappe
import json

def run():
    # Lead Custom Fields
    lead_fields = [
        {
            "fieldname": "policy_type",
            "label": "Policy Type",
            "fieldtype": "Select",
            "options": "Motor\nHealth\nLife\nTravel\nHome\nFire\nMarine\nOther",
            "insert_after": "company",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "vehicle_details",
            "label": "Vehicle Details",
            "fieldtype": "Small Text",
            "insert_after": "policy_type",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "vehicle_number",
            "label": "Vehicle Number",
            "fieldtype": "Data",
            "insert_after": "vehicle_details",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "coverage_amount",
            "label": "Coverage Amount",
            "fieldtype": "Currency",
            "insert_after": "vehicle_number",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "preferred_insurer",
            "label": "Preferred Insurer",
            "fieldtype": "Data",
            "insert_after": "coverage_amount",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "lead_source_detail",
            "label": "Lead Source Detail",
            "fieldtype": "Data",
            "insert_after": "source",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "insurance_requirement",
            "label": "Insurance Requirement",
            "fieldtype": "Text Editor",
            "insert_after": "preferred_insurer",
            "reqd": 0,
            "hidden": 0
        }
    ]

    # Deal Custom Fields
    deal_fields = [
        {
            "fieldname": "policy_type",
            "label": "Policy Type",
            "fieldtype": "Select",
            "options": "Motor\nHealth\nLife\nTravel\nHome\nFire\nMarine\nOther",
            "insert_after": "organization",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "premium_amount",
            "label": "Premium Amount",
            "fieldtype": "Currency",
            "insert_after": "policy_type",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "coverage_amount",
            "label": "Coverage Amount",
            "fieldtype": "Currency",
            "insert_after": "premium_amount",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "policy_tenure",
            "label": "Policy Tenure (Years)",
            "fieldtype": "Int",
            "insert_after": "coverage_amount",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "selected_insurer",
            "label": "Selected Insurer",
            "fieldtype": "Data",
            "insert_after": "policy_tenure",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "vehicle_details",
            "label": "Vehicle Details",
            "fieldtype": "Small Text",
            "insert_after": "selected_insurer",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "vehicle_number",
            "label": "Vehicle Number",
            "fieldtype": "Data",
            "insert_after": "vehicle_details",
            "reqd": 0,
            "hidden": 0
        },
        {
            "fieldname": "notes",
            "label": "Internal Notes",
            "fieldtype": "Text Editor",
            "insert_after": "notes",
            "reqd": 0,
            "hidden": 0
        }
    ]

    # Create Lead Custom Fields
    for field in lead_fields:
        if not frappe.db.exists("Custom Field", {"dt": "CRM Lead", "fieldname": field["fieldname"]}):
            cf = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "CRM Lead",
                "module": "CRM",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", ""),
                "insert_after": field["insert_after"],
                "reqd": field.get("reqd", 0),
                "hidden": field.get("hidden", 0)
            })
            cf.insert(ignore_permissions=True)
            print(f"Created custom field: {field['fieldname']} in Lead")

    # Create Deal Custom Fields
    for field in deal_fields:
        if not frappe.db.exists("Custom Field", {"dt": "CRM Deal", "fieldname": field["fieldname"]}):
            cf = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "CRM Deal",
                "module": "CRM",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", ""),
                "insert_after": field["insert_after"],
                "reqd": field.get("reqd", 0),
                "hidden": field.get("hidden", 0)
            })
            cf.insert(ignore_permissions=True)
            print(f"Created custom field: {field['fieldname']} in Deal")

    frappe.db.commit()
    print("Custom fields created successfully!")

run()
