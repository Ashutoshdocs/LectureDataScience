# Import modules from the shop package.

from shop import products
from shop import billing

print("Package Demo")

items = products.list_products()
print("Products:", items)

total = billing.calculate_total(500, 3)
print("Total bill:", total)
