from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicBoolCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicList
from bpy.props import BoolProperty
from bpy.props import StringProperty


@node_type
class LogicNodeListVariables(LogicNodeActionType):
    bl_idname = "NLActionListVariables"
    bl_label = "List Saved Variables"
    nl_module = 'actions'
    nl_class = "ULListVariables"

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
        self.add_input(NodeSocketLogicBoolCondition, 'Condition')
        self.add_input(NodeSocketLogicString, 'Filename', {'value': 'variables'})
        self.add_input(NodeSocketLogicBoolean, 'Print')
        self.add_output(NodeSocketLogicCondition, 'Done')
        self.add_output(NodeSocketLogicList, 'List')
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
        return ["condition", 'file_name', 'print_list']

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
        return ["OUT", 'LIST']
