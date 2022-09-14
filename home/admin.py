from django.contrib import admin

# Register your models here.
from .models import User, PostsModel, AppointmentModel

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}


admin.site.register(User)
admin.site.register(PostsModel,PostAdmin)
admin.site.register(AppointmentModel)