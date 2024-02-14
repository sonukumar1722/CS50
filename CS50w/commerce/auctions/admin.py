from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','dob','password')

class CreateAdmin(admin.ModelAdmin):
    list_display= ('id','owner','title','discription','price','category','image','date','status')

class CommentAdmin(admin.ModelAdmin):
    list_display= ('id','commenter','product_id','comment','date')

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id','watchlister','product_id','ids')

class BidAdmin(admin.ModelAdmin):
    list_display = ('id','bidder','bid_value','product_id','ids','status')

admin.site.register(User, UserAdmin)
admin.site.register(Create, CreateAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
