from django.db import models

# Create your models here.

class Billing(models.Model):
    generate_date= models.DateField(auto_now_add=True)
    paid_date= models.DateField(null=True)
    from_date= models.DateField()
    to_date= models.DateField()
    total_in= models.IntegerField()
    total_out= models.IntegerField()
    hosting= models.FloatField()
    total= models.FloatField()
    status= models.IntegerField(default=0)

 