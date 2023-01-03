from django.contrib import admin

from .models import MyModel, MyOtherModel


@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    pass

@admin.register(MyOtherModel)
class MyOtherModelAdmin(admin.ModelAdmin):
    pass
