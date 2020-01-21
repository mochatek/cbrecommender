from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()
    
setup(
    name = 'cbrecommender',
    version = '1.0',
    author = 'Akash S Panickar',
    author_email = 'akashsabu@ymail.com',
    description = 'Library for implementing Content-Based Recommendation System',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'http://github.com/mochatek/cbrecommender',
    license = 'MIT',
    install_requires = ['pandas','numpy'],
    packages = ['cbrecommender'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe = False
    )
