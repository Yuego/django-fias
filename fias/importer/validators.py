# coding: utf-8
from __future__ import unicode_literals, absolute_import


__all__ = ['validators']


def socr_base_validator(item, **kwargs):
    return item.scname and item.socrname


def common_validator(item, today, **kwargs):
    return item.startdate < today < item.enddate


def addrobj_validator(item, today, **kwargs):
    return (
        not item.nextid and
        item.actstatus and
        common_validator(item, today=today, **kwargs)
    )


def room_validator(item, today, **kwargs):
    return (
        not item.nextid and
        common_validator(item, today=today, **kwargs)
    )


def stead_validator(item, today, **kwargs):
    return (
        not item.nextid and
        common_validator(item, today=today, **kwargs)
    )

validators = {
    'socrbase': socr_base_validator,

    'addrobj': addrobj_validator,
    'house': common_validator,
    'houseint': common_validator,
    'landmark': common_validator,
    'room': room_validator,
    'stead': stead_validator,
}
