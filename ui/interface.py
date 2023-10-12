_panels = []
_lists = []
_menu_items = []


def ui_panel(obj):
    _panels.append(obj)
    return obj


def ui_list(obj):
    _lists.append(obj)
    return obj


def menu_item(obj):
    _menu_items.append(obj)
    return obj