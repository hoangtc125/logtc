from setuptools import setup, find_packages

setup(
    name='logtc',
    version='0.1',
    packages=find_packages(),
    description='Log chains for webserver',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cong Hoang Tran',
    author_email='trconghoangg@gmail.com',
    url='facebook.com/hoang2k1111',
    install_requires=[
        'requests',
        'python-socketio',
        'websocket-client'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
