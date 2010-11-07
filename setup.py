from setuptools import setup, find_packages

setup(
    name='glamkit-convenient',
    author='Julien Phalip',
    author_email='julien@interaction.net.au',
    version='0.1',
    description='Unclassifiable, but oh so convenient, code for your glamkit and django projects',
    url='http://github.com/glamkit/glamkit-convenient',
    packages=find_packages(),
    package_data={},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)