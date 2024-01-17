from setuptools import setup, find_packages

setup(
    name='logngo',
    version='0.7',
    packages=find_packages(),
    description='Log chains for webserver',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cong Hoang Tran',
    author_email='trconghoangg@gmail.com',
    url='https://github.com/hoangtc125/logtc',
    install_requires=[
        'requests',
        'python-socketio',
        'websocket-client',
        'contextvars'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
