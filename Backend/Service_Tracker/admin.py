from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    CountyNotice,
    Application,
    StatusLog,
)


# ======================
# Status Log Inline
# ======================

class StatusLogInline(admin.TabularInline):
    """Display application history."""

    model = StatusLog
    extra = 0
    can_delete = False
    readonly_fields = (
        "from_state",
        "to_state",
        "changed_by",
        "comment",
        "timestamp",
    )


# ======================
# User Admin
# ======================

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Manage system users."""

    ordering = ("email",)

    list_display = (
        "email",
        "role",
        "county_code",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "phone_number",
        "county_code",
    )

    fieldsets = (
        (
            "Account",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                )
            },
        ),
        (
            "Role",
            {
                "fields": (
                    "role",
                    "county_code",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "county_code",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    readonly_fields = (
        "last_login",
        "date_joined",
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )


# ======================
# County Notice Admin
# ======================

@admin.register(CountyNotice)
class CountyNoticeAdmin(admin.ModelAdmin):
    """Manage county notices."""

    list_display = (
        "title",
        "county_id",
        "service_type",
        "deadline",
        "scraped_at",
    )

    list_filter = (
        "county_id",
        "service_type",
    )

    search_fields = (
        "title",
        "county_id",
    )

    ordering = (
        "-scraped_at",
    )

    readonly_fields = (
        "scraped_at",
    )


# ======================
# Application Admin
# ======================

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Manage applications."""

    list_display = (
        "tracking_number",
        "citizen",
        "county_id",
        "service_type",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "county_id",
        "service_type",
    )

    search_fields = (
        "tracking_number",
        "citizen__email",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "tracking_number",
        "created_at",
        "updated_at",
    )

    inlines = [
        StatusLogInline,
    ]


# ======================
# Status Log Admin
# ======================

@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    """View workflow history."""

    list_display = (
        "application",
        "from_state",
        "to_state",
        "changed_by",
        "timestamp",
    )

    list_filter = (
        "to_state",
        "timestamp",
    )

    search_fields = (
        "application__tracking_number",
        "changed_by__email",
    )

    ordering = (
        "-timestamp",
    )

    readonly_fields = (
        "application",
        "from_state",
        "to_state",
        "changed_by",
        "comment",
        "timestamp",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False