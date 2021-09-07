import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqaure-game",
    version="0.0.1",
    author="Tristan Laanait",
    author_email="tristanlaanait@gmail.com",
    description="a square game based on pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tristanML/sqaure-game",
    project_urls={
        "Bug Tracker": "https://github.com/tristanML/sqaure-game/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
