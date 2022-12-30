from setuptools import setup

description = "asyncio-based Python wrapper for the Rocket.Chat Realtime API."
with open("README.md", "r") as fin:
    long_description = fin.read()

setup(
    name="rocketchat-async",
    version="0.1.0",
    description=description,
    long_description=long_description,
    author="Hynek Urban",
    author_email="hynek.urban@gmail.com",
    packages=["rocketchat_async"],
    package_dir={"rocketchat_async": "rocketchat_async"},
    install_requires=["websockets==10.4"],
)
