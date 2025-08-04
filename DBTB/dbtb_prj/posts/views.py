from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import * 
# Create your views here.

def main(request):
    categories = Category.objects.all()
    category_posts = {}

    for category in categories:
        posts = Post.objects.filter(postcategory__category=category).order_by('-created_at')[:4]
        category_posts[category] = posts


    return render(request, 'posts/main.html' , {'category_posts': category_posts})

def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render (request, 'posts/detail.html', {'post':post})


def update(request,id):
    post = get_object_or_404(Post, id=id)

    if request.method =='POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.is_anonymous = request.POST.get('is_anonymous') == "on"
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        if image:
            post.image.delete()
            post.image = image
        
        if video:
            post.video.delete()
            post.video = video

        post.save()

        return redirect ('posts:detail', id)
    return render(request, 'posts/update.html', {'post':post})

def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect ('posts:main')

def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == "on"

        Comment.objects.create(
            post = post,
            content=content,
            author=request.user,
            is_anonymous = is_anonymous
        )
        return redirect('posts:detail', post_id)
    return redirect('posts:main')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect ('posts:detail', post_id=comment.post.id)

@login_required
def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    # 예시: 해당 카테고리의 글 목록 가져오기
    posts = Post.objects.filter(category=category).order_by('-created_at')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_anonymous = request.POST.get('is_anonymous') == "on"  #체크박스 처리


        post = Post.objects.create(
            title=title, 
            content=content,
            author = request.user,
            is_anonymous = is_anonymous
        )

        PostCategory.objects.create(post=post, category=category)

        return redirect ('posts:category', slug=slug)
    else: # GET 요청일 때는 기존 글 목록 보여주기
        return render(request, 'posts/category.html', {'category': category,  'posts': posts})
    
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user= request.user

    if user in post.like.all(): #사용자가 좋아요를 눌렀는지 확인하는 함수
        post.like.remove(user) #눌렀으면 취소한다 ( 두번 누르면 취소 )
    else:
        post.like.add(user)
    return redirect('posts:detail', post_id)

def scrap(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user= request.user

    if user in post.scrap.all(): #사용자가 좋아요를 눌렀는지 확인하는 함수
        post.scrap.remove(user) #눌렀으면 취소한다 ( 두번 누르면 취소 )
    else:
        post.scrap.add(user)
    return redirect('posts:detail', post_id)

