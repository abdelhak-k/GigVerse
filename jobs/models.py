from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone

# Custom User model


STATUS_CHOICES = [
        ('no-status', 'No Status'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

class User(AbstractUser):
    def __str__(self):
        return self.username

# Wallet model
class Wallet(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        self.save()

# Job model
class Job(models.Model):
    # many to one : many jobs to one owner (foregien key)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="jobs", null=False, blank=False)
    
    
    participants= models.ManyToManyField("User", related_name="jobs_done", blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    max_participants = models.IntegerField()
    price= models.FloatField()

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.username, 
            "title": self.title,
            "description": self.description,
            "date_posted": self.date_posted.strftime("%b %d %Y, %I:%M %p"),
            "max_participants": self.max_participants,
            "remaining_participants": max(0,self.max_participants - self.participants.count()),
        }


class Proof(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="proofs")
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="proofs")
    description = models.TextField()  # Field for the job proof description
    image = models.ImageField(upload_to='proofs/', blank=True, null=True)  # Field for the image of the proof
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='no-status')  # Status of the proof
    def __str__(self):
        return f"Proof for {self.job.title} by {self.owner.username}"
