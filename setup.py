from setuptools import find_packages, setup

setup(
    name='sabimillionaire',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'waitress'
        'Flask==2.1.2',
        'Flask_Admin==1.6.0',
        'Flask_Login==0.6.1',
        'Flask_Mail==0.9.1',
        'Flask_Migrate==3.1.0',
        'Flask_Security==3.0.0',
        'Flask_SQLAlchemy==2.5.1',
        'Flask_WTF==1.0.1',
        'Jinja2==3.1.2',
        'python-decouple==3.6',
        'python-dotenv==0.20.0',
        'requests==2.28.0',
        'Werkzeug==2.1.2',
        'WTForms==3.0.1',
    ]
)