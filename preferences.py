import bpy
import sys
from .props.propertyfilter import LogicNodesPropertyFilter
from .props.customnode import CustomNodeReference


_uplogic_versions = [
    ('latest', 'Latest', 'Download the latest version'),
    None,
    ('1.9.5', '1.9.5', 'Suitable for Logic Nodes 2.4'),
    ('2.0.1', '2.0.1', 'Suitable for Logic Nodes 3.0'),
    ('3.2', '3.2', 'Suitable for Logic Nodes 3.2'),
    ('3.2.1', '3.2.1', 'Suitable for Logic Nodes 3.2.1'),
    ('4.5', '4.5', 'Suitable for Logic Nodes 4.5')
]


class LogicNodesAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = 'bge_netlogic'

    use_reload_text: bpy.props.BoolProperty(default=True)
    auto_switch_trees: bpy.props.BoolProperty(default=True, description='Automatically switch to relevant logic trees when selecting objects')
    uplogic_version: bpy.props.EnumProperty(items=_uplogic_versions, default='4.5', name='Uplogic Version')
    use_node_debug: bpy.props.BoolProperty(default=True)
    use_node_notify: bpy.props.BoolProperty(default=True)
    prop_filter: bpy.props.PointerProperty(type=LogicNodesPropertyFilter)
    use_fmod_nodes: bpy.props.BoolProperty(name='FMOD Support', description='')

    custom_logic_nodes: bpy.props.CollectionProperty(
        type=CustomNodeReference
    )

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
            'auto_switch_trees',
            text="Auto-switch logic trees"
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
        col.label(text='Additional Nodes')
        box = col.box()
        row = box.row(align=True)
        row.prop(self, 'use_fmod_nodes')
        if self.use_fmod_nodes:
            row.operator('logic_nodes.install_pyfmodex', icon='URL', text='Install')
        col.separator()
        link_row = col.row(align=True)
        link_row.operator("logic_nodes.open_github", icon="URL")
        link_row.operator("logic_nodes.open_donate", icon="FUND")
        contrib_row = col.row()
        contrib_row.label(text='Contributors: VUAIEO, Simon, L_P, p45510n')
