from django.urls import path, include
from .views import *


urlpatterns = [
    # path('', listing),
    path('search', search, name='search'),
    # todo 传递一个flag表明当前所在的是大分类还是小分类
    path('category=<category_name>',get_category, name='show1'),
    path('ccategory=<category_name>', get_small_category, name='show2'),
    path('callback=<category_name>', callback, name='callback'),
    # todo 没办法，只能把小分类和大分类的排序函数分开了，并设定url一者为categery=，另一者为ccategory=
    path('sort_by_price=<category_name>', sort_by_price, name='sort_by_price'),
    path('sort_by_comments=<category_name>', sort_by_comments, name='sort_by_comments'),
    path('go!!!<page>',get_input_page, name='input_page'),
]