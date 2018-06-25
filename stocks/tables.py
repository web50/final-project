#For building the Table in "Portfolio Status" page using DJANGO_TABLES2:
import django_tables2 as tables
from .models import Portfolio

def symbolNet_footer(table):
    s = sum(x.symbolNet for x in table.data)
    return s

class PortfolioTable(tables.Table):
    symbolNet = tables.Column(footer=symbolNet_footer)

    class Meta:
        model = Portfolio
        template_name = 'django_tables2/bootstrap.html'
        fields = ('symbolCust', 'symbol', 'symbolPrice', 'symbolQty', 'symbolNet')
