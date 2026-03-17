"""
Insurance CRM Dashboard - Enterprise Dashboard Widgets
"""

import frappe
import frappe.utils
from frappe import _
from datetime import datetime, timedelta

@frappe.whitelist()
def get_dashboard_data():
    """Get all dashboard data in one call"""
    return {
        "leads": get_lead_summary(),
        "deals": get_deal_summary(),
        "activities": get_today_activities(),
        "tasks": get_pending_tasks(),
        "notifications": get_notifications()
    }

@frappe.whitelist()
def get_lead_summary():
    """Get lead summary for dashboard"""
    try:
        total = frappe.db.count("CRM Lead")
        new_leads = frappe.db.count("CRM Lead", {"status": "New"})
        contacted = frappe.db.count("CRM Lead", {"status": "Contacted"})
        qualified = frappe.db.count("CRM Lead", {"status": "Qualified"})
        converted = frappe.db.count("CRM Lead", {"status": "Converted"})
        lost = frappe.db.count("CRM Lead", {"status": "Lost"})
        
        # This week
        week_ago = frappe.utils.add_days(frappe.utils.today(), -7)
        this_week = frappe.db.count("CRM Lead", {"creation": [">=", week_ago]})
        
        # By rating
        hot = frappe.db.count("CRM Lead", {"lead_rating": "Hot"})
        warm = frappe.db.count("CRM Lead", {"lead_rating": "Warm"})
        cold = frappe.db.count("CRM Lead", {"lead_rating": "Cold"})
        
        return {
            "total": total,
            "by_status": {
                "new": new_leads,
                "contacted": contacted,
                "qualified": qualified,
                "converted": converted,
                "lost": lost
            },
            "by_rating": {
                "hot": hot,
                "warm": warm,
                "cold": cold
            },
            "this_week": this_week,
            "conversion_rate": round((converted / total * 100) if total > 0 else 0, 1)
        }
    except Exception as e:
        return {"error": str(e)}

@frappe.whitelist()
def get_deal_summary():
    """Get deal pipeline summary"""
    try:
        total = frappe.db.count("CRM Deal")
        open_deals = frappe.db.count("CRM Deal", {"status": ["in", ["Open", "Draft"]]})
        won = frappe.db.count("CRM Deal", {"status": "Won"})
        lost = frappe.db.count("CRM Deal", {"status": "Lost"})
        
        # Pipeline value
        pipeline_value = frappe.db.sql("""
            SELECT SUM(premium_amount) as total 
            FROM `tabCRM Deal` 
            WHERE status IN ('Open', 'Draft')
        """)[0][0] or 0
        
        won_value = frappe.db.sql("""
            SELECT SUM(premium_amount) as total 
            FROM `tabCRM Deal` 
            WHERE status = 'Won'
        """)[0][0] or 0
        
        return {
            "total": total,
            "open": open_deals,
            "won": won,
            "lost": lost,
            "pipeline_value": float(pipeline_value),
            "won_value": float(won_value),
            "win_rate": round((won / total * 100) if total > 0 else 0, 1)
        }
    except Exception as e:
        return {"error": str(e)}

@frappe.whitelist()
def get_today_activities():
    """Get today's activities"""
    try:
        today = frappe.utils.today()
        
        activities = frappe.get_all(
            "CRM Activity",
            filters={
                "status": ["!=", "Completed"],
                "due_date": ["<=", today]
            },
            fields=["name", "activity_type", "description", "due_date", "lead", "deal"],
            order_by="due_date asc",
            limit=10
        )
        
        return activities
    except Exception as e:
        return []

@frappe.whitelist()
def get_pending_tasks():
    """Get pending tasks count"""
    try:
        today = frappe.utils.today()
        
        return {
            "overdue": frappe.db.count("CRM Activity", {
                "status": ["!=", "Completed"],
                "due_date": ["<", today]
            }),
            "due_today": frappe.db.count("CRM Activity", {
                "status": ["!=", "Completed"],
                "due_date": today
            }),
            "due_this_week": frappe.db.count("CRM Activity", {
                "status": ["!=", "Completed"],
                "due_date": ["between", [today, frappe.utils.add_days(today, 7)]]
            })
        }
    except Exception as e:
        return {"error": str(e)}

@frappe.whitelist()
def get_notifications():
    """Get CRM notifications"""
    try:
        notifications = []
        
        # Follow-ups due today
        followups = frappe.db.count("CRM Lead", {
            "follow_up_date": frappe.utils.today(),
            "status": ["in", ["New", "Contacted", "Qualified"]]
        })
        if followups > 0:
            notifications.append({
                "type": "warning",
                "title": "Follow-ups Due",
                "message": f"{followups} leads have follow-up scheduled for today"
            })
        
        # Overdue follow-ups
        overdue = frappe.db.count("CRM Lead", {
            "follow_up_date": ["<", frappe.utils.today()],
            "lead_rating": ["!=", "Cold"]
        })
        if overdue > 0:
            notifications.append({
                "type": "danger",
                "title": "Overdue Follow-ups",
                "message": f"{overdue} follow-ups are overdue"
            })
        
        # Unassigned leads
        unassigned = frappe.db.count("CRM Lead", {
            "owner": "Administrator",
            "status": ["!=", "Lost"]
        })
        if unassigned > 0:
            notifications.append({
                "type": "info",
                "title": "Unassigned Leads",
                "message": f"{unassigned} leads are unassigned"
            })
        
        return notifications
    except Exception as e:
        return []

@frappe.whitelist()
def get_policy_breakdown():
    """Get lead/deal breakdown by policy type"""
    try:
        data = frappe.db.sql("""
            SELECT 
                policy_type,
                COUNT(*) as leads,
                (SELECT COUNT(*) FROM `tabCRM Deal` d WHERE d.policy_type = l.policy_type) as deals,
                (SELECT SUM(premium_amount) FROM `tabCRM Deal` d WHERE d.policy_type = l.policy_type AND d.status = 'Won') as revenue
            FROM `tabCRM Lead` l
            WHERE policy_type IS NOT NULL
            GROUP BY policy_type
        """, as_dict=True)
        
        return data
    except Exception as e:
        return []

@frappe.whitelist()
def get_activity_timeline(limit=20):
    """Get recent activity timeline"""
    try:
        activities = frappe.get_all(
            "CRM Activity",
            fields=["name", "activity_type", "description", "creation", "status", "lead", "deal"],
            order_by="creation desc",
            limit=limit
        )
        return activities
    except Exception as e:
        return []

# ============================================
# QUICK ACTIONS
# ============================================

@frappe.whitelist()
def quick_create_lead(lead_name, phone, email, policy_type=None):
    """Quick lead creation from anywhere"""
    try:
        lead = frappe.get_doc({
            "doctype": "CRM Lead",
            "lead_name": lead_name,
            "phone": phone,
            "email_id": email,
            "policy_type": policy_type,
            "status": "New",
            "lead_rating": "Warm"
        })
        lead.insert(ignore_permissions=True)
        return {"success": True, "lead": lead.name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def quick_create_deal(organization, lead=None, policy_type=None, premium_amount=None):
    """Quick deal creation"""
    try:
        deal = frappe.get_doc({
            "doctype": "CRM Deal",
            "organization": organization,
            "lead": lead,
            "policy_type": policy_type,
            "premium_amount": premium_amount,
            "status": "Open"
        })
        deal.insert(ignore_permissions=True)
        return {"success": True, "deal": deal.name}
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_kanban_data(doctype="CRM Lead"):
    """Get kanban view data"""
    try:
        if doctype == "CRM Lead":
            statuses = ["New", "Contacted", "Qualified", "Proposal", "Negotiation"]
        else:
            statuses = ["Open", "Quotation", "Negotiation", "Won", "Lost"]
        
        kanban = {}
        for status in statuses:
            records = frappe.get_all(
                doctype,
                filters={"status": status},
                fields=["name", "lead_name", "organization", "policy_type", "premium_amount", "lead_rating"],
                limit=20
            )
            kanban[status] = records
        
        return kanban
    except Exception as e:
        return {"error": str(e)}
