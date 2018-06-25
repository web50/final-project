Final Project:

- This project is the "Stock Portfolio Management and Live-Pricing Website".
- Users can use this website to:
  (1) Search for pricing trends for any symbol/stock for last 6 months.
  (2) Build their portfolio for any symbols/stocks bought or sold. Their real-time prices will be retrieved and stored in Database (DJANGO's).
  (3) View their Portfolio with details on every stock, quantity, prices, and "total" price for all stocks at the table's footer. 
- It is built on DJANGO and PYTHON.
- It uses the API from "AlphaVantage" for retrieving the Real-Time Market-Data.
- The charts are built using the "PLOTLY".
- The Portfolio Status tables are built using the "DJANGO_TABLES2".

Tools/Utilities Needed:
1) DJANGO
2) PYTHON 3.6
3) PLOTLY:
   - To generate the PLOTLY charts, please follow the below instructions:
   - import plotly
   - Locate the plotly directory in your home directory: ~/.plotly
   - Edit the .credentials file as:
       "username": "yankeeguy_leo",
       "api_key": "rOvGbu95QlXYqnsINi6f",
4) django_tables2

5) All classes/lib's imported:
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
