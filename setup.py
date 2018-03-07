"""
Flask-Encryptor
-------------

This Flask extension attempts to ease users' uploaded file encryption.
    - PyCrypto is used to encrypt/decrypt files
    - Automatically rename and associate encrypted files
    - Can be used to generate a download link and immediately delete the decrypted file
"""
from setuptools import setup


setup(
    name                    = 'Flask-Encryptor',
    version                 = '1.0',
    url                     = 'https://github.com/Querdos/Flask-Encryptor',
    license                 = 'BSD',
    author                  = 'Hamza ESSAYEGH',
    author_email            = 'hamza.essayegh@protonmail.com',
    description             = 'Flask extension helping encrypting users personal files',
    long_description        = __doc__,
    py_modules              = ['flask_encryptor'],
    zip_safe                = False,
    include_package_data    = True,
    platforms               ='any',
    install_requires=[
        'flask',
        'pycrypto'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
