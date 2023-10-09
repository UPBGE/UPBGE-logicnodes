from ..utilities import notify
from .operator import operator
from .operator import _enum_components
from .operator import reload_texts
from bpy.types import Operator
import bpy


COMPONENT_TEMPLATE = """\
import bge, bpy
from collections import OrderedDict
class {}(bge.types.KX_PythonComponent):
    {}
    def start(self, args): pass
    def update(self): pass"""


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
        comp_name = self.component
        select_text = context.scene.nl_componenthelper
        mod_name = select_text.name[:len(select_text.name) - 3]
        body = select_text.as_string()
        cargs = ''
        in_args = False
        for line in select_text.lines:
            if comp_name in line.body:
                continue
            line.body = line.body.replace(' ', '')
            if line.body.startswith('@'):
                continue
            if 'args=' in line.body:
                in_args = True
            if '])' in line.body:
                cargs += line.body
                break
            if in_args:
                cargs += line.body
        text = COMPONENT_TEMPLATE.format(comp_name, cargs)
        try:
            select_text.clear()
            select_text.write(text)
            notify(f'Adding {mod_name}.{comp_name} to {context.active_object.name}...')
            bpy.ops.logic.python_component_register(component_name=f'{mod_name}.{comp_name}')
            select_text.clear()
            select_text.write(body)
        except Exception as e:
            select_text.clear()
            select_text.write(body)
            self.report({"ERROR"}, str(e))
        return {'FINISHED'}

    def invoke(self, context, event):
        reload_texts()
        if self.component:
            return context.window_manager.invoke_props_dialog(self, width=400)
        else:
            return {'CANCELLED'}