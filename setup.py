from setuptools import setup, find_packages

setup(
    name='aiomysql_server',
    version='0.1.0',
    description='Custom aiomysql',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ái Lị Hy Nhã',
    author_email='elysiabot301127@gmail.com',

    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
