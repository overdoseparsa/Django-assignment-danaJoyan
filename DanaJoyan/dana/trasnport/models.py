from django.db import models

from dana.common.models import BaseModel
from dana.users.models import (
    Admin,
    User,
)


class Company(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    author = models.ForeignKey(
        Admin, on_delete=models.CASCADE, related_name="companies"
    )

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class Bus(BaseModel):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="buses")
    count_seats = models.IntegerField()

    author = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["name", "company"]),
        ]


class Seat(BaseModel):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    author = models.ForeignKey(Admin, on_delete=models.CASCADE)

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    gender_choice = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.MALE
    )

    def __str__(self) -> str:
        return f"{self.bus.name} - {self.seat_number}"

class Transport(BaseModel):
    name = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat = models.ManyToManyField(Seat) 
    author = models.ForeignKey(Admin, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name

