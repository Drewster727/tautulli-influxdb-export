import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tautulli-influxdb-export",
    version="0.0.1",
    author="Drew",
    author_email="drewm727@hotmail.com",
    description="Export Tautulli (formerly PlexPy) stats to InfluxDB ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drewster727/tautulli-influxdb-export",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'influxdb'],
    scripts=['plexpy_influxdb_export.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
