from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CommentForm, PostForm
from .models import Post, Comment

 
def homePage(request):
    user = request.user if request.user.is_authenticated else None

    all_posts = Post.objects.all()

    paginator = Paginator(all_posts, 5)   
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'user': user, 'posts': posts})


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'register.html', {'form': form, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  
        else: 
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'login.html')    


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by("-created_on")
    new_comment = None
    new_comment_form = CommentForm()
    post_form = PostForm(instance=post)  
    user_authenticated = request.user.is_authenticated
    username = request.user.username

    if request.method == "POST": 
        comment_form = CommentForm(data=request.POST)
        print(comment_form)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            new_comment_form = CommentForm()
            return redirect('post_detail', slug=slug)

    return render(
        request,
        'post_detail.html',
        {
            "username": username,
            "slug": slug,
            "user_authenticated": user_authenticated,
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": new_comment_form,
            "post_form": post_form,
        },
    )


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user_authenticated = request.user.is_authenticated
    username = request.user.username

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=slug)
    else:
        form = PostForm(instance=post)

    return render(
        request, 
        'edit_post.html', 
        {
            'form': form, 
            'post': post,
            'user_authenticated': user_authenticated,
            'username':username
        }
    )
