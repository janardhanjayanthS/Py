from csv import DictReader
from typing import Any, Iterator, Optional
from pydantic import ValidationError

from .model import ProductFactory, BaseProduct
from .log import logger, construct_log_message
from .utility import ProductDetails, convert_to_bool
from .config import ConfigLoader
from .file_manager import check_low_stock_or_print_details

product_factory: ProductFactory = ProductFactory()


class Inventory:
    def __init__(self) -> None:
        self.products: list = []
        self.config: ConfigLoader = ConfigLoader()
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

                    self.products.append(self.__get_product_from_dict(row=row))
        except FileNotFoundError as e:
            print(f"File not found {e}")
            return

    def __get_product_from_dict(self, row: dict[str, Any]) -> BaseProduct:
        """
        returns product object from a row dictionary

        Args:
            row: Dictionary representing inventory row detail

        Returns:
            BaseProduct: product object
        """
        return self.product_factory.create_product(
            product_details=ProductDetails(
                id=row["row_id"],
                name=row["row_name"],
                type=row["type"],
                quantity=row["quantity"],
                price=row["price"],
                days_to_expire=row["days_to_expire"],
                is_vegetarian=convert_to_bool(data=row["is_vegetarian"]),
                warranty_period_in_years=row["warranty_period_in_years"],
            )
        )

    def add_product(self, product_details: ProductDetails) -> None:
        """
        add a new product to products list

        Args:
            product_details: contains product's details
        """
        ...
        product = self.product_factory.create_product(product_details=product_details)
        self.products.append(product)

    def update_stock(self, product_id: str, new_quantity: int) -> None: 
        """
        Updates quanitiy of a specific product

        Args:
            product_id: id of the product to update
            new_quantity: current number for stock
        """
        for product in self.products:
            if product.product_id == product_id:
                print(f'Product details before update: {product}')
                product.quantity = new_quantity
                print(f'Product details after update: {product}')
                return
        print(f'Cannot find product with {product_id} id')
    

    def generate_low_quantity_report(self) -> None:
        """
        Generates a low stock report if quantity of stock is lesser
        than low_stock_threshold
        """ 
        for product in self.products:
            self.__validate_product(product=product)
            

    def __validate_product(self, product: BaseProduct) -> None:
        """
        validates a product, if its valid then displays its details, 
        if it has any validation error (raised by Pydantic) then logs it to errors.log
        if the prodcut is valid and has low stock then adds it to low_stock_report.txt
        Args:
            product: product object 
        """
        try:
            product_factory.create_product(
                product_details=ProductDetails(
                    id=product.product_id,
                    name=product.product_name,
                    type=product.type,
                    quantity=product.quantity,
                    price=product.price,
                    days_to_expire=product.days_to_expire, # type: ignore
                    is_vegetarian=product.is_vegetarian, # type: ignore
                    warranty_period_in_years=product.warranty_period_in_years, # type: ignore
                )
            )
            check_low_stock_or_print_details(product=product)
        except ValidationError as e:
            print(
                f"Requested product {product.product_name} has a validation error: {e.errors()[0]['msg']}"
            )
            logger.error(
                construct_log_message(
                    message=e.errors()[0]["msg"],
                    product=product,
                )
            )