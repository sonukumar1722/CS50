from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    dob = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.id}, {self.username}, ({self.email}), {self.dob}, {self.password}"

class Create(models.Model):
    image = models.URLField(blank=True)
    title = models.CharField(max_length=64)
    discription = models.TextField(max_length=200, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=64, default= 0.00)
    category = models.CharField(max_length=64, null =True)
    date = models.DateTimeField(auto_now=True, null=True)
    owner = models.CharField(max_length=64)
    status = models.BooleanField(default=False,null=True)

    def __str__(self):
        return f"{self.owner} {self.image} {self.title} {self.price} {self.category} {self.discription} {self.status}"

class Comment(models.Model):
    product_id = models.IntegerField() 
    comment = models.TextField(max_length = 200)
    date = models.DateTimeField(auto_now = True, null=True)
    commenter = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.comment} {self.product_id} {self.commenter} {self.date}"

class Watchlist(models.Model):
    product_id = models.IntegerField()
    watchlister = models.CharField(max_length=64)
    ids = models.JSONField(null=True)

    def __str__(self):
        return f"{self.watchlister} {self.product_id}"

class Bid(models.Model):
    product_id = models.IntegerField()
    ids = models.JSONField(null = True)
    bidder = models.CharField(max_length = 64)
    bid_value = models.DecimalField(decimal_places=2, max_digits=64)
    status = models.BooleanField(default=False, null = True)

    def __str__(self):
        return f"{self.id} {self.bidder} {self.product_id} {self.bid_value} {self.ids} {self.status}"