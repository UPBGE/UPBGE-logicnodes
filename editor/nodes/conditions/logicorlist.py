from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeLogicOrList(LogicNodeConditionType):
    bl_idname = "NLConditionOrList"
    bl_label = "Or List"
    bl_width_min = 60
    bl_width_default = 100
    nl_module = 'uplogic.nodes.conditions'
    deprecated = True
    deprecation_message = 'Replaced by "Gate List" Node.'


    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "A")
        self.add_input(NodeSocketLogicCondition, "B")
        self.add_input(NodeSocketLogicCondition, "C")
        self.add_input(NodeSocketLogicCondition, "D")
        self.add_input(NodeSocketLogicCondition, "E")
        self.add_input(NodeSocketLogicCondition, "F")
        self.add_output(NodeSocketLogicCondition, "Or...")
        LogicNodeConditionType.init(self, context)
        self.hide = True

    def update_draw(self, context=None):
        for x in range(5):
            if self.inputs[x].is_linked:
                self.inputs[x].enabled = True
                self.inputs[x+1].enabled = True
            else:
                self.inputs[x+1].enabled = False
        if self.inputs[-1].is_linked:
            self.inputs[-1].enabled = True

    nl_class = "ULOrList"

    def get_input_names(self):
        return [
            "ca",
            "cb",
            "cc",
            "cd",
            "ce",
            "cf"
        ]
