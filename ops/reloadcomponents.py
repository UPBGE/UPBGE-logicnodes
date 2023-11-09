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
        bpy.ops.logic_nodes.generate_code()
        reload_texts()
        # obj = context.active_object
        active_object = context.object
        for obj in bpy.data.objects:
            if obj.name in bpy.context.view_layer.objects:
                bpy.context.view_layer.objects.active = obj
            for i, c in enumerate(obj.game.components):
                text = bpy.data.texts[f'{c.module}.py']
                ogtext = text.as_string()
                for line in text.lines:
                    if (
                        'uplogic' in line.body
                        or line.body.startswith('from bge ')
                        or 'bgui' in line.body
                        or line.body.startswith('@')
                        or line.body.startswith('from .')
                    ):
                        line.body = '# ' + line.body
                bpy.ops.logic.python_component_reload(index=i)
                text.from_string(ogtext)
            reload_texts()
        
        if obj.name in bpy.context.view_layer.objects:
            bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}