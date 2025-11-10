from setuptools import find_packages, setup

setup(
    name="inventory_manager",
    version="0.0.1",
    description="Package to interact with inventory data",
    package_dir={"": "inventory_manager"},
    packages=find_packages(where="inventory_manager"),
    author="janardhanjayanthS",
    install_requires=["pydantic>=2.12"],
    python_requires=">=3.10"
)

