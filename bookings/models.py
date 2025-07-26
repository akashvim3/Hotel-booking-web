from django.db import models
from users.models import User
from hotels.models import Room

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    # ...add more fields as needed...

    def __str__(self):
        return f'{self.user.username} - {self.room} ({self.check_in} to {self.check_out})'

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for {self.booking} - {self.amount} ({self.status})'
