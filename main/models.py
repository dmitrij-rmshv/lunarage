from django.db import models


class BirthDay(models.Model):
    birthday = models.DateTimeField()

    def __str__(self):
        return self.birthday.strftime("%Y-%m-%d")


class IP(models.Model):
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, primary_key=True)
    count = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.ip


class BDayIP(models.Model):
    birth_day = models.ForeignKey(BirthDay, on_delete=models.CASCADE)
    ip = models.ForeignKey(IP, on_delete=models.CASCADE, related_name='birth_days', related_query_name='birthday')
    requested_at = models.DateTimeField(auto_now_add=True, verbose_name='Запрошено_в_')
