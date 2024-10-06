from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Policy, PolicyStateHistory


@receiver(pre_save, sender=Policy)
def log_policy_state_change(sender, instance, **kwargs):
    """
    Log the state change of a policy.
    """
    if instance.pk:
        old_policy = Policy.objects.get(pk=instance.pk)
        if old_policy.state != instance.state:
            PolicyStateHistory.objects.create(policy=instance, state=instance.state)
