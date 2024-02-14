from itertools import product
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    return render(request, "auctions/index.html")

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@csrf_exempt
def create(request):
    if request.method == "POST":
        send = Create()
        send.title = request.POST["title"]
        send.price = request.POST["price"]
        send.discription = request.POST["discription"]
        send.image = request.POST["image"]
        send.category = request.POST["category"] 
        send.owner = request.user.username
        send.status = False
        send.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'auctions/create.html')

@csrf_exempt
def comment(request, item_id):
    if request.method == "POST":
        send = Comment()
        send.comment = request.POST['comment']
        send.commenter = request.user.username
        send.product_id = item_id
        send.save()

        return HttpResponseRedirect(reverse('listing',args=(item_id,)))


def index(request):
    keys = []
    items = Create.objects.all()

    try:
        data = Watchlist.objects.get(watchlister = request.user.username)
        [keys.append(int(key)) for key in data.ids]
    except:
        pass

    return render(request, 'auctions/index.html',{
        "items" : items,
        "watchlist_ids":keys,
    })


def category(request, cato):

    list = ['Books', 'Clothes', 'Crockry', 'Electronics', 'Fantasy', 'Fashion', 'Furnitures', 'Home Affairs', 'Jwellery', 'Toys']

    return render(request, 'auctions/category.html',{
        "categories": list,
        "items" : Create.objects.filter(category = cato)
    })


def listing(request, item_id):
    keys = []
    item = Create.objects.get(id=item_id)

    try:
        data = Watchlist.objects.get(watchlister = request.user.username)
        [keys.append(int(key)) for key in data.ids]
    except:
        pass
    try:
        bidder = Bid.objects.get(product_id = item_id)
    except:
        bidder = None

    return render(request, 'auctions/listing.html', {
        "item" : item,
        "comments": Comment.objects.filter(product_id = item_id),
        "watchlist_ids":keys,
        "bidder" : bidder,
    })


@csrf_exempt
def watchlist(request):
    keys = []

    try:
        data = Watchlist.objects.get(watchlister = request.user.username)
        [keys.append(int(key)) for key in data.ids]
    except:
        pass

    if request.method == "POST":
        product_id = request.POST['product_id']
        watchlister = request.user.username 

        try:
            update = Watchlist.objects.get(watchlister = request.user.username)
            if (not product_id in update.ids):
                update.ids.append(int(product_id))
                update.save()
        except:
            Watchlist(product_id=product_id, watchlister=watchlister,ids = [product_id]).save()
        return HttpResponseRedirect(reverse('watchlist'))

    return render(request, 'auctions/watchlist.html',{
        'items': Create.objects.all(),
        'item_id': keys
    })
    

@csrf_exempt
def remove(request):
    if request.method == "POST":
        item_id = (request.POST['product_id'])
        outdate = Watchlist.objects.get(watchlister = request.user.username)

        try:
            outdate.ids.remove(int(item_id))
        except:
            outdate.ids.remove(str(item_id))
            
        outdate.save()
        return HttpResponseRedirect(reverse("watchlist"))


@csrf_exempt
def bidding(request):
    if request.method == "POST":
        ids = {}
        bidder = request.user.username
        product_id = request.POST['product_id']
        try:
            bid_value = float(request.POST["bid_value"])
        except:
            bid_value = 0

        item = Create.objects.get(id = product_id)
        if (bid_value > item.price):

            try:
                update = Bid.objects.get(product_id = product_id)
                update.ids[f"{product_id}"] = bid_value
                update.bidder = bidder
                update.bid_value = bid_value
                update.save()
            except:
                Bid(ids=ids, bidder=bidder, product_id=product_id, bid_value=bid_value,status = False).save()

            item.price = (f'{bid_value}')
            item.save()

    return HttpResponseRedirect(reverse('listing',args=(product_id,)))


@csrf_exempt
def close(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]

        try: 
            winner = Bid.objects.get(product_id = product_id)
            winner.status = True
            winner.save()
        except:
            pass

        send = Create.objects.get(id = product_id)
        send.status = True
        send.save()
    return HttpResponseRedirect(reverse('index'))
        