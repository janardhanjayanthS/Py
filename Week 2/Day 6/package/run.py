from inventory_manager.inventory_manager import Inventory

inv = Inventory()
inv.load_from_csv(filepath="new_inventory.csv")

print(inv.products)
