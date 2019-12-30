from django.utils import timezone
from django.contrib.auth.models import User

from .exceptions import LogicError
from .models import Event, Registration

def add_registration(user, event):
    now = timezone.now()
    print('add_registration', user, event, now)

    if now < event.register_start_at:
        raise LogicError("Registration has not started yet.")
    if now > event.register_ended_at:
        raise LogicError("Registration has ended.")
    if Registration.objects.filter(user=user, event=event).count() > 0:
        raise LogicError("Registration sent already.")

    num_confirmed = Registration.objects.filter(
        event=event,
        status=Registration.RegistrationStatus.ACCEPTED,
    ).count()
    num_needed = 1 # TODO

    if now >= event.result_release_at:
        if num_confirmed >= num_needed:
            raise LogicError("No more slots.")
        else:
            status = Registration.RegistrationStatus.ACCEPTED
    else:
        status = RegistrationStatus.RegistrationStatus.PENDING

    Registration.objects.create(
        user=user,
        event=event,
        status=status
    )
