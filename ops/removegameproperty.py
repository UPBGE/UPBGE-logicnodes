from .operator import operator
from bpy.types import Operator
from bpy.props import IntProperty
import bpy


@operator
class LOGIC_NODES_OT_remove_game_property(Operator):
    bl_idname = "logic_nodes.remove_game_property"
    bl_label = "Add Game Property"
    bl_description = "Remove this property"
    bl_options = {'REGISTER', 'UNDO'}
    index: IntProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_remove(index=self.index)
        return {'FINISHED'}