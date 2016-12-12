#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from pyquery import PyQuery
import telegram
from repository import find_user_by_user_id, check_user_permission


def get_who():

    while True:
        try:
            url = 'http://sugus.eii.us.es/en_sugus.html'
            #html = AssertionErrorurlopen(url).read()
            html = urlopen(url).read()
            pq = PyQuery(html)
            break
        except:
            raise

    ul = pq('ul.usuarios > li')
    who = [w.text() for w in ul.items() if w.text() != "Parece que no hay nadie."]

    return who


def check_type_and_text_start(aText = None, aUName = None, cText = None, aType = None, cType = None, cUId = None, perm_required=None):
    # Si perm_required es None y cUId no es None entonces se busca que el usuario esté en cualquier grupo

    result = True

    if cType is not None:
        result = aType == cType
    if cUId is not None:
        if perm_required is None:  # Comprobar solo usuario y permiso
            result = result and find_user_by_user_id(cUId)
        else:  # Comprobar usuario y permiso
            result = result and check_user_permission(cUId, perm_required)
    if cText is not None:
        result = result and aText.startswith(cText)

    return result

def show_list(header, contains, positions = None):

    result = [header + "\n"]

    if contains:
        if positions:
            for a in contains:
                a_ordered = [a[i] for i in positions]
                result.append("{} {}\n".format(telegram.Emoji.SMALL_BLUE_DIAMOND," ".join(a_ordered)))
        else:
            rows = ["{} {}\n".format(telegram.Emoji.SMALL_BLUE_DIAMOND ," ".join(a)) for a in contains]
            result += rows

    return "".join(result)
