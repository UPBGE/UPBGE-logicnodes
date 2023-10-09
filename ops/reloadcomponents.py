from ..utilities import notify
from ..utilities import error
from ..utilities import success
from .operator import operator
from .operator import reload_texts
from bpy.types import Operator
import bpy


@operator
class LOGIC_NODES_OT_reload_components(Operator):
    bl_idname = "logic_nodes.reload_components"
    bl_label = "Reload Components"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Reload all components applied to this object"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        reload_texts()
        obj = context.active_object
        for i, c in enumerate(obj.game.components):
            text = bpy.data.texts[f'{c.module}.py']
            for line in text.lines:
                if (
                    'uplogic' in line.body
                    or line.body.startswith('from bge ')
                    or 'bgui' in line.body
                    or line.body.startswith('@')
                ):
                    line.body = '# ' + line.body
            bpy.ops.logic.python_component_reload(index=i)
        reload_texts()
        return {'FINISHED'}