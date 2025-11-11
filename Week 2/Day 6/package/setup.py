from setuptools import find_packages, setup

setup(
    name="inventory_manager",
    version="0.0.3",
    description="Package to interact with inventory csv data",
    long_description="Package to manipulate with inventory csv data that uses generators to read from csv file. Can manipulate multiple type - Regular, Food, Electronic - data.",
    package_dir={"": "inventory_manager"},
    packages=find_packages(where="inventory_manager"),
    author="janardhanjayanthS",
    install_requires=["pydantic>=2.12"],
    python_requires=">=3.10",
)
