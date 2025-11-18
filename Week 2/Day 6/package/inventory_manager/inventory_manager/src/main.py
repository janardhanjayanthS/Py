from csv import DictReader
from typing import Any, Iterator, Optional
from pydantic import ValidationError

from .model import ProductFactory, BaseProduct
from .log import log_error, construct_log_message
from .utility import ProductDetails, convert_to_bool
from .file_manager import check_low_stock_or_print_details


class Inventory:
    def __init__(self) -> None:
        self.products: list = []
        self.product_factory: ProductFactory = ProductFactory()

    def load_from_csv(self, filepath: str) -> Optional[Iterator[dict[str, Any]]]:
        """
        loads data from inventory csv,
        converts it into product object and adds it to products list

        Args:
            filepath : path to inventory csv file
        """
        try:
            with open(filepath, "r") as csv_file:
                reader = DictReader(csv_file)
                for row in reader:
                    self.add_product(row)
        except FileNotFoundError as e:
            print(f"File not found {e}")
            return

    def __get_valid_product_or_log_error(
        self, row: dict[str, Any]
    ) -> BaseProduct | None:
        """
        returns product object from a row dictionary

        Args:
            row: Dictionary representing inventory row detail

        Returns:
            BaseProduct: product object
        """
        try:
            return self.product_factory.create_product(
                product_details=ProductDetails(
                    id=row["product_id"],
                    name=row["product_name"],
                    type=row["type"],
                    quantity=row["quantity"],
                    price=row["price"],
                    days_to_expire=row["days_to_expire"],
                    is_vegetarian=convert_to_bool(data=row["is_vegetarian"]),
                    warranty_period_in_years=row["warranty_period_in_years"],
                )
            )
        except ValidationError as e:
            print(
                f"product name: {row['product_name']} has a validation error: {e.errors()[0]['msg']}"
            )
            log_error(
                construct_log_message(
                    message=e.errors()[0]["msg"],
                    product_dict=row,
                )
            )

    def add_product(self, product_info: dict[str, Any]) -> None:
        """
        add a new product to products list if product_id does not already exist

        Args:
            product_info: dictionary containing details about the product
            format: keys -> same as columns in inventory csv
                    values: strings overall.
                            quantity, days_to_expire, warranty_period_in_years: int
                            price: float
        """
        self.__check_if_product_exists(product_id=product_info["product_id"])
        product = self.__get_valid_product_or_log_error(row=product_info)
        if product:
            self.products.append(product)

    def __check_if_product_exists(self, product_id) -> None:
        """
        Checks if product with an id already exists in the list of products
        if so then prints its info and returns

        Args:
            product_id: id of the product to check
        """
        for product in self.products:
            if product.product_id == product_id:
                print(f"Product with: {product_id} already exists: {product}")
                return

    def update_stock(self, product_id: str, new_quantity: int) -> None:
        """
        Updates quanitiy of a specific product

        Args:
            product_id: id of the product to update
            new_quantity: current number for stock
        """
        for product in self.products:
            if product.product_id == product_id:
                print(f"Product details before update: {product}")
                product.quantity = new_quantity
                print(f"Product details after update: {product}")
                return
        print(f"Cannot find product with {product_id} id")

    def generate_low_quantity_report(self) -> None:
        """
        Generates a low stock report if quantity of stock is lesser
        than low_stock_threshold
        """
        for product in self.products:
            check_low_stock_or_print_details(product=product)
