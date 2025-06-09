from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time
import requests
from decouple import config

SENDGRID_API_KEY = config('SENDGRID_API_KEY')
MSG91_AUTH_KEY = config('MSG91_AUTH_KEY')

FROM_EMAIL = 'adnaikprasanna1055@gmail.com'

def send_scheduled_email(to_email, subject, message, send_datetime):
    send_at_timestamp = int(time.mktime(send_datetime.timetuple()))

    mail = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=message,
    )

    mail.send_at = send_at_timestamp

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(mail)
        print(f"Scheduled email sent! Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending scheduled email: {e}")
        return False



def send_sms_via_msg91(phone, message):
    url = "https://control.msg91.com/api/v5/flow/"
    
    headers = {
        "accept": "application/json",
        "authkey": MSG91_AUTH_KEY,  
        "content-type": "application/json"
    }

    payload = {
        "flow_id": "YOUR_FLOW_ID",  
        "sender": "SENDERID",       
        "mobiles": f"91{phone}",    
        "VAR1": message            
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
