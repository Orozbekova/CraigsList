from django.contrib import admin

# Register your models here.
from applications.board.models import *

admin.site.register(Category)
admin.site.register(SubCategory)
# admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Likes)
# admin.site.register(Order)
admin.site.register(Favorite)
class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 3

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]
