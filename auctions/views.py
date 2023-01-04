from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Auction, Bet, Comment, Wishes

def index(request):
    auctions = Auction.objects.filter(status=True).all()
    bets = {record.id: f"{record.bet.order_by('-bet').first().bet:.2f} {record.bet.order_by('-bet').first().currency}" for record in auctions}
    return render(request, "auctions/index.html", {
        "title": "Активні лоти", 
        "auctions": auctions, 
        "bets": bets, 
        "categories": dict(Auction.PRODUCT_CATEGORY)
    })

def favorites(request):
    wishlist = Wishes.objects.filter(username=request.user).first()
    if wishlist:
        title = "Обране"
        auctions = wishlist.auction.filter(status=True)
        bets = {record.id: f"{record.bet.order_by('-bet').first().bet:.2f} {record.bet.order_by('-bet').first().currency}" for record in auctions}
    else:
        title = "Жодного обраного..."
        auctions = []
        bets = []
    return render(request, "auctions/index.html", {
        "title": title, 
        "auctions": auctions, 
        "bets": bets, 
        "categories": dict(Auction.PRODUCT_CATEGORY)
    })

def category(request, cat):
    auctions = Auction.objects.filter(status=True, category=cat).all()
    bets = {record.id: f"{record.bet.order_by('-bet').first().bet:.2f} {record.bet.order_by('-bet').first().currency}" for record in auctions}
    return render(request, "auctions/index.html", {
        "title": "Активні лоти в категорії", 
        "category": dict(Auction.PRODUCT_CATEGORY)[cat], 
        "auctions": auctions, 
        "bets": bets, 
        "categories": dict(Auction.PRODUCT_CATEGORY)
    })

def archive(request):
    auctions = Auction.objects.filter(status=False).all()
    bets = {record.id: f"{record.bet.order_by('-bet').first().bet:.2f} {record.bet.order_by('-bet').first().currency}" for record in auctions}
    return render(request, "auctions/index.html", {
        "title": "Завершені лоти", 
        "auctions": auctions, 
        "bets": bets, 
        "categories": dict(Auction.PRODUCT_CATEGORY)
    })

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

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if confirmation != password:
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

def create(request):
    #! get form's data
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        bet = request.POST["bet"]
        currency = request.POST["currency"]
        #! write bet
        start_bet = Bet(username=request.user, bet=bet, currency=currency)
        start_bet.save()
        #! write lot
        lot = Auction(title=title, description=description, image_url=image_url, category=category, username=request.user)
        lot.save()
        lot.bet.add(start_bet)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "categories": Auction.PRODUCT_CATEGORY, 
        "currencies": Bet.CURRENCIES
    })

def lot(request, id):
    #! general data
    lot = Auction.objects.get(pk=id)
    #! current (max) bet value
    last_bet = lot.bet.order_by('-bet').first()
    #! get user wishlist
    if request.user.is_authenticated:
        wishes = Wishes.objects.filter(username=request.user).first()
        if wishes:
            wishlist = [record.id for record in wishes.auction.all()]
        else:
            wishlist = []
    else:
        wishlist = []
    #! get lot comments
    comments = Comment.objects.filter(auction=lot).all()
    if request.method == "POST":
        bet = request.POST["bet"]
        currency = request.POST["currency"]
        #! write bet
        new_bet = Bet(username=request.user, bet=bet, currency=currency)
        new_bet.save()
        #! append current to lot
        lot = Auction.objects.get(pk=id)
        lot.bet.add(new_bet)
        lot.save()
        return HttpResponseRedirect(reverse("lot", args=(id,)))
    return render(request, "auctions/lot.html", {
        "lot": lot, 
        "last_bet": f"{last_bet.bet:.2f}", 
        "bet_currency": last_bet.currency,
        "bet_owner": last_bet.username, 
        "categories": dict(Auction.PRODUCT_CATEGORY), 
        "currencies": Bet.CURRENCIES, 
        "comments": comments, 
        "wishlist": wishlist
    })

def comment(request, id):
    #! general data
    lot = Auction.objects.get(pk=id)
    #! current (max) bet value
    last_bet = lot.bet.order_by('-bet').first()
    #! get user wishlist
    if request.user.is_authenticated:
        wishes = Wishes.objects.filter(username=request.user).first()
        if wishes:
            wishlist = [record.id for record in wishes.auction.all()]
        else:
            wishlist = []
    else:
        wishlist = []
    #! get lot comments
    comments = Comment.objects.filter(auction=lot).all()
    if request.method == "POST":
        comment = request.POST["comment"]
        #! write comment
        new_comment = Comment(username=request.user, auction=lot, comment=comment)
        new_comment.save()
        return HttpResponseRedirect(reverse("lot", args=(id,)))
    return render(request, "auctions/lot.html", {
        "lot": lot, 
        "last_bet": f"{last_bet.bet:.2f}", 
        "bet_currency": last_bet.currency,
        "bet_owner": last_bet.username, 
        "categories": dict(Auction.PRODUCT_CATEGORY), 
        "currencies": Bet.CURRENCIES, 
        "comments": comments, 
        "wishlist": wishlist
    })

def wish(request, id):
    #! get user wishlist
    auction = Auction.objects.get(pk=id)
    entry = Wishes.objects.filter(username=request.user, auction=auction).first()
    if entry:
        entry.auction.remove(auction)
    else:
        exists = Wishes.objects.filter(username=request.user)
        if exists:
            entry = exists.first()
        else:
            entry = Wishes(username=request.user)
            entry.save()
        entry.auction.add(auction)
    return HttpResponseRedirect(reverse("lot", args=(id,)))

def close(request, id):
    auction = Auction.objects.get(pk=id)
    auction.status = False
    auction.save()
    return HttpResponseRedirect(reverse("lot", args=(id,)))