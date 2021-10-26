'''TODO: Documentation
'''

from bge import logic, render
from bge.types import KX_GameObject as GameObject
from mathutils import Vector
import bpy
import json
import math
import operator


###############################################################################
# CONSTANTS
###############################################################################

class _Status(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return self._name


NO_VALUE = _Status("NO_VALUE")
STATUS_WAITING = _Status("WAITING")
STATUS_READY = _Status("READY")
STATUS_INVALID = _Status("INVALID")


LOGIC_OPERATORS = [
    operator.eq,
    operator.ne,
    operator.gt,
    operator.lt,
    operator.ge,
    operator.le
]


LO_AXIS_TO_STRING_CODE = {
    0: "X", 1: "Y", 2: "Z",
    3: "-X", 4: "-Y", 5: "-Z",
}


LO_AXIS_TO_VECTOR = {
    0: Vector((1, 0, 0)), 1: Vector((0, 1, 0)),
    2: Vector((0, 0, 1)), 3: Vector((-1, 0, 0)),
    4: Vector((0, -1, 0)), 5: Vector((0, 0, -1)),
}


###############################################################################
# LOGIC NODES
###############################################################################


def _name_query(named_items, query):
    assert len(query) > 0
    postfix = (query[0] == "*")
    prefix = (query[-1] == "*")
    infix = (prefix and postfix)
    if infix:
        token = query[1:-1]
        for item in named_items:
            if token in item.name:
                return item
    if prefix:
        token = query[:-1]
        for item in named_items:
            if item.name.startswith(token):
                return item
    if postfix:
        token = query[1:]
        for item in named_items:
            if item.name.endswith(token):
                return item
    for item in named_items:
        if item.name == query:
            return item
    return None


def check_game_object(query, scene=None):
    '''TODO: Documentation
    '''
    if not scene:
        scene = logic.getCurrentScene()
    else:
        scene = scene
    if (query is None) or (query == ""):
        return
    if not is_invalid(scene):
        # find from scene
        return _name_query(scene.objects, query)


def compute_distance(parama, paramb) -> float:
    '''TODO: Documentation
    '''
    if is_invalid(parama):
        return None
    if is_invalid(paramb):
        return None
    if hasattr(parama, "getDistanceTo"):
        return parama.getDistanceTo(paramb)
    if hasattr(paramb, "getDistanceTo"):
        return paramb.getDistanceTo(parama)
    va = Vector(parama)
    vb = Vector(paramb)
    return (va - vb).length


def debug(message: str):
    if not hasattr(bpy.types.Scene, 'logic_node_settings'):
        return
    if not bpy.context or not bpy.context.scene:
        return
    if not bpy.context.scene.logic_node_settings.use_node_debug:
        return
    else:
        print('[Logic Nodes] ' + message)


def is_invalid(*a) -> bool:
    for ref in a:
        if ref is None or ref is STATUS_WAITING or ref == '':
            return True
        if not hasattr(ref, "invalid"):
            continue
        elif ref.invalid:
            return True
    return False


def is_waiting(*args) -> bool:
    if STATUS_WAITING in args:
        return True
    return False


def make_valid_name(name):
    valid_characters = (
        "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    clsname = name.replace(' ', '_')
    stripped_name = "".join(
        [c for c in clsname if c in valid_characters]
    )
    return stripped_name


def not_met(*conditions) -> bool:
    for c in conditions:
        if (
            c is STATUS_WAITING or
            c is None or
            c is False
        ):
            return True
    return False


def load_user_module(module_name, clsname):
    import sys
    order = f'import {module_name}'
    print(order)
    exec(order)
    print('#######################################################')
    for t in globals():
        print(t)
    print('#######################################################')
    print(sys.modules[module_name].globals())  # {clsname}']()


def unload_nodes(a, b):
    if not hasattr(bpy.types.Scene, 'nl_globals_initialized'):
        return
    delattr(bpy.types.Scene, 'nl_globals_initialized')


###############################################################################
# DATA
###############################################################################

def load_json_as_dict(filepath):
    if not filepath.endswith('.json'):
        path = f'{filepath}.json'
    if path:
        f = open(path, 'r')
        data = json.load(f)
        f.close()
        return data


###############################################################################
# SCENE
###############################################################################

def make_unique_light(old_lamp_ge: GameObject) -> GameObject:
    '''TODO: Documentation
    '''
    scene = logic.getCurrentScene()
    name = old_lamp_ge.name
    old_lamp = old_lamp_ge.blenderObject
    old_lamp.name = 'OLD_LAMP'

    settings = [
        'color',
        'energy',
        'diffuse_factor',
        'specular_factor',
        'volume_factor',
        'shadow_soft_size',
        'use_custom_distance',
        'cutoff_distance',
        'spot_size',
        'spot_blend',
        'show_cone',
        'angle',
        'shape',
        'size',
        'size_y',
        'use_shadow',
        'shadow_buffer_clip_start',
        'shadow_buffer_bias',
        'use_soft_shadows',
        'use_contact_shadow',
        'contact_shadow_distance',
        'contact_shadow_bias',
        'contact_shadow_thickness',
        'shadow_cascade_count',
        'shadow_cascade_fade',
        'shadow_cascade_max_distance',
        'shadow_cascade_exponent'
    ]

    types = {
        'POINT': 'Point',
        'AREA': 'Area',
        'SPOT': 'Spot',
        'SUN': 'Sun'
    }

    light_type = old_lamp.data.type
    bpy.ops.object.light_add(
        type=light_type,
        location=old_lamp_ge.worldPosition,
        rotation=old_lamp_ge.worldOrientation.to_euler()
    )
    index = 1
    light = None
    while light is None:
        if types[light_type] in bpy.data.objects[-index].name:
            light = bpy.data.objects[-index]
        index += 1
    for attr in settings:
        try:
            setattr(light.data, attr, getattr(old_lamp.data, attr))
        except Exception:
            pass
    light.name = name
    new_lamp_ge = scene.convertBlenderObject(light)
    for p in old_lamp_ge.getPropertyNames():
        new_lamp_ge[p] = old_lamp_ge[p]
    old_lamp_ge.endObject()
    real_name = light.name
    light.name = real_name
    if old_lamp_ge.parent:
        new_lamp_ge.setParent(old_lamp_ge.parent)
    return new_lamp_ge


def get_instance_by_distance(game_obj: GameObject, name: str):
    '''TODO: Documentation
    '''
    objs = []
    distances = {}
    for obj in logic.getCurrentScene().objects:
        if obj.name == name:
            objs.append(obj)
    for obj in objs:
        distances[game_obj.getDistanceTo(obj)] = obj
    return distances[min(distances.keys())]


###############################################################################
# MATH
###############################################################################

def interpolate(a: float, b: float, fac: float) -> float:
    '''TODO: Documentation
    '''
    if -.001 < a-b < .001:
        return b
    return (fac * b) + ((1-fac) * a)


def lerp(a: float, b: float, fac: float) -> float:
    '''TODO: Documentation
    '''
    if -.001 < a-b < .001:
        return b
    return (fac * b) + ((1-fac) * a)


def vec_abs(vec):
    vec = vec.copy()
    vec.x = abs(vec.x)
    vec.y = abs(vec.y)
    vec.z = abs(vec.z)
    return vec


def get_angle(a: Vector, b: Vector, up=Vector((0, 0, 1))) -> float:
    direction = get_direction(a, b)
    rad: float = direction.angle(up)
    deg: float = rad * 180/math.pi
    return deg


def get_direction(a, b, local=False):
    start = a.worldPosition.copy() if hasattr(a, "worldPosition") else a
    if hasattr(b, "worldPosition"):
        b = b.worldPosition.copy()
    if local:
        b = start + b
    d = b - start
    d.normalize()
    return d


def ray_data(origin, dest, local, dist):
    start = origin.worldPosition.copy() if hasattr(origin, "worldPosition") else origin
    if hasattr(dest, "worldPosition"):
        dest = dest.worldPosition.copy()
    if local:
        dest = start + dest
    d = dest - start
    d.normalize()
    return d, dist if dist else (start - dest).length, dest


def raycast(
    caster,
    origin,
    dest,
    distance=0,
    property_name='',
    xray=False,
    local=False,
    visualize=False
):
    direction, distance, dest = ray_data(origin, dest, local, distance)
    obj, point, normal = caster.rayCast(
        dest,
        origin,
        distance,
        property_name,
        xray=xray
    )
    if visualize:
        origin = getattr(origin, 'worldPosition', origin)
        line_dest: Vector = direction.copy()
        line_dest.x *= distance
        line_dest.y *= distance
        line_dest.z *= distance
        line_dest = line_dest + origin
        render.drawLine(
            origin,
            line_dest,
            [1, 0, 0, 1]
        )
        if obj:
            render.drawLine(
                origin,
                point,
                [0, 1, 0, 1]
            )
    return obj, point, normal, direction
