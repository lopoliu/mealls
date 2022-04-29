from django.db import models
from mealls.common.base_model import BaseModel
from mealls.common.tools import to_md5


class User(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    type = models.IntegerField(default=1)
    address = models.CharField(max_length=256, default=None, blank=True, null=True)

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.name + " | " + self.email

    def check_password(self, password):
        if self.password == to_md5(password):
            return True
