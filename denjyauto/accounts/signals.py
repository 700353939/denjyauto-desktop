from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from denjyauto.accounts.models import CustomUser
from denjyauto.clients.models import Client

@receiver(post_save, sender=Client)
def create_user_for_client(sender, instance, created, **kwargs):

        if instance.points >= 10 and instance.user is None:
            user = CustomUser.objects.create_user(
                username=instance.username or f'{instance.name[:5].lower()}{instance.pk}',
                email=instance.email or "default@email.com",
                password="defaultpassword123"
            )
            user.is_client = True
            user.save()

            clients_group, created = Group.objects.get_or_create(name='Clients')

            user.groups.add(clients_group)

            Client.objects.filter(pk=instance.pk).update(user=user, username=user.username)
