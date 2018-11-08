from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

"""
   post = get_object_or_404(Post, pk=pk)

   try:
        post = Post.objects.get(pk=pk)

    except Post.DoesNotExist:   
        return http404
"""
def post_list(request):
   
    qs = Post.objects.all()
    qs = qs.filter(published_date__lte=timezone.now())
    qs = qs.order_by('published_date')

    return render(request, 'blog/post_list.html', {
        'post_list' : qs,
    })

def post_detail(request, pk):

    # try except 구문을 간단하게 정리
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {
        'post': post
    })

@login_required # 로그인을 필수로 하는 장식자
def post_new(request):
    
    # POST값: request.POST, request.FILES
    
    if request.method == "POST":
        # request.POST, request.FILES 순서 중요 (값을 가져와서 FORM을 만든다.)
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {
        'form': form 
    })

@login_required
def post_edit(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
       
        # instance : 수정할 qs를 넣어준다.
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {
        'form': form
    })

@login_required
def post_draft_list(request):

    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    
    return render(request, 'blog/post_draft_list.html', { 'posts': posts })

def post_publish(request, pk):
    
    post = get_object_or_404(Post, pk=pk)
    post.publish()

    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    
    return redirect('post_list')

def add_comment_to_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', pk=post.pk)
        
    else:
        form = CommentForm()
        
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()

    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()

    return redirect('post_detail', pk=comment.post.pk)
