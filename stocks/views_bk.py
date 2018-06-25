from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django import forms
import requests
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as opy

# Create random data with numpy
import numpy as np
#from .forms import UserRegistrationForm

#from .models import Topping, Menu, Order, Customer

# Create your views here.

#Index page, for authentication and appropriate routing to login / registration / menu:
def index(request):


    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AMZN&interval=1min&apikey=4LGYQ85VR5EGTT7C'
    stock_results = requests.get(url)
    stock_results_json = stock_results.json()

    N = 100
    random_x = np.linspace(0, 1, N)
    random_y0 = np.random.randn(N)+5
    random_y1 = np.random.randn(N)
    random_y2 = np.random.randn(N)-5

    # Create traces
    trace0 = go.Scatter(
        x = random_x,
        y = random_y0,
        mode = 'lines',
        name = 'lines'
    )
    trace1 = go.Scatter(
        x = random_x,
        y = random_y1,
        mode = 'lines+markers',
        name = 'lines+markers'
    )
    trace2 = go.Scatter(
        x = random_x,
        y = random_y2,
        mode = 'markers',
        name = 'markers'
    )
    data = [trace0, trace1, trace2]

    #py.iplot(data, filename='line-mode')

    div = opy.plot(data, filename='line-mode', auto_open=False, output_type='div')

    #context['graph'] = div

    #context = {
    #"stock_results": stock_results_json
    #"stock_results": plot_sample
    #}
    #return render(request, "tickers/index.html", context)

class Graph(TemplateView):
    template_name = 'graph.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        x = [-2,0,4,6,7]
        y = [q**2-q+3 for q in x]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
                            mode="lines",  name='1st Trace')

        data=go.Data([trace1])
        layout=go.Layout(title="Meine Daten", xaxis={'title':'x1'}, yaxis={'title':'x2'})
        figure=go.Figure(data=data,layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div

        return render(request, "tickers/index.html", context)
