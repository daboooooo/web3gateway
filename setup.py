from setuptools import setup


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
    tests_require=[
        'pytest',
        'pytest-asyncio',
        'pytest-cov',
        'pytest-mock',
    ],
    install_requires=install_requires,
    extras_require=extras_require,
    url="https://github.com/daboooooo/web3gateway",
)