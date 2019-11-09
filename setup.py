import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pocket-mongo",
    version="0.0.2",
    author="Bruno Gonçalves dos Santos",
    author_email="brunogoncalves.santos@gmail.com",
    description="An easy-to-use and quick setup interface for MongoDB.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gssbruno/pocket-mongo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
