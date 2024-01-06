from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from bpy.props import BoolProperty
from bpy.props import StringProperty


@node_type
class LogicNodeRemoveVariable(LogicNodeActionType):
    bl_idname = "NLActionRemoveVariable"
    bl_label = "Remove Variable"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULRemoveVariable"

    custom_path: BoolProperty(name='Custom Path')
    path: StringProperty(
        subtype='DIR_PATH',
        name='Path',
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        )
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicString, 'Filename', None, {'default_value': 'variables'})
        self.add_input(NodeSocketLogicString, 'Name', None, {'default_value': 'var'})
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

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

    def get_input_names(self):
        return ["condition", 'file_name', 'name']

    def get_attributes(self):
        s_path = self.path
        if s_path.endswith('\\'):
            s_path = s_path[:-1]
        path_formatted = s_path.replace('\\', '/')
        return [(
            "path",
            "'{}'".format(
                path_formatted
            ) if self.custom_path else "''"
        )]

    def get_output_names(self):
        return ["OUT"]
