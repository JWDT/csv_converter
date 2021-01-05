import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv_converter",
    version="0.0.6",
    author="JWDT",
    author_email="pypi@zephyr.ltd.uk",
    description="Tool to convert CSV files based on JSON config.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JWDT/csv_converter",
    packages='.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
