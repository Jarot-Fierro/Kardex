# # users/signals.py
#
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from users.models import PerfilUser
#
#
# @receiver(post_save, sender=User)
# def crear_perfil_usuario(sender, instance, created, **kwargs):
#     if created:
#         PerfilUser.objects.create(users=instance)
