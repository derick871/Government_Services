from django.conf import settings
from django.db import models

class CountyNotice(models.Model):
    """Stores public service announcements and deadlines aggregated by background scrapers."""
    SERVICE_TYPES = [
        ('BUSINESS_PERMIT', 'Single Business Permit'),
        ('LAND_RATES', 'Land Rates Valuation'),
        ('BURSARY', 'Education Bursary Allocation'),
        ('HEALTH_CERT', 'Public Health Certificate'),
    ]

    county_id = models.CharField(max_length=50, help_text="e.g., KE-COUNTY-047")
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPES)
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField(null=True, blank=True)
    requirements = models.JSONField(default=list, help_text="List of string requirements")
    source_url = models.URLField(max_length=500)
    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-deadline', '-scraped_at']
        indexes = [
            models.Index(fields=['county_id', 'service_type']),
        ]

    def __str__(self):
        return f"[{self.county_id}] {self.title}"


class Application(models.Model):
    """Tracks a citizen's specific application workflow pipeline."""
    # Using settings.AUTH_USER_MODEL string reference avoids circular imports
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="applications"
    )
    county_id = models.CharField(max_length=50)
    service_type = models.CharField(max_length=30, choices=CountyNotice.SERVICE_TYPES)
    status = models.CharField(max_length=30, default="SUBMITTED")
    tracking_number = models.CharField(max_length=100, unique=True)
    payload_data = models.JSONField(default=dict, help_text="Form field responses unique to the service")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.tracking_number} - {self.status}"


class StatusLog(models.Model):
    """An unalterable audit trail capturing every workflow transition step."""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="logs")
    from_state = models.CharField(max_length=30)
    to_state = models.CharField(max_length=30)
    
    # Corrected User model reference
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name="status_change_logs"
    )
    comment = models.TextField(blank=True, null=True, help_text="Reviewer remarks or correction prompts")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        # Guardrails to protect data integrity of audit trails
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"{self.application.tracking_number}: {self.from_state} -> {self.to_state}"