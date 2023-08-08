_enum_local_axis = [
    ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "Y Axis", "The Local Y Axis [Integer Value 1]"),
    ("2", "Z Axis", "The Local Z Axis [Integer Value 2]")
]

_enum_look_axis = [
    ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "Y Axis", "The Local Y Axis [Integer Value 1]")
]

_enum_vector_types = [
    ("0", "Vector", "Vector XYZ"),
    ("1", "Euler", "Euler XYZ")
]

_enum_local_oriented_axis = [
    ("0", "+X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "+Y Axis", "The Local Y Axis [Integer Value 1]"),
    ("2", "+Z Axis", "The Local Z Axis [Integer Value 2]"),
    ("3", "-X Axis", "The Local X Axis [Integer Value 3]"),
    ("4", "-Y Axis", "The Local Y Axis [Integer Value 4]"),
    ("5", "-Z Axis", "The Local Z Axis [Integer Value 5]")
]

_enum_mouse_wheel_direction = [
    ("1", "Scroll Up", "Mouse Wheel Scrolled Up [1]"),
    ("2", "Scroll Down", "Mouse Wheel Scrolled Down [2]"),
    ("3", "Scroll Up or Down", "Mouse Wheel Scrolled either Up or Down[3]")
]


_enum_vector_math_options = [
    ("scale", "Scale", "A multiplied by Scale"),
    ("length", "Length", "Length of A"),
    ("distance", "Distance", "Distance between A and B"),
    None,
    ("dot", "Dot Product", "A dot B"),
    ("faceforward", "Faceforward", "Orients a vector A to point away from a surface B as defined by its normal C. Returns A if A.dot(B) < 0 else -A"),
    ("refract", "Refract", "For a given incident vector A, a surface normal B and ratio of indices of refraction, Ior, refract returns the refraction vector, R"),
    ("reflect", "Reflect", "Reflect A around the normal B. B doesn't need to be normalized"),
    ("project", "Project", "Project this vector onto another"),
    ("cross", "Cross Product", "Project A onto B"),
    None,
    ("multadd", "Multiply Add", "A * B + C"),
    ("divide", "Divide", "Entry-wise divide"),
    ("multiply", "Multiply", "Entry-wise multiply"),
    ("subtract", "Subtract", "A - B"),
    ("add", "Add", "A + B"),
    ("", "Operation", ""),
    None,
    ("normalize", "Normalize", "Rescale all values to 0 - 1"),
    ("lerp", "Lerp", "Linear Interpolation between the two vectors"),
    ("slerp", "Spherical Lerp", "Spherical Interpolation between the two vectors"),
    ("negate", "Negate", "Multiply all values by -1")
]


_enum_type_casts = [
    ("int", "To Integer", "Convert this value to an integer type"),
    ("bool", "To Boolean", "Convert this value to a boolean type"),
    ("str", "To String", "Convert this value to a string type"),
    ("float", "To Float", "Convert this value to a float type")
]


_enum_distance_models = [
    ('INVERSE', 'Inverse', 'Sound will fade exponentially (Realistic)'),
    ('INVERSE_CLAMPED', 'Inverse Clamped',
     'Sound will fade exponentially (Realistic, Clamped)'),
    ('EXPONENT', 'Exponent', 'Sound will fade detemined by an exponent (Good audibility)'),
    ('EXPONENT_CLAMPED', 'Exponent Clamped',
     'Sound will fade detemined by an exponent (Good audibility, Clamped)'),
    ('LINEAR', 'Linear', 'Sound will fade in a linear relation to distance'),
    ('LINEAR_CLAMPED', 'Linear Clamped',
     'Sound will fade in a linear relation to distance (Clamped)'),
    ('NONE', 'None', "Don't use a distance model")
]


_enum_object_property_types = [
    ('GAME', 'Game Property', 'Edit Game Property'),
    ('ATTR', 'Attribute', 'Edit Internal Attribute (can be used in materials)')
]


_enum_2d_filters = [
    ('FXAA', 'FXAA', 'Fast Anti-Aliasing'),
    ('HBAO', 'HBAO', 'Horizon-Based Ambient Occlusion'),
    ('SSAO', 'SSAO', 'Screen-Space Ambient Occlusion'),
    ('VIGNETTE', 'Vignette', 'Fade to color at screen edges'),
    ('BRIGHTNESS', 'Brightness', 'Overall brightness'),
    ('CHROMAB', 'Chromatic Aberration', 'Lens light bending effect'),
    ('GRAYSCALE', 'Grayscale', 'Convert image to grayscale'),
    ('LEVELS', 'Levels', 'Control color levels'),
    ('MIST', 'Mist', 'Classic depth fog implementation')
]


_enum_constraint_types = [
    (
        "bge.constraints.POINTTOPOINT_CONSTRAINT",
        "Ball",
        "Allow rotation around all axis"
    ),
    (
        "bge.constraints.LINEHINGE_CONSTRAINT",
        "Hinge",
        "Work on one plane, allow rotations on one axis only"
    ),
    (
        "bge.constraints.CONETWIST_CONSTRAINT",
        "Cone Twist",
        (
            'Allow rotations around all axis with limits for the cone '
            'and twist axis'
        )
    ),
    (
        "bge.constraints.GENERIC_6DOF_CONSTRAINT",
        "Generic 6 DOF",
        "No constraints by default, limits can be set individually"
    )
]


_enum_ik_mode_values = [
    ("None", "None", "Not set"),
    (
        "bge.logic.CONSTRAINT_IK_MODE_INSIDE",
        "Inside",
        "Keep the bone with IK Distance of target"
    ),
    (
        "bge.logic.CONSTRAINT_IK_MODE_OUTSIDE",
        "Outside",
        "Keep the bone outside IK Distance of target"
    ),
    (
        "bge.logic.CONSTRAINT_IK_MODE_ONSURFACE",
        "On Surface",
        "Keep the bone exactly at IK Distance of the target"
    )
]


_enum_field_value_types = [
    ("STRING", "String", "A String"),
    ("FLOAT", "Float", "A Float value"),
    ("INTEGER", "Integer", "An Integer value"),
    ("BOOLEAN", "Bool", "A True/False value"),
    ("FILE_PATH", "File Path", 'Choose a file path')
]

_enum_numeric_field_value_types = [
    ("NONE", "None", "The None value"),
    ("INTEGER", "Integer", "An Integer value"),
    ("FLOAT", "Float", " A Float value"),
    ("EXPRESSION", "Expression", "A numeric expression")
]

_enum_optional_float_value_types = [
    ("NONE", "None", "No value"),
    ("FLOAT", "Float", "A decimal value"),
    ("EXPRESSION", "Expression", "A numeric expression")
]

_enum_vehicle_axis = [
    ("REAR", "Rear", "Apply to wheels without steering"),
    ("FRONT", "Front", "Apply to wheels with steering"),
    ("ALL", "All", "Apply to all wheels")
]


_enum_loop_count_values = [
    (
        "ONCE",
        "Play",
        (
            'Play once when condition is TRUE, then wait for '
            'the condition to become TRUE again to play it again.'
        )
    ), (
        "INFINITE",
        "Loop",
        "When condition is TRUE, start repeating the sound until stopped."
    ), (
        "CUSTOM",
        "Times",
        "When the condition it TRUE, play the sound N times"
    )
]


_enum_readable_member_names = [
    ("worldPosition", "Position (Global)", "The World Position of the object"),
    ("localPosition", "Position (Local)", "The local position of the object"),
    (
        "worldOrientation",
        "Rotation (Global)",
        "The World Orientation of the object"
    ), (
        "localOrientation",
        "Rotation (Local)",
        "The local orientation of the object"
    ), (
        "worldLinearVelocity",
        "Linear Velocity (Global)",
        "The local linear velocity of the object"
    ), (
        "localLinearVelocity",
        "Linear Velocity (Local)",
        "The local linear velocity of the object"
    ), (
        "worldAngularVelocity",
        "Angular Velocity (Global)",
        "The local angular velocity of the object"
    ), (
        "localAngularVelocity",
        "Angular Velocity (Local)",
        "The local angular velocity of the object"
    ), (
        "worldTransform",
        "Transform (Global)",
        (
            'The World Transform of the '
            'object'
        )
    ), (
        "localTransform",
        "Transform (Local)",
        (
            'The local transform of the '
            'object'
        )
    ),
    ("worldScale", "World Scale", "The global scale of the object"),
    ("localScale", "Local Scale", "The local scale of the object"),
    ("name", "Name", "The name of the object"),
    ("color", "Color", "The solid color of the object"),
    (
        "visible",
        "Visibility",
        "True if the object is set to visible, False if it is set of invisible"
    )
]

_enum_writable_member_names = [
    ("color", "Color", "The solid color of the object"),
    ("worldPosition", "Position (Global)", "The World Position of the object"),
    ("localPosition", "Position (Local)", "The local position of the object"),
    (
        "worldOrientation",
        "Rotation (Global)",
        "The World Orientation of the object"
    ), (
        "localOrientation",
        "Rotation (Local)",
        "The local orientation of the object"
    ), (
        "worldLinearVelocity",
        "Linear Velocity (Global)",
        "The local linear velocity of the object"
    ), (
        "localLinearVelocity",
        "Linear Velocity (Local)",
        "The local linear velocity of the object"
    ), (
        "worldAngularVelocity",
        "Angular Velocity (Global)",
        "The local rotational velocity of the object"
    ), (
        "localAngularVelocity",
        "Angular Velocity (Local)",
        "The local rotational velocity of the object"
    ), (
        "worldTransform",
        "Transform (Global)",
        (
            'The World Transform of the '
            'object'
        )
    ), (
        "localTransform",
        "Transform (Local)",
        (
            'The local transform of the '
            'object'
        )
    ),
    ("worldScale", "Scale", "The global scale of the object")
]

_enum_mouse_buttons = [
    ("bge.events.LEFTMOUSE", "Left Button", "Left Mouse Button"),
    ("bge.events.MIDDLEMOUSE", "Middle Button", "Middle Mouse Button"),
    ("bge.events.RIGHTMOUSE", "Right Button", "Right Mouse Button")
]

_enum_vsync_modes = [
    ("bge.render.VSYNC_OFF", "Off", "Disable Vsync"),
    ("bge.render.VSYNC_ON", "On", "Enable Vsync"),
    (
        "bge.render.VSYNC_ADAPTIVE",
        "Adaptive",
        (
            'Enable adaptive Vsync '
            '(if supported)'
        )
    )
]

_enum_string_ops = [
    ("0", "Postfix", "Insert A after String"),
    ("1", "Prefix", "Insert A before String"),
    ("2", "Infix", "Insert A before String, B after String."),
    ("3", "Remove Last", "Remove Last Character from String"),
    ("4", "Remove First", "Remove First Character from String"),
    (
        "5",
        "Replace",
        'Replace all occurences of A with B'
    ),
    ("6", "Upper Case", "Convert to Upper Case"),
    ("7", "Lower Case", "Convert to Lower Case"),
    (
        "8",
        "Remove Range",
        'Remove characters from index A to index B'
    ),
    (
        "9",
        "Insert At",
        "Insert A at index B"
    ),
    (
        "10",
        "Length",
        "Character Count (returns a Number)"
    ),
    (
        "11",
        "Substring",
        "Characters between index A and index B"
    ),
    (
        "12",
        "First Index Of",
        "Position of the first occurence of A"
    ),
    (
        "13",
        "Last Index Of",
        "Position of the last occurence of A"
    )
]

_enum_quality_levels = [
    ("LOW", "Low", "Set a lower quality to increase performance"),
    ("MEDIUM", "Medium", "Set a medium quality for a balanced performance"),
    ("HIGH", "High", "Set a high quality at the cost of performance"),
    ("ULTRA", "Ultra", "Set a very high quality at the cost of performance")
]

_enum_math_operations = [
    ("ADD", "Add", "Sum A and B"),
    ("SUB", "Subtract", "Subtract B from A"),
    ("DIV", "Divide", "Divide A by B"),
    ("MUL", "Multiply", "Multiply A by B"),
    ("POW", "Power", "A to the power of B"),
    ("MOD", "Modulo", "Modulo of A by B"),
    ("FDIV", "Floor Divide", "Floor Divide A by B"),
    ("MATMUL", "Matrix Multiply", "Transform A by B")
]

_enum_greater_less = [
    ("GREATER", "Greater", "Value greater than Threshold"),
    ("LESS", "Less", "Value less than Threshold")
]

_enum_in_or_out = [
    ("INSIDE", "Within", "Value is within Range"),
    ("OUTSIDE", "Outside", "Value is outside Range")
]

_enum_logic_operators = [
    ("0", "Equal", "A equals B"),
    ("1", "Not Equal", "A not equals B"),
    ("2", "Greater Than", "A greater than B"),
    ("3", "Less Than", "A less than B"),
    ("4", "Greater or Equal", "A greater or equal to B"),
    ("5", "Less or Equal", "A less or equal to B")
]


_enum_controller_stick_operators = [
    ("0", "Left Stick", "Left Stick Values"),
    ("1", "Right Stick", "Right Stick Values")
]

_enum_controller_trigger_operators = [
    ("0", "Left Trigger", "Left Trigger Values"),
    ("1", "Right Trigger", "Right Trigger Values")
]

_enum_vrcontroller_trigger_operators = [
    ("0", "Left", "Left Controller Values"),
    ("1", "Right", "Right Controller Values")
]


_enum_controller_buttons_operators = [
    ("0", "A / Cross", "A / Cross Button"),
    ("1", "B / Circle", "B / Circle Button"),
    ("2", "X / Square", "X / Square Button"),
    ("3", "Y / Triangle", "Y / Triangle Button"),
    ("4", "Select / Share", "Select / Share Button"),
    ("6", "Start / Options", "Start / Options Button"),
    ("7", "L3", "Left Stick Button"),
    ("8", "R3", "Right Stick Button"),
    ("9", "LB / L1", "Left Bumper / L1 Button"),
    ("10", "RB / R1", "Right Bumper / R1 Button"),
    ("11", "D-Pad Up", "D-Pad Up Button"),
    ("12", "D-Pad Down", "D-Pad Down Button"),
    ("13", "D-Pad Left", "D-Pad Left Button"),
    ("14", "D-Pad Right", "D-Pad Right Button")
]


_enum_play_mode_values = [
    ("bge.logic.KX_ACTION_MODE_PLAY", "Play", "Play the action once"),
    ("bge.logic.KX_ACTION_MODE_LOOP", "Loop", "Loop the action"),
    (
        "bge.logic.KX_ACTION_MODE_PING_PONG",
        "Ping Pong",
        "Play the action in one direction then in the opposite one"
    ),
    ("bge.logic.KX_ACTION_MODE_PLAY + 3", "Play Stop", "Play the action once"),
    ("bge.logic.KX_ACTION_MODE_LOOP + 3", "Loop Stop", "Loop the action"),
    (
        "bge.logic.KX_ACTION_MODE_PING_PONG + 3",
        "Ping Pong Stop",
        "Play the action in one direction then in the opposite one"
    )
]

_enum_blend_mode_values = [
    (
        "bge.logic.KX_ACTION_BLEND_BLEND",
        "Blend",
        "Blend layers using linear interpolation"
    ),
    ("bge.logic.KX_ACTION_BLEND_ADD", "Add", "Adds the layer together")
]

_enum_spawn_types = [
    ("Simple", "Simple", "Spawn an instance without behavior"),
    ("SimpleBullet", "Simple Bullet", "Spawn a bullet that travels linearly along its local +Y axis"),
    ("PhysicsBullet", "Physical Bullet", "Spawn a bullet that travels along a trajectory aimed at its local +Y axis")
]

_serialize_types = [
    ("builtin", "Built-In", "Serialize Built-In data type (int, float, bool, dict, etc.)"),
    ("Vec2", "2D Vector", "Serialize a 2D Vector"),
    ("Vec3", "3D Vector", "Serialize a 3D Vector"),
    ("Vec4", "4D Vector", "Serialize a 4D Vector"),
    ("Mat3", "3x3 Matrix", "Serialize a 3x3 Matrix"),
    ("Mat4", "4x4 Matrix", "Serialize a 4x4 Matrix"),
    ("GameObj", "Game Object", "Serialize a Game Object (Note: Not all data can be serialized)")
]


_enum_msg_types = [
    ("INFO", "Info", "Will print the message in white (on-screen console)"),
    ("DEBUG", "Debug", "Will print the message in light yellow (on-screen console)"),
    ("WARNING", "Warning", "Will print the message in yellow (on-screen console)"),
    ("ERROR", "Error", "Will print the message in red (on-screen console)"),
    ("SUCCESS", "Success", "Will print the message in green (on-screen console)")
]