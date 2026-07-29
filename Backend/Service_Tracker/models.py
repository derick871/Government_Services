from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# ==========================================
# IDENTITY & ACCESS LAYER (RBAC)
# ==========================================

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field (uses email)."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model implementing strict Role-Based Access Control (RBAC)."""
    ROLE_CHOICES = (
        ('ADMIN', 'System Administrator'),
        ('OFFICER', 'County Government Officer'),
        ('CITIZEN', 'Standard Citizen Account'),
    )

    username = None 
    email = models.EmailField("Email Address", unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    county_code = models.CharField(max_length=10, blank=True, null=True, help_text="Target region tag if role is OFFICER")
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"


# ==========================================
# BUSINESS LOGIC & WORKFLOW LAYER
# ==========================================

class CountyNotice(models.Model):
    """Stores public service announcements and deadlines aggregated by background scrapers."""
    SERVICE_TYPES = [
        ('BUSINESS_PERMIT', 'Single Business Permit'),
        ('LAND_RATES', 'Land Rates Valuation'),
        ('BURSARY', 'Education Bursary Allocation'),
        ('HEALTH_CERT', 'Public Health Certificate'),
    ]

    county_id  = models.CharField(max_length=50, help_text="e.g., KE-COUNTY-047")
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
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"{self.application.tracking_number}: {self.from_state} -> {self.to_state}"