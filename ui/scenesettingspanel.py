import bpy
from ..utilities import preferences
from .interface import ui_panel


@ui_panel
class LOGIC_NODES_PT_scene_settings(bpy.types.Panel):
    bl_label = "Uplogic Settings"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    name: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        prefs = preferences()
        layout.prop(context.scene, 'jump_in_game_cam')
        layout.prop(context.scene, 'use_vr_audio_space')
        row = layout.row()
        row.prop(context.scene, 'use_screen_console')
        part = row.row()
        part.prop(context.scene, 'screen_console_open', text='Debug')
        # op = layout.operator("logic_nodes.key_selector", text=prefs.screen_console_key)
        # op.is_socket = False
        part.enabled = getattr(context.scene, 'use_screen_console', False)

        use_mainloop = context.scene.get('__main__', '') != ''
        layout.operator(
            'logic_nodes.custom_mainloop',
            text='Remove Custom Mainloop' if use_mainloop else 'Use Custom Mainloop',
            icon='CANCEL' if use_mainloop else 'PLAY'
        )
        layout.separator()
        layout.operator(
            'logic_nodes.audio_system',
            icon='PLAY'
        )