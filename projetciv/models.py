from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class Lieu(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=225)
    latitude = models.CharField(max_length=225)
    longitude = models.CharField(max_length=225)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    
class Secteur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=225)
    description = models.TextField()
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
        
class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminManager"), (2, "PlateformManager"), (3, "Manager"))
    user_type = models.CharField(default=2, choices=user_type_data, max_length=25)


class AdminManagers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    

class PlateformManagers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    date_de_naissance = models.DateTimeField(auto_now_add=True)
    lieu_de_naissance = models.CharField(max_length=225)
    genre = models.CharField(max_length=50)
    photo_de_profil = models.FileField()
    adresse = models.TextField()
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    

class Managers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    date_de_naissance = models.DateTimeField(auto_now_add=True)
    lieu_de_naissance = models.CharField(max_length=225)
    genre = models.CharField(max_length=50)
    photo_de_profil = models.FileField()
    adresse = models.TextField()
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Chefdedepartement(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=225)
    prenom = models.CharField(max_length=225)
    date_de_naissance = models.DateTimeField()
    lieu_de_naissance = models.CharField(max_length=225)
    genre = models.CharField(max_length=50)
    photo_de_profil = models.FileField()
    adresse = models.CharField(max_length=225)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    
class Departement(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=225)
    description = models.TextField()
    chef_de_departement = models.ForeignKey(Chefdedepartement, on_delete=models.CASCADE)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    
class ProjectManager (models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=225)
    prenom = models.CharField(max_length=225)
    date_de_naissance = models.DateTimeField()
    lieu_de_naissance = models.CharField(max_length=225)
    genre = models.CharField(max_length=50)
    photo_de_profil = models.FileField()
    adresse = models.CharField(max_length=225)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    objects = models.Manager()
   

class Project(models.Model):
    STATUS = (
    (0,"En cours"),
    (1,"Achevé")) 
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=225)
    description = models.TextField()
    partenaire = models.CharField(max_length=225)
    financement = models.CharField(max_length=225)
    secteur = models.ForeignKey(Secteur, on_delete=models.CASCADE)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
    chef_de_projet = models.ForeignKey(ProjectManager, on_delete=models.CASCADE)
    date_de_debut = models.DateTimeField(auto_now_add=True)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    objects = models.Manager()
    

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminManagers.objects.create(admin=instance)
        if instance.user_type == 2:
            PlateformManagers.objects.create(admin=instance, lieu_de_naissance="", genre="", photo_de_profil="", adresse="")
        if instance.user_type == 3:
            Managers.objects.create(admin=instance, lieu_de_naissance="", genre="", photo_de_profil="", adresse="")
    
    
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminManagers.save()
    if instance.user_type == 2:
        instance.plateformManagers.save()
    if instance.user_type == 3:
        instance.managers.save()