from setuptools import find_packages, setup

package_name = "americanobot"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="kiwi",
    maintainer_email="dlacksdn352@gmail.com",
    description="ROKEYC B4 COBOT1 PACAKGE",
    license="Apache 2.0 License",
    entry_points={
        "console_scripts": [
            "americano_bot=rokey.basic.americano_bot:main",
        ],
    },
)
