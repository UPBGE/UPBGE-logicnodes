from bpy.types import PropertyGroup
import bpy


_properties = []


def propgroup(obj: PropertyGroup) -> PropertyGroup:
    _properties.append(obj)
    return obj


def get_global_category():
    scene = bpy.context.scene
    return (
        scene.nl_global_categories[0]
        if
        scene.nl_global_cat_selected > len(scene.nl_global_categories) - 1
        else
        scene.nl_global_categories[scene.nl_global_cat_selected]
    )


def get_global_value():
    cat = get_global_category()
    if len(cat.content) < 1:
        return None
    return (
        cat.content[0]
        if
        cat.selected > len(cat.content) - 1
        else
        cat.content[cat.selected]
    )


def check_double_name(self, data):
    name = base = self.name
    names = []
    for p in data:
        if p != self:
            names.append(p.name)
    if base in names:
        count = 1
        name = f'{base}.{count:03}'
        while name in names:
            count += 1
            name = f'{base}.{count:03}'
        self.name = name

def check_double_cat(self, context):
    cats = bpy.context.scene.nl_global_categories
    check_double_name(self, cats)


def check_double_prop(self, context):
    category = get_global_category()
    props = category.content
    check_double_name(self, props)