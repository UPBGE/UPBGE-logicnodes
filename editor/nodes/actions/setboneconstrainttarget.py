from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicBoneConstraint
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeSetBoneConstraintTarget(LogicNodeActionType):
    bl_idname = "NLSetBoneConstraintTarget"
    bl_label = "Set Target"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetBoneConstraintTarget"

    search_tags = [
        ['Set Bone Constraint Target', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicArmature, "Armature")
        self.add_input(NodeSocketLogicBone, "", None, {'ref_index': 1})
        self.add_input(NodeSocketLogicBoneConstraint, "", None, {'ref_index': 2})
        self.add_input(NodeSocketLogicObject, "Target")
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
            "target"
        ]
