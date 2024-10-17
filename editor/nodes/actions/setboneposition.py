from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeSetBonePosition(LogicNodeActionType):
    bl_idname = "NLActionSetBonePos"
    bl_label = "Set Bone Position"
    bl_description = 'Set the position of an armature bone'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetBonePosition"
    deprecated = True
    deprecation_message = 'Replaced by "Set Bone Attribute" node'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicArmature, "Armature", 'armature')
        self.add_input(NodeSocketLogicBone, "Bone Name", 'bone_name', {'ref_index': 1})
        self.add_input(NodeSocketLogicVectorXYZ, "Set Pos", 'set_translation')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "armature", "bone_name", "set_translation"]
