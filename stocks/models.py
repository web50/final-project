from django.db import models

# Create your models here.


class Customer(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    custUserID = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.first} {self.last}"

class Portfolio(models.Model):
    symbolCust = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='User Name')
    symbol = models.CharField(max_length=64, blank=True, null=True, verbose_name='Symbol')
    symbolPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Symbol Price')
    symbolQty = models.IntegerField(verbose_name='Symbol Quantity')
    symbolNet = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Symbol Net Cost')


    def __str__(self):
        return f"{self.id} - Customer: {self.symbolCust}, Symbol: {self.symbol}, Symbol-Price: {self.symbolPrice}, Symbol-Qty: {self.symbolQty}, Symbol-Cost: {self.symbolNet}"
