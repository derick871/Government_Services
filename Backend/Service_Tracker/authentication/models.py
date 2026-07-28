from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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
    
    ROLE_CHOICES = (
        ('ADMIN', 'System Administrator'),
        ('OFFICER', 'County Government Officer'),
        ('CITIZEN', 'Standard Citizen Account'),
    )

    username = None # Remove standard username field
    email = models.EmailField("Email Address", unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    county_code = models.CharField(max_length=10, blank=True, null=True, help_index="Target region tag if role is OFFICER")
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default now

    def __str__(self):
        return f"{self.email} ({self.role})"
    