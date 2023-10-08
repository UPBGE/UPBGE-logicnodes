from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicIntegerPositive
from bpy.props import BoolProperty
from bpy.props import StringProperty


@node_type
class LogicNodeSaveGame(LogicNodeActionType):
    bl_idname = "NLActionSaveGame"
    bl_label = "Save Game"
    bl_icon = 'FILE_TICK'
    nl_category = "Game"
    nl_module = 'actions'
    nl_class = "ULSaveGame"

    custom_path: BoolProperty(name='Custom Path')

    path: StringProperty(
        subtype='FILE_PATH',
        description=(
            'Choose a Path to save the file to. '
            'Start with "./" to make it relative to the file path.'
        ), name='Path'
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicIntegerPositive, 'Slot')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(
            self,
            "custom_path",
            toggle=True,
            text="Custom Path" if self.custom_path else "File Path/Saves",
            icon='FILE_FOLDER'
        )
        if self.custom_path:
            layout.prop(self, "path", text='')

    def get_input_names(self):
        return ["condition", 'slot']

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
