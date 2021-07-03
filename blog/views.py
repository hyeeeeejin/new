from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogForm

# Create your views here.

# READ
def home(request):
    blogs = Blog.objects.all()
    # 최신순으로 글 정리 blogs = Blog.objects.order_by('-pub_date')
    # 오래된 순으로 글 정리 blogs = Blog.objects.order_by('pub_date')
    # 검색 기능(filter)
    search = request.GET.get('search')
    if search == 'true' :
        author = request.GET.get('writer')
        blogs = Blog.objects.filter(writer=author)
        return render(request,'home.html', {blogs:'blogs'})
    # 검색 기능(검색한 거 제외, exclude)
    # search = request.GET.get('search')
    # if search == 'true' :
    #     author = request.GET.get('writer')
    #     blogs = Blog.objects.exclude(writer=author)
    #     return render(request,'home.html', {blogs:'blogs'})

    paginator = Paginator(blogs, 3)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'home.html', {'blogs':blogs})

def detail(request, id):
    #blog = Blog.objects.get(id = id) 밑에 거랑 똑같은 거.
    blog = get_object_or_404(Blog, pk = id)
    return render(request, 'detail.html', {'blog':blog})

# CREATE
def new(request) :
    form = BlogForm()
    return render(request,'new.html', {'form':form})

def create(request) :
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid() :
        new_blog = form.save(commit=False)
        new_blog.pub_date = timezone.now()
        new_blog.save()
        return redirect('detail', new_blog.id)
    return redirect('home')

# UPDATE
def edit(request, id):
    edit_blog = Blog.objects.get(id = id)
    return render(request, 'edit.html', {'blog' : edit_blog})

def update(request, id):
    update_blog = Blog.objects.get(id = id)
    update_blog.title = request.POST['title']
    update_blog.writer = request.POST['writer']
    update_blog.body = request.POST['body']
    update_blog.pub_date = timezone.now()
    update_blog.save()
    return redirect('detail', update_blog.id)

def delete(request, id) :
    delete_blog = Blog.objects.get(id=id)
    delete_blog.delete()
    return redirect('home')