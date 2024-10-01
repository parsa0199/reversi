from sms_ir import SmsIr  # Import the SmsIr class from sms_ir
from .models import SmsLog
from celery import shared_task
from accounts.models import User
from django.db.models import Q
import json


@shared_task
def send_sms(data, subject, user=None, phone=None, template_id=None):
    # Initialize SmsIr with your API Key and line number
    api_key = 'EzXkfWzMr60fE5iJpUaE0uVeichUFU0stezNrqcrGo0fsuhEvdjzwYu2J6sePDOh'
    linenumber = '30007732000687'
    sms_ir = SmsIr(api_key, linenumber)

    status = True
    if user and str(user).isdigit():
        user = User.objects.get(Q(pk=user))

    try:
        # Send SMS using SmsIr
        number = data.get('receptor', None)
        if subject == 'phone_verify':
            code = data.get('code', None)
            parametrs =  [{
                "name": "code",
                "value": code
            }]
            result = sms_ir.send_verify_code(number=number,
                                            template_id=template_id,
                                            parameters=parametrs)
        
        elif subject == 'new_order_admin':
            code = data.get('code', None)
            date = data.get('date', None)
            price = str(data.get('price', 0))
            parametrs =  [
                {
                "name": "price",
                "value": price
                },
                
                {
                "name": "date",
                "value": date
                },

                {
                "name": "code",
                "value": code
                },

            ]
            result = sms_ir.send_verify_code(number=phone,
                                            template_id=template_id,
                                            parameters=parametrs)

        elif subject == 'new_order_customer':
            code = data.get('code', None)
            date = data.get('date', None)
            name = data.get('name', None)
            parametrs =  [
                {
                "name": "name",
                "value": name
                },

                {
                "name": "code",
                "value": code
                },

                {
                "name": "date",
                "value": date
                },
            ]
            result = sms_ir.send_verify_code(number=phone,
                                            template_id=template_id,
                                            parameters=parametrs)
        else:
              # Replace with the appropriate field from 'data'
            message = data.get('token', None)  # Replace with the appropriate field from 'data'
            result = sms_ir.send_sms(number, message)
        print(result.json())

        # Check if the SMS was sent successfully
        if result.status_code == 200:
            new_sms_log = SmsLog(is_sent=True)
        else:
            status = False
            new_sms_log = SmsLog(is_sent=False)

        new_sms_log.status_code = result.status_code  # Use appropriate field from the response
        new_sms_log.subject = subject
        new_sms_log.user = user
        new_sms_log.phone = phone
        new_sms_log.save()
    except Exception as e:
        print(e)
        new_sms_log = SmsLog(is_sent=False)
        new_sms_log.subject = subject
        new_sms_log.user = user
        new_sms_log.phone = phone
        new_sms_log.status_code = 999
        new_sms_log.save()
        status = False

    return status
