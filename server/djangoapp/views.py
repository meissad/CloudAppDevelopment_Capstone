from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')



# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("djangoapp:index"))
        else:
            return render(request, "djangoapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "djangoapp/login.html")


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse("djangoapp:index"))

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_name = request.POST["username"]
        password = request.POST["password"]

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=user_name, first_name=first_name, last_name=last_name,password=password)
        except IntegrityError as e:
            print(e)
            return render(request, "djangoapp/registration.html", {
                "message": "username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("djangoapp:index"))
    else:
        return render(request, "djangoapp/registration.html")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://promeissa1-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        #print(dealerships)
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = ""
        context = []
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context.append(reviews)
        return HttpResponse(context)

# Create a `add_review` view to submit a review
@login_required
def add_review(request, dealer_id):
    
    review = {}
    review["time"] = datetime.utcnow().isoformat()
    review["dealership"] = 11
    review["review"] = "This is a great car dealer"

    json_payload = {}
    json_payload["review"] = review
    result = post_request(url,json_payload, dealerId=dealer_id)
    return HttpResponse("Review posted")