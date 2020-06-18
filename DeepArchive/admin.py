from django.contrib import admin

from .models import Archive, ItemSet, ItemSetImage, Item

class ItemSetImageAdmin(admin.StackedInline):
    model = ItemSetImage


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    model = Archive


@admin.register(ItemSet)
class ItemSetAdmin(admin.ModelAdmin):
    inlines = [ItemSetImageAdmin]

    class Meta:
        model = ItemSet


@admin.register(ItemSetImage)
class ItemSetImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    model = Item
