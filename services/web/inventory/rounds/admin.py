from django.contrib import admin

from .models import RoundsPanel, WRFRound, RoundStatus


class WRFRoundInline(admin.TabularInline):
    model = WRFRound
    extra = 0
    readonly_fields = ("timestamp", "status")


@admin.register(RoundsPanel)
class RoundsPanelAdmin(admin.ModelAdmin):
    inlines = (WRFRoundInline,)


@admin.register(WRFRound)
class WRFRoundAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "timestamp", "panel")
    actions = ["send_selected_to_queue"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.status == RoundStatus.PENDING:
            obj.send_to_queue()
            self.message_user(request, "Round enviado automaticamente para a fila.")
