from .socket import NodeSocketLogic
from .socket import PARAMETER_SOCKET_COLOR
from .socket import socket_type
from ..enum_types import _enum_field_value_types
from ...utilities import parse_value_type
from ...utilities import update_draw
from bpy.types import NodeSocket
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import EnumProperty
from bpy.props import BoolProperty
from bpy.props import IntProperty


@socket_type
class NodeSocketLogicValueOptional(NodeSocket, NodeSocketLogic):
    bl_idname = "NLOptionalValueFieldSocket"
    bl_label = "Value"
    value: StringProperty(update=update_draw)

    def on_type_changed(self, context):
        if self.value_type == "BOOLEAN":
            self.value = str(self.bool_editor)
        if self.value_type == "STRING":
            self.value = str(self.string_editor)
        if self.value_type == "FILE_PATH":
            self.value = str(self.path_editor)
        update_draw(self, context)

    value_type: EnumProperty(
        name='Type',
        items=_enum_field_value_types,
        update=on_type_changed
    )

    use_value: BoolProperty(
        update=update_draw
    )

    def store_boolean_value(self, context):
        self.value = str(self.bool_editor)
        update_draw(self, context)

    bool_editor: BoolProperty(update=store_boolean_value)

    def store_int_value(self, context):
        self.value = str(self.int_editor)

    int_editor: IntProperty(update=store_int_value)

    def store_float_value(self, context):
        self.value = str(self.float_editor)

    float_editor: FloatProperty(update=store_float_value)

    def store_string_value(self, context):
        self.value = self.string_editor

    string_editor: StringProperty(update=store_string_value)

    def store_path_value(self, context):
        self.value = self.path_editor

    path_editor: StringProperty(
        update=store_path_value,
        subtype='FILE_PATH'
    )

    def draw_color(self, context, node):
        return PARAMETER_SOCKET_COLOR

    def get_unlinked_value(self):
        return parse_value_type(self.value_type, self.value) if self.use_value or self.is_linked else "utils.STATUS_INVALID"

    def draw(self, context, layout, node, text):
        if self.is_linked or self.is_output:
            layout.label(text=text)
        else:
            col = layout.column()
            if text:
                name_row = col.row()
                name_row.label(text=text)
                name_row.prop(self, "use_value", text="")
            if not self.use_value:
                return
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
