from .operator import operator
from bpy.types import Operator
from bpy.props import IntProperty
from ..utilities import preferences
import bpy


@operator
class LOGIC_NODES_OT_edit_custom_node(Operator):
    bl_idname = "logic_nodes.edit_custom_node"
    bl_label = "Edit Custom Logic Node"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Edit Custom Logic Node"
    index: IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        node = preferences().custom_logic_nodes[self.index]
        t = bpy.data.texts.get(node.idname, None)
        if t is None:
            t = bpy.data.texts.new(node.idname)
        t.clear()
        t.write(node.ui_code)

        t = bpy.data.texts.get(node.modname, None)
        if t is None:
            t = bpy.data.texts.new(node.modname)
        t.clear()
        t.write(node.logic_code)
        return {'FINISHED'}
