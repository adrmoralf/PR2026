from glob import glob

from setuptools import setup

package_name = "camarero"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="adrmoralf",
    description="Lógica del robot camarero: pedidos por mesa y navegación con Nav2.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={"console_scripts": ["camarero = camarero.camarero_node:main"]},
)
