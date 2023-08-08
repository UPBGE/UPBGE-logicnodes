import bpy


_items = []

def menu_item(obj):
    global _items
    _items.append(obj)


def draw_add_menu(self, context):
    if context.space_data.tree_type != "BGELogicTree":
        return
    layout = self.layout
    layout.operator_context = "INVOKE_DEFAULT"

    layout.operator('bge_netlogic.node_search', text="Search", icon="VIEWZOOM")
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
    layout.menu("LN_MT_raycast_menu", text="Ray Casts", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_time_menu", text="Time", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_python_menu", text="Python", icon="RIGHTARROW_THIN")
    layout.separator()
    layout.menu("LN_MT_file_menu", text="File", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_network_menu", text="Network", icon="RIGHTARROW_THIN")
    layout.menu("LN_MT_data_menu", text="Data", icon="RIGHTARROW_THIN")
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
        item.value = value
    return operator


@menu_item
class CustomEventsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_custom_events_menu"
    bl_label = "Custom Events Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionCreateMessage", "Send")
        insertNode(layout, "NLParameterReceiveMessage", "Receive")


@menu_item
class EventsMenu(bpy.types.Menu):
    bl_idname = "LN_MT_events_menu"
    bl_label = "Events Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLOnInitConditionNode", "On Init")
        insertNode(layout, "NLOnUpdateConditionNode", "On Update")
        insertNode(layout, "NLConditionNextFrameNode", "On Next Tick")
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
        insertNode(layout, "NLActionStartGame", "Load File")
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
        insertNode(layout, "NLMousePressedCondition", "Button Down")
        insertNode(layout, "NLMouseReleasedCondition", "Button Up")
        insertNode(layout, "NLConditionMousePressedOn", "Button Over")
        insertNode(layout, "NLActionSetMouseCursorVisibility", "Cursor Visibility")
        insertNode(layout, "NLActionMouseLookNode", "Mouse Look")
        insertNode(layout, "NLMouseDataParameter", "Mouse Status")
        insertNode(layout, "NLMouseMovedCondition", "Moved")
        insertNode(layout, "NLConditionMouseTargetingNode", "Over")
        insertNode(layout, "NLActionSetMousePosition", "Set Position")
        insertNode(layout, "NLConditionMouseWheelMoved", "Wheel")


@menu_item
class KeyboardMenu(bpy.types.Menu):
    bl_idname = "LN_MT_keyboard_menu"
    bl_label = "Keyboard Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLKeyboardActive", "Keyboard Active")
        insertNode(layout, "NLKeyPressedCondition", "Key Down")
        insertNode(layout, "NLKeyReleasedCondition", "Key Up")
        insertNode(layout, "NLParameterKeyboardKeyCode", "Key Code")
        insertNode(layout, "NLKeyLoggerAction", "Logger")


@menu_item
class GamepadMenu(bpy.types.Menu):
    bl_idname = "LN_MT_gamepad_menu"
    bl_label = "Gamepad Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLGamepadActive", "Gamepad Active")
        insertNode(layout, "NLGamepadButtonsCondition", "Button Down")
        insertNode(layout, "NLGamepadButtonUpCondition", "Button Up")
        insertNode(layout, "NLGamepadLook", "Gamepad Look")
        insertNode(layout, "NLGamepadSticksCondition", "Sticks")
        insertNode(layout, "NLGamepadTriggerCondition", "Trigger")
        insertNode(layout, "NLGamepadVibration", "Vibration")


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
        layout.menu("LN_MT_simple_values_menu", text="Simple", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_global_values_menu", text="Global", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_vector_values_menu", text="Vector", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_random_values_menu", text="Random", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLParameterFileValue", "File Path")
        insertNode(layout, "NLParameterFormattedString", "Formatted String")
        insertNode(layout, "NLInvertValueNode", "Invert")
        insertNode(layout, "NLStoreValue", "Store Value")
        insertNode(layout, "NLValueSwitch", "Value Switch")
        insertNode(layout, "NLValueSwitchList", "Value Switch List")
        insertNode(layout, "NLValueSwitchListCompare", "Value Switch List Compare")
        insertNode(layout, "NLConditionValueValidNode", "Value Valid")


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
        insertNode(layout, "NLParameterVector2SimpleNode", "Vector XY")
        insertNode(layout, "NLParameterVector3SimpleNode", "Vector XYZ")
        insertNode(layout, "NLParameterVector4SimpleNode", "Vector XYZW")
        insertNode(layout, "NLParameterEulerSimpleNode", "Euler")


@menu_item
class RandomValuesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_random_values_menu"
    bl_label = "Random Values Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionRandomFloat", "Random Float")
        insertNode(layout, "NLActionRandomInteger", "Random Integer")
        insertNode(layout, "NLRandomVect", "Random Vector")


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
        layout.menu("LN_MT_armature_rig_menu", text="Armature / Rig", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_boneconstraints_menu", text="Bone Constraints", icon="RIGHTARROW_THIN")


@menu_item
class ArmatureRigMenu(bpy.types.Menu):
    bl_idname = "LN_MT_armature_rig_menu"
    bl_label = "Armature / Rig Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterBoneStatus", "Bone Status")
        insertNode(layout, "NLActionEditBoneNode", "Edit Bone")
        insertNode(layout, "NLActionSetBonePos", "Set Bone Position")


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
        insertNode(layout, "NLSetLightColorAction", "Set Light Color")
        insertNode(layout, "NLGetLightEnergy", "Get Light Energy")
        insertNode(layout, "NLSetLightEnergyAction", "Set Light Energy")
        insertNode(layout, "NLSetLightShadowAction", "Set Light Shadow")
        insertNode(layout, "NLMakeUniqueLight", "Make Unique")


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
        insertNode(layout, "NLSetMaterial", "Set Material")
        insertNode(layout, "NLGetMaterialNode", "Get Node")
        insertNode(layout, "NLPlayMaterialSequence", "Play Sequence")
        layout.separator()
        insertNode(layout, "NLGetMaterialNodeValue", "Get Socket Value")
        insertNode(layout, "NLSetMaterialNodeValue", "Set Socket Value")
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
        insertNode(layout, "NLSetGeometryNodeValue", "Set Socket Value")
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
        insertNode(layout, "NLSetNodeTreeNodeValue", "Set Socket Value")
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
        layout.menu("LN_MT_property_menu", text="Properties", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_object_data_menu", text="Object Data", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_curve_menu", text="Curves", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLAddObjectActionNode", "Add Object")
        insertNode(layout, "NLActionEndObjectNode", "Remove Object")
        insertNode(layout, "NLActionSetGameObjectVisibility", "Set Visibility")
        layout.separator()
        insertNode(layout, "NLActionFindObjectNode", "Get Object")
        insertNode(layout, "NLOwnerGameObjectParameterNode", "Get Owner")
        insertNode(layout, "NLParameterFindChildByIndexNode", "Get Child By Index")
        insertNode(layout, "NLParameterFindChildByNameNode", "Get Child By Name")
        insertNode(layout, "NLParameterGameObjectParent", "Get Parent")
        insertNode(layout, "NLActionSetParentNode", "Set Parent")
        insertNode(layout, "NLActionRemoveParentNode", "Remove Parent")
        layout.separator()
        insertNode(layout, "NLActionSendMessage", "Send Message")
        insertNode(layout, "LogicNodeSpawnPool", "Spawn Pool")


@menu_item
class TransformMenu(bpy.types.Menu):
    bl_idname = "LN_MT_transform_menu"
    bl_label = "Transformation Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionApplyLocation", "Apply Movement")
        insertNode(layout, "NLActionApplyRotation", "Apply Rotation")
        insertNode(layout, "NLActionApplyForce", "Apply Force")
        insertNode(layout, "NLActionApplyTorque", "Apply Torque")
        insertNode(layout, "NLActionApplyImpulse", "Apply Impulse")
        layout.separator()
        insertNode(layout, "NLActionAlignAxisToVector", "Align Axis to Vector")
        insertNode(layout, "NLActionFollowPath", "Follow Path")
        insertNode(layout, "NLActionMoveTo", "Move To")
        insertNode(layout, "NLActionNavigate", "Move To with Navmesh")
        insertNode(layout, "NLActionRotateTo", "Rotate To")
        insertNode(layout, "NLSlowFollow", "Slow Follow")
        insertNode(layout, "NLActionTranslate", "Translate")


@menu_item
class PropertyMenu(bpy.types.Menu):
    bl_idname = "LN_MT_property_menu"
    bl_label = "Properties Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLGameObjectPropertyParameterNode", "Get Property")
        insertNode(layout, "NLSetGameObjectGamePropertyActionNode", "Set Property")
        insertNode(layout, "NLGameObjectHasPropertyParameterNode", "Has Property")
        insertNode(layout, "NLToggleGameObjectGamePropertyActionNode", "Toggle Property")
        insertNode(layout, "NLAddToGameObjectGamePropertyActionNode", "Modify Property")
        insertNode(layout, "NLClampedModifyProperty", "Clamped Modify Property")
        insertNode(layout, "NLObjectPropertyOperator", "Evaluate Property")
        insertNode(layout, "NLCopyPropertyFromObject", "Copy From Object")


@menu_item
class ObjectDataMenu(bpy.types.Menu):
    bl_idname = "LN_MT_object_data_menu"
    bl_label = "Object Data Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterAxisVector", "Get Axis Vector")
        insertNode(layout, "NLGetObjectDataName", "Get Internal Name")
        insertNode(layout, "NLGetObjectVertices", "Get Vertices")
        # insertNode(layout, "NLObjectAttributeParameterNode", "Get Position / Rotation / Scale etc.")
        insertNode(layout, "NLActionReplaceMesh", "Replace Mesh")
        # insertNode(layout, "NLSetObjectAttributeActionNode", "Set Position / Rotation / Scale etc.")


@menu_item
class GetAttributesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_getattributes_menu"
    bl_label = "Get Attributes Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Position", settings={'attr_name': repr('worldPosition'), 'label': repr('Get Position')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Rotation", settings={'attr_name': repr('worldOrientation'), 'label': repr('Get Rotation')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Linear Velocity", settings={'attr_name': repr('worldLinearVelocity'), 'label': repr('Get Linear Velocity')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Angular Velocity", settings={'attr_name': repr('worldAngularVelocity'), 'label': repr('Get Angular Velocity')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get World Transform", settings={'attr_name': repr('worldTransform'), 'label': repr('Get Transform')})
        layout.separator()
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Position", settings={'attr_name': repr('localPosition'), 'label': repr('Get Position')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Rotation", settings={'attr_name': repr('localOrientation'), 'label': repr('Get Rotation')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Linear Velocity", settings={'attr_name': repr('localLinearVelocity'), 'label': repr('Get Linear Velocity')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Angular Velocity", settings={'attr_name': repr('localAngularVelocity'), 'label': repr('Get Angular Velocity')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Local Transform", settings={'attr_name': repr('localTransform'), 'label': repr('Get Transform')})
        layout.separator()
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Name", settings={'attr_name': repr('name'), 'label': repr('Get Name')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Scale", settings={'attr_name': repr('worldScale'), 'label': repr('Get Scale')})
        insertNode(layout, "NLObjectAttributeParameterNode", "Get Color", settings={'attr_name': repr('color'), 'label': repr('Get Color')})


@menu_item
class SetAttributesMenu(bpy.types.Menu):
    bl_idname = "LN_MT_setattributes_menu"
    bl_label = "Get Attributes Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Position", settings={'value_type': repr('worldPosition'), 'label': repr('Set Position')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Rotation", settings={'value_type': repr('worldOrientation'), 'label': repr('Set Rotation')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Linear Velocity", settings={'value_type': repr('worldLinearVelocity'), 'label': repr('Set Linear Velocity')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Angular Velocity", settings={'value_type': repr('worldAngularVelocity'), 'label': repr('Set Angular Velocity')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set World Transform", settings={'value_type': repr('worldTransform'), 'label': repr('Set Transform')})
        layout.separator()
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Position", settings={'value_type': repr('localPosition'), 'label': repr('Set Position')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Rotation", settings={'value_type': repr('localOrientation'), 'label': repr('Set Rotation')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Linear Velocity", settings={'value_type': repr('localLinearVelocity'), 'label': repr('Set Linear Velocity')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Angular Velocity", settings={'value_type': repr('localAngularVelocity'), 'label': repr('Set Angular Velocity')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Local Transform", settings={'value_type': repr('localTransform'), 'label': repr('Set Transform')})
        layout.separator()
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Scale", settings={'value_type': repr('worldScale'), 'label': repr('Set Scale')})
        insertNode(layout, "NLSetObjectAttributeActionNode", "Set Color", settings={'value_type': repr('color'), 'label': repr('Set Color')})


@menu_item
class CurveMenu(bpy.types.Menu):
    bl_idname = "LN_MT_curve_menu"
    bl_label = "Curves Menu"

    def draw(self, context):
        layout = self.layout
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
        insertNode(layout, "NLLoadScene", "Load Scene")
        layout.separator()
        insertNode(layout, "NLGetGravityNode", "Get Gravity")
        insertNode(layout, "NLActionSetGravity", "Set Gravity")
        insertNode(layout, "NLParameterGetTimeScale", "Get Timescale")
        insertNode(layout, "NLActionSetTimeScale", "Set Timescale")
        # insertNode(layout, "NLSetCurvePoints", "Cursor Behaviour")


@menu_item
class CameraMenu(bpy.types.Menu):
    bl_idname = "LN_MT_camera_menu"
    bl_label = "Camera Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActiveCameraParameterNode", "Get Active Camera")
        insertNode(layout, "NLActionSetActiveCamera", "Set Active Camera")
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
        insertNode(layout, "NLRemoveOverlayCollection", "Remove Overlay Collections")


@menu_item
class SoundMenu(bpy.types.Menu):
    bl_idname = "LN_MT_sound_menu"
    bl_label = "Sound Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionStartSound", "2D Sound")
        insertNode(layout, "NLActionStart3DSoundAdv", "3D Sound")
        insertNode(layout, "NLActionPauseSound", "Pause Sound")
        insertNode(layout, "NLActionResumeSound", "Resume Sound")
        insertNode(layout, "NLPlaySpeaker", "Start Speaker")
        insertNode(layout, "NLActionStopAllSounds", "Stop All Sounds")
        insertNode(layout, "NLActionStopSound", "Stop Sound")


@menu_item
class LogicMenu(bpy.types.Menu):
    bl_idname = "LN_MT_logic_menu"
    bl_label = "Logic Menu"

    def draw(self, context):
        layout = self.layout
        layout.menu("LN_MT_logic_tree_menu", text="Trees", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_logic_brick_menu", text="Bricks", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLConditionAndNode", "And")
        insertNode(layout, "NLConditionAndList", "And List")
        insertNode(layout, "NLConditionAndNotNode", "And Not")
        insertNode(layout, "NLConditionNone", "None")
        insertNode(layout, "NLConditionNotNode", "Not")
        insertNode(layout, "NLConditionNotNoneNode", "Not None")
        insertNode(layout, "NLConditionOrNode", "Or")
        insertNode(layout, "NLConditionOrList", "Or List")
        insertNode(layout, "NLParameterSwitchValue", "True / False")


@menu_item
class LogicTreeMenu(bpy.types.Menu):
    bl_idname = "LN_MT_logic_tree_menu"
    bl_label = "Logic Tree Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLStartLogicNetworkActionNode", "Start Logic Tree")
        insertNode(layout, "NLActionExecuteNetwork", "Execute Logic Tree")
        insertNode(layout, "NLStopLogicNetworkActionNode", "Stop Logic Tree")
        layout.separator()
        insertNode(layout, "NLActionInstallSubNetwork", "Add Logic Tree to Object")
        insertNode(layout, "NLConditionLogitNetworkStatusNode", "Logic Network Status")


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
        insertNode(layout, "NLRunActuatorNode", "Run Actuator")
        insertNode(layout, "NLGetSensorNode", "Sensor Positive")


@menu_item
class MathMenu(bpy.types.Menu):
    bl_idname = "LN_MT_math_menu"
    bl_label = "Math Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLArithmeticOpParameterNode", "Math")
        insertNode(layout, "NLVectorMath", "Vector Math")
        layout.menu("LN_MT_vector_math_menu", text="Vectors", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLInterpolateValueNode", "Interpolate")
        insertNode(layout, "NLAbsoluteValue", "Absolute")
        insertNode(layout, "NLClampValueNode", "Clamp")
        insertNode(layout, "NLConditionLogicOperation", "Compare")
        insertNode(layout, "NLParameterMathFun", "Formula")
        insertNode(layout, "NLMapRangeNode", "Map Range")
        # insertNode(layout, "NLParameterDistance", "Distance")
        insertNode(layout, "NLThresholdNode", "Threshold")
        insertNode(layout, "NLRangedThresholdNode", "Ranged Threshold")
        insertNode(layout, "NLLimitRange", "Limit Range")
        insertNode(layout, "NLWithinRangeNode", "Within Range")


@menu_item
class VectorMathMenu(bpy.types.Menu):
    bl_idname = "LN_MT_vector_math_menu"
    bl_label = "Vector Math Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLVectorAngle", "Angle")
        insertNode(layout, "NLVectorAngleCheck", "Check Angle")
        insertNode(layout, "NLConditionDistanceCheck", "Compare Distance")
        insertNode(layout, "NLParameterAbsVector3Node", "Absolute Vector")
        insertNode(layout, "NLConditionCompareVecs", "Compare Vectors")
        insertNode(layout, "NLParameterEulerToMatrixNode", "XYZ to Matrix")
        insertNode(layout, "NLParameterMatrixToEulerNode", "Matrix to XYZ")
        # insertNode(layout, "NLVectorLength", "Vector Length")


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
        insertNode(layout, "NLSetCollisionGroup", "Set Collision Group")
        insertNode(layout, "NLSetCollisionMask", "Set Collision Mask")
        layout.separator()
        insertNode(layout, "NLActionAddPhysicsConstraint", "Add Constraint")
        insertNode(layout, "NLActionRemovePhysicsConstraint", "Remove Constraint")
        layout.separator()
        insertNode(layout, "NLActionSetPhysicsNode", "Set Phyics")
        insertNode(layout, "NLActionSetCharacterGravity", "Set Gravity")
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
        insertNode(layout, "NLVehicleSetAttributes", "Set Attributes")
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
        insertNode(layout, "NLActionSetCharacterVelocity", "Set Velocity")


@menu_item
class PythonMenu(bpy.types.Menu):
    bl_idname = "LN_MT_python_menu"
    bl_label = "Python Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLParameterPythonModuleFunction", "Run Python Code")
        insertNode(layout, "NLParameterGetAttribute", "Get Object Attribute")
        insertNode(layout, "NLParameterSetAttribute", "Set Object Attribute")
        insertNode(layout, "NLParameterTypeCast", "Typecast")


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
        insertNode(layout, "NLActionTimeFilter", "Pulsify")
        insertNode(layout, "NLActionTimeDelay", "Delay")
        insertNode(layout, "NLParameterTimeNode", "Time Data")
        insertNode(layout, "LogicNodeTimeFactor", "Delta Factor")
        insertNode(layout, "NLActionTimeBarrier", "Barrier")
        insertNode(layout, "NLConditionTimeElapsed", "Timer")


@menu_item
class FileMenu(bpy.types.Menu):
    bl_idname = "LN_MT_file_menu"
    bl_label = "File Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "LogicNodeGetFont", "Get Font")
        insertNode(layout, "NLGetImage", "Get Image")
        insertNode(layout, "NLGetSound", "Get Sound")
        layout.separator()
        insertNode(layout, "NLLoadFileContent", "Load File Content")


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


@menu_item
class DataMenu(bpy.types.Menu):
    bl_idname = "LN_MT_data_menu"
    bl_label = "Data Menu"

    def draw(self, context):
        layout = self.layout
        layout.menu("LN_MT_list_menu", text="List", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_dict_menu", text="Dict", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_variable_menu", text="Variables", icon="RIGHTARROW_THIN")


@menu_item
class ListMenu(bpy.types.Menu):
    bl_idname = "LN_MT_list_menu"
    bl_label = "List Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLInitEmptyList", "Create Empty")
        insertNode(layout, "NLInitNewList", "Create From Items")
        layout.separator()
        insertNode(layout, "NLAppendListItem", "Append")
        insertNode(layout, "NLExtendList", "Extend")
        insertNode(layout, "NLRemoveListIndex", "Remove Index")
        insertNode(layout, "NLRemoveListValue", "Remove Value")
        layout.separator()
        insertNode(layout, "NLGetListIndexNode", "Get Index")
        insertNode(layout, "NLSetListIndex", "Set Index")
        insertNode(layout, "NLGetRandomListIndex", "Get Random Item")
        insertNode(layout, "NLDuplicateList", "Duplicate")


@menu_item
class DictMenu(bpy.types.Menu):
    bl_idname = "LN_MT_dict_menu"
    bl_label = "Dictionary Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLInitEmptyDict", "Create Empty")
        insertNode(layout, "NLInitNewDict", "Create From Item")
        layout.separator()
        insertNode(layout, "NLGetDictKeyNode", "Get Key")
        insertNode(layout, "NLSetDictKeyValue", "Set Key")
        insertNode(layout, "NLSetDictDelKey", "Remove Key")


@menu_item
class VariableMenu(bpy.types.Menu):
    bl_idname = "LN_MT_variable_menu"
    bl_label = "Variable Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionSaveVariable", "Save Variable")
        insertNode(layout, "NLActionLoadVariable", "Load Variable")
        insertNode(layout, "NLActionRemoveVariable", "Remove Variable")
        layout.separator()
        insertNode(layout, "NLActionSaveVariables", "Save Variable Dict")
        insertNode(layout, "NLActionLoadVariables", "Load Variable Dict")
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
        layout.menu("LN_MT_draw_menu", text="Draw", icon="RIGHTARROW_THIN")
        layout.menu("LN_MT_eevee_menu", text="EEVEE", icon="RIGHTARROW_THIN")
        layout.separator()
        insertNode(layout, "NLGetFullscreen", "Get Fullscreen")
        insertNode(layout, "NLGetResolution", "Get Resolution")
        insertNode(layout, "NLGetVsyncNode", "Get VSync")
        insertNode(layout, "NLActionSetFullscreen", "Set Fullscreen")
        insertNode(layout, "NLActionSetResolution", "Set Resolution")
        insertNode(layout, "NLActionSetVSync", "Set Vsync")
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
        # insertNode(layout, "NLSetEeveeSMAA", "Set SMAA")
        # insertNode(layout, "NLSetEeveeSMAAQuality", "Set SMAA Quality")
        insertNode(layout, "NLSetEeveeSSR", "Set SSR")
        insertNode(layout, "NLSetEeveeVolumetrics", "Set Volumetric Light")


@menu_item
class UIMenu(bpy.types.Menu):
    bl_idname = "LN_MT_ui_menu"
    bl_label = "UI Menu"

    def draw(self, context):
        layout = self.layout
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
        insertNode(layout, "LogicNodeCreateUICanvas", "Create Canvas")
        insertNode(layout, "LogicNodeCreateUILayout", "Create Layout")
        layout.separator()
        insertNode(layout, "LogicNodeCreateUIButton", "Create Button")
        insertNode(layout, "LogicNodeCreateUILabel", "Create Label")
        insertNode(layout, "LogicNodeCreateUIImage", "Create Image")
        insertNode(layout, "LogicNodeCreateUISlider", "Create Slider")


@menu_item
class UtilityMenu(bpy.types.Menu):
    bl_idname = "LN_MT_utility_menu"
    bl_label = "Utility Menu"

    def draw(self, context):
        layout = self.layout
        insertNode(layout, "NLActionGetPerformanceProfileNode", "Get Profile")
        insertNode(layout, "NLActionPrint", "Print")
