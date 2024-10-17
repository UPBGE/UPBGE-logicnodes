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
    bl_description = 'Set the target of an armature bone constraint'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetBoneConstraintTarget"

    search_tags = [
        ['Set Bone Constraint Target', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicArmature, "Armature", 'armature')
        self.add_input(NodeSocketLogicBone, "", 'bone', {'ref_index': 1})
        self.add_input(NodeSocketLogicBoneConstraint, "", 'constraint', {'ref_index': 2})
        self.add_input(NodeSocketLogicObject, "Target", 'target')
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
            "target"
        ]
