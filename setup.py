from setuptools import find_packages, setup


def parse_requirements(filename):
    """ parse requirements from requirements.txt file."""
    packages = []
    with open(filename, encoding='utf-8') as file:
        for line in file:
            line.strip()
            if not line.startswith('#') and not line.startswith('-r'):
                packages.append(line)
    return packages


install_requires = parse_requirements('requirements.txt')
extras_require = {
    'dev': parse_requirements('requirements-dev.txt')
}


setup(
    name="web3-gateway",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "web3>=6.0.0",
        "pydantic>=1.8.0",
        "requests>=2.26.0",
        "python-multipart",  # for FastAPI forms
    ],
    entry_points={
        "console_scripts": [
            "web3gateway=web3gateway.main:main",
        ],
    },
    author="daboooooo",
    author_email="horsen666@gmail.com",
    description="A high-performance Web3 RESTful gateway service",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/daboooooo/web3gateway.git",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio',
        'pytest-cov',
        'pytest-mock',
    ],
    extras_require=extras_require,
)
