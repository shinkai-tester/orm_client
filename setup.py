from distutils.core import setup

REQUIRES = [
    'structlog',
    'allure-pytest',
    'sqlalchemy',
    'records'
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
