from .operator import operator
from bpy.types import Operator
import bpy


@operator
class LOGIC_NODES_OT_custom_mainloop(Operator):
    bl_idname = "logic_nodes.custom_mainloop"
    bl_label = "Use Custom Mainloop"
    bl_description = ('Use a custom Mainloop for this scene')
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        name = scene.name.lower()
        if scene.get('__main__', '') != '':
            scene['__main__'] = ''
            scene.game_settings.use_frame_rate = True
            return {"FINISHED"}
        main = bpy.data.texts.get(f'{name}.py')
        if main is None:
            main = bpy.data.texts.new(f'{name}.py')
            main.write(
f'''from uplogic import ULLoop


class {scene.name}Loop(ULLoop):

    def start(self):
        """This code runs once on scene start."""
        pass

    def update(self):
        """This code runs when a frame is rendered (default up to 60x/second)."""
        pass

    def stop(self):
        """This code runs when the game is stopped."""
        pass


{scene.name}Loop()'''
)
        scene['__main__'] = f'{name}.py'
        scene.game_settings.use_frame_rate = False
        return {"FINISHED"}