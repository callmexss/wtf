from setuptools import setup


setup(
        name='wtf',
        version='0.1',
        py_modules=['wtf'],
        install_requires=[
            'click',
            'requests',
            'bs4',
            'lxml',
            'prettytable',
            ],
        entry_points='''
        [console_scripts]
        wtf=wtf:wtf
        ''',
        )
