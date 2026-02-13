from inventory_manager.inventory_manager import Inventory

inv = Inventory()
inv.load_from_csv(filepath="new_inventory.csv")

print(inv.products)
inv.generate_low_quantity_report()

inv.update_stock(product_id="P196", new_quantity=200)

inv.add_product({
    'product_id': 'P9933',
    'product_name': 'Milton Themosteel bottle',
    'quantity': 300,
    'price': 750.00,
    'type': 'regular',
    'days_to_expire': '',
    'is_vegetarian': '',
    'warranty_period_in_years': 8
})

inv.add_product({
    'product_id': 'P9933',
    'product_name': 'Milton Themosteel bottle',
    'quantity': 300,
    'price': 750.00,
    'type': 'regular',
    'days_to_expire': '',
    'is_vegetarian': '',
    'warranty_period_in_years': 8
})

inv.add_product({
    'product_id': 'P70983',
    'product_name': 'Unibic cashew badam cookies',
    'quantity': 10_000,
    'price': 5.00,
    'type': 'food',
    'days_to_expire': '90',
    'is_vegetarian': 'yes',
    'warranty_period_in_years': ''
})

print(inv.products)
