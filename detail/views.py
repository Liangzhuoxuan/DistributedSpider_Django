from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect

from detail.photo_crawler import PhotoCrawler

from .models import *
import pickle

# 执行某一页对应的图片的爬取
def download(books):
    img_list = []
    url_list = []
    for book in books:
        if book.img != 'None':
            # url = book.img[2:-2]
            url = book.img
            url_list.append(url)
            # downloader(book.img[0])
            # response = requests.get(url)
            # path = self.url[-16:]
            # part_of_path = r'C:\Users\14128\Desktop\abcdefghijk\static\img'
            # path = os.path.join(part_of_path, url[-16:])
            # with open(path, 'wb') as fp:
            #     fp.write(response.content)
            # urlretrieve(url,path)
            img_list.append('img/' + book.img[-16:])
        else:
            img_list.append('')
    crawler = PhotoCrawler()
    crawler.more_processing(url_list)
    new_list = list(zip(books, img_list))
    return new_list, books


# 商品展示
def listing(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 12)  # 30个一页

    page = request.GET.get('page')
    try:
        books = paginator.page(page)

    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    # 执行图片下载
    new_list, books = download(books)
    return render(request, 'details.html', {'books': books, 'new_list': new_list})


# 大分类页和详情页的搜索功能
def search(request):
    # 搜索的时候重定向不一样，需要携带参数，所以进行url的拼接
    first = request.path
    second = request.GET.get('keyword')
    with open('D:/referer_url.pk', 'wb') as fp:
        pickle.dump(first+'?keyword='+second, fp)

    if request.method == 'GET':
        # 设置keyword的默认值为''空
        keyword = request.GET.get('keyword', '')
        # 搜索标题，作者，出版社中有搜索关键字的信息
        book_list = Book.objects.filter(
            Q(title__icontains=keyword) | Q(author__icontains=keyword) | Q(publisher__icontains=keyword))
        paginator = Paginator(book_list, 12)
        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        # 执行图片下载
        new_list, books = download(books)
        # 此处的category_name为搜索的keyword的名字，用于搜索后的排序和分页
        return render(request, 'details.html',
                      {'books': books, 'category_name': keyword + 'flagshere', 'new_list': new_list})


# 从外面的大分类点击 “查看更多”的时候进入的分页
def get_category(request, category_name):
    book_list = Book.objects.filter(large_category=category_name)
    # 实现点击返回原页面排序的操作
    with open('D:/referer_url.pk', 'wb') as fp:
        pickle.dump(request.path, fp)

    paginator = Paginator(book_list, 12)  # 30个一页

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    # 执行图片下载
    new_list, books = download(books)
    return render(request, 'details.html', {'new_list': new_list, 'books': books, 'category_name': category_name})

# 通过小分类进行商品的筛选
def get_small_category(request, category_name):
    book_list = Book.objects.filter(small_category=category_name)
    paginator = Paginator(book_list, 12)  # 30个一页

    with open('D:/referer_url.pk', 'wb') as fp:
        pickle.dump(request.path, fp)

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    # 执行图片下载
    new_list, books = download(books)
    return render(request, 'details.html', {'new_list': new_list, 'books': books, 'category_name': category_name})

'''问题：实现  搜索后的排序，分类后的排序'''


# 再次点击综合排序的时候，返回最初的排序
def callback(request, category_name):
    # referer = request.META.get('HTTP_REFERER')
    # flag为1是小分类的标志。flag为0是大分类的标志
    # if  flag == 1:
    #     return redirect('show2', category_name=category_name, flag=1)
    with open('D:/referer_url.pk', 'rb') as fp:
        go_to = pickle.load(fp)
    return redirect(go_to)



# 通过价格排序
def sort_by_price(request, category_name):
    # 设置搜索后的标签
    if category_name.endswith('flagshere'):
    # if flag == 3:
        category_name = category_name.replace('flagshere', '')
        book_list = Book.objects.filter(Q(title__icontains=category_name) | Q(author__icontains=category_name) | Q(
            publisher__icontains=category_name)).order_by('-price')
        paginator = Paginator(book_list, 12)  # 30个一页

        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        category_name += 'flagshere'
        # 执行图片下载
        new_list, books = download(books)
        witch = 'pri'
        return render(request, 'details.html', {'new_list': new_list, 'books': books, 'category_name': category_name, 'witch':witch})
    # 否则就是来自大分类的大兄弟了
    else:
        book_list = Book.objects.filter(large_category=category_name).order_by('-price')
        if book_list:
            pass
        else:
            book_list = Book.objects.filter(small_category=category_name).order_by('-price')
        paginator = Paginator(book_list, 12)  # 30个一页

        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        # 执行图片下载
        new_list, books = download(books)
        witch = 'pri'
        return render(request, 'details.html', {'new_list': new_list, 'books': books, 'category_name': category_name, 'witch':witch})


# 按照评论数排序
def sort_by_comments(request, category_name):
    # 设置搜索后的标签
    if category_name.endswith('flagshere'):
    # if flag == 3:
        category_name = category_name.replace('flagshere', '')
        book_list = Book.objects.filter(Q(title__icontains=category_name) | Q(author__icontains=category_name) | Q(
            publisher__icontains=category_name)).order_by('-comments')
        paginator = Paginator(book_list, 12)  # 30个一页

        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        category_name += 'flagshere'
        # 执行图片下载
        new_list, books = download(books)
        witch = 'coms'
        return render(request, 'details.html', {'new_list': new_list, 'books': books, 'category_name': category_name, 'witch':witch})
    # 否则就是来自大分类的大兄弟了
    else:
        book_list = Book.objects.filter(large_category=category_name).order_by('-comments')
        if book_list:
            pass
        else:
            book_list = Book.objects.filter(small_category=category_name).order_by('-comments')
        paginator = Paginator(book_list, 12)  # 30个一页

        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        # 执行图片下载
        new_list, books = download(books)
        witch = 'coms'
        return render(request, 'details.html', {'new_list': new_list, 'books': books, 'category_name': category_name,'witch':witch})

def get_input_page(request,page):
    page_number = request.GET.get('want_to_got_page')
    referer = request.META.get('HTTP_REFERER')
    print(page_number)
    print(type(page))
    if page == '1':
        part_of_url = referer.split('page')[0]
        url = part_of_url + '?page=' + page_number
    else:
        part_of_url = referer.split('page')[0]
        url = part_of_url + 'page=' + page_number
    return redirect(url)



