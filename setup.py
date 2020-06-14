from setuptools import setup, find_packages

url = ""
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="icon-prometheus-exporter",
    packages=find_packages(),
    # packages=["icon-prometheus-exporter"],
    version=version,
    description="exporter agent for icon blockchain",
    long_description=readme,
    include_package_data=True,
    author="Haitham Ghalwash",
    author_email="h.ghalwash@gmail.com",
    url=url,
    install_requires=[],
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
