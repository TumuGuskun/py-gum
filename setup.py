from setuptools import find_packages, setup


setup(
    name="gum",
    version="0.0.1",
    description="a Python wrapper around gum cli",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    url="git@github.com:TumuGuskun/py-gum.git",
    author="TumuGuskun",
    author_email="johntgaskin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
