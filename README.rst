Flask-Encryptor
----------------

Introduction
----------------
This Flask extension attempts to ease users' uploaded file encryption.
* PyCrypto is used to encrypt/decrypt files
* Automatically rename and associate encrypted files
* Can be used to generate a download link and immediately delete the decrypted file

For now, for database side, it only support SQLAlchemy.

Requirements and installation
------------------------------

In order to work, flask-encryptor is based on these following modules:
* flask
* flask-sqlalchemy
* pycrypto

To install Flask-Encryptor, simply:

    $ pip install flask-encryptor

Or alternatively, you can download the repository and install manually by running:

    $ git clone https://github.com/Querdos/Flask-Encryptor.git
    cd Flask-Encryptor
    python setup.py install
