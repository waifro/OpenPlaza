import shutil
import os

from .models import Product
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify

#elimina tutti i file ricorrenti al prodotto durante l'eliminazione del prodotto
@receiver(post_delete, sender=Product)
def delete_product_folder(sender, instance, **kwargs):
    username = slugify(instance.seller.username)
    product_name = slugify(instance.name)

    folder_path = os.path.join('media', 'upload_image', username, product_name)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

# elimina tutti i prodotti associati all'utente durante la sua eliminazione
@receiver(post_delete, sender=User)
def delete_user_media(sender, instance, **kwargs):
    user_folder = os.path.join(settings.MEDIA_ROOT, f'upload_image/{instance.username}')
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
