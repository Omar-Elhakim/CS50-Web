from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.activeListings, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories/", views.categories, name="Categories"),
    path(
        "categories/<str:ncategory>/", views.category_listing, name="category_listing"
    ),
    path("watchlist", views.watchlist, name="watchlist"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
