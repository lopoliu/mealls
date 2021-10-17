from django.db import models
import hashlib


class User(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    password = models.CharField(max_length=256)

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.name

    def set_password(self, password):
        self.password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()

    def check_password(self, password):
        if self.password == hashlib.md5(password.encode(encoding='UTF-8')).hexdigest():
            return True
