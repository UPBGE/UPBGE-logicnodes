from .operator import operator
from bpy.types import Operator
import bpy


@operator
class LOGIC_NODES_OT_add_game_property(Operator):
    bl_idname = "logic_nodes.add_game_property"
    bl_label = "Add Game Property"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Adds a property available to the UPBGE"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_new()
        return {'FINISHED'}
