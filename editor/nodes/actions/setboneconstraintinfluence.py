from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicBoneConstraint
from ...sockets import NodeSocketLogicFloatFactor


@node_type
class LogicNodeSetBoneConstraintInfluence(LogicNodeActionType):
    bl_idname = "NLSetBoneConstraintInfluence"
    bl_label = "Set Influence"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetBoneConstraintInfluence"

    search_tags = [
        ['Set Bone Constraint Influence', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicArmature, "Armature")
        self.add_input(NodeSocketLogicBone, "", None, {'ref_index': 1})
        self.add_input(NodeSocketLogicBoneConstraint, "", None, {'ref_index': 2})
        self.add_input(NodeSocketLogicFloatFactor, "Influence")
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
            "influence"
        ]
