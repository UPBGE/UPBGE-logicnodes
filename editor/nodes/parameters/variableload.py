from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicFilePath
from ...sockets import NodeSocketLogicValueOptional
from ...sockets import NodeSocketLogicParameter
from bpy.props import BoolProperty
from bpy.props import StringProperty


@node_type
class LogicNodeVariableLoad(LogicNodeParameterType):
    bl_idname = "NLActionLoadVariable"
    bl_label = "Load Variable"
    bl_description = 'Load an externally saved value'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "ULLoadVariable"

    def init(self, context):
        self.add_input(NodeSocketLogicFilePath, 'Path', 'path', {'default_value': '//Data'})
        self.add_input(NodeSocketLogicString, 'File', 'file_name', {'default_value': 'variables'})
        self.add_input(NodeSocketLogicString, 'Name', 'name', {'default_value': 'var'})
        self.add_input(NodeSocketLogicValueOptional, 'Default Value', 'default_value')
        self.add_output(NodeSocketLogicParameter, 'Value', 'VAR')
        LogicNodeParameterType.init(self, context)

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ['path', 'file_name', 'name', 'default_value']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['VAR']
