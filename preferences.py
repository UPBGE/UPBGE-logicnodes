import bpy
import sys
from .props.propertyfilter import LogicNodesPropertyFilter

_uplogic_versions = [
    ('1.9.5', '1.9.5', 'Suitable for Logic Nodes 2.4')
]


class LogicNodesAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = 'bge_netlogic'

    use_reload_text: bpy.props.BoolProperty(default=True)
    uplogic_version: bpy.props.EnumProperty(items=_uplogic_versions)
    use_node_debug: bpy.props.BoolProperty(default=True)
    use_node_notify: bpy.props.BoolProperty(default=True)
    prop_filter: bpy.props.PointerProperty(type=LogicNodesPropertyFilter)
    use_vr_audio_space: bpy.props.BoolProperty(name='Use VR Audio Space', default=False)
    jump_in_game_cam: bpy.props.BoolProperty(name='Use Game Camera On Start', default=False)
    use_screen_console: bpy.props.BoolProperty(name='Screen Console', description='Print messages to an on-screen console.\nNeeds at least one uplogic import or Logic Node Tree.\nNote: Errors are not printed to this console')
    screen_console_open: bpy.props.BoolProperty(name='Open', description='Start the game with the on-screen console already open')

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label(
            text='Logic Nodes require the uplogic module, please install if missing.',
            icon='CHECKMARK' if 'uplogic' in sys.modules else 'ERROR'
        )
        row = col.row(align=True)
        row.operator('logic_nodes.install_uplogic', icon='IMPORT')
        row.prop(self, 'uplogic_version', text='')
        main_row = layout.row()
        col = main_row.column()
        col.prop(
            self,
            'use_reload_text',
            text="Reload Scripts on Game Start"
        )
        col.prop(
            self,
            'use_node_notify',
            text="Notifications"
        )
        col.prop(
            self,
            'use_node_debug',
            text="Debug Mode (Print Errors to Console)"
        )
        col.separator()
        link_row = col.row(align=True)
        link_row.operator("logic_nodes.open_github", icon="URL")
        link_row.operator("logic_nodes.open_donate", icon="FUND")
        contrib_row = col.row()
        contrib_row.label(text='Contributors: VUAIEO, Simon, L_P, p45510n')