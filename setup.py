from setuptools import setup

description = "asyncio-based Python wrapper for the Rocket.Chat Realtime API."
with open("README.md", "r") as fin:
    long_description = fin.read()

setup(
    name="rocketchat-async",
    version="4.2.0",
    description=description,
    long_description=long_description,
    url="https://github.com/hynek-urban/rocketchat-async",
    license="MIT",
    author="Hynek Urban",
    author_email="hynek.urban@gmail.com",
    packages=["rocketchat_async"],
    package_dir={"rocketchat_async": "rocketchat_async"},
    python_requires=">=3.7",
    install_requires=["websockets==10.4", "dacite==1.8.1"],
)
