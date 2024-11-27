from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString
from bpy.props import StringProperty
import bpy


@node_type
class LogicNodeFModSetEventParameter(LogicNodeActionType):
    bl_idname = "LogicNodeFModSetEventParameter"
    bl_label = "Set Event Instance Parameter"
    bl_width_default = 180
    bl_description = 'Set a parameter on an active event instance'
    nl_module = 'uplogic.nodes.fmod'
    nl_class = "FModSetEventParameterNode"

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
    
    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'parameter', text='')

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicPython, "Event Instance", 'event')
        self.add_input(NodeSocketLogicString, "", '_parameter', settings={'enabled': False})
        self.add_input(NodeSocketLogicFloat, "Value", 'value')
        self.add_input(NodeSocketLogicBoolean, "Ignore Seek", 'ignore_seek')
        self.add_output(NodeSocketLogicCondition, "Done", 'DONE')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [('parameter', repr(self.parameter))]
