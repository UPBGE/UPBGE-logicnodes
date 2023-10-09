from .operator import operator
from .. import audio
from bpy.types import Operator
import bpy


@operator
class LOGIC_NODES_OT_start_game_from_view(Operator):
    bl_idname = "logic_nodes.start_game_from_view"
    bl_label = "Start Game Here"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Select the object this tree is applied to"

    @classmethod
    def poll(cls, context):
        if context.area.type != 'VIEW_3D':
            return False
        return 'Player' in [obj.name for obj in context.scene.objects]

    def execute(self, context):
        cam = audio.ViewportCamera()
        player = context.scene.objects['Player']
        pos = player.location
        player.location = cam.location
        bpy.ops.view3d.view_camera()
        bpy.ops.view3d.game_start()
        player = context.scene.objects['Player']
        player.location = pos
        return {'FINISHED'}