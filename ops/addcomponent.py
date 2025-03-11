from ..utilities import add_component
from .operator import operator
from .operator import _enum_components
from .operator import reload_texts
from bpy.types import Operator
import bpy


@operator
class LOGIC_NODES_OT_add_component(Operator):
    bl_idname = "logic_nodes.add_component"
    bl_label = "Add Component"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a python Component to the selected object"

    component: bpy.props.EnumProperty(
        name="Component Name",
        description="Add this Component to the current object",
        items=_enum_components
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        add_component(bpy.context.scene.componenthelper, self.component)
        return {'FINISHED'}

    def invoke(self, context, event):
        reload_texts()
        if self.component:
            return context.window_manager.invoke_props_dialog(self, width=400)
        else:
            return {'CANCELLED'}