"""
Insurance CRM Integrations Module
WhatsApp, SMS, Payments, Video Calling, AI & More
"""

import frappe
import requests
import json
from frappe import _
from frappe.utils import now_datetime, today, get_datetime, add_days
from datetime import datetime, timedelta

# ============================================
# WHATSAPP INTEGRATION (WhatsApp Business API)
# ============================================

class WhatsAppIntegration:
    """WhatsApp Business API integration for sending messages"""
    
    def __init__(self):
        self.settings = frappe.get_single("WhatsApp Settings")
        self.enabled = self.settings.enable_whatsapp
        self.api_url = self.settings.api_url
        self.token = self.settings.get_password("api_token")
    
    def send_message(self, phone, message, template=None):
        """Send WhatsApp message to customer"""
        if not self.enabled:
            return {"success": False, "error": "WhatsApp integration disabled"}
        
        try:
            # Format phone number
            phone = self._format_phone(phone)
            
            payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "text",
                "text": {"body": message}
            }
            
            if template:
                payload = {
                    "messaging_product": "whatsapp",
                    "to": phone,
                    "type": "template",
                    "template": {
                        "name": template,
                        "language": {"code": "en_US"}
                    }
                }
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(f"{self.api_url}/messages", json=payload, headers=headers)
            
            if response.status_code == 201:
                return {"success": True, "message_id": response.json().get("messages", [{}])[0].get("id")}
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            frappe.log_error(f"WhatsApp Error: {e}")
            return {"success": False, "error": str(e)}
    
    def send_template(self, phone, template_name, parameters=None):
        """Send WhatsApp template message"""
        if not self.enabled:
            return {"success": False, "error": "WhatsApp integration disabled"}
        
        try:
            phone = self._format_phone(phone)
            
            payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": "en_US"},
                    "components": []
                }
            }
            
            if parameters:
                payload["template"]["components"] = [{
                    "type": "body",
                    "parameters": [
                        {"type": "text", "parameter_name": k, "text": v} 
                        for k, v in parameters.items()
                    ]
                }]
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(f"{self.api_url}/messages", json=payload, headers=headers)
            return {"success": response.status_code == 201, "response": response.json()}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _format_phone(self, phone):
        """Format phone number for WhatsApp"""
        phone = str(phone).strip().replace(" ", "").replace("-", "").replace("+", "")
        if not phone.startswith("91") and len(phone) == 10:
            phone = "91" + phone
        return phone

# Pre-built WhatsApp templates for insurance
WHATSAPP_TEMPLATES = {
    "lead_acknowledgment": "Your inquiry for {policy_type} insurance has been received. We'll contact you shortly.",
    "quote_ready": "Your insurance quote is ready! Premium: {premium}, Coverage: {coverage}. Reply to know more.",
    "followup_reminder": "Reminder: We have a pending follow-up on your {policy_type} insurance. Call us!",
    "policy_renewal": "Your {policy_type} policy is due for renewal on {renewal_date}. Avail our best offers!",
    "claim_status": "Your claim status: {status}. For queries, contact our support.",
    "birthday_wish": "Happy Birthday! 🎂 Avail special insurance offers exclusively for you."
}

def send_whatsapp(phone, message_or_template, is_template=False):
    """Helper function to send WhatsApp messages"""
    wa = WhatsAppIntegration()
    if is_template:
        return wa.send_template(phone, message_or_template)
    else:
        return wa.send_message(phone, message_or_template)

# ============================================
# SMS INTEGRATION (Twilio/Nexmo)
# ============================================

class SMSIntegration:
    """SMS gateway integration"""
    
    def __init__(self):
        self.settings = frappe.get_single("SMS Settings")
        self.enabled = self.settings.enable_sms
    
    def send(self, phone, message):
        """Send SMS to customer"""
        if not self.enabled:
            return {"success": False, "error": "SMS integration disabled"}
        
        try:
            phone = self._format_phone(phone)
            
            # Using Twilio as example (can be swapped for any provider)
            account_sid = self.settings.get_password("account_sid")
            auth_token = self.settings.get_password("auth_token")
            from_number = self.settings.from_number
            
            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            
            payload = {
                "To": phone,
                "From": from_number,
                "Body": message
            }
            
            response = requests.post(url, data=payload, auth=(account_sid, auth_token))
            
            if response.status_code in [200, 201]:
                return {"success": True, "message_id": response.json().get("sid")}
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            frappe.log_error(f"SMS Error: {e}")
            return {"success": False, "error": str(e)}
    
    def _format_phone(self, phone):
        phone = str(phone).strip().replace(" ", "").replace("-", "").replace("+", "")
        if not phone.startswith("+"):
            phone = "+91" + phone
        return phone

def send_sms(phone, message):
    """Helper to send SMS"""
    sms = SMSIntegration()
    return sms.send(phone, message)

# ============================================
# RAZORPAY PAYMENT INTEGRATION
# ============================================

class RazorpayIntegration:
    """Razorpay payment gateway for India"""
    
    def __init__(self):
        self.settings = frappe.get_single("Razorpay Settings")
        self.enabled = self.settings.enable_razorpay
        self.key_id = self.settings.key_id
        self.key_secret = self.settings.get_password("key_secret")
    
    def create_payment_link(self, amount, currency="INR", customer, description, callback_url=None):
        """Create Razorpay payment link"""
        if not self.enabled:
            return {"success": False, "error": "Razorpay integration disabled"}
        
        try:
            import razorpay
            
            client = razorpay.Client(auth=(self.key_id, self.key_secret))
            
            payload = {
                "amount": int(amount * 100),  # Razorpay uses paise
                "currency": currency,
                "description": description,
                "customer": {
                    "name": customer.get("name"),
                    "email": customer.get("email"),
                    "contact": customer.get("phone")
                },
                "notify": {
                    "email": True,
                    "sms": True
                }
            }
            
            if callback_url:
                payload["callback_url"] = callback_url
            
            response = client.payment_link.create(payload)
            
            return {
                "success": True,
                "payment_link": response.get("short_url"),
                "payment_id": response.get("id")
            }
            
        except Exception as e:
            frappe.log_error(f"Razorpay Error: {e}")
            return {"success": False, "error": str(e)}
    
    def verify_payment(self, payment_id):
        """Verify payment status"""
        try:
            import razorpay
            client = razorpay.Client(auth=(self.key_id, self.key_secret))
            payment = client.payment.fetch(payment_id)
            return {"success": True, "payment": payment}
        except Exception as e:
            return {"success": False, "error": str(e)}

def create_payment_link(amount, customer, description):
    """Helper to create payment link"""
    rp = RazorpayIntegration()
    return rp.create_payment_link(amount, customer=customer, description=description)

# ============================================
# JITSI VIDEO CALLING INTEGRATION
# ============================================

class JitsiIntegration:
    """Jitsi Meet video calling integration"""
    
    def __init__(self):
        self.settings = frappe.get_single("Jitsi Settings")
        self.enabled = self.settings.enable_jitsi
        self.domain = self.settings.domain or "meet.jit.si"
    
    def create_meeting(self, topic, host):
        """Create a new Jitsi meeting room"""
        if not self.enabled:
            return {"success": False, "error": "Jitsi integration disabled"}
        
        try:
            import uuid
            room_id = str(uuid.uuid4())[:8]
            room_name = f"insurance-{room_id}"
            
            meeting_url = f"https://{self.domain}/{room_name}"
            
            # Create meeting record
            meeting = frappe.get_doc({
                "doctype": "Insurance Meeting",
                "topic": topic,
                "host": host,
                "meeting_url": meeting_url,
                "room_id": room_name,
                "status": "Scheduled",
                "scheduled_time": now_datetime()
            })
            meeting.insert(ignore_permissions=True)
            
            return {
                "success": True,
                "meeting_url": meeting_url,
                "meeting_id": meeting.name,
                "room_id": room_name
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_meeting_link(self, room_id):
        """Get existing meeting link"""
        return f"https://{self.domain}/{room_id}"

def create_video_meeting(topic, host):
    """Helper to create video meeting"""
    jitsi = JitsiIntegration()
    return jitsi.create_meeting(topic, host)

# ============================================
# CHATWOOT LIVE CHAT INTEGRATION
# ============================================

class ChatwootIntegration:
    """Chatwoot live chat integration"""
    
    def __init__(self):
        self.settings = frappe.get_single("Chatwoot Settings")
        self.enabled = self.settings.enable_chatwoot
        self.account_id = self.settings.account_id
        self.api_token = self.settings.get_password("api_token")
        self.base_url = self.settings.base_url or "https://app.chatwoot.com"
    
    def create_contact(self, name, phone=None, email=None):
        """Create contact in Chatwoot"""
        if not self.enabled:
            return {"success": False, "error": "Chatwoot integration disabled"}
        
        try:
            url = f"{self.base_url}/api/v1/accounts/{self.account_id}/contacts"
            
            payload = {
                "name": name,
                "phone_number": phone,
                "email": email
            }
            
            headers = {
                "Content-Type": "application/json",
                "Api-Token": self.api_token
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                return {"success": True, "contact": response.json()}
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_message(self, conversation_id, message):
        """Send message to conversation"""
        try:
            url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
            
            payload = {
                "message_type": "outgoing",
                "content": message
            }
            
            headers = {
                "Content-Type": "application/json",
                "Api-Token": self.api_token
            }
            
            response = requests.post(url, json=payload, headers=headers)
            return {"success": response.status_code in [200, 201], "response": response.json()}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# ============================================
# AI-POWERED LEAD SCORING
# ============================================

class AILeadScoring:
    """AI-powered lead scoring using simple rules + ML-like scoring"""
    
    def score_lead(self, lead):
        """Score a lead based on multiple factors"""
        score = 0
        
        # Rating factor
        rating_scores = {"Hot": 30, "Warm": 20, "Cold": 10}
        score += rating_scores.get(lead.get("lead_rating"), 10)
        
        # Has email
        if lead.get("email_id"):
            score += 10
        
        # Has phone
        if lead.get("phone"):
            score += 15
        
        # Has coverage amount
        if lead.get("coverage_amount"):
            coverage = float(lead.get("coverage_amount", 0))
            if coverage >= 500000:
                score += 20
            elif coverage >= 100000:
                score += 15
            else:
                score += 10
        
        # Source factor
        source_scores = {
            "Website": 15,
            "Referral": 20,
            "Advertisement": 10,
            "Cold Call": 5,
            "Exhibition": 15
        }
        score += source_scores.get(lead.get("source"), 10)
        
        # Policy type factor (premium policies = higher score)
        policy_scores = {
            "Motor": 15,
            "Health": 20,
            "Life": 15,
            "Home": 10,
            "Travel": 5
        }
        score += policy_scores.get(lead.get("policy_type"), 10)
        
        # Converted to percentage
        final_score = min(score, 100)
        
        # Determine rating based on score
        if final_score >= 75:
            rating = "Hot"
        elif final_score >= 50:
            rating = "Warm"
        else:
            rating = "Cold"
        
        return {
            "score": final_score,
            "rating": rating,
            "factors": {
                "rating_factor": rating_scores.get(lead.get("lead_rating"), 10),
                "contact_factor": 25 if (lead.get("email_id") and lead.get("phone")) else 0,
                "coverage_factor": min(20, int(lead.get("coverage_amount", 0) / 50000)),
                "source_factor": source_scores.get(lead.get("source"), 10)
            }
        }
    
    def update_all_lead_scores(self):
        """Update scores for all leads"""
        leads = frappe.get_all("CRM Lead", fields=["name", "lead_rating", "email_id", "phone", "coverage_amount", "source", "policy_type"])
        
        for lead in leads:
            score_data = self.score_lead(lead)
            frappe.db.set_value("CRM Lead", lead.name, "lead_rating", score_data["rating"])
        
        frappe.db.commit()
        return {"success": True, "updated": len(leads)}

def calculate_lead_score(lead):
    """Helper to calculate lead score"""
    scorer = AILeadScoring()
    return scorer.score_lead(lead)

# ============================================
# INTEGRATION HELPERS
# ============================================

@frappe.whitelist()
def test_whatsapp(phone, message="Test message"):
    """Test WhatsApp integration"""
    return send_whatsapp(phone, message)

@frappe.whitelist()
def test_sms(phone, message="Test message"):
    """Test SMS integration"""
    return send_sms(phone, message)

@frappe.whitelist()
def test_payment(amount=100):
    """Test Razorpay payment link"""
    customer = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "9999999999"
    }
    return create_payment_link(amount, customer, "Test Payment")

@frappe.whitelist()
def create_meeting(topic="Insurance Discussion"):
    """Create video meeting"""
    return create_video_meeting(topic, frappe.session.user)

@frappe.whitelist()
def refresh_lead_scores():
    """Refresh all lead scores"""
    scorer = AILeadScoring()
    return scorer.update_all_lead_scores()
