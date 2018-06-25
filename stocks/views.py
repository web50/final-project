from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django import forms
import requests

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as opy
from datetime import datetime
import pandas as pd
from decimal import *

import django_tables2 as tables
from django_tables2 import RequestConfig
from .tables import PortfolioTable

import numpy as np

from .forms import UserRegistrationForm
from .models import Portfolio, Customer

#Index page, for authentication and appropriate routing to login / registration / menu:

def index(request):
    if not request.user.is_authenticated:
        return render(request, "tickers/login.html", {"message": None})
    context = {
        "user": request.user
    }

    #to create user in local table as well:
    first = request.user.first_name
    last = request.user.last_name
    custUserID = request.user.username

    try:
        login_check = Customer.objects.get(custUserID=custUserID)
    except Customer.DoesNotExist:
        cust = Customer(first=first, last=last, custUserID=custUserID)
        cust.save()

    login_check = Customer.objects.get(custUserID=custUserID)

    if login_check is None:
        cust = Customer(first=first, last=last, custUserID=custUserID)
        cust.save()
    return render(request, "tickers/portindex.html", context)

#Login page:
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tickers/login.html", {"message": "Invalid credentials."})

#Logout page:
def logout_view(request):
    logout(request)
    return render(request, "tickers/login.html", {"message": "Logged out."})

#User Registration:
def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            first_name = userObj['first_name']
            last_name = userObj['last_name']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists()):
                new_user = User.objects.create_user(username, email, password)
                new_user.is_active = True
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.save()
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError("Username already exists.")
    else:
        form = UserRegistrationForm()
    return render(request, 'tickers/register.html', {'form': form})

#Portfolio Management Main Page Routing:
def portfolioroute(request):
    login_user = request.user.username
    login_customer = Customer.objects.get(custUserID=login_user)
    context = {
        "user": request.user,
        "customers": login_customer
    }
    return render(request, "tickers/manageportfolio.html", context)

#Search for live-pricing using API from AlphaVantage, and Buy/Sell the Stocks:
def manageportfolio(request):
    customer_id = request.POST.get('Customer', False)
    symbol_id_temp = request.POST.get('stockname', False)
    symbol_id = symbol_id_temp.upper()
    symbolPrice = float(0)
    symbolNet = float(0)
    customer = Customer.objects.get(pk=customer_id)

    #Check for missing quantity:
    try:
        symbolQty = request.POST.get('Quantity', False)
    except ValueError:
        return render(request, "tickers/portindex.html", context)

    try:
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={0}&interval=1min&apikey=rOvGbu95QlXYqnsINi6f&datatype=csv".format(symbol_id)
    except ValueError:
        message = "Something went wrong. Please check the Symbol and try again."
        return render(request, "tickers/manageportfolio.html", context)

    #Pandas being used for reading the CSV output from API respose:
    df = pd.read_csv(url)
    symbolPriceCheck = df.close.head(1)

    #Cost calculations:
    symbolQty_int = int(float(symbolQty))
    symbolPrice_temp = symbolPriceCheck
    symbolPrice = symbolPrice_temp[0]
    symbolNet_temp = symbolPrice * symbolQty_int
    symbolNet = round(symbolNet_temp, 2)

    #Add record to the Portfolio for the logged-in user:
    portfolio = Portfolio(symbolCust=customer, symbol=symbol_id, symbolPrice=symbolPrice, symbolQty=symbolQty_int, symbolNet=symbolNet)
    portfolio.save()
    portfolio_create_id = Portfolio.objects.latest('id').id

    portfolio_disp = Portfolio.objects.get(id=portfolio_create_id)
    context = {
        "portfolios": portfolio_disp,
        "customer": customer
    }

    table = PortfolioTable(Portfolio.objects.filter(symbolCust=customer))
    RequestConfig(request).configure(table)
    return render(request, 'tickers/portfoliostatus.html', {'table': table})

#Portfolio Status page, returns results only for the logged in user:
def portfoliostatus(request):
    login_user = request.user.username
    login_customer = Customer.objects.get(custUserID=login_user)

    table = PortfolioTable(Portfolio.objects.filter(symbolCust=login_customer))
    RequestConfig(request).configure(table)
    return render(request, 'tickers/portfoliostatus.html', {'table': table})

#Charting section for listing the Real-Time Market-Data on the basis of response from AlphaVantage API. Charts are built using PLOTLY (thanks to Seb):
def results(request):

    stock_id = request.POST.get('stockname', False)
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={0}&apikey=rOvGbu95QlXYqnsINi6f&datatype=csv".format(stock_id)
    df = pd.read_csv(url)

    trace_open = go.Scatter(
        x=df.timestamp,
        y=df['open'],
        name = "Open",
        line = dict(color = '#0D0E0D'),
        opacity = 0.8)

    trace_high = go.Scatter(
        x=df.timestamp,
        y=df['high'],
        name = "High",
        line = dict(color = '#33FF33'),
        opacity = 0.8)

    trace_low = go.Scatter(
        x=df.timestamp,
        y=df['low'],
        name = "Low",
        line = dict(color = '#FF5733'),
        opacity = 0.8)

    trace_close = go.Scatter(
        x=df.timestamp,
        y=df['close'],
        name = "Close",
        line = dict(color = '#3339FF'),
        opacity = 0.8)

    data = [trace_open,trace_high,trace_low,trace_close]

    layout = dict(
        title='Time Series with Rangeslider',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label='1m',
                            step='month',
                            stepmode='backward'),
                        dict(count=6,
                            label='6m',
                            step='month',
                            stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(),
                type='date'
            )
    )

    fig = dict(data=data, layout=layout)
    div = opy.plot(fig, auto_open=False, output_type='div', filename = "Time Series with Rangeslider")

    context = {
                  "stock_results": div
              }
    return render(request, "tickers/results.html", context)
