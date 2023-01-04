from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ("id", "username", "email")

class BetAdmin(admin.ModelAdmin):
	list_display = ("id", "timestamp", "bet")

class CommentAdmin(admin.ModelAdmin):
	list_display = ("id", "timestamp", "auction", "comment")

class AuctionAdmin(admin.ModelAdmin):
	list_display = ("id", "timestamp", "title", "description")

class WishesAdmin(admin.ModelAdmin):
	list_display = ("id", "username")

admin.site.register(User, UserAdmin)
admin.site.register(Bet, BetAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Wishes, WishesAdmin)