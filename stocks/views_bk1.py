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
#import pandas_datareader.data as web
import pandas as pd

# Create random data with numpy
import numpy as np
#from .forms import UserRegistrationForm

#from .models import Topping, Menu, Order, Customer

# Create your views here.

#Index page, for authentication and appropriate routing to login / registration / menu:
def index(request):


    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AMZN&interval=1min&apikey=4LGYQ85VR5EGTT7C'
    stock_results = requests.get(url)
    r1 = stock_results.json()
    r2 = r1['Time Series (1min)']

    N = 100
    random_x = np.linspace(0, 1, N)
    random_y0 = np.random.randn(N)+5
    random_y1 = np.random.randn(N)
    random_y2 = np.random.randn(N)-5

    Snap = "1. open"
    for p_id, p_info in r2.items():
        TimeStamp = p_id
        RateSnap = p_info[Snap]
        #print("\nTimeStamp:", p_id)
        #print(Snap + ':', p_info[Snap])
        #print(TimeStamp + ',' + RateSnap)


    # Create traces
        trace0 = go.Scatter(
            x = TimeStamp,
            y = RateSnap,
            line = dict(color = '#17BECF'),
            opacity = 0.8
            #mode = 'lines',
            #name = 'lines'
            )

        data = [trace0]

    #py.iplot(data, filename='line-mode')


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
        #py.iplot(fig, filename = "Time Series with Rangeslider")


        #div = opy.plot(data, auto_open=False, output_type='div', layout=layout)
        div = opy.plot(fig, auto_open=False, output_type='div', filename = "Time Series with Rangeslider")

    #context['graph'] = div

        context = {
    #"stock_results": stock_results_json
        "stock_results": div
        }
        return render(request, "tickers/index.html", context)
