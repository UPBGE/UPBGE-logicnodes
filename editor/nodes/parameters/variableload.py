from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicValueOptional
from ...sockets import NodeSocketLogicParameter
from bpy.props import BoolProperty
from bpy.props import StringProperty


@node_type
class LogicNodeVariableLoad(LogicNodeParameterType):
    bl_idname = "NLActionLoadVariable"
    bl_label = "Load Variable"
    nl_module = 'uplogic.nodes.parameters'

    custom_path: BoolProperty()
    path: StringProperty(
        subtype='DIR_PATH',
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        self.add_input(NodeSocketLogicString, 'Filename', {'default_value': 'variables'})
        self.add_input(NodeSocketLogicString, 'Name', {'default_value': 'var'})
        self.add_input(NodeSocketLogicValueOptional, 'Default Value')
        self.add_output(NodeSocketLogicParameter, 'Value')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Data",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    nl_class = "ULLoadVariable"

    def get_input_names(self):
        return ['file_name', 'name', 'default_value']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [("path", f"'{path_formatted}'" if self.custom_path else "''")]

    def get_output_names(self):
        return ['VAR']
