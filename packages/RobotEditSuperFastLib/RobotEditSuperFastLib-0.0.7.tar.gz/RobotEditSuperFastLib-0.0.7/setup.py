import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RobotEditSuperFastLib",
    version="0.0.7",
    py_modules=["RobotEditSuperFastLib"],
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.baidu.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# python setup.py sdist upload
# pip install --upgrade RobotEditSuperFastLib -i https://pypi.org/simple
