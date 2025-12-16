import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, NewPost, Follow, Likes, Comment


@csrf_exempt
def index(request):

    # Attempt to get all the post
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            NewPost.objects.create(content=content, creator=request.user)
        return HttpResponseRedirect(reverse('index'))
    # Attempts to save the post
    posts = NewPost.objects.all().order_by('-datetime')
    return render(request, "network/index.html", {'posts': posts})

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(request, "network/login.html", {"message": "Invalid username and/or password."})
    return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if password != confirmation:
            return render(request, "network/register.html", {"message": "Passwords must match."})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            return render(request, "network/register.html", {"message": "Username already taken."})
    return render(request, "network/register.html")

def profile(request, user_id):

    # Attempt to get all the post in reverse chronological order
    user = get_object_or_404(User, id=user_id)
    posts = NewPost.objects.filter(creator=user).order_by('-datetime')
    following_count = Follow.objects.filter(follower=user).count()
    follower_count = Follow.objects.filter(following=user).count()
    return render(request, "network/profile.html", {
        'posts': posts,
        'user_id': user_id,
        'follower_count': follower_count,
        'following_count': following_count,
        'profile_user': user,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.profile_picture = request.POST.get('profile_picture', '')
        user.contact_email = request.POST.get('contact_email', '')
        user.bio = request.POST.get('bio', '')
        user.save()
    return HttpResponseRedirect(reverse('profile', args=(request.user.id,)))


@csrf_exempt
def follow(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        following_user = get_object_or_404(User, id=data.get('following_id'))
        if data.get('followed'):
            Follow.objects.get_or_create(follower=request.user, following=following_user)
        else:
            Follow.objects.filter(follower=request.user, following=following_user).delete()
        return HttpResponseRedirect(reverse('profile', args=(user_id,)))

    followed = Follow.objects.filter(follower=request.user, following_id=user_id).exists()
    return JsonResponse({"followed": followed})


@login_required
def following(request):
    following_rels = Follow.objects.filter(follower=request.user).select_related('following')
    following_users = [rel.following for rel in following_rels]
    follower_counts = {
        row['following']: row['count']
        for row in Follow.objects.filter(following__in=following_users)
        .values('following').annotate(count=Count('id'))
    }
    following_counts = {
        row['follower']: row['count']
        for row in Follow.objects.filter(follower__in=following_users)
        .values('follower').annotate(count=Count('id'))
    }
    context_users = []
    for u in following_users:
        context_users.append({
            'user': u,
            'follower_count': follower_counts.get(u.id, 0),
            'following_count': following_counts.get(u.id, 0),
        })
    return render(request, 'network/following.html', {'following_users': context_users})


@login_required
def followers(request):
    follower_rels = Follow.objects.filter(following=request.user).select_related('follower')
    follower_users = [rel.follower for rel in follower_rels]
    follower_counts = {
        row['following']: row['count']
        for row in Follow.objects.filter(following__in=follower_users)
        .values('following').annotate(count=Count('id'))
    }
    following_counts = {
        row['follower']: row['count']
        for row in Follow.objects.filter(follower__in=follower_users)
        .values('follower').annotate(count=Count('id'))
    }
    context_users = []
    for u in follower_users:
        context_users.append({
            'user': u,
            'follower_count': follower_counts.get(u.id, 0),
            'following_count': following_counts.get(u.id, 0),
        })
    return render(request, 'network/followers.html', {'follower_users': context_users})


@csrf_exempt
@login_required
def edit(request):
    # Attempt to edit the content of the post
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        post = get_object_or_404(NewPost, id=post_id)
        if post.creator == request.user:
            post.content = content
            post.save()
        return HttpResponseRedirect(reverse('index'))


@csrf_exempt
@login_required
def like(request):

    # Attempt to like/unlike the posts
    if request.method == "PUT":
        data = json.loads(request.body)

        post_id = data.get('post_id')
        post = NewPost.objects.get(id=post_id)

        # Update the likes count
        if data.get('liked') == True:
            # Check if user already liked this post
            like_obj, created = Likes.objects.get_or_create(
                liked_user=request.user,
                liked_post=post,
                defaults={'liked': True}
            )
            if created or not like_obj.liked:
                like_obj.liked = True
                like_obj.save()
                post.likes += 1
                post.save()

        elif data.get('liked') == False:
            # Check if user liked this post and remove the like
            try:
                like_obj = Likes.objects.get(liked_user=request.user, liked_post=post)
                if like_obj.liked:
                    like_obj.liked = False
                    like_obj.save()
                    post.likes -= 1
                    if post.likes < 0:
                        post.likes = 0
                    post.save()
            except Likes.DoesNotExist:
                pass

        return JsonResponse({"like_count": post.likes}, safe=False)

    liked = Likes.objects.filter(liked_user=request.user).values()
    return JsonResponse(list(liked), safe=False)


@csrf_exempt
def comments(request, post_id):
    post = get_object_or_404(NewPost, id=post_id)

    if request.method == 'GET':
        top_level = post.comments.filter(parent__isnull=True).order_by('-datetime')
        def serialize_comment(c):
            return {
                "id": c.id,
                "author": c.author.username,
                "author_id": c.author_id,
                "content": c.content,
                "datetime": c.datetime.isoformat(),
                "parent_id": c.parent_id,
                "replies": [
                    {
                        "id": r.id,
                        "author": r.author.username,
                        "author_id": r.author_id,
                        "content": r.content,
                        "datetime": r.datetime.isoformat(),
                        "parent_id": r.parent_id,
                        "parent_author": c.author.username,
                    }
                    for r in c.replies.order_by('datetime')
                ]
            }
        data = [serialize_comment(c) for c in top_level]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=403)

        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        if not content or content.strip() == "":
            return JsonResponse({"error": "Content required"}, status=400)

        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=int(parent_id), post=post)
            except (ValueError, Comment.DoesNotExist):
                return JsonResponse({"error": "Invalid parent"}, status=400)

        comment = Comment.objects.create(post=post, author=request.user, content=content.strip(), parent=parent)
        data = {
            "id": comment.id,
            "author": comment.author.username,
            "author_id": comment.author_id,
            "content": comment.content,
            "datetime": comment.datetime.isoformat(),
            "parent_id": comment.parent_id,
        }
        return JsonResponse(data, status=201)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@login_required
def comment_detail(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == 'PUT':
        if comment.author != request.user:
            return JsonResponse({"error": "Forbidden"}, status=403)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        content = data.get('content', '').strip()
        if not content:
            return JsonResponse({"error": "Content required"}, status=400)
        comment.content = content
        comment.save()
        return JsonResponse({
            "id": comment.id,
            "author": comment.author.username,
            "author_id": comment.author_id,
            "content": comment.content,
            "datetime": comment.datetime.isoformat(),
            "parent_id": comment.parent_id,
        })

    return JsonResponse({"error": "Method not allowed"}, status=405)
