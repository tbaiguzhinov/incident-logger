from django.contrib import admin

from .models import HS_incident, Injury, Illness

class InjuryInline(admin.TabularInline):
    model = Injury
    extra = 1

class IllnessInlline(admin.TabularInline):
    model = Illness
    extra = 1

@admin.register(HS_incident)
class IncidentAdmin(admin.ModelAdmin):
    inlines = [
        InjuryInline,
        IllnessInlline,
    ]

@admin.register(Injury)
class InjuryAdmin(admin.ModelAdmin):
    pass

@admin.register(Illness)
class IllnessAdmin(admin.ModelAdmin):
    pass
