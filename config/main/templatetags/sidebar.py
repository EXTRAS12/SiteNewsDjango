from django import template

from ..models import Category, News, Tag

register = template.Library()


@register.inclusion_tag('main/utils/menuCategory.html')
def show_menu(menu_class='menu'):
    categories = Category.objects.all()
    return {'categories': categories, 'menu_class': menu_class}


@register.inclusion_tag('main/utils/popular_post.html')
def get_popular(cnt=3):
    news = News.objects.order_by('-views')[:cnt].select_related('category', 'author')

    return {'news': news}


@register.inclusion_tag('main/utils/menuTags.html')
def get_tags():
    tags = Tag.objects.all()
    return {'tags': tags}
