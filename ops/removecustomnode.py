from .operator import operator
from bpy.types import Operator
from bpy.props import IntProperty
from ..utilities import preferences
from ..props.customnode import _registered_custom_classes
import bpy


@operator
class LOGIC_NODES_OT_remove_custom_node(Operator):
    bl_idname = "logic_nodes.remove_custom_node"
    bl_label = "Remove Custom Logic Node"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove Custom Logic Node"
    index: IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        node = preferences().custom_logic_nodes[self.index]
        for c in _registered_custom_classes:
            if c.bl_idname == node.idname:
                bpy.utils.unregister_class(c)
                _registered_custom_classes.remove(c)
        preferences().custom_logic_nodes.remove(self.index)
        bpy.ops.wm.save_userpref()
        return {'FINISHED'}