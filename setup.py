from setuptools import setup, find_packages

setup(
    name='DjangoJSONLinesGitBackend',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django database backend that uses JSONLines and Git to store data',
    url='https://github.com/youen/DjangoJSONLinesGitBackend',
    author='Youen Péron',
    author_email='youen.peron@gmail.com',
    install_requires=[
        'Django>=4.1',
        'pandas>=1.5',
        'GitPython>=3.1.3'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
