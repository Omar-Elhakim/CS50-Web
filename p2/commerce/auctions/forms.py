from django import forms
from django.forms import ModelForm
from .models import *


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ["current_bid", "owner", "is_open"]
        labels = {"image": "Image link"}

    widgets = {
        "owner": forms.HiddenInput(),
    }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": "Add your comment: "}

    # Custom widgets
    widgets = {
        "listing": forms.HiddenInput(),  # Hidden field
        "user": forms.HiddenInput(),  # Hidden field
        "content": forms.Textarea(
            attrs={"cols": 80, "rows": 20}
        ),  # Custom textarea size
    }


class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = "__all__"


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]
        labels = {"price": "Place your bid "}

    widgets = {
        "bidder": forms.HiddenInput(),
        "listing": forms.HiddenInput(),
    }
