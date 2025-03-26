from .operator import operator
from bpy.types import Operator
import bpy
import sys


def _enum_texts(self, context):
    items = []
    for t in bpy.data.texts:
        items.append((t.name, t.name, t.name))
    return items


@operator
class LOGIC_NODES_OT_register_custom_node(Operator):
    bl_idname = "logic_nodes.register_custom_node"
    bl_label = "Register Custom Logic Node"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Register Custom Logic Node"

    text_name: bpy.props.EnumProperty(
        name="Node",
        description="Register a node defined in a python file",
        items=_enum_texts
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        string = bpy.data.texts[self.text_name].as_string()
        text = bpy.data.texts.new(f'__customnodetemp__')
        text.write(string)
        exec(string, {'bge_netlogic': sys.modules['bge_netlogic']})
        bpy.data.texts.remove(text)
        return {'FINISHED'}

    def invoke(self, context, event):
        if self.text_name:
            return context.window_manager.invoke_props_dialog(self, width=400)
        else:
            return {'CANCELLED'}