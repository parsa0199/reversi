# myapp/management/commands/check_weight.py
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'check if products has weight'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        for product in products:
            #check if products has single weight
            if product.weight:
                if product.weight == 222:
                    print(f"{product.title} has the default weight")
            else:

                product.weight = 222
                product.save()
                print(f"{product.title}  takes  the default weight")


