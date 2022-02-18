from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, News, Tag


class NewsAdminForm(forms.ModelForm):
    """Форма для контента ckeditor"""
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    """Для статей"""
    list_display = ('id', 'title', 'is_published', 'author', 'get_photo',
                    'category', 'slug', 'created_at', 'updated_at', 'views')
    prepopulated_fields = {'slug': ('title',)}
    form = NewsAdminForm
    save_as = True
    save_on_top = True
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content', 'author')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category', 'tags')
    fields = ('title', 'author', 'slug', 'category', 'content', 'photo', 'is_published', 'views',
              'created_at', 'updated_at', 'tags')
    readonly_fields = ('views', 'created_at', 'updated_at')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return '-'


class CategoryAdmin(admin.ModelAdmin):
    """Для категорий"""
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


class TagAdmin(admin.ModelAdmin):
    """Для тэгов"""
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)


admin.site.site_title = 'Управление публикациями'
admin.site.site_header = 'Управление публикациями'
