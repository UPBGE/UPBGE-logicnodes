from ..node import node_type
from ..node import LogicNodeUIType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatAngle
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicColorRGBA
from ...sockets import NodeSocketLogicUI


@node_type
class LogicNodeCreateUIPath(LogicNodeUIType):
    bl_idname = "LogicNodeCreateUIPath"
    bl_label = "Create Path"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "CreateUIPathNode"
    bl_description = 'Create a new widget that draws a path on the screen'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicUI, "Parent", 'parent')
        self.add_input(NodeSocketLogicBoolean, "Relative Position", 'rel_pos')
        self.add_input(NodeSocketLogicVectorXY, "", 'pos')
        self.add_input(NodeSocketLogicBoolean, "Relative Points", 'rel_points')
        self.add_input(NodeSocketLogicVectorXY, "Points", 'points', shape='SQUARE', settings={'list_mode': True})
        self.add_input(NodeSocketLogicColorRGBA, "Line Color", 'line_color', {'default_value': (1, 1, 1, 1)})
        self.add_input(NodeSocketLogicIntegerPositive, "Line Width", 'line_width', {'default_value': 1})
        self.add_input(NodeSocketLogicFloatAngle, "Angle", 'angle')
        self.add_output(NodeSocketLogicCondition, "Done", 'DONE')
        self.add_output(NodeSocketLogicUI, "Path", 'PATH')
        LogicNodeUIType.init(self, context)
    
    def get_ui_class(self):
        from uplogic.ui.path import Path
        return Path
