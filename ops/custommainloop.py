from .operator import operator
from bpy.types import Operator
import bpy


MAINLOOP_TEMPLATE = '''from uplogic.loop import MainLoop, CustomLoop


class {}Loop(CustomLoop):

    def start(self):
        """This code runs once on scene start.
        Use 'self.scene' to get the current 'KX_Scene'.
        You can use '...kx_scene["uplogic.mainloop"] to retrieve the customloop object in other scripts'.
        If you want other callbacks to be run on update, you can call 'MainLoop.on_update(callback)'.
        You can overwrite 'self.quit_key' with any key (e.g.: 'A') to change the key binding for game exit.
        """
        pass

    def update(self):
        """This code runs when a frame is rendered (default up to 60x/second)."""
        pass

    def stop(self):
        """This code runs when the game is stopped."""
        pass


{}Loop()'''


def make_custom_mainloop(scene):
    text = MAINLOOP_TEMPLATE.format(scene.name, scene.name)
    name = scene.name.lower()
    main = bpy.data.texts.get(f'{name}.py')
    if main is None:
        main = bpy.data.texts.new(f'{name}.py')
        main.write(text)
    scene['__main__'] = f'{name}.py'
    scene.game_settings.use_frame_rate = False

def remove_custom_mainloop(scene):
    scene['__main__'] = ''
    scene.game_settings.use_frame_rate = True


@operator
class LOGIC_NODES_OT_custom_mainloop(Operator):
    bl_idname = "logic_nodes.custom_mainloop"
    bl_label = "Use Custom Mainloop"
    bl_description = ('Use a custom Mainloop for this scene')
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        if scene.get('__main__', '') != '':
            remove_custom_mainloop(scene)
            return {"FINISHED"}
        make_custom_mainloop(scene)
        return {"FINISHED"}