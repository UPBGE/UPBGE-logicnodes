import bpy
from .interface import menu_item
from ..utilities import preferences


def draw_add_menu(self, context):
    if context.space_data.tree_type != "BGELogicTree":
        return
    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"

    # layout.operator('logic_nodes.node_search', text="Search", icon="VIEWZOOM")
    # layout.separator()
    if len(preferences().custom_logic_nodes) > 0:
        layout.menu("LN_MT_custom_menu", text="Custom Nodes", icon="RIGHTARROW_THIN")
        layout.separator()
    layout.menu("LN_MT_events_menu", text="Events", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_game_menu", text="Game", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_input_menu", text="Input", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_values_menu", text="Values", icon="RIGHTARROW_THIN")
    layout.separator()
    layout.menu("LN_MT_animation_menu", text="Animation", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_lights_menu", text="Lights", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_nodes_menu", text="Nodes", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_objects_menu", text="Objects", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_scene_menu", text="Scene", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_sound_menu", text="Sound", icon="RIGHTARROW_THIN")
    layout.separator()
    layout.menu("LN_MT_logic_menu", text="Logic", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_math_menu", text="Math", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_physics_menu", text="Physics", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_python_menu", text="Python", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_raycast_menu", text="Raycasts", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_time_menu", text="Time", icon="RIGHTARROW_THIN")
    layout.separator()
    layout.menu("LN_MT_data_menu", text="Data", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_file_menu", text="File", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_network_menu", text="Network", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_portal_menu", text="Portals", icon="RIGHTARROW_THIN")
    layout.separator()
    layout.menu("LN_MT_render_menu", text="Render", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_ui_menu", text="UI", icon="RIGHTARROW_THIN")
    layout.separator()
    layout.menu("LN_MT_layout_menu", text="Layout", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_utility_menu", text="Utility", icon="RIGHTARROW_THIN")


def insertNode(layout, type, text, icon="NONE", settings={}):
    operator = layout.operator("node.add_node", text=text, icon=icon)
    operator.type = type
    operator.use_transform = True
    for name, value in settings.items():
        item = operator.settings.add()
        item.name = name
        item.value = repr(value)
    return operator


def insertPortal(layout, text, mode='in', icon="NONE", settings={}):
    operator = layout.operator(f'logic_nodes.add_portal_{mode}', text=text, icon=icon)
    return operator


@menu_item
class CustomEventsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_custom_events_menu"
    bl_label = "Custom Events Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionCreateMessage", "Send Event")
        insertNode(layout, "NLParameterReceiveMessage", "Receive Event")


@menu_item
class EventsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_events_menu"
    bl_label = "Events Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLOnInitConditionNode", "On Init")
        insertNode(layout, "NLOnUpdateConditionNode", "On Update")
        insertNode(layout, "NLConditionNextFrameNode", "On Next Frame")
        insertNode(layout, "NLConditionValueTriggerNode", "On Value Changed To")
        insertNode(layout, "NLConditionValueChanged", "On Value Changed")
        insertNode(layout, "NLConditionOnceNode", "Once")
        layout.separator()
        layout.menu("LN_MT_custom_events_menu", text="Custom", icon="RIGHTARROW_THIN")


@menu_item
class GameMenu(bpy.types.Menu):
    bl_idname = "LN_MT_game_menu"
    bl_label = "Game Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionStartGame", "Load Blender File")
        insertNode(layout, "NLActionLoadGame", "Load Game")
        insertNode(layout, "NLActionEndGame", "Quit Game")
        insertNode(layout, "NLActionRestartGame", "Restart Game")
        insertNode(layout, "NLActionSaveGame", "Save Game")


@menu_item
class InputMenu(bpy.types.Menu):
    bl_idname = "LN_MT_input_menu"
    bl_label = "Input Menu"

    def draw(self, context):
        layout = self.layout
        layout.menu("LN_MT_mouse_menu", text="Mouse", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_keyboard_menu", text="Keyboard", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_gamepad_menu", text="Gamepad", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_vr_menu", text="VR", icon="RIGHTARROW_THIN")


@menu_item
class MouseMenu(bpy.types.Menu):
    bl_idname = "LN_MT_mouse_menu"
    bl_label = "Mouse Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLMousePressedCondition", "Mouse Button")
        insertNode(layout, "NLMouseDataParameter", "Mouse Wheel", settings={'mode': '2'})
        insertNode(layout, "NLMouseMovedCondition", "Mouse Moved")
        insertNode(layout, "NLConditionMouseTargetingNode", "Mouse Over")
        layout.separator()
        insertNode(layout, "NLActionSetMouseCursorVisibility", "Cursor Visibility")
        insertNode(layout, "NLMouseDataParameter", "Cursor Position", settings={'mode': '0'})
        insertNode(layout, "NLActionSetMousePosition", "Set Cursor Position")
        insertNode(layout, "NLMouseDataParameter", "Cursor Movement", settings={'mode': '1'})
        # insertNode(layout, "NLConditionMouseWheelMoved", "Wheel")
        layout.separator()
        insertNode(layout, "NLActionMouseLookNode", "Mouse Look")


@menu_item
class KeyboardMenu(bpy.types.Menu):
    bl_idname = "LN_MT_keyboard_menu"
    bl_label = "Keyboard Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLKeyPressedCondition", "Keyboard Key")
        # insertNode(layout, "NLKeyReleasedCondition", "Key Up")
        insertNode(layout, "NLKeyboardActive", "Keyboard Active")
        layout.separator()
        insertNode(layout, "NLParameterKeyboardKeyCode", "Key Code")
        insertNode(layout, "NLKeyLoggerAction", "Key Logger")


@menu_item
class GamepadMenu(bpy.types.Menu):
    bl_idname = "LN_MT_gamepad_menu"
    bl_label = "Gamepad Menu"

    def draw(self, context):
        layout = self.layout
        # insertNode(layout, "NLGamepadButtonUpCondition", "Button Up")
        insertNode(layout, "NLGamepadButtonsCondition", "Gamepad Button")
        insertNode(layout, "NLGamepadSticksCondition", "Gamepad Sticks")
        # insertNode(layout, "NLGamepadTriggerCondition", "Trigger")
        insertNode(layout, "NLGamepadActive", "Gamepad Active")
        layout.separator()
        insertNode(layout, "NLGamepadVibration", "Gamepad Vibrate")
        insertNode(layout, "NLGamepadLook", "Gamepad Look")


@menu_item
class VRMenu(bpy.types.Menu):
    bl_idname = "LN_MT_vr_menu"
    bl_label = "VR Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLGetVRHeadsetValues", "VR Headset")
        insertNode(layout, "NLGetVRControllerValues", "VR Controller")


@menu_item
class ValuesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_values_menu"
    bl_label = "Values Menu"

    def draw(self, context):
        layout = self.layout
        # layout.menu("LN_MT_simple_values_menu", text="Simple", icon="RIGHTARROW_THIN")
        insertNode(layout, "LogicNodeSimpleValue", "Boolean", settings={'value_type': '2'})
        insertNode(layout, "LogicNodeSimpleValue", "Float", settings={'value_type': '0'})
        insertNode(layout, "LogicNodeSimpleValue", "Integer", settings={'value_type': '1'})
        insertNode(layout, "LogicNodeSimpleValue", "String", settings={'value_type': '3'})
        layout.separator()
        insertNode(layout, "LogicNodeVector", "Vector")
        layout.separator()
        # layout.menu("LN_MT_global_values_menu", text="Global", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_vector_values_menu", text="Vector", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_property_menu", text="Properties", icon="RIGHTARROW_THIN")
        # layout.menu("LN_MT_random_values_menu", text="Random", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "LogicNodeRandomValue", "Random Value")
        insertNode(layout, "NLInvertValueNode", "Invert")
        insertNode(layout, "LogicNodeStringOperation", "String Operation")
        insertNode(layout, "NLParameterFormattedString", "Formatted String")
        insertNode(layout, "NLParameterFileValue", "File Path")
        layout.separator()
        insertNode(layout, "NLStoreValue", "Store Value")
        insertNode(layout, "NLValueSwitch", "Value Switch")
        insertNode(layout, "NLValueSwitchList", "Value Switch List")
        insertNode(layout, "NLValueSwitchListCompare", "Value Switch List Compare")
        # insertNode(layout, "NLConditionValueValidNode", "Value Valid")


@menu_item
class SimpleValuesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_simple_values_menu"
    bl_label = "Simple Values Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterBooleanValue", "Boolean")
        insertNode(layout, "NLParameterFloatValue", "Float")
        insertNode(layout, "NLParameterIntValue", "Integer")
        insertNode(layout, "NLParameterStringValue", "String")


@menu_item
class GlobalValuesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_global_values_menu"
    bl_label = "Global Values Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterGetGlobalValue", "Get Global Value")
        insertNode(layout, "NLActionSetGlobalValue", "Set Global Value")
        insertNode(layout, "NLActionListGlobalValues", "List Global Category")


@menu_item
class VectorValuesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_vector_values_menu"
    bl_label = "Vector Values Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterRGBNode", "Color RGB")
        insertNode(layout, "NLParameterRGBANode", "Color RGBA")
        insertNode(layout, "NLParameterVector2SplitNode", "Separate XY")
        insertNode(layout, "NLParameterVector3SplitNode", "Separate XYZ")
        insertNode(layout, "NLParameterVector2SimpleNode", "Combine XY")
        insertNode(layout, "NLParameterVector3SimpleNode", "Combine XYZ")
        insertNode(layout, "NLParameterVector4SimpleNode", "Combine XYZW")
        insertNode(layout, "NLParameterEulerSimpleNode", "Euler")
        insertNode(layout, "LogicNodeResizeVector", "Resize Vector")


@menu_item
class RandomValuesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_random_values_menu"
    bl_label = "Random Values Menu"

    def draw(self, context):
        layout = self.layout
        # insertNode(layout, "NLActionRandomFloat", "Random Float")
        # insertNode(layout, "NLActionRandomInteger", "Random Integer")
        # insertNode(layout, "NLRandomVect", "Random Vector")


@menu_item
class AnimationMenu(bpy.types.Menu):
    bl_idname = "LN_MT_animation_menu"
    bl_label = "Animation Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionPlayActionNode", "Play Animation")
        insertNode(layout, "NLActionStopAnimation", "Stop Animation")
        insertNode(layout, "NLActionSetAnimationFrame", "Set Animation Frame")
        insertNode(layout, "NLParameterActionStatus", "Animation Status")
        layout.separator()
        layout.menu("LN_MT_get_bone_data_menu", text="Get Bone Data", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_set_bone_data_menu", text="Set Bone Data", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_boneconstraints_menu", text="Bone Constraints", icon="RIGHTARROW_THIN")


@menu_item
class GetBoneDataMenu(bpy.types.Menu):
    bl_idname = "LN_MT_get_bone_data_menu"
    bl_label = "Get Bone Data"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Name", settings={'attribute': 'name'})
        layout.separator()
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Location", settings={'attribute': 'location'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Euler Rotation", settings={'attribute': 'pose_rotation_euler'})
        layout.separator()
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Head", settings={'attribute': 'head'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Local Head", settings={'attribute': 'head_local'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Pose Head", settings={'attribute': 'head_local'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Center", settings={'attribute': 'center'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Local Center", settings={'attribute': 'center_local'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Pose Center", settings={'attribute': 'center_local'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Tail", settings={'attribute': 'tail'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Local Tail", settings={'attribute': 'tail_local'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Pose Tail", settings={'attribute': 'tail_pose'})
        layout.separator()
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Inherit Scale", settings={'attribute': 'inherit_scale'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Inherit Rotation", settings={'attribute': 'inherit_rotation'})
        layout.separator()
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Connected", settings={'attribute': 'connected'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Deform", settings={'attribute': 'deform'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Local", settings={'attribute': 'use_local_location'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Relative Parent", settings={'attribute': 'use_relative_parent'})
        insertNode(layout, "LogicNodeGetRigBoneAttribute", "Get Bone Scale Easing", settings={'attribute': 'use_scale_easing'})


@menu_item
class SetBoneDataMenu(bpy.types.Menu):
    bl_idname = "LN_MT_set_bone_data_menu"
    bl_label = "Set Bone Data"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Location", settings={'attribute': 'location'})
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Euler Rotation", settings={'attribute': 'pose_rotation_euler'})
        layout.separator()
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Inherit Scale", settings={'attribute': 'inherit_scale'})
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Inherit Rotation", settings={'attribute': 'inherit_rotation'})
        layout.separator()
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Connected", settings={'attribute': 'connected'})
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Deform", settings={'attribute': 'deform'})
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Local", settings={'attribute': 'use_local_location'})
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Relative Parent", settings={'attribute': 'use_relative_parent'})
        insertNode(layout, "LogicNodeSetRigBoneAttribute", "Set Bone Scale Easing", settings={'attribute': 'use_scale_easing'})
        # insertNode(layout, "NLActionSetBonePos", "Set Bone Position")


@menu_item
class BoneConstraintsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_boneconstraints_menu"
    bl_label = "Bone Constraints Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLSetBoneConstraintAttribute", "Set Attribute")
        insertNode(layout, "NLSetBoneConstraintInfluence", "Set Influence")
        insertNode(layout, "NLSetBoneConstraintTarget", "Set Target")


@menu_item
class LightsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_lights_menu"
    bl_label = "Lights Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLGetLightColorAction", "Get Light Color")
        insertNode(layout, "NLGetLightEnergy", "Get Light Power")
        layout.separator()
        insertNode(layout, "NLSetLightColorAction", "Set Light Color")
        insertNode(layout, "NLSetLightEnergyAction", "Set Light Power")
        insertNode(layout, "NLSetLightShadowAction", "Set Light Shadow")
        layout.separator()
        insertNode(layout, "NLMakeUniqueLight", "Make Light Unique")


@menu_item
class NodesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_nodes_menu"
    bl_label = "Nodes Menu"

    def draw(self, context):
        layout = self.layout
        layout.menu("LN_MT_matnodes_menu", text="Materials", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_geonodes_menu", text="Geometry", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_groupnodes_menu", text="Groups", icon="RIGHTARROW_THIN")


@menu_item
class MatNodesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_matnodes_menu"
    bl_label = "Material Nodes Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLGetMaterialNode", "Get Node")
        insertNode(layout, "NLPlayMaterialSequence", "Play Sequence")
        layout.separator()
        insertNode(layout, "NLGetMaterialNodeValue", "Get Socket Value")
        insertNode(layout, "NLSetMaterialNodeValue", "Set Socket")
        layout.separator()
        insertNode(layout, "NLGetMaterialNodeAttribute", "Get Node Value")
        insertNode(layout, "NLSetMaterialNodeAttribute", "Set Node Value")


@menu_item
class GeoNodesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_geonodes_menu"
    bl_label = "Geometry Nodes Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLGetGeometryNodeValue", "Get Socket Value")
        insertNode(layout, "NLSetGeometryNodeValue", "Set Socket")
        layout.separator()
        insertNode(layout, "NLGetGeometryNodeAttribute", "Get Node Value")
        insertNode(layout, "NLSetGeometryNodeAttribute", "Set Node Value")


@menu_item
class GroupNodesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_groupnodes_menu"
    bl_label = "Node Groups Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLGetNodeGroupNodeValue", "Get Socket Value")
        insertNode(layout, "NLSetNodeTreeNodeValue", "Set Socket")
        layout.separator()
        insertNode(layout, "NLGetNodeTreeNodeAttribute", "Get Node Value")
        insertNode(layout, "NLSetNodeTreeNodeAttribute", "Set Node Value")


@menu_item
class ObjectsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_objects_menu"
    bl_label = "Objects Menu"

    def draw(self, context):
        layout = self.layout
        
        layout.menu("LN_MT_getattributes_menu", text="Get Attribute", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_setattributes_menu", text="Set Attribute", icon="RIGHTARROW_THIN")
        layout.separator()
        layout.menu("LN_MT_transform_menu", text="Transformation", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_object_data_menu", text="Object Data", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_curve_menu", text="Curves", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLAddObjectActionNode", "Add Object")
        insertNode(layout, "NLActionEndObjectNode", "Remove Object")
        insertNode(layout, "NLActionSetGameObjectVisibility", "Set Visibility")
        layout.separator()
        insertNode(layout, "NLActionFindObjectNode", "Get Object")
        insertNode(layout, "LogicNodeObjectByName", "Get Object By Name")
        # insertNode(layout, "NLOwnerGameObjectParameterNode", "Get Owner")
        insertNode(layout, "NLParameterFindChildByIndexNode", "Get Child By Index")
        insertNode(layout, "NLParameterFindChildByNameNode", "Get Child By Name")
        insertNode(layout, "NLParameterGameObjectParent", "Get Parent")
        insertNode(layout, "NLActionSetParentNode", "Set Parent")
        insertNode(layout, "NLActionRemoveParentNode", "Remove Parent")
        insertNode(layout, "NLSetMaterial", "Set Material")
        layout.separator()
        insertNode(layout, "NLActionSendMessage", "Send Message")
        insertNode(layout, "LogicNodeSpawnPool", "Spawn Pool")


@menu_item
class TransformMenu(bpy.types.Menu):
    bl_idname = "LN_MT_transform_menu"
    bl_label = "Transformation Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeApplyTransform", "Apply Movement")
        insertNode(layout, "LogicNodeApplyTransform", "Apply Rotation", settings={'mode': '1'})
        insertNode(layout, "LogicNodeApplyTransform", "Apply Force", settings={'mode': '2'})
        insertNode(layout, "LogicNodeApplyTransform", "Apply Torque", settings={'mode': '3'})
        insertNode(layout, "LogicNodeApplyTransform", "Apply Impulse", settings={'mode': '4'})
        layout.separator()
        insertNode(layout, "NLActionAlignAxisToVector", "Align Axis to Vector")
        insertNode(layout, "NLActionFollowPath", "Follow Path")
        insertNode(layout, "NLActionMoveTo", "Move To")
        insertNode(layout, "NLActionNavigate", "Move To with Navmesh")
        insertNode(layout, "NLActionRotateTo", "Rotate To")
        insertNode(layout, "NLSlowFollow", "Slow Follow")
        # insertNode(layout, "NLActionTranslate", "Translate")


@menu_item
class PropertyMenu(bpy.types.Menu):
    bl_idname = "LN_MT_property_menu"
    bl_label = "Properties Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeGetLogicTreeProperty", "Get Tree Property")
        insertNode(layout, "LogicNodeSetLogicTreeProperty", "Set Tree Property")
        layout.separator()
        insertNode(layout, "NLGameObjectPropertyParameterNode", "Get Object Property")
        insertNode(layout, "NLSetGameObjectGamePropertyActionNode", "Set Object Property")
        insertNode(layout, "NLGameObjectHasPropertyParameterNode", "Object Has Property")
        insertNode(layout, "NLToggleGameObjectGamePropertyActionNode", "Toggle Object Property")
        insertNode(layout, "NLAddToGameObjectGamePropertyActionNode", "Modify Object Property")
        insertNode(layout, "NLObjectPropertyOperator", "Evaluate Object Property")
        insertNode(layout, "NLCopyPropertyFromObject", "Copy Property From Object")
        layout.separator()
        insertNode(layout, "NLParameterGetGlobalValue", "Get Global Property")
        insertNode(layout, "NLActionSetGlobalValue", "Set Global Property")


@menu_item
class ObjectDataMenu(bpy.types.Menu):
    bl_idname = "LN_MT_object_data_menu"
    bl_label = "Object Data Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterAxisVector", "Get Axis Vector")
        insertNode(layout, "NLGetObjectDataName", "Get Object ID")
        insertNode(layout, "NLGetObjectVertices", "Get Vertices")
        # insertNode(layout, "NLObjectAttributeParameterNode", "Get Position / Rotation / Scale etc.")
        insertNode(layout, "NLActionReplaceMesh", "Replace Mesh")
        insertNode(layout, "LogicNodeSetConstraintAttribute", "Set Constraint Attribute")
        # insertNode(layout, "NLSetObjectAttributeActionNode", "Set Position / Rotation / Scale etc.")


@menu_item
class GetAttributesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_getattributes_menu"
    bl_label = "Get Attributes Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Position", settings={'attr_name': 'worldPosition', 'nl_label': 'Get World Position'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Orientation", settings={'attr_name': 'worldOrientation', 'nl_label': 'Get World Orientation'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Linear Velocity", settings={'attr_name': 'worldLinearVelocity', 'nl_label': 'Get World Linear Velocity'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Angular Velocity", settings={'attr_name': 'worldAngularVelocity', 'nl_label': 'Get World Angular Velocity'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Transform", settings={'attr_name': 'worldTransform', 'nl_label': 'Get World Transform'})
        layout.separator()
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Position", settings={'attr_name': 'localPosition', 'nl_label': 'Get Local Position'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Orientation", settings={'attr_name': 'localOrientation', 'nl_label': 'Get Local Orientation'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Linear Velocity", settings={'attr_name': 'localLinearVelocity', 'nl_label': 'Get Local Linear Velocity'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Angular Velocity", settings={'attr_name': 'localAngularVelocity', 'nl_label': 'Get Local Angular Velocity'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Transform", settings={'attr_name': 'localTransform', 'nl_label': 'Get Local Transform'})
        layout.separator()
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Name", settings={'attr_name': 'name', 'nl_label': 'Get Name'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Scale", settings={'attr_name': 'worldScale', 'nl_label': 'Get World Scale'})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Color", settings={'attr_name': 'color', 'nl_label': 'Get Color'})


@menu_item
class SetAttributesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_setattributes_menu"
    bl_label = "Set Attributes Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Position", settings={'value_type': 'worldPosition', 'nl_label': 'Set World Position'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Orientation", settings={'value_type': 'worldOrientation', 'nl_label': 'Set World Orientation'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Linear Velocity", settings={'value_type': 'worldLinearVelocity', 'nl_label': 'Set World Linear Velocity'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Angular Velocity", settings={'value_type': 'worldAngularVelocity', 'nl_label': 'Set World Angular Velocity'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Transform", settings={'value_type': 'worldTransform', 'nl_label': 'Set World Transform'})
        layout.separator()
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Position", settings={'value_type': 'localPosition', 'nl_label': 'Set Local Position'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Orientation", settings={'value_type': 'localOrientation', 'nl_label': 'Set Local Orientation'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Linear Velocity", settings={'value_type': 'localLinearVelocity', 'nl_label': 'Set Local Linear Velocity'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Angular Velocity", settings={'value_type': 'localAngularVelocity', 'nl_label': 'Set Local Angular Velocity'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Transform", settings={'value_type': 'localTransform', 'nl_label': 'Set Local Transform'})
        layout.separator()
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Scale", settings={'value_type': 'worldScale', 'nl_label': 'Set World Scale'})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Color", settings={'value_type': 'color', 'nl_label': 'Set Color'})


@menu_item
class CurveMenu(bpy.types.Menu):
    bl_idname = "LN_MT_curve_menu"
    bl_label = "Curves Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeDistributeCurvePoints", "Distribute Points on Curve")
        insertNode(layout, "LogicNodeEvaluateCurve", "Evaluate Curve")
        layout.separator()
        insertNode(layout, "NLGetCurvePoints", "Get Curve Points")
        insertNode(layout, "NLSetCurvePoints", "Set Curve Points")


@menu_item
class SceneMenu(bpy.types.Menu):
    bl_idname = "LN_MT_scene_menu"
    bl_label = "Scene Menu"

    def draw(self, context):
        layout = self.layout
        layout.menu("LN_MT_camera_menu", text="Camera", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_post_fx_menu", text="Post FX", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_collections_menu", text="Collections", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLGetScene", "Get Scene")
        insertNode(layout, "NLSetScene", "Set Scene")
        layout.separator()
        insertNode(layout, "NLParameterGetTimeScale", "Get Timescale")
        insertNode(layout, "NLActionSetTimeScale", "Set Timescale")
        # insertNode(layout, "NLSetCurvePoints", "Cursor Behaviour")


@menu_item
class CameraMenu(bpy.types.Menu):
    bl_idname = "LN_MT_camera_menu"
    bl_label = "Camera Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActiveCameraParameterNode", "Active Camera")
        insertNode(layout, "NLActionSetActiveCamera", "Set Camera")
        insertNode(layout, "NLActionSetCameraFov", "Set FOV")
        insertNode(layout, "NLActionSetCameraOrthoScale", "Set Orthographic Scale")
        insertNode(layout, "NLParameterScreenPosition", "World To Screen")
        insertNode(layout, "NLParameterWorldPosition", "Screen To World")


@menu_item
class PostFXMenu(bpy.types.Menu):
    bl_idname = "LN_MT_post_fx_menu"
    bl_label = "Post FX Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLAddFilter", "Add Filter")
        insertNode(layout, "NLRemoveFilter", "Remove Filter")
        insertNode(layout, "NLSetFilterState", "Set Filter State")
        insertNode(layout, "NLToggleFilter", "Toggle Filter")


@menu_item
class CollectionsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_collections_menu"
    bl_label = "Collection Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLGetCollectionNode", "Get Collection")
        insertNode(layout, "NLGetCollectionObjectNamesNode", "Get Object Names")
        insertNode(layout, "NLGetCollectionObjectsNode", "Get Objects")
        layout.separator()
        insertNode(layout, "NLActionSetCollectionVisibility", "Set Collection Visibility")
        insertNode(layout, "NLSetOverlayCollection", "Set Overlay Collection")
        insertNode(layout, "NLRemoveOverlayCollection", "Remove Overlay Collection")


@menu_item
class SoundMenu(bpy.types.Menu):
    bl_idname = "LN_MT_sound_menu"
    bl_label = "Sound Menu"

    def draw(self, context):
        layout = self.layout
        # insertNode(layout, "NLActionStartSound", "2D Sound")
        # insertNode(layout, "NLActionStart3DSoundAdv", "3D Sound")
        insertNode(layout, "LogicNodeStartSound", "Start Sound")
        insertNode(layout, "NLPlaySpeaker", "Start Speaker")
        layout.separator()
        insertNode(layout, "NLActionPauseSound", "Pause Sound")
        insertNode(layout, "NLActionResumeSound", "Resume Sound")
        insertNode(layout, "NLActionStopSound", "Stop Sound")
        insertNode(layout, "NLActionStopAllSounds", "Stop All Sounds")
        if preferences().use_fmod_nodes:
            layout.separator()
            layout.menu("LN_MT_fmod_sound_menu", text="FMOD", icon="RIGHTARROW_THIN")


@menu_item
class FMODSoundMenu(bpy.types.Menu):
    bl_idname = "LN_MT_fmod_sound_menu"
    bl_label = "FMOD"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeFModLoadBank", "Load Bank")
        insertNode(layout, "LogicNodeFModStartEvent", "Start Event Instance")
        layout.separator()
        insertNode(layout, "LogicNodeFModGetEventAttribute", "Get Event Instance Attribute")
        insertNode(layout, "LogicNodeFModSetEventAttribute", "Set Event Instance Attribute")
        layout.separator()
        insertNode(layout, "LogicNodeFModGetEventParameter", "Get Event Instance Parameter")
        insertNode(layout, "LogicNodeFModSetEventParameter", "Set Event Instance Parameter")
        insertNode(layout, "LogicNodeFModModifyEventParameter", "Modify Event Instance Parameter")


@menu_item
class LogicMenu(bpy.types.Menu):
    bl_idname = "LN_MT_logic_menu"
    bl_label = "Logic Menu"

    def draw(self, context):
        layout = self.layout
        layout.menu("LN_MT_logic_tree_menu", text="Trees", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_logic_brick_menu", text="Bricks", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "LogicNodeLogicGate", "Gate")
        insertNode(layout, "NLParameterSwitchValue", "Branch")
        layout.separator()
        insertNode(layout, "LogicNodeLogicGateList", "Gate List")
        insertNode(layout, "NLConditionNone", "None")
        insertNode(layout, "NLConditionNotNoneNode", "Not None")
        layout.separator()
        insertNode(layout, "LogicNodeLoop", "Loop")
        insertNode(layout, "LogicNodeLoopFromList", "Loop From List")


@menu_item
class LogicTreeMenu(bpy.types.Menu):
    bl_idname = "LN_MT_logic_tree_menu"
    bl_label = "Logic Tree Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLStartLogicNetworkActionNode", "Start Logic Tree")
        insertNode(layout, "NLActionExecuteNetwork", "Run Logic Tree")
        insertNode(layout, "NLStopLogicNetworkActionNode", "Stop Logic Tree")
        layout.separator()
        insertNode(layout, "NLActionInstallSubNetwork", "Add Logic Tree to Object")
        insertNode(layout, "NLConditionLogitNetworkStatusNode", "Logic Tree Status")


@menu_item
class LogicBrickMenu(bpy.types.Menu):
    bl_idname = "LN_MT_logic_brick_menu"
    bl_label = "Logic Brick Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLSensorValueNode", "Get Sensor Value")
        insertNode(layout, "NLSetSensorValueNode", "Set Sensor Value")
        insertNode(layout, "NLGetActuatorValue", "Get Actuator Value")
        insertNode(layout, "NLSetActuatorValueNode", "Set Actuator Value")
        layout.separator()
        insertNode(layout, "NLControllerStatus", "Controller Status")
        # insertNode(layout, "NLRunActuatorNode", "Run Actuator")
        insertNode(layout, "NLGetSensorNode", "Sensor Positive")


@menu_item
class MathMenu(bpy.types.Menu):
    bl_idname = "LN_MT_math_menu"
    bl_label = "Math Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeMath", "Math")
        insertNode(layout, "NLParameterMathFun", "Formula")
        insertNode(layout, "LogicNodeVectorMath", "Vector Math")
        insertNode(layout, "LogicNodeRotateByPoint", "Vector Rotate")
        layout.separator()
        insertNode(layout, "NLClampValueNode", "Clamp")
        insertNode(layout, "NLConditionLogicOperation", "Compare")
        insertNode(layout, "NLMapRangeNode", "Map Range")
        layout.separator()
        insertNode(layout, "LogicNodeCurveInterpolation", "Curve Interpolation")
        insertNode(layout, "LogicNodeTweenValue", "Tween Value")
        insertNode(layout, "NLThresholdNode", "Threshold")
        insertNode(layout, "NLRangedThresholdNode", "Ranged Threshold")
        insertNode(layout, "NLLimitRange", "Limit Range")
        insertNode(layout, "NLWithinRangeNode", "Within Range")
        layout.separator()
        insertNode(layout, "NLParameterEulerToMatrixNode", "XYZ to Matrix")
        insertNode(layout, "NLParameterMatrixToEulerNode", "Matrix to XYZ")


@menu_item
class PhysicsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_physics_menu"
    bl_label = "Physics Menu"

    def draw(self, context):
        layout = self.layout
        layout.menu("LN_MT_vehicle_menu", text="Vehicle", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_character_menu", text="Character", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLConditionCollisionNode", "Collision")
        insertNode(layout, "LogicNodeGetCollisionBitMask", "Get Collision Mask", settings={'mode': '1'})
        insertNode(layout, "NLSetCollisionGroup", "Set Collision Mask", settings={'mode': '1'})
        insertNode(layout, "LogicNodeGetCollisionBitMask", "Get Collision Group")
        insertNode(layout, "NLSetCollisionGroup", "Set Collision Group")
        layout.separator()
        insertNode(layout, "NLActionAddPhysicsConstraint", "Add Physics Constraint")
        insertNode(layout, "NLActionRemovePhysicsConstraint", "Remove Physics Constraint")
        layout.separator()
        insertNode(layout, "NLGetGravityNode", "Get Gravity")
        insertNode(layout, "NLActionSetGravity", "Set Gravity")
        insertNode(layout, "NLActionSetPhysicsNode", "Set Physics")
        insertNode(layout, "NLActionSetDynamicsNode", "Set Dynamics")
        insertNode(layout, "NLSetRigidBody", "Set Rigid Body")


@menu_item
class VehicleMenu(bpy.types.Menu):
    bl_idname = "LN_MT_vehicle_menu"
    bl_label = "Vehicle Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLCreateVehicleFromParent", "Create New Vehicle")
        layout.separator()
        insertNode(layout, "NLVehicleApplyEngineForce", "Accelerate")
        insertNode(layout, "NLVehicleApplyBraking", "Brake")
        insertNode(layout, "NLVehicleSetAttributes", "Set Vehicle Attributes")
        insertNode(layout, "NLVehicleApplySteering", "Steer")


@menu_item
class CharacterMenu(bpy.types.Menu):
    bl_idname = "LN_MT_character_menu"
    bl_label = "Character Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionSetCharacterWalkDir", "Walk")
        insertNode(layout, "NLActionCharacterJump", "Jump")
        layout.separator()
        insertNode(layout, "NLActionGetCharacterInfo", "Get Physics Info")
        insertNode(layout, "NLSetCharacterJumpSpeed", "Set Jump Force")
        insertNode(layout, "NLSetActionCharacterJump", "Set Max Jumps")
        insertNode(layout, "NLActionSetCharacterGravity", "Set Gravity")
        insertNode(layout, "NLActionSetCharacterVelocity", "Set Velocity")


@menu_item
class PythonMenu(bpy.types.Menu):
    bl_idname = "LN_MT_python_menu"
    bl_label = "Python Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterPythonModuleFunction", "Run Python Code")
        layout.separator()
        insertNode(layout, "NLParameterGetAttribute", "Get Instance Attribute")
        insertNode(layout, "NLParameterSetAttribute", "Set Object Attribute")
        insertNode(layout, "NLParameterTypeCast", "Typecast Value")


@menu_item
class RaycastMenu(bpy.types.Menu):
    bl_idname = "LN_MT_raycast_menu"
    bl_label = "Raycast Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionRayCastNode", "Raycast")
        insertNode(layout, "NLActionMousePickNode", "Mouse Ray")
        insertNode(layout, "NLActionCameraPickNode", "Camera Ray")
        insertNode(layout, "NLProjectileRayCast", "Projectile Ray")


@menu_item
class TimeMenu(bpy.types.Menu):
    bl_idname = "LN_MT_time_menu"
    bl_label = "Time Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterTimeNode", "Time")
        insertNode(layout, "NLParameterTimeNode", "Delta (Frametime)")
        insertNode(layout, "NLParameterTimeNode", "FPS")
        insertNode(layout, "LogicNodeTimeFactor", "Delta Factor")
        layout.separator()
        insertNode(layout, "NLActionTimeDelay", "Delay")
        insertNode(layout, "NLConditionTimeElapsed", "Timer")
        insertNode(layout, "NLActionTimeFilter", "Pulsify")
        insertNode(layout, "NLActionTimeBarrier", "Barrier")


@menu_item
class FileMenu(bpy.types.Menu):
    bl_idname = "LN_MT_file_menu"
    bl_label = "File Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeGetFont", "Get Font")
        insertNode(layout, "NLGetImage", "Get Image")
        insertNode(layout, "NLGetSound", "Get Sound")


@menu_item
class NetworkMenu(bpy.types.Menu):
    bl_idname = "LN_MT_network_menu"
    bl_label = "File Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeLocalServer", "LAN Server")
        insertNode(layout, "LogicNodeLocalClient", "LAN Client")
        layout.separator()
        insertNode(layout, "LogicNodeRebuildData", "Rebuild Data")
        insertNode(layout, "LogicNodeSendNetworkMessage", "Send Data")
        insertNode(layout, "LogicNodeSerializeData", "Serialize Data")
        layout.separator()
        insertNode(layout, "LogicNodeOSCSetupServer", "Setup OSC Server")
        insertNode(layout, "LogicNodeOSCReceive", "Receive OSC Message")
        insertNode(layout, "LogicNodeOSCSend", "Send OSC Message")

@menu_item
class PathMenu(bpy.types.Menu):
    bl_idname = "LN_MT_path_menu"
    bl_label = "Path"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeGetMasterFolder", "Get Master Folder")
        insertNode(layout, "LogicNodeJoinPath", "Join Path")


@menu_item
class DataMenu(bpy.types.Menu):
    bl_idname = "LN_MT_data_menu"
    bl_label = "Data Menu"

    def draw(self, context):
        layout = self.layout
        layout.menu("LN_MT_list_menu", text="List", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_dict_menu", text="Dict", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_variable_menu", text="Variables", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLLoadScene", "Load Scene")
        insertNode(layout, "NLLoadFileContent", "Load File Content")
        layout.separator()
        layout.menu("LN_MT_path_menu", text="Path", icon="RIGHTARROW_THIN")


@menu_item
class PortalMenu(bpy.types.Menu):
    bl_idname = "LN_MT_portal_menu"
    bl_label = "Portal Menu"

    def draw(self, context):
        layout = self.layout
        insertPortal(layout, "Portal In", 'in')
        # insertPortal(layout, "Portal Out", 'out')
        if len(context.scene.nl_portals):
            layout.separator()
        for portal in context.scene.nl_portals:
            insertNode(layout, "LogicNodeGetPortal", f"{portal.name}", settings={'portal': portal.name, 'hide': True, 'nl_label': portal.name})


@menu_item
class ListMenu(bpy.types.Menu):
    bl_idname = "LN_MT_list_menu"
    bl_label = "List Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLInitEmptyList", "New List")
        insertNode(layout, "LogicNodeListFromItems", "List From Items")
        layout.separator()
        insertNode(layout, "NLAppendListItem", "Append")
        insertNode(layout, "NLExtendList", "Extend")
        insertNode(layout, "NLRemoveListIndex", "Remove Index")
        insertNode(layout, "NLRemoveListValue", "Remove Value")
        layout.separator()
        insertNode(layout, "NLGetListIndexNode", "Get List Index")
        insertNode(layout, "NLSetListIndex", "Set List Index")
        insertNode(layout, "NLGetRandomListIndex", "Get Random List Item")
        insertNode(layout, "NLDuplicateList", "Duplicate")


@menu_item
class DictMenu(bpy.types.Menu):
    bl_idname = "LN_MT_dict_menu"
    bl_label = "Dictionary Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLInitEmptyDict", "New Dictionary")
        insertNode(layout, "NLInitNewDict", "Dictionary From Items")
        layout.separator()
        insertNode(layout, "NLGetDictKeyNode", "Get Dictionary Key")
        insertNode(layout, "NLSetDictKeyValue", "Set Dictionary Key")
        insertNode(layout, "NLSetDictDelKey", "Remove Dictionary Key")
        layout.separator()
        insertNode(layout, "LogicNodeDictGetKeys", "Get Dictionary Keys")
        # insertNode(layout, "NLGetDictKeyNode", "Get Dictionary Key")


@menu_item
class VariableMenu(bpy.types.Menu):
    bl_idname = "LN_MT_variable_menu"
    bl_label = "Variable Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionLoadVariable", "Load Variable")
        insertNode(layout, "NLActionSaveVariable", "Save Variable")
        insertNode(layout, "NLActionRemoveVariable", "Remove Variable")
        layout.separator()
        insertNode(layout, "NLActionLoadVariables", "Load Variable Dict")
        insertNode(layout, "NLActionSaveVariables", "Save Variable Dict")
        insertNode(layout, "NLActionClearVariables", "Clear Variables")
        layout.separator()
        insertNode(layout, "NLActionListVariables", "List Saved Variables")


@menu_item
class LayoutMenu(bpy.types.Menu):
    bl_idname = "LN_MT_layout_menu"
    bl_label = "Layout Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NodeReroute", "Reroute")
        insertNode(layout, "NodeFrame", "Frame")


@menu_item
class RenderMenu(bpy.types.Menu):
    bl_idname = "LN_MT_render_menu"
    bl_label = "Render Menu"

    def draw(self, context):
        layout = self.layout
        # layout.menu("LN_MT_eevee_menu", text="EEVEE", icon="RIGHTARROW_THIN")
        insertNode(layout, "NLGetFullscreen", "Get Fullscreen")
        insertNode(layout, "NLActionSetFullscreen", "Set Fullscreen")
        insertNode(layout, "NLGetResolution", "Get Resolution")
        insertNode(layout, "NLActionSetResolution", "Set Resolution")
        insertNode(layout, "NLGetVsyncNode", "Get VSync")
        insertNode(layout, "NLActionSetVSync", "Set VSync")
        layout.separator()
        insertNode(layout, "NLShowFramerate", "Show Framerate")
        insertNode(layout, "NLSetProfile", "Show Profile")


@menu_item
class DrawMenu(bpy.types.Menu):
    bl_idname = "LN_MT_draw_menu"
    bl_label = "Draw Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLDrawLine", "Line")
        insertNode(layout, "NLDrawCube", "Cube")
        insertNode(layout, "NLDrawBox", "Box")


@menu_item
class EeveeMenu(bpy.types.Menu):
    bl_idname = "LN_MT_eevee_menu"
    bl_label = "EEVEE Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLSetEeveeAO", "Set Ambient Occlusion")
        insertNode(layout, "NLSetEeveeBloom", "Set Bloom")
        insertNode(layout, "NLSetExposureAction", "Set Exposure")
        insertNode(layout, "NLSetGammaAction", "Set Gamma")
        insertNode(layout, "NLSetEeveeSSR", "Set SSR")
        insertNode(layout, "NLSetEeveeVolumetrics", "Set Volumetric Light")


@menu_item
class UIMenu(bpy.types.Menu):
    bl_idname = "LN_MT_ui_menu"
    bl_label = "UI Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeCreateUICanvas", "Create Canvas")
        layout.separator()
        layout.menu("LN_MT_widget_menu", text="Widgets", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "LogicNodeAddUIWidget", "Add Widget")
        insertNode(layout, "LogicNodeGetUIWidgetAttr", "Get Widget Attribute")
        insertNode(layout, "LogicNodeSetUIWidgetAttr", "Set Widget Attribute")
        layout.separator()
        insertNode(layout, "LogicNodeSetCustomCursor", "Set Custom Cursor")


@menu_item
class WidgetMenu(bpy.types.Menu):
    bl_idname = "LN_MT_widget_menu"
    bl_label = "Widget Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeCreateUILayout", "Create Layout")
        layout.separator()
        insertNode(layout, "LogicNodeCreateUIButton", "Create Button")
        insertNode(layout, "LogicNodeCreateUILabel", "Create Label")
        insertNode(layout, "LogicNodeCreateUIImage", "Create Image")
        insertNode(layout, "LogicNodeCreateUISliderWidget", "Create Slider")
        insertNode(layout, "LogicNodeCreateUIPath", "Create Path")


@menu_item
class UtilityMenu(bpy.types.Menu):
    bl_idname = "LN_MT_utility_menu"
    bl_label = "Utility Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionPrint", "Print")
        insertNode(layout, "LogicNodeDraw", "Draw")


@menu_item
class CustomMenu(bpy.types.Menu):
    bl_idname = "LN_MT_custom_menu"
    bl_label = "Custom Menu"

    def draw(self, context):
        layout = self.layout
        for node in preferences().custom_logic_nodes:
            insertNode(layout, node.idname, node.label)
