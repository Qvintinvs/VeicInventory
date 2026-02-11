from django.contrib import admin

from .models import RoundsPanel, WRFRound


class WRFRoundInline(admin.TabularInline):
    model = WRFRound
    extra = 0
    readonly_fields = ("timestamp", "status")


@admin.register(RoundsPanel)
class RoundsPanelAdmin(admin.ModelAdmin):
    inlines = (WRFRoundInline,)
