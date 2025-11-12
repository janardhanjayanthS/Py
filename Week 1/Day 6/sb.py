from model import Product


print(Product, type(Product))
p = Product(
    product_id='01A1',
    product_name='Fan',
    price=900.00,
    quantity=11
)
print(p, type(p), p.__dict__)