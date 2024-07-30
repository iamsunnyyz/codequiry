from setuptools import setup, find_packages

setup(
    name="codequiry",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests_toolbelt',
        'ConfigParser',
        'python-socketio'
    ],
    description="Python SDK for Codequiry API",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url="https://codequiry.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
