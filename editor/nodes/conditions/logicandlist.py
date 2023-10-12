from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type


@node_type
class LogicNodeLogicAndList(LogicNodeConditionType):
    bl_idname = "NLConditionAndList"
    bl_label = "And List"
    bl_width_min = 60
    bl_width_default = 100
    nl_module = 'uplogic.nodes.conditions'
    deprecated = True
    deprecation_message = 'Replaced by "Gate List" Node.'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "A")
        self.inputs[-1].default_value = "True"
        self.add_input(NodeSocketLogicCondition, "B")
        self.inputs[-1].default_value = "True"
        self.add_input(NodeSocketLogicCondition, "C")
        self.inputs[-1].default_value = "True"
        self.add_input(NodeSocketLogicCondition, "D")
        self.inputs[-1].default_value = "True"
        self.add_input(NodeSocketLogicCondition, "E")
        self.inputs[-1].default_value = "True"
        self.add_input(NodeSocketLogicCondition, "F")
        self.inputs[-1].default_value = "True"
        self.add_output(NodeSocketLogicCondition, "If All True")
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

    nl_class = "ULAndList"

    def get_input_names(self):
        return [
            "ca",
            "cb",
            "cc",
            "cd",
            "ce",
            "cf"
        ]
