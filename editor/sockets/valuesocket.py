from .socket import SOCKET_TYPE_GENERIC, NodeSocketLogic
from .socket import SOCKET_COLOR_GENERIC
from .socket import socket_type
from .socket import update_draw
from ..enum_types import _enum_field_value_types
from ...utilities import parse_value_type
from bpy.types import NodeSocket
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import EnumProperty
from bpy.props import BoolProperty
from bpy.props import IntProperty


@socket_type
class NodeSocketLogicValue(NodeSocket, NodeSocketLogic):
    bl_idname = "NLValueFieldSocket"
    bl_label = "Value"
    nl_type = SOCKET_TYPE_GENERIC
    nl_color = SOCKET_COLOR_GENERIC

    default_value: StringProperty(update=update_draw)
    # XXX: Remove value property
    value: StringProperty(update=update_draw)

    def on_type_changed(self, context):
        if self.value_type == "BOOLEAN":
            self.default_value = str(self.bool_editor)
        if self.value_type == "STRING":
            self.default_value = str(self.string_editor)
        if self.value_type == "FILE_PATH":
            self.default_value = str(self.path_editor)

    value_type: EnumProperty(
        name='Type',
        items=_enum_field_value_types,
        default='FLOAT',
        update=on_type_changed
    )

    def store_boolean_value(self, context):
        self.default_value = str(self.bool_editor)

    bool_editor: BoolProperty(update=store_boolean_value)

    def store_int_value(self, context):
        self.default_value = str(self.int_editor)

    int_editor: IntProperty(update=store_int_value)

    def store_float_value(self, context):
        self.default_value = str(self.float_editor)

    float_editor: FloatProperty(update=store_float_value)

    def store_string_value(self, context):
        self.default_value = self.string_editor

    string_editor: StringProperty(update=store_string_value)

    def store_path_value(self, context):
        self.default_value = self.path_editor

    path_editor: StringProperty(
        update=store_path_value,
        subtype='FILE_PATH'
    )

    def get_unlinked_value(self):
        return parse_value_type(self.value_type, self.default_value)

    def draw_color(self, context, node) -> tuple[float]:
        from_socket = self.get_from_socket()
        if from_socket:
            return from_socket.nl_color
        return self.nl_color

    def _draw(self, context, layout, node, text):
        if self.is_output or self.is_multi_input:
            layout.label(text=text)
            return
        if self.linked_valid:
            layout.label(text=self.links[0].from_socket.name)
        else:
            col = layout.column()
            if text:
                name_row = col.row()
                name_row.label(text=text)
            val_line = col.row()
            val_row = val_line.split()
            if self.value_type == "BOOLEAN":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "bool_editor", text="")
            elif self.value_type == "INTEGER":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "int_editor", text="")
            elif self.value_type == "FLOAT":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "float_editor", text="")
            elif self.value_type == "STRING":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "string_editor", text="")
            elif self.value_type == "FILE_PATH":
                val_row.prop(self, "value_type", text="")
                val_row.prop(self, "path_editor", text="")
