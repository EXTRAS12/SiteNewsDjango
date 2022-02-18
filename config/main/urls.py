from django.urls import path

from .views import *

urlpatterns = [

    path('', HomeNews.as_view(), name='home'),
    path('category/<str:slug>/', NewsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', NewsByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
    path('news/<str:slug>/', NewsDetail.as_view(), name='news_detail'),
    path('news/<str:slug>/update', NewsUpdate.as_view(), name='news_update'),
    path('news/<str:slug>/delete', NewsDelete.as_view(), name='news_delete'),
    path('my-post/', MyPost.as_view(), name='my_post'),
    path('add-news/', create_news, name='add_news'),
    path('contacts/', contacts, name='contacts'),
]
