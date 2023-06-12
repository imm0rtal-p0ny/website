from django.contrib import admin
from .models import Board, Status, Division, Region, Condition, delete_photos_except_default


class BoardAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        delete_photos_except_default(obj)
        super().delete_model(request, obj)


class StatusAdmin(admin.ModelAdmin):
    pass


class DivisionAdmin(admin.ModelAdmin):
    pass


class RegionAdmin(admin.ModelAdmin):
    pass


class ConditionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Board, BoardAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Condition, ConditionAdmin)

