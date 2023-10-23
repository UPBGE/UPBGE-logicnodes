from ..utilities import notify
from ..utilities import error
from ..utilities import success
from .operator import operator
from bpy.types import Operator
from bpy.props import IntProperty
from bpy.props import StringProperty
import bpy


@operator
class LOGIC_NODES_OT_move_game_property(Operator):
    bl_idname = "logic_nodes.move_game_property"
    bl_label = "Move Game Property"
    bl_description = "Move Game Property"
    bl_options = {'REGISTER', 'UNDO'}
    index: IntProperty()
    direction: StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.game_property_move(
            index=self.index,
            direction=self.direction
        )
        return {'FINISHED'}