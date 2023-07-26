from django.contrib import admin
from .models import Board, Status, Division, Region, Condition, delete_photos_except_default
from .forms import BoardUpdateForm


class BoardAdmin(admin.ModelAdmin):
    readonly_fields = ['view_count', 'photo_icon', 'photo_page']
    form = BoardUpdateForm

    def delete_queryset(self, request, queryset):
        for item in queryset:
            item.delete()

    def save_model(self, request, obj, form, change):
        if change:
            old_photo = form.initial.get('photo')
            clear_photo = form.cleaned_data.get('clear_photo')
            obj.update_photo(old_photo=old_photo, clear_photo=clear_photo)
        obj.save()


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

