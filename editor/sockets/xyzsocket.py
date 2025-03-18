from ...utilities import DEPRECATED
from .socket import SOCKET_COLOR_DICTIONARY, SOCKET_TYPE_DICTIONARY, NodeSocketLogic
from .socket import socket_type
from bpy.types import NodeSocket
from bpy.props import BoolVectorProperty
from bpy.props import BoolProperty
import bpy


@socket_type
class NodeSocketLogicXYZ(NodeSocket, NodeSocketLogic):
    bl_idname = "NLXYZSocket"
    bl_label = "XYZ"
    default_value: BoolVectorProperty(name='XYZ', size=3)

    x: BoolProperty(default=True)
    y: BoolProperty(default=True)
    z: BoolProperty(default=True)

    def _update_prop_name(self):
        # XXX: Remove value override
        x = getattr(self, 'x', DEPRECATED)
        y = getattr(self, 'y', DEPRECATED)
        z = getattr(self, 'z', DEPRECATED)
        def_val = [False, False, False]
        if x is not DEPRECATED:
            def_val[0] = x
        if y is not DEPRECATED:
            def_val[1] = y
        if z is not DEPRECATED:
            def_val[2] = z
        self.default_value = def_val

    nl_color = SOCKET_COLOR_DICTIONARY
    nl_type = SOCKET_TYPE_DICTIONARY

    def _draw(self, context, layout, node, text):
        if self.linked_valid or self.is_output or self.is_multi_input:
            layout.label(text=text)
        else:
            row = layout.row()
            row.prop(self, 'default_value', text='XYZ')

    def get_unlinked_value(self):
        v = self.default_value
        return f"dict(x={v[0]}, y={v[1]}, z={v[2]})"
