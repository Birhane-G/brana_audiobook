from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in brana_audiobook/__init__.py
from brana_audiobook import __version__ as version

setup(
	name="brana_audiobook",
	version=version,
	description="Brana AudioBook Backend development",
	author="Birhane Gebrial",
	author_email="Birhanegebrial1@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
