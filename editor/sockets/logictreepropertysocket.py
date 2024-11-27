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
    bl_label = "Logic Tree Property"

    default_value: StringProperty(
        update=update_draw,
        description="Look for Tree Properties and display if this tree is applied to the selected object",
        name='Property'
    )
    # XXX: Remove value property
    value: StringProperty(
        update=update_draw,
        description="Look for Tree Properties and display if this tree is applied to the selected object",
        name='Property'
    )
    ref_index: IntProperty(default=0)
    use_custom: BoolProperty(
        name='Free Edit'
    )

    show_prop: BoolProperty(
        default=False,
        name='Show Default',
        description='Show the default value for this property'
    )

    def _get_active_prop(self, context):
        tree = getattr(context.space_data, 'edit_tree', None)
        if tree is None:
            return None
        obj = bpy.context.view_layer.objects.active
        if obj:
            comp = obj.game.components.get(make_valid_name(tree.name))
            if not (comp is not None and self.default_value is not None):
                return None
            return comp.properties.get(self.default_value, None)

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

    nl_color = SOCKET_COLOR_STRING
    nl_type = SOCKET_TYPE_STRING

    def _draw(self, context, layout, node, text):
        if self.is_output or self.is_multi_input:
            layout.label(text=self.name)
        elif self.linked_valid:
            layout.label(text=self.name)
        else:
            tree = getattr(context.space_data, 'edit_tree', None)
            prop = self._get_active_prop(context)
            tprop = tree.properties.get(self.default_value)
            col = layout.column(align=False)
            r = col.row(align=True)
            if not tree:
                return
            if tprop and self.show_prop and not self.is_output:
                col2 = col.column(align=True)
                col2.prop(tprop, 'value_type', text='')
            r.prop_search(
                self,
                'default_value',
                tree,
                'properties',
                icon='NONE',
                text=''
            )
            r.prop(self, 'show_prop', text='', icon='HIDE_OFF' if self.show_prop else 'HIDE_ON')
            if not self.show_prop:
                return
            if prop is None:
                col.label(text='Tree not applied!', icon='ERROR')
                return
            vtype = tree.properties.get(self.default_value).value_type
            if vtype == '5':
                col2.prop(self, 'color_solid', text='')
            elif vtype == '6':
                col2.prop(self, 'color_alpha', text='')
            else:
                col2.prop(prop, 'value', text='')

    def get_unlinked_value(self):
        return '"{}"'.format(self.default_value)