from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def index(request):
    return render(request, "auctions/index.html")


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_listing(request):
    if request.method == "POST":
        populatedForm = ListingForm(request.POST, request.FILES)
        listing = populatedForm.save(commit=False)
        listing.owner = request.user
        listing.save()

        return HttpResponseRedirect(
            reverse("listing", kwargs={"listing_id": listing.id})
        )
    else:
        form = ListingForm()
        return render(request, "auctions/new_listing.html", {"form": form})


def listing(request, listing_id):
    nListing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=nListing)
    newCommentForm = CommentForm()
    newBidForm = BidForm()

    message = ""
    try:
        Watchlist.objects.get(
            user=request.user, listing=Listing.objects.get(pk=listing_id)
        )
        added = True
    except Exception:
        added = False
    if request.method == "POST":
        if request.POST["action"] == "comment":
            request.POST["content"]  # if its a comment
            commentForm = CommentForm(request.POST)
            comment = commentForm.save(commit=False)
            comment.listing = nListing
            comment.user = request.user
            comment.save()
        elif "Watchlist" in request.POST["action"]:
            # nListing = Listing.objects.get(pk=request.POST["listing_id"])
            if request.POST["action"] == "addWatchlist":
                new_watchlist = Watchlist(user=request.user, listing=nListing)
                new_watchlist.save()
                added = True
            else:
                del_watchlist = Watchlist.objects.filter(
                    user=request.user, listing=nListing
                )
                del_watchlist.delete()
                added = False
        elif request.POST["action"] == "bid":
            if nListing.current_bid == None:
                if float(request.POST["price"]) <= nListing.starting_bid:
                    message = "You can't bid same as current bid or lower!"
                else:
                    bidform = BidForm(request.POST)
                    bid = bidform.save(commit=False)
                    bid.bidder = request.user
                    bid.save()
                    nListing.current_bid = bid
                    nListing.save()
                    # bid.listing=nListing
            else:
                if float(request.POST["price"]) <= nListing.current_bid.price:
                    message = "You can't bid same as current bid or lower!"
                else:
                    bidform = BidForm(request.POST)
                    bid = bidform.save(commit=False)
                    bid.bidder = request.user
                    bid.save()
                    nListing.current_bid = bid
                    nListing.save()
                    # bid.listing=nListing
        elif request.POST["action"] == "close":
            nListing.is_open = False
            nListing.save()

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": nListing,
            "comments": comments,
            "commentForm": newCommentForm,
            "bidForm": newBidForm,
            "added": added,
            "message": message,
        },
    )


def activeListings(request):
    return render(
        request,
        "auctions/activeListings.html",
        {"listings": Listing.objects.filter(is_open=True)},
    )


def categories(request):
    ncategories = (
        Listing.objects.filter(is_open=True)
        .values_list("category", flat=True)
        .distinct()
    )
    return render(request, "auctions/categories.html", {"Categories": ncategories})


def category_listing(request, ncategory):
    listings = Listing.objects.filter(category=ncategory)
    return render(request, "auctions/activeListings.html", {"listings": listings})


@login_required
def watchlist(request):
    if request.method == "POST":
        nListing = Listing.objects.get(pk=request.POST["listing_id"])
        del_watchlist = Watchlist.objects.filter(user=request.user, listing=nListing)
        del_watchlist.delete()
    querySet = Watchlist.objects.filter(user=request.user)
    listings = []
    for watchlist in querySet:
        listings.append(watchlist.listing)
    return render(request, "auctions/watchlist.html", {"listings": listings})
