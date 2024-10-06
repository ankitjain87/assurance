from django.db import models
from django.utils import timezone

# Create your models here.

STATE_CHOICES = [
    ("new", "New"),
    ("quoted", "Quoted"),
    ("accepted", "Accepted"),
    ("bound", "Bound"),
    ("active", "Active"),
    ("declined", "Declined"),
    ("expired", "Expired"),
]


class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.dob}"


class Policy(models.Model):
    POLICY_TYPES = [
        ("personal_accident", "Personal Accident"),
        ("health", "Health Insurance"),
        ("life", "Life Insurance"),
        ("home", "Home Insurance"),
        ("travel", "Travel Insurance"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    policy_type = models.CharField(max_length=50, choices=POLICY_TYPES)
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cover = models.DecimalField(max_digits=12, decimal_places=2, default=200000)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="new")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quote for {self.customer} - {self.policy_type} ({self.state})"


class PolicyStateHistory(models.Model):
    policy = models.ForeignKey(
        "Policy", on_delete=models.CASCADE, related_name="state_history"
    )
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Policy {self.policy.id} changed to {self.state} on {self.updated_at}"
