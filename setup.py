import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="marketdatacollector",
    packages=setuptools.find_packages(),
    version="0.0.1",
    license="MIT",
    description="Market data collector developed to collect data in various financial areas for analysis.",
    author="I-Chi",
    author_email="ichiho1990@yahoo.com.tw",
    url="https://github.com/ichiho1990/MarketDataCollector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["fundamental", "analysis", "finance"],
)