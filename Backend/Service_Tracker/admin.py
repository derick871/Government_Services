from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    CountyNotice,
    Application,
    StatusLog,
)

# =====================================================
# USER ADMIN
# =====================================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "role",
        "phone_number",
        "county_code",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
        "is_superuser",
    )

    search_fields = (
        "email",
        "phone_number",
        "county_code",
    )

    readonly_fields = (
        "last_login",
        "date_joined",
    )

    fieldsets = (
        ("Login Information", {
            "fields": (
                "email",
                "password",
            )
        }),

        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "phone_number",
            )
        }),

        ("Role & County", {
            "fields": (
                "role",
                "county_code",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
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
                    "phone_number",
                    "county_code",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )


# =====================================================
# COUNTY NOTICE ADMIN
# =====================================================

@admin.register(CountyNotice)
class CountyNoticeAdmin(admin.ModelAdmin):

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
        "-deadline",
    )

    readonly_fields = (
        "scraped_at",
    )


# =====================================================
# APPLICATION ADMIN
# =====================================================

class StatusLogInline(admin.TabularInline):
    model = StatusLog
    extra = 0
    readonly_fields = (
        "from_state",
        "to_state",
        "changed_by",
        "comment",
        "timestamp",
    )

    can_delete = False


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

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
        "service_type",
        "county_id",
    )

    search_fields = (
        "tracking_number",
        "citizen__email",
    )

    readonly_fields = (
        "tracking_number",
        "created_at",
        "updated_at",
    )

    inlines = [StatusLogInline]

    date_hierarchy = "created_at"

    list_per_page = 20


# =====================================================
# STATUS LOG ADMIN
# =====================================================

@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):

    list_display = (
        "application",
        "from_state",
        "to_state",
        "changed_by",
        "timestamp",
    )

    list_filter = (
        "from_state",
        "to_state",
        "timestamp",
    )

    search_fields = (
        "application__tracking_number",
        "changed_by__email",
    )

    readonly_fields = (
        "application",
        "from_state",
        "to_state",
        "changed_by",
        "comment",
        "timestamp",
    )

    ordering = (
        "-timestamp",
    )