from django.db import models
from django.contrib.auth.models import User


class userInfo(models.Model):
    OCCUPATION_CHOICES = [
        ("Doctor", "Doctor"),
        ("Tutor", "Tutor"),
        ("Service Provider", "Service Provider"),
        ("Logistic", "Logistic"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10)
    flat_no = models.CharField(max_length=10)
    occupation = models.CharField(max_length=50, choices=OCCUPATION_CHOICES)

    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Other(models.Model):
    other = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.other.username


class Logistic(models.Model):

    LOGISTIC_CHOICES = [
        ("Recycling Logistics", "Recycling Logistics"),
        ("Recovery Logistics", "Recovery Logistics"),
        ("Sales Logistics", "Sales Logistics"),
        ("Production Logistics", "Production Logistics"),
        ("Procurement Logistics", "Procurement Logistics"),
        ("Other", "Other"),
    ]

    logistic = models.ForeignKey(User, on_delete=models.CASCADE)
    logistic_type = models.CharField(max_length=50, choices=LOGISTIC_CHOICES)
    description = models.TextField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.logistic.username


class Service_Provider(models.Model):

    SERVICE_CHOICES = [
        ("Electrician", "Electrician"),
        ("Plumber", "Plumber"),
        ("Driver", "Driver"),
        ("Mechanic", "Mechanic"),
        ("Grocer", "Grocer"),
        ("Carpenter", "Carpenter"),
        ("Consultant", "Consultant"),
        ("Chef", "Chef"),
        ("Barber", "Barber"),
        ("Other", "Other"),
    ]

    service_provider = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    description = models.TextField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.service_provider.username


class Tutor(models.Model):

    DEGREE_CHOICES = [
        ("PHD", "Doctor of Philosophy(PHD)"),
        ("BSC", "Bachelor of Science(BSC)"),
        ("MSC", "Master of Science(MSC)"),
        ("B.COM", "Bachelor of Commerce(B.COM)"),
        ("M.COM", "Master of Commerce(M.COM)"),
        ("B.Ed", "Bachelor’s in Education(B.Ed)"),
        ("B.Tech", "Bachelor of Technology(B.Tech)"),
        ("M.Tech", "Master of Technology(M.Tech)"),
        ("Other", "Other"),
    ]

    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    degree_type = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    description = models.TextField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.tutor.username


class Doctor(models.Model):

    DEGREE_CHOICES = [
        ("MBBS", "Bachelor of Medicine, Bachelor of Surgery(MBBS)"),
        ("BDS", "Bachelor of Dental Surgery(BDS)"),
        ("BAMS", "Bachelor of Ayurvedic Medicine and Surgery(BAMS)"),
        ("BAMS", "Bachelor of Unani Medicine and Surgery(BUMS)"),
        ("BHMS", "Bachelor of Homeopathy Medicine and Surgery(BHMS)"),
        ("BYNS", "Bachelor of Yoga and Naturopathy Sciences(BYNS)"),
        (
            "B.V.Sc & AH",
            "Bachelor of Veterinary Sciences and Animal Husbandry(BVSc&AH)",
        ),
        ("MD", "Doctor of Medicine(MD)"),
        ("MS", "Master of Surgery(MS)"),
        ("DM", "Doctorate of Medicine(DM)"),
    ]

    SPECIALITIES_CHOICES = [
        ("ENT", "Ear, Nose and Throat"),
        ("GS", "General Surgery"),
        ("OP", "Ophthalmology"),
        ("OR", "Orthopaedics"),
        ("OAG", "Obstetrics and Gynaecology"),
        ("DVL", "Dermatology, Venerology and Leprosy"),
        ("AST", "Anaesthesiology"),
        ("PSY", "Psychiatry"),
        ("PTH", "Pathology"),
        ("SVD", "Skin and Venereal diseases"),
        ("PHRM", "Pharmacology"),
        ("PMR", "Physical Medicine and Rehabilitation"),
        ("PHY", "Physiology"),
        ("CRD", "Cardiology"),
        ("PDT", "Paediatrics"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Transgender", "Transgender"),
        ("Prefer Not to Say", "Prefer Not to Say"),
    ]

    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    degree_type = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    specialities_type = models.CharField(max_length=50, choices=SPECIALITIES_CHOICES)
    dob = models.CharField(max_length=10)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    bio = models.TextField(blank=True)
    description = models.TextField()

    def __str__(self):
        return self.doctor.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ("timestamp",)
