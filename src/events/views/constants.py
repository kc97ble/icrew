from events.models.constants import TimeStatus, EventStatus, RegStatus, MessageLevel

TIME_STATUS_CLASS = {
    TimeStatus.ON_TIME.value: "badge badge-light",
    TimeStatus.DELAYED.value: "badge badge-warning",
    TimeStatus.CANCELED.value: "badge badge-danger",
}

STATUS_CLASS = {
    EventStatus.CLOSED_NONE.value: "badge badge-secondary",
    EventStatus.CLOSED_UNOPENED.value: "badge badge-secondary",
    EventStatus.CLOSED_EVENT_CANCELLED.value: "badge badge-danger",
    EventStatus.CLOSED_REG_CLOSED.value: "badge badge-secondary",
    EventStatus.OPEN_REG_AND_WAIT.value: "badge badge-info",
    EventStatus.OPEN_FCFS.value: "badge badge-warning",
    EventStatus.CLOSED_UNFULFILLED.value: "badge badge-secondary",
    EventStatus.CLOSED_DEMAND_FULFILLED.value: "badge badge-dark",
}

REG_STATUS_CLASS = {
    RegStatus.NONE.value: "badge badge-light",
    RegStatus.PENDING.value: "badge badge-info",
    RegStatus.ACCEPTED.value: "badge badge-success",
    RegStatus.REJECTED.value: "badge badge-danger",
}


DECORATION_REG_STATUS = {
    RegStatus.NONE.value: {
        "reg_status_label": "Unregistered",
        "reg_status_class": "badge badge-light",
    },
    RegStatus.PENDING.value: {
        "reg_status_label": "Registration pending",
        "reg_status_class": "badge badge-info",
        "card_header": {
            "icon": "fa fa-circle",
            "label": "Pending",
            "class": "bg-info text-white",
        },
        "card_border": {"class": "border-info"},
    },
    RegStatus.ACCEPTED.value: {
        "reg_status_label": "Registration accepted",
        "reg_status_class": "badge badge-success",
        "card_header": {
            "icon": "fa fa-check",
            "label": "Allocated",
            "class": "bg-success text-white",
        },
        "card_border": {"class": "border-success"},
    },
    RegStatus.REJECTED.value: {
        "reg_status_label": "Registration rejected",
        "reg_status_class": "badge badge-danger",
        "card_header": {
            "icon": "fa fa-times",
            "label": "Rejected",
            "class": "bg-danger text-white",
        },
        "card_border": {"class": "border-danger"},
    },
}

DECORATION_TAG_LEVEL = {
    MessageLevel.INFO.value: {"class": "badge badge-light"},
    MessageLevel.WARNING.value: {"class": "badge badge-warning"},
    MessageLevel.ERROR.value: {"class": "badge badge-danger"},
    MessageLevel.FATAL.value: {"class": "badge badge-danger"},
}
