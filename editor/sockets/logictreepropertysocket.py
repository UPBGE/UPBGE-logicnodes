from .socket import SOCKET_TYPE_STRING, NodeSocketLogic
from .socket import SOCKET_COLOR_STRING
from .socket import socket_type
from .socket import update_draw
from ...utilities import make_valid_name
from bpy.types import NodeSocket
from bpy.props import StringProperty
from bpy.props import FloatVectorProperty
from bpy.props import BoolProperty
from bpy.props import IntProperty
import bpy


@socket_type
class NodeSocketLogicTreeProperty(NodeSocket, NodeSocketLogic):
    bl_idname = "NodeSocketLogicTreeProperty"
    bl_label = "Property"

    value: StringProperty(
        update=update_draw,
        description="Look for Tree Properties and display if this tree is applied to the selected object",
        name='Property'
    )
    ref_index: IntProperty(default=0)
    use_custom: BoolProperty(
        name='Free Edit'
    )

    show_prop: BoolProperty(default=True)

    def _get_active_prop(self, context):
        tree = getattr(context.space_data, 'edit_tree', None)
        if tree is None:
            return None
        obj = bpy.context.view_layer.objects.active
        if obj:
            comp = obj.game.components.get(make_valid_name(tree.name))
            if not (comp and self.value):
                return None
            return comp.properties.get(self.value, None)

    def update_color(self, context=None):
        prop = self._get_active_prop(context)
        if prop:
            col = self.color_solid
            prop.value = col

    def update_color_alpha(self, context=None):
        prop = self._get_active_prop(context)
        if prop:
            col = self.color_alpha
            prop.value = col

    color_solid: FloatVectorProperty(
        min=0.0,
        max=1.0,
        name='Color',
        subtype='COLOR_GAMMA',
        default=(0.5, 0.5, 0.5),
        update=update_color
    )

    color_alpha: FloatVectorProperty(
        min=0.0,
        max=1.0,
        name='Color',
        subtype='COLOR_GAMMA',
        size=4,
        default=(0.5, 0.5, 0.5, 1.0),
        update=update_color_alpha
    )

    color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.label(text=self.name)
        elif self.is_linked:
            layout.label(text=self.name)
        else:
            col = layout.column(align=False)
            tree = getattr(context.space_data, 'edit_tree', None)
            if not tree:
                return
            col.prop_search(
                self,
                'value',
                tree,
                'properties',
                icon='NONE',
                text=''
            )
            if not self.show_prop:
                return
            prop = self._get_active_prop(context)
            if prop is None:
                return
            vtype = tree.properties.get(self.value).value_type
            if vtype == '5':
                col.prop(self, 'color_solid', text='')
            elif vtype == '6':
                col.prop(self, 'color_alpha', text='')
            else:
                col.prop(prop, 'value', text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.value)