"""
Insurance CRM Analytics Module
Enterprise-grade analytics for lead generation and conversion
"""

import frappe
import frappe.utils
from frappe import _
from datetime import datetime, timedelta

@frappe.whitelist()
def get_lead_funnel_data(filters=None):
    """
    Get lead funnel data for analytics
    Returns: dict with lead counts by status
    """
    try:
        # Get all leads
        leads = frappe.get_all(
            "CRM Lead",
            fields=["status", "COUNT(*) as count"],
            group_by="status"
        )
        
        # Get leads by source
        leads_by_source = frappe.get_all(
            "CRM Lead",
            fields=["source", "COUNT(*) as count"],
            group_by="source"
        )
        
        # Get leads by policy type
        leads_by_policy = frappe.get_all(
            "CRM Lead",
            fields=["policy_type", "COUNT(*) as count"],
            group_by="policy_type"
        )
        
        # Get leads by rating
        leads_by_rating = frappe.get_all(
            "CRM Lead",
            fields=["lead_rating", "COUNT(*) as count"],
            group_by="lead_rating"
        )
        
        # Calculate conversion rates
        total_leads = sum(l.count for l in leads)
        converted = sum(l.count for l in leads if l.status == "Converted")
        conversion_rate = (converted / total_leads * 100) if total_leads > 0 else 0
        
        return {
            "success": True,
            "leads_by_status": leads,
            "leads_by_source": leads_by_source,
            "leads_by_policy": leads_by_policy,
            "leads_by_rating": leads_by_rating,
            "total_leads": total_leads,
            "converted_leads": converted,
            "conversion_rate": round(conversion_rate, 2)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_deal_pipeline_data(filters=None):
    """
    Get deal pipeline analytics
    """
    try:
        # Get deals by stage
        deals_by_stage = frappe.get_all(
            "CRM Deal",
            fields=["status", "COUNT(*) as count", "SUM(premium_amount) as total_value"],
            group_by="status"
        )
        
        # Get deals by policy type
        deals_by_policy = frappe.get_all(
            "CRM Deal",
            fields=["policy_type", "COUNT(*) as count", "SUM(premium_amount) as total_value"],
            group_by="policy_type"
        )
        
        # Calculate pipeline value
        total_pipeline = sum(d.total_value or 0 for d in deals_by_stage)
        won_value = sum(d.total_value or 0 for d in deals_by_stage if d.status == "Won")
        
        return {
            "success": True,
            "deals_by_stage": deals_by_stage,
            "deals_by_policy": deals_by_policy,
            "total_pipeline": total_pipeline or 0,
            "won_value": won_value,
            "win_rate": round((won_value / total_pipeline * 100) if total_pipeline > 0 else 0, 2)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_dropoff_analysis():
    """
    Analyze drop-off points in the funnel
    """
    try:
        # Lead stage progression
        lead_stages = ["New", "Contacted", "Qualified", "Proposal", "Negotiation", "Converted", "Lost"]
        
        dropoff_data = []
        for i, stage in enumerate(lead_stages[:-1]):
            current_count = frappe.db.count("CRM Lead", {"status": stage}) or 0
            next_count = frappe.db.count("CRM Lead", {"status": lead_stages[i+1]}) or 0
            
            # Also check leads lost at this stage
            lost_at_stage = frappe.db.count("CRM Lead", {
                "status": ["in", ["Lost", "Converted"]],
                "lead_rating": stage
            }) or 0
            
            conversion_rate = (next_count / current_count * 100) if current_count > 0 else 0
            dropoff_rate = 100 - conversion_rate
            
            dropoff_data.append({
                "stage": stage,
                "leads_in": current_count,
                "leads_out": next_count,
                "conversion_rate": round(conversion_rate, 2),
                "dropoff_rate": round(dropoff_rate, 2)
            })
        
        return {
            "success": True,
            "dropoff_analysis": dropoff_data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_performance_metrics(days=30):
    """
    Get performance metrics for the last N days
    """
    try:
        from_date = frappe.utils.add_days(frappe.utils.today(), -int(days))
        
        # New leads in period
        new_leads = frappe.db.count("CRM Lead", {
            "creation": [">=", from_date]
        })
        
        # Converted leads in period
        converted_leads = frappe.db.count("CRM Lead", {
            "status": "Converted",
            "modified": [">=", from_date]
        })
        
        # Deals won in period
        won_deals = frappe.db.count("CRM Deal", {
            "status": "Won",
            "modified": [">=", from_date]
        })
        
        # Revenue from won deals
        revenue = frappe.db.sql("""
            SELECT SUM(premium_amount) as total
            FROM `tabCRM Deal`
            WHERE status = 'Won' AND modified >= %s
        """, (from_date,))[0][0] or 0
        
        # Follow-ups due today
        followups_due = frappe.db.count("CRM Lead", {
            "follow_up_date": frappe.utils.today(),
            "status": ["!=", "Converted"]
        })
        
        # Avg response time (days from creation to first activity)
        avg_response_time = frappe.db.sql("""
            SELECT AVG(DATEDIFF(min(creation), lead.creation))
            FROM `tabCRM Activity` activity
            JOIN `tabCRM Lead` lead ON activity.lead = lead.name
            WHERE activity.creation >= %s
        """, (from_date,))[0][0] or 0
        
        return {
            "success": True,
            "period_days": days,
            "new_leads": new_leads,
            "converted_leads": converted_leads,
            "won_deals": won_deals,
            "revenue": revenue,
            "followups_due": followups_due,
            "avg_response_days": round(avg_response_time, 1),
            "lead_to_deal_rate": round((won_deals / new_leads * 100) if new_leads > 0 else 0, 2)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_policy_type_performance():
    """
    Get performance metrics by policy type
    """
    try:
        policy_types = ["Motor", "Health", "Life", "Travel", "Home", "Fire", "Marine", "Other"]
        
        performance = []
        for ptype in policy_types:
            # Leads for this policy type
            lead_count = frappe.db.count("CRM Lead", {"policy_type": ptype})
            
            # Deals for this policy type
            deal_count = frappe.db.count("CRM Deal", {"policy_type": ptype})
            
            # Won deals and value
            won = frappe.db.sql("""
                SELECT COUNT(*) as count, SUM(premium_amount) as value
                FROM `tabCRM Deal`
                WHERE policy_type = %s AND status = 'Won'
            """, (ptype,))[0]
            
            if lead_count > 0:
                conversion_rate = (won.count / lead_count * 100) if won.count else 0
            else:
                conversion_rate = 0
            
            performance.append({
                "policy_type": ptype,
                "leads": lead_count,
                "deals": deal_count,
                "won": won.count or 0,
                "revenue": won.value or 0,
                "conversion_rate": round(conversion_rate, 2)
            })
        
        return {
            "success": True,
            "policy_performance": performance
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_team_performance():
    """
    Get performance metrics by sales agent
    """
    try:
        performance = frappe.db.sql("""
            SELECT 
                owner as agent,
                COUNT(DISTINCT name) as total_leads,
                COUNT(DISTINCT CASE WHEN status = 'Converted' THEN name END) as converted,
                COUNT(DISTINCT CASE WHEN status = 'Lost' THEN name END) as lost
            FROM `tabCRM Lead`
            WHERE creation >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY owner
        """, as_dict=True)
        
        for p in performance:
            p.conversion_rate = round((p.converted / p.total_leads * 100) if p.total_leads > 0 else 0, 2)
        
        return {
            "success": True,
            "team_performance": performance
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
