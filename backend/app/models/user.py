from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Model):
    username = fields.CharField(max_length=255, unique=True, index=True)
    email = fields.CharField(max_length=512, default='')
    password = fields.CharField(max_length=2048, null=True, default=None)
    first_name = fields.CharField(max_length=255, default='')
    last_name = fields.CharField(max_length=255, default='')

    def set_password(self, raw_password: str):
        self.password = pwd_context.hash(raw_password)

    def check_password(self, raw_password: str):
        return pwd_context.verify(raw_password, self.password)
