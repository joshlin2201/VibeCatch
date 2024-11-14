from setuptools import setup, find_packages

setup(
    name="vibecatch",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyaudio==0.2.14",
        "numpy==1.26.4",
        "requests==2.31.0",
        "PyQt5==5.15.10"
    ],
    entry_points={
        "console_scripts": [
            "vibecatch=vibecatch.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
