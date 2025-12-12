from setuptools import setup

requires = [
    'pyramid',
    'waitress',
    'SQLAlchemy',
    'psycopg2-binary',
    'python-dotenv',
    'requests',
    'google-generativeai'
]

setup(
    name='review_analyzer',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = app:main',
        ],
    },
)
