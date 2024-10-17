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
    bl_description = 'Set the influence of an armature bone constraint'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetBoneConstraintInfluence"

    search_tags = [
        ['Set Bone Constraint Influence', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicArmature, "Armature", 'armature')
        self.add_input(NodeSocketLogicBone, "", 'bone', {'ref_index': 1})
        self.add_input(NodeSocketLogicBoneConstraint, "", 'constraint', {'ref_index': 2})
        self.add_input(NodeSocketLogicFloatFactor, "Influence", 'influence')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "armature",
            "bone",
            "constraint",
            "influence"
        ]
