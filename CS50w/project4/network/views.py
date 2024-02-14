import json
from re import T
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *


@csrf_exempt
def index(request):

    # Attempt to get all the post
    if request.method != 'POST':
        posts = NewPost.objects.all().order_by('-datetime')
        return render(request, "network/index.html", {
        'posts': posts,
        })

    # Attempt to save the new psot
    content = request.POST['content']
    creator = request.user
    NewPost(content= content, creator = creator).save()

    return HttpResponseRedirect(reverse('index'))

@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()

            
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, user_id):

    # Attempt to get all the post in reverse chronological order
    posts = NewPost.objects.filter(creator_id= user_id).order_by('-datetime')
    following_count = len(Follow.objects.filter(follower_id= user_id))
    follower_count = len(Follow.objects.filter(following_id= user_id))
    return render(request, "network/profile.html", {
        'posts': posts,
        'user_id': user_id,
        'follower_count': follower_count,
        'following_count': following_count,
    })


@csrf_exempt
def follow(request, user_id):
    user_ = None

    # Attempt to follow/unfollow the post
    if request.method == 'PUT':
        data = json.loads(request.body)
        user_ = User.objects.get(id= data.get('following_id'))

        # Attempt to follow the post
        if data.get('followed') == True:
            Follow(followed = True, follower = request.user, following = user_).save()

        # Attempt unfollow the post
        elif data.get('followed') == False:
            Follow.objects.get(followed = True, follower = request.user.id , following = user_).delete()

        return HttpResponseRedirect(reverse('profile', args=(user_id,)))

    # Attempt to change the follow button style from follow to unfollow or vice versa
    try:
        element = Follow.objects.get(followed = True, follower = request.user.id , following = user_id)
        return JsonResponse({"followed": element.followed}, safe = False)
    except:
        return JsonResponse({"followed": False}, safe = False)


@login_required
def following(request):

    # Display all the post of other user whom the current user follows
    posts = []
    user_follow_list = Follow.objects.filter(follower_id= request.user.id)
    for user_ids in user_follow_list:
        all_posts =  NewPost.objects.filter(creator_id= user_ids.following_id)
        for post in all_posts:
            posts.append(post)
            print(posts)
    return render(request, 'network/following.html', {
        'posts': posts
    })


@csrf_exempt
@login_required
def edit(request):

    # Attempt to edit the content of the post
    if request.method == "POST":
        post_id = request.POST['post_id']
        content = request.POST['content']
        element = NewPost.objects.get(id= post_id)
        element.content = content
        element.save()
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

    liked = Likes.objects.filter(liked_user_id= request.user.id).values()
    return JsonResponse(list(liked), safe=False)
