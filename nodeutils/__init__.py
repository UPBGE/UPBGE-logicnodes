# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
import nodeitems_utils

_cat_icons = {
    'Animation': 'ARMATURE_DATA',
    'Armature / Rig': 'GROUP_BONE',
    'Bricks': 'LOGIC',
    'Bone Constraints': 'CONSTRAINT_BONE',
    'Camera': 'CAMERA_DATA',
    'Character': 'GHOST_ENABLED',
    'Collections': 'OUTLINER_COLLECTION',
    'Custom': 'INFO',
    'Data': 'CON_OBJECTSOLVER',
    'Dictionary': 'SNAP_VERTEX',
    'Events': 'RIGHTARROW_THIN',
    'File': 'FILEBROWSER',
    'Game': 'IMAGE_BACKGROUND',
    'Gamepad': 'LOGIC',
    'Geometry': 'CONE',
    'Global': 'WORLD',
    'Groups': 'NODETREE',
    'Input': 'VIEW_PAN',
    'Keyboard': 'SORTALPHA',
    'Layout': 'EMPTY_DATA',
    'Lights': 'OUTLINER_OB_LIGHT',
    'List': 'COLLAPSEMENU',
    'Logic': 'SETTINGS',
    'Materials': 'MATERIAL',
    'Math': 'CON_TRANSFORM',
    'Mouse': 'MOUSE_MMB',
    'Nodes': 'NODETREE',
    'Objects': 'OBJECT_DATAMODE',
    'Physics': 'PHYSICS',
    'Properties': 'PROPERTIES',
    'Python': 'FILE_SCRIPT',
    'Random': 'QUESTION',
    'Ray Casts': 'TRACKING_FORWARDS_SINGLE',
    'Render': 'SCENE',
    'Scene': 'SCENE_DATA',
    'Simple': 'CON_TRANSFORM',
    'Sound': 'OUTLINER_DATA_SPEAKER',
    'Time': 'TIME',
    'Transformation': 'VIEW3D',
    'Trees': 'OUTLINER',
    'Utilities': 'PLUGIN',
    'Values': 'RADIOBUT_OFF',
    'Variables': 'FILE',
    'Vector Math': 'EMPTY_ARROWS',
    'Vectors': 'EMPTY_ARROWS',
    'Vehicle': 'AUTO',
    'Visuals': 'HIDE_OFF',
    'VR': 'CAMERA_STEREO'
}

_main_menues = [
    'Events',
    'Game',
    'Input',
    'Scene',
    'Values',
    'Animation',
    'Lights',
    'Nodes',
    'Objects',
    'Sound',
    'Logic',
    'Math',
    'Physics',
    'Python',
    'Ray Casts',
    'Time',
    'File',
    'Variables',
    'Render',
    'Layout',
    'Utilities'
]

_cat_separators = [
    'Values',
    'Sound',
    'Time',
    'Render'
]


class NodeCategory(nodeitems_utils.NodeCategory):

    @staticmethod
    def draw(self, layout, context):

        layout.menu("NODE_MT_category_%s" % self.identifier)


class NodeItem(nodeitems_utils.NodeItem):

    def __init__(
        self,
        nodetype,
        icon='DOT',
        label=None,
        settings={},
        poll=None
    ):
        self.nodetype = nodetype
        self._label = label
        self.icon = icon
        self.settings = settings
        self.poll = poll

    @staticmethod
    def draw(self, layout, context):
        default_context = bpy.app.translations.contexts.default

        props = layout.operator(
            "node.add_node",
            text=self.label,
            text_ctxt=default_context,
            icon=self.icon
        )
        props.type = self.nodetype
        props.use_transform = True

        for setting in self.settings.items():
            ops = props.settings.add()
            ops.name = setting[0]
            ops.value = setting[1]


class NodeItemCustom(nodeitems_utils.NodeItemCustom):
    pass


_node_categories = nodeitems_utils._node_categories


def register_node_categories(identifier, cat_list):
    if identifier in _node_categories:
        raise KeyError("Node categories \
            list '%s' already registered" % identifier)
        return

    # works as draw function for both menus and panels
    def draw_node_item(self, context):
        layout = self.layout
        col = layout.column()
        for item in self.category.items(context):
            item.draw(item, col, context)

    menu_types = []
    for cat in cat_list:
        menu_type = type(
            "NODE_MT_category_" + cat.identifier,
            (bpy.types.Menu,),
            {
                "bl_space_type": 'NODE_EDITOR',
                "bl_label": cat.name,
                "category": cat,
                "poll": cat.poll,
                "draw": draw_node_item,
            }
        )

        menu_types.append(menu_type)

        bpy.utils.register_class(menu_type)

    def draw_add_menu(self, context):
        layout = self.layout

        menues = []
        for cat in cat_list:
            if cat.poll(context):
                if cat.identifier in _main_menues:
                    menues.append(cat)

        li = []
        for entry in _main_menues:
            for m in menues:
                if entry == m.name:
                    li.append(m)

        for cat in li:
            layout.menu(
                "NODE_MT_category_%s" % cat.identifier,
                icon=_cat_icons.get(cat.identifier, 'DISCLOSURE_TRI_RIGHT')
            )
            if cat.identifier in _cat_separators:
                layout.separator()

    # stores: (categories list, menu draw function, submenu types, panel types)
    _node_categories[identifier] = (cat_list, draw_add_menu, menu_types)


def node_categories_iter(context):
    for cat_type in _node_categories.values():
        for cat in cat_type[0]:
            if cat.poll and cat.poll(context):
                yield cat


def node_items_iter(context):
    for cat in node_categories_iter(context):
        for item in cat.items(context):
            yield item


def unregister_node_cat_types(cats):
    pass


def unregister_node_categories(identifier=None):
    # unregister existing UI classes
    if identifier:
        cat_types = _node_categories.get(identifier, None)
        if cat_types:
            unregister_node_cat_types(cat_types)
        del _node_categories[identifier]

    else:
        for cat_types in _node_categories.values():
            unregister_node_cat_types(cat_types)
        _node_categories.clear()
