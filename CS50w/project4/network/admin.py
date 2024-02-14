from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','password')
class LikesAdmin(admin.ModelAdmin):
    list_display = ('id','liked', 'liked_user', 'liked_post')
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id','follower', 'following', 'followed')
class NewPostAdmin(admin.ModelAdmin):
    list_display = ('id','content','creator', 'likes', 'comment')

admin.site.register(User, UserAdmin)
admin.site.register(Likes, LikesAdmin)
admin.site.register(NewPost, NewPostAdmin)
admin.site.register(Follow, FollowAdmin)