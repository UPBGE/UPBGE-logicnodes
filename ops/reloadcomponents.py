from ..utilities import notify
from ..utilities import warn
from ..utilities import error
from ..utilities import success
from ..generator.tree_code_generator import generate_logic_node_code
from .operator import operator
from .operator import reload_texts
from bpy.types import Operator
import bpy


COMPONENT_TEMPLATE = """\
import bge, bpy
from collections import OrderedDict
import mathutils
class {}(bge.types.KX_PythonComponent):
    {}
    def start(self, args): pass
    def update(self): pass"""


def build_dummy_text(comp_name, textblock):
    cargs = ''
    in_args = False
    textblock_c = textblock.copy()
    textblock.clear()
    for line in textblock_c.lines:
        if comp_name in line.body:
            continue
        line.body = line.body.replace(' ', '')
        if line.body.startswith('@'):
            continue
        if 'args =' in line.body or 'args=' in line.body:
            in_args = True
        if '])' in line.body:
            cargs += line.body
            break
        if in_args:
            cargs += line.body
    bpy.data.texts.remove(textblock_c)
    return COMPONENT_TEMPLATE.format(comp_name, cargs)


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
        generate_logic_node_code()
        reload_texts()
        # obj = context.active_object
        active_object = context.object
        for obj in bpy.data.objects:
            if obj.name in bpy.context.view_layer.objects:
                bpy.context.view_layer.objects.active = obj
            for i, c in enumerate(obj.game.components):
                text = bpy.data.texts[f'{c.module}.py']
                ogtext = text.as_string()
                text.write(build_dummy_text(c.name, text))
                try:
                    bpy.ops.logic.python_component_reload(index=i)
                except Exception as e:
                    warn(f'Could not reload component {c.name}! Reason: {e}')
                text.clear()
                text.from_string(ogtext)
            reload_texts()
        
        if obj.name in bpy.context.view_layer.objects:
            bpy.context.view_layer.objects.active = active_object
        return {'FINISHED'}