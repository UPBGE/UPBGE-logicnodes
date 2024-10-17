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
    bl_description = 'Set an attribute of an armature bone constraint by name'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetBoneConstraintAttribute"

    search_tags = [
        ['Set Bone Constraint Attribute', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicArmature, "Armature", 'armature')
        self.add_input(NodeSocketLogicBone, "", 'bone', {'ref_index': 1})
        self.add_input(NodeSocketLogicBoneConstraint, "", 'constraint', {'ref_index': 2})
        self.add_input(NodeSocketLogicString, "Attribute", 'attribute')
        self.add_input(NodeSocketLogicValue, "", 'value')
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
            "attribute",
            "value",
        ]
