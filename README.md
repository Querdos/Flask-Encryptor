# Flask-Encryptor

## Introduction
This Flask extension attempts to ease users' uploaded file encryption.

- PyCrypto (AES.MODE_CBC, AES.MODE_CFB) is used to encrypt/decrypt files
- Automatically rename and associate encrypted files
- Can be used to generate a download link and immediately delete the decrypted file

For now, for database side, it only support SQLAlchemy.

## Requirements and installation

In order to work, flask-encryptor is based on these following modules:

- flask
- flask-sqlalchemy
- pycrypto

To install Flask-Encryptor, simply::

```bash
$ pip install flask-encryptor
```

Or alternatively, you can download the repository and install manually by running::

```bash
$ git clone https://github.com/Querdos/Flask-Encryptor.git
$ cd Flask-Encryptor
$ python setup.py install
```

## Usage and documentation
Let's suppose we have simple Flask application with the following structure::
```
flask_app_test
    |-- data
    |-- template
    |-- static
    config.py
    models.py
    main.py
```

This flask extension concentrate on personal users files encryption, meaning that we will cover two part of a flask application.
The user part and the file upload one. You will need to implement a user class (what attributes depend on what you need
for your application), and UploadedFile and Token classes that both inherit (respectively) from BaseFile and BaseToken::

```python
from main import db
from flask_encryptor.models import BaseFile, BaseToken

class UploadedFile(db.Model, BaseFile):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Token(db.Model, BaseToken):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user    = db.relationship('User', back_populates='token')

class User(db.Model):
    __tablename__   = 'users'
    [...]
    uploaded_files      = db.relationship('UploadedFile',   backref='users', lazy=True)
    token               = db.relationship('Token',          uselist=False, back_populates="user")
```

Let's concentrate now on the main script, main.py. The initialization is quite simple with a few constants to set if needed::
```python
from flask              import Flask
from flask_sqlalchemy   import SQLAlchemy
from flask_encryptor    import FileEncryptor

# initializating the application
app = Flask(__name__)

# database configuration
app.config['SQLALCHEMY_DATABASE_URI']           = '...'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = False

# initializing the database
db  = SQLAlchemy(app)

# FileEncryptor configuration
# (Note that values here are default one)
app.config['FILE_ENCRYPTOR_CHUNK_SIZE'] = 64 * 1024
app.config['FILE_ENCRYPTOR_TMP_DIR']    = tempfile.mkdtemp(prefix='fencryptor_')
app.config['FILE_ENCRYPTOR_DATA_DIR']   = app.root_path+'/data/uploads'
app.config['FILE_ENCRYPTOR_GLOBAL_KEY'] = 'aAa8KxQx4Eoxwu41HTaa'

# initializing the file_encryptor object
file_encryptor = FileEncryptor(app, db)
```
Details about constants :

| Constant                  | Description                                                 |
|---------------------------|-------------------------------------------------------------|
| FILE_ENCRYPTOR_CHUNK_SIZE | Chunk size that will be used for file encryption/decryption |
| FILE_ENCRYPTOR_TMP_DIR    | Temporary folder that will be used to store decrypted files |
| FILE_ENCRYPTOR_DATA_DIR   | Folder used to store encrypted file                         |
| FILE_ENCRYPTOR_GLOBAL_KEY | Global key used to encrypt file informations                |

For this example, we are supposing to have three routes::
```python
    @app.route('/', methods=['GET', 'POST'])
    def index_action():
        # something
        return render_template('index.html'), 200

    @app.route('/upload/<upload_filename>', methods=['GET', 'POST'])
    def uploaded_file_action(upload_filename):
        # something
        return [...], 200
```