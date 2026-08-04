from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# ======================
# Custom User Manager
# ======================

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


# ======================
# User Model
# ======================

class User(AbstractUser):

    ROLE_CHOICES = (
        ("ADMIN", "Administrator"),
        ("OFFICER", "County Officer"),
        ("CITIZEN", "Citizen"),
    )

    username = None

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="CITIZEN"
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    county_code = models.CharField(
        max_length=20,
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_admin(self):
        return self.role == "ADMIN"

    @property
    def is_officer(self):
        return self.role == "OFFICER"

    @property
    def is_citizen(self):
        return self.role == "CITIZEN"

    def __str__(self):
        return self.email


# ======================
# County Notices
# ======================

class CountyNotice(models.Model):

    SERVICE_TYPES = (
        ("BUSINESS_PERMIT", "Business Permit"),
        ("LAND_RATES", "Land Rates"),
        ("BURSARY", "Bursary"),
        ("HEALTH_CERT", "Health Certificate"),
    )

    county_id = models.CharField(max_length=50)

    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_TYPES
    )

    title = models.CharField(max_length=255)

    requirements = models.JSONField(default=list)

    deadline = models.DateTimeField(
        null=True,
        blank=True
    )

    source_url = models.URLField()

    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scraped_at"]

    def __str__(self):
        return self.title


# ======================
# Citizen Applications
# ======================

class Application(models.Model):

    STATUS_CHOICES = (
        ("SUBMITTED", "Submitted"),
        ("UNDER_REVIEW", "Under Review"),
        ("ACTION_REQUIRED", "Action Required"),
        ("VERIFIED", "Verified"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    county_id = models.CharField(max_length=50)

    service_type = models.CharField(
        max_length=30,
        choices=CountyNotice.SERVICE_TYPES
    )

    tracking_number = models.CharField(
        max_length=20,
        unique=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="SUBMITTED"
    )

    payload_data = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.tracking_number


# ======================
# Status History
# ======================

class StatusLog(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    from_state = models.CharField(max_length=30)

    to_state = models.CharField(max_length=30)

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    comment = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.application.tracking_number} ({self.to_state})"