from setuptools import setup

setup(
    name='fixgres',
    version='0.2.0',
    author='Christopher Brown',
    author_email='io@henrian.com',
    packages=['fixgres'],
    include_package_data=False,
    zip_safe=True,
    install_requires=[
        'psycopg2',
        'sqlalchemy',
        'python-dateutil',
    ],
    entry_points={
        'console_scripts': [
            'fixgres_config = fixgres.config:main',
            'fixgres_read_var_mail = fixgres.mail:main',
        ]
    },
)
