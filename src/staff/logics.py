from events.models import Event


def normalize(text):
    return "".join([c.upper() for c in text if ord(c) < 128 and c.isalnum()])


def inconsistent_events(week_no, data):
    events = [e for e in Event.objects.all() if e.week_no() == week_no]
    n_data = normalize(data)
    return [
        {"source": normalize(e.description), "target": n_data, **e.__dict__}
        for e in events
        if normalize(e.description) not in n_data
    ]


def all_inconsistent_events(data):
    events = Event.objects.all()
    n_data = normalize(data)
    return [e for e in events if normalize(e.description) not in n_data]
