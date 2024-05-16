from django.contrib import admin
from .models import NavBarList, Sublist
# Register your models here.


@admin.register(NavBarList)
class NavBarListAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nav_name', 'slug']
    
@admin.register(Sublist)
class SublistAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nav_main', 'nav_sub_name', 'slug']
    