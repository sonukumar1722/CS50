import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, NewPost, Follow, Likes


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
    })


@csrf_exempt
def follow(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        following_user = get_object_or_404(User, id=data.get('following_id'))
        if data.get('followed'):
            Follow.objects.get_or_create(follower=request.user, following=following_user, defaults={'followed': True})
        else:
            Follow.objects.filter(follower=request.user, following=following_user, followed=True).delete()
        return HttpResponseRedirect(reverse('profile', args=(user_id,)))

    followed = Follow.objects.filter(follower=request.user, following_id=user_id, followed=True).exists()
    return JsonResponse({"followed": followed})


@login_required
def following(request):

    user_follow_list = Follow.objects.filter(follower=request.user)
    posts = NewPost.objects.filter(creator__in=[follow.following for follow in user_follow_list]).order_by('-datetime')
    return render(request, 'network/following.html', {'posts': posts})


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
        post = NewPost.objects.get(id= post_id)
        element = Likes()

        # Update the likes count
        if data.get('liked') == True:
            post.likes += 1
            post.save()

            element.liked = True
            element.liked_user = request.user
            element.liked_post = post
            element.save()

        elif data.get('liked') == False:
            post.likes -= 1
            post.save()

            element.liked = False
            element.liked_user = request.user
            element.liked_post = post
            element.save()

        return JsonResponse({"like_count": post.likes}, safe=False)

    liked = Likes.objects.filter(liked_user=request.user).values()
    return JsonResponse(list(liked), safe=False)
