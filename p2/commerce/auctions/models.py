from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    # listing = models.ForeignKey(Listing  , on_delete=models.CASCADE , related_name="bids")
    price = models.DecimalField(max_digits=12, decimal_places=1)

    def __str__(self):
        return f"{self.bidder.username} bid {self.price} "


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    current_bid = models.ForeignKey(
        Bid, null=True, on_delete=models.SET_NULL, related_name="listing", blank=True
    )
    title = models.CharField(max_length=30)
    starting_bid = models.IntegerField(validators=[MinValueValidator(limit_value=0)])
    description = models.CharField(max_length=600)
    # image = models.ImageField(upload_to="images/", blank=True)
    image = models.CharField(max_length=50000, blank=True)
    category = models.CharField(max_length=30, blank=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=400)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f" {self.content} is written by {self.user.username}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watchlist"
    )

    def __str__(self):
        return f"{self.listing} with id :{self.listing.id} is on the watchlist of {self.user}"
