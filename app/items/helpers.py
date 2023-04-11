import os
from flask import current_app


def get_previous_next_item(item):
    offer = item.offer_name
    for lsn in offer.items:
        if lsn.title == item.title:
            index = offer.items.index(lsn)
            previous_item = offer.items[index - 1] if index > 0 else None
            next_item = (
                offer.items[index + 1] if index < len(offer.items) - 1 else None
            )
            break
    return previous_item, next_item


def delete_picture(picture_name, path):
    picture_path = os.path.join(current_app.root_path, path, picture_name)
    try:
        os.remove(picture_path)
    except:
        pass
