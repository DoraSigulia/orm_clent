from setuptools import setup

REQUIRES = [
    'sqlalchemy',
    'structlog',
    'allure-pytest'
]

setup(
    name='orm_client',
    version='0.0.1',
    packages=['orm_client'],
    url='https://github.com/DoraSigulia/orm_clent.git',
    license='MIT',
    author='Daria Sigulya',
    author_email='',
    install_requires=REQUIRES,
    description='orm client'
)
