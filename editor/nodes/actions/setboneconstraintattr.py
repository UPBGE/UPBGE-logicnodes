from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicBoneConstraint
from ...sockets import NodeSocketLogicValue


@node_type
class LogicNodeSetBoneConstraintAttr(LogicNodeActionType):
    bl_idname = "NLSetBoneConstraintAttribute"
    bl_label = "Set Attribute"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetBoneConstraintAttribute"

    search_tags = [
        ['Set Bone Constraint Attribute', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicArmature, "Armature")
        self.add_input(NodeSocketLogicBone, "", {'ref_index': 1})
        self.add_input(NodeSocketLogicBoneConstraint, "", {'ref_index': 2})
        self.add_input(NodeSocketLogicString, "Attribute")
        self.add_input(NodeSocketLogicValue, "")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return [
            "condition",
            "armature",
            "bone",
            "constraint",
            "attribute",
            "value",
        ]
