from bpy.types import Context, UILayout
from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicFloat
from ...sockets import NodeSocketLogicString
from bpy.props import BoolProperty
from bpy.props import StringProperty
import bpy


@node_type
class LogicNodeFModGetEventParameter(LogicNodeActionType):
    bl_idname = "LogicNodeFModGetEventParameter"
    bl_label = "Get Event Instance Parameter"
    bl_width_default = 180
    bl_description = 'Get a parameter on an active event instance'
    nl_module = 'uplogic.nodes.fmod'
    nl_class = "FModGetEventParameterNode"

    actual: BoolProperty(name='Use Actual', description='Use the actual current value instead of the target value (only relevant with a seek speed > 0)')

    def _get_fmod_parameter(self):
        return bpy.context.scene.nl_fmod_parameters.get(self.get_fmod_parameter())

    def get_fmod_parameters(self, context, edit_text):
        if edit_text != '' and edit_text not in [parameter.name for parameter in bpy.context.scene.nl_fmod_parameters]:
            yield edit_text
        for parameter in bpy.context.scene.nl_fmod_parameters:
            yield (parameter.name, 'PLUS')

    def get_fmod_parameter(self):
        return self.get('parameter_name', '')

    def clear_fmod_parameter(self, parameter):
        if parameter is None:
            return
        parameter.users -= 1
        if parameter.users == 0:
            bpy.context.scene.nl_fmod_parameters.remove(
                bpy.context.scene.nl_fmod_parameters.find(parameter.name)
            )

    def set_fmod_parameter(self, value):
        current_parameter = self._get_fmod_parameter()
        new_parameter = bpy.context.scene.nl_fmod_parameters.get(value)
        if value != '' and new_parameter is None:
            new_parameter = bpy.context.scene.nl_fmod_parameters.add()
            new_parameter.name = value
        if new_parameter is not None:
            new_parameter.users += 1
        if current_parameter is not new_parameter:
            if current_parameter is not None:
                self.clear_fmod_parameter(current_parameter)
        self['parameter_name'] = value
        return None

    def copy(self, node) -> None:
        parameter = self._get_fmod_parameter()
        if parameter is not None:
            parameter.users += 1

    def free(self) -> None:
        self.clear_fmod_parameter(self._get_fmod_parameter())
        super().free()

    fmod_parameter: StringProperty(
        name='Parameter',
        description='Name of the event parameter',
        get=get_fmod_parameter,
        set=set_fmod_parameter,
        search=get_fmod_parameters,  # XXX: Reactivate, botched for some reason
        search_options={'SUGGESTION'}
    )

    def draw_buttons(self, context: Context, layout: UILayout) -> None:
        layout.prop(self, 'fmod_parameter', text='')
        layout.prop(self, 'actual')

    def init(self, context):
        self.add_input(NodeSocketLogicPython, "Event Instance", 'event')
        self.add_input(NodeSocketLogicString, "", '_parameter', settings={'enabled': False})
        self.add_output(NodeSocketLogicFloat, "Value", 'VAL')
        LogicNodeActionType.init(self, context)

    def get_attributes(self):
        return [('actual', self.actual), ('parameter', repr(self.fmod_parameter))]
