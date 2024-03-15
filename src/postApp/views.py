from django.shortcuts import render, redirect, get_object_or_404
from django.http import  JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from .forms import  CommentForm, PostForm, SearchForm
from .models import Post
from django.db.models import Q 
 
def homePage(request):
    user_authenticated = request.user.is_authenticated 
    all_posts = Post.objects.all() 
    paginator = Paginator(all_posts, 5)   
    page = request.GET.get('page', 1) 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    form = SearchForm(request.GET)
    query = request.GET.get('query', '')
    # print(form)

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        ).distinct()

    return render(request, 'post/home.html', {'user_authenticated': user_authenticated, 'posts': posts, 'form': form, 'query': query})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by("-created_on")
    new_comment = None
    new_comment_form = CommentForm()
    post_form = PostForm(instance=post)  
    user_authenticated = request.user.is_authenticated
    username = request.user.username
    attachment = request.FILES.get('attachment') 

    if request.method == "POST": 
        comment_form = CommentForm(data=request.POST)
        # print(comment_form)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            new_comment_form = CommentForm()
            return redirect('post_detail', slug=slug)

    return render(
        request,
        'post/post_detail.html',
        {
            "username": username,
            'user_authenticated': user_authenticated,
            "slug": slug, 
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": new_comment_form,
            "post_form": post_form,
            "attachment": attachment, 
        },
    )

def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user_authenticated = request.user.is_authenticated
    username = request.user.username 
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES ,instance=post)
        # print(form)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=slug)
    else:
        form = PostForm(instance=post)

    return render(
        request, 
        'post/edit_post.html', 
        {
            'form': form, 
            'post': post,
            'user_authenticated': user_authenticated,
            'username':username, 
        }
    )

def create_post(request):
    user_authenticated = request.user.is_authenticated
    print("hi")
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print("hello")  
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = Post.create_unique_slug(post)
            post.author = request.user  
            post.save()
            return redirect('post_detail', slug=post.slug)   
    else:
        form = PostForm(request.POST, request.FILES)

    return render(request, 'post/create_post.html', {'form': form, 'user_authenticated': user_authenticated})

def post_list(request):
    form = SearchForm(request.GET)
    query = request.GET.get('query', '')

    if query:
        # Perform the search using case-insensitive and partial matching
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.all()

    return render(request, 'post/post_list.html', {'posts': posts, 'form': form, 'query': query})

def delete_post(request, slug): 
    if request.method == 'DELETE':
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        # print('Post Deleted')
        return JsonResponse({'message': 'Post deleted successfully'}, status=204)
    else:
        # print('Not allowed')
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def search_posts(request, slug):
    if request.method == 'GET':
        filtered_posts = Post.objects.filter(
            Q(title__icontains=slug) | Q(text__icontains=slug)
        ).values('slug', 'title', 'updated_on')
 
        if filtered_posts.count() > 6:
            filtered_posts = filtered_posts[:6]
 
        serialized_posts = list(filtered_posts)
        return JsonResponse(serialized_posts, safe=False, status=200)
    else:
        return JsonResponse({'error': 'Not searched'}, status=405)