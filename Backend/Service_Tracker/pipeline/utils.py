import logging
import os
import requests
from django.core.mail import send_mail
from django.conf import settings

logger=logging.getLogger(__name__)

class CommunicationHub:
    @staticmethod

    def send_sms_alert(phone_number, message):
        userName= os.getenv("userName")
        api_key= os.getenv ("API_KEY")

        if not api_key:
            logger.warning(f"[MOCK SMS] Outbount to {phone_number}: {message}")
            return True
