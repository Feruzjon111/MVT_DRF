from django.db import models
from django.conf import settings

class Transaction(models.Model):
    TYPE_CHOICES = (
        ('IN', 'Kirim'),
        ('OUT', 'Chiqim'),
    )

    PUL_TURLARI = (
        ('naqd', 'Naqd'),
        ('karta', 'Karta'),
        ('valyuta', 'Valyuta'),
    )

    KATEGORIYALAR = (
        ('oylik', 'Oylik ish haqi'),
        ('avans', 'Avans'),
        ('kunlik', 'Kunlik ish'),
        ('sovga', 'Sovg‘a'),
        ('xizmat', 'Xizmat haqi'),
        ('boshqa_kirim', 'Boshqa kirim'),

        ('ovqat', 'Ovqat'),
        ('yoqilg‘i', 'Yoqilg‘i'),
        ('ijara', 'Ijara haqi'),
        ('internet', 'Internet/xizmatlar'),
        ('sotib_olish', 'Sotib olish'),
        ('boshqa_chiqim', 'Boshqa chiqim'),
    )

    karta_nomi = models.CharField(max_length=100, blank=True, null=True)
    valyuta_turi = models.CharField(max_length=10, blank=True, null=True, choices=[
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RUB', 'RUB'),
    ])

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=KATEGORIYALAR)
    pul_turi = models.CharField(max_length=10, choices=PUL_TURLARI, default='naqd')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} {self.get_pul_turi_display()} - {self.category}"
