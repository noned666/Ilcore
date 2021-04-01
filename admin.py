from django.contrib import admin
from .models import  Article, Category, Comment, Profile
from PIL import Image

class PostAdmin(Article):

    MUN_RESOLUTION = (4000, 4000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field['image'].help_text = 'Загружайте изображение с минимальным размеров {}x{}'.format(*self.MIN_RESOLUTION)


    def clean_image(self):
        image = self.cleaned_data['image']
        img = image.open(image)
        if img.height <min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального')
        return image
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_date','category', 'image']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','email', 'author', 'created_date' ]

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Category,  CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, AuthorAdmin)
