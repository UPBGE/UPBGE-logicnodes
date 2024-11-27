from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicString
from ...enum_types import _enum_math_operations
from bpy.props import EnumProperty
from bpy.props import BoolProperty
from bpy.props import StringProperty
import bpy


@node_type
class LogicNodeFModModifyEventParameter(LogicNodeActionType):
    bl_idname = "LogicNodeFModModifyEventParameter"
    bl_label = "Modify Event Instance Parameter"
    bl_width_default = 220
    bl_description = 'Modify a parameter on an active event instance'
    nl_module = 'uplogic.nodes.fmod'
    nl_class = "FModModifyEventParameterNode"

    def _get_parameter(self):
        return bpy.context.scene.nl_fmod_parameters.get(self.get_parameter())

    def get_parameters(self, context, edit_text):
        if edit_text != '' and edit_text not in [parameter.name for parameter in bpy.context.scene.nl_fmod_parameters]:
            yield edit_text
        for parameter in context.scene.nl_fmod_parameters:
            yield (parameter.name, 'PLUS')

    def get_parameter(self):
        return self.get('parameter_name', '')

    def clear_parameter(self, parameter):
        if parameter is None:
            return
        parameter.users -= 1
        if parameter.users == 0:
            bpy.context.scene.nl_fmod_parameters.remove(
                bpy.context.scene.nl_fmod_parameters.find(parameter.name)
            )

    def copy(self, node) -> None:
        parameter = self._get_parameter()
        if parameter is not None:
            parameter.users += 1

    def free(self) -> None:
        self.clear_parameter(self._get_parameter())
        super().free()

    def set_parameter(self, value):
        current_parameter = self._get_parameter()
        new_parameter = bpy.context.scene.nl_fmod_parameters.get(value)
        if value != '' and new_parameter is None:
            new_parameter = bpy.context.scene.nl_fmod_parameters.add()
            new_parameter.name = value
        if new_parameter is not None:
            new_parameter.users += 1
        if current_parameter is not new_parameter:
            if current_parameter is not None:
                self.clear_parameter(current_parameter)
        self['parameter_name'] = value
        return None
    
    parameter: StringProperty(
        name='Parameter',
        description='Name of the event',
        get=get_parameter,
        set=set_parameter,
        search=get_parameters,  # XXX: Reactivate, botched for some reason
        search_options={'SUGGESTION'}
    )

    def update_draw(self, context=None):
        self.inputs[4].enabled = self.inputs[5].enabled = self.clamp

    operation: EnumProperty(items = _enum_math_operations, name='Operation')
    clamp: BoolProperty(name='Clamp', update=update_draw)

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'parameter', text='')
        layout.prop(self, 'operation', text='')
        layout.prop(self, 'clamp')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicPython, "Event Instance", 'event')
        self.add_input(NodeSocketLogicString, "", '_parameter', settings={'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_input(NodeSocketLogicFloat, "Min", 'minimum')
        self.add_input(NodeSocketLogicFloat, "Max", 'maximum')
        self.add_output(NodeSocketLogicCondition, "Condition", 'condition')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [
            ('parameter', repr(self.parameter)),
            ('operation', f'OPERATORS.get("{self.operation}")')
        ]
