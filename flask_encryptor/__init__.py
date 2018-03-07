# coding=utf-8
from Crypto.Cipher              import AES
from Crypto                     import Random
from os                         import mkdir, unlink
from os.path                    import isdir, join, getsize
from uuid                       import uuid4
from .models                    import BaseFile

import struct
import hashlib
import tempfile
import random

def convert_key(key_value):
    return hashlib.sha256(key_value).digest()

class FileEncryptor(object):
    def __init__(self, app=None, db=None):
        self.app                = app
        self.db                 = db
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # setting defaults
        app.config.setdefault('FILE_ENCRYPTOR_CHUNK_SIZE',  64 * 1024     )
        # app.config.setdefault('FILE_ENCRYPTOR_TMP_PREFIX',  'fencryptor_' )
        app.config.setdefault('FILE_ENCRYPTOR_TMP_DIR',     tempfile.mkdtemp(prefix='fencryptor_'))
        app.config.setdefault('FILE_ENCRYPTOR_DATA_DIR',    '{0}/data/uploads'.format(app.root_path))
        app.config.setdefault('FILE_ENCRYPTOR_GLOBAL_KEY',  'aAa8KxQx4Eoxwu41HTaa')

        # creating data dir
        if not isdir(app.config['FILE_ENCRYPTOR_DATA_DIR']):
            mkdir(app.config['FILE_ENCRYPTOR_DATA_DIR'])

    def upload_encrypt(self, u_file, user):
        # attributes validation
        if not hasattr(user, 'token'):
            raise Exception('User class has no attribute `token`.')
        elif not hasattr(user, 'uploaded_files'):
            raise Exception('User class has no attribute `uploaded_files`.')

        # checking that token has been generated
        if user.token is None:
            user.create_token(uuid4().hex)
            self.db.session.commit()

        # global encryptor initialization
        global_iv        = Random.new().read(AES.block_size)
        global_encryptor = AES.new(convert_key(self.app.config['FILE_ENCRYPTOR_GLOBAL_KEY']), AES.MODE_CFB, global_iv)

        # saving unencrypted file
        u_file.save(join(self.app.config['FILE_ENCRYPTOR_DATA_DIR'], u_file.filename))
        in_filename     = '{0}/{1}'.format(self.app.config['FILE_ENCRYPTOR_DATA_DIR'], u_file.filename)
        out_filename    = '{0}/{1}'.format(self.app.config['FILE_ENCRYPTOR_DATA_DIR'],
                                           uuid4().hex)
        filesize        = getsize(in_filename)

        # encrypting file content with user token
        iv              = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        stream_encyptor = AES.new(convert_key(user.token.value), AES.MODE_CBC, iv)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(self.app.config['FILE_ENCRYPTOR_CHUNK_SIZE'])
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(stream_encyptor.encrypt(chunk))

        # removing original file
        unlink(in_filename)

        return {
            'filename': out_filename.split('/')[-1],
            'realname': global_iv + global_encryptor.encrypt(in_filename.split('/')[-1])
        }

    def decrypt_file(self, uploaded_file, user):
        # decrypting realname
        iv               = uploaded_file.realname[:AES.block_size]
        global_decryptor = AES.new(convert_key(self.app.config['FILE_ENCRYPTOR_GLOBAL_KEY']), AES.MODE_CFB, iv)
        realname_dec     = global_decryptor.decrypt(uploaded_file.realname[AES.block_size:])

        # decrypting file content
        in_filename      = '{0}/{1}'.format(uploaded_file.path, uploaded_file.filename)
        out_filename     = '{0}/{1}'.format(self.app.config['FILE_ENCRYPTOR_TMP_DIR'], realname_dec)
        key              = convert_key(user.token.value)

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(self.app.config['FILE_ENCRYPTOR_CHUNK_SIZE'])
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)

        return realname_dec
