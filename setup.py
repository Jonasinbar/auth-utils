from setuptools import setup, find_packages

setup(
    name='auth_utils',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'grpcio',
        'protobuf',
        'cryptography',
        'PyJWT',
        'requests',
    ],
)
