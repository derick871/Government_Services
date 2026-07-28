import logging
from datetime import datetime
from django.core.exceptions import ValidationError
from Service_Tracker.models import CountyNotice

logger = logging.getLogger(__name__)

class NoticeNomalizer:
    REQUIRED_FIELDS = {"county_id", "title", "service_type", "deadline", "source_url"}
    VALID_SERVICES = {"LAND_RATE", "SINGLE_BUSINESS_PERMIT", "BURSARY", "HEALTH_CERTIFICATE", "OTHER"}

    @classmethod

    def nomalize_and_save(cls, raw_payload):
        try:
            # Structural Validation
            missing_fields = cls.REQUIRED_FIELDS - set(raw_payload.keys())
            if missing_fields:
                raise ValidationError(f"Missing mandatory data contracts: {missing_fields}")

            # Text Normalization
            clean_title = raw_payload["title"].strip().upper()
            clean_county = raw_payload["county_id"].strip().upper()
            
            #  Service Type Mapping & Fallback
            service_type = raw_payload["service_type"].strip().upper()
            if service_type not in cls.VALID_SERVICES:
                service_type = "OTHER"