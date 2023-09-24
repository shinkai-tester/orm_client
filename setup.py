from setuptools import setup

REQUIRES = [
    'structlog>=23.1.0',
    'allure-pytest>=2.13.2',
    'sqlalchemy==1.4.46'
]

setup(
    name='orm_client',
    version='0.0.1',
    packages=['orm_client'],
    url='https://github.com/shinkai-tester/orm_client.git',
    license='MIT',
    author='Aleksandra Klimantova',
    author_email='',
    install_requires=REQUIRES,
    description='ORM client with Allure and Logger'
)
