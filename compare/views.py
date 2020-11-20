from django.shortcuts import render
from detail.models import Book
# Create your views here.

def compare(request):
    category_list = Book.objects.values('large_category').distinct()
    # small_category_list = Book.objects.values('large_category').distinct().values('small_category').distinct()
    name_list = list(category_list)
    small_category_dict = {}
    for category in name_list:
        small_category_dict[category['large_category']] = Book.objects.filter(large_category=category['large_category']).values_list('small_category').distinct()
        # print(small_category_dict[category['large_category']])
    context = {
        'category_list': category_list,
        'small_category_dict': small_category_dict,
    }
    return render(request, 'analysis.html', context=context)