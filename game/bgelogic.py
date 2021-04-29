from bge import logic
import bge
import bpy
import aud
import mathutils
import math
import numbers
import collections
import time
import os
import random
import sys
import operator
import json


DISTANCE_MODELS = {
    'INVERSE': aud.DISTANCE_MODEL_INVERSE,
    'INVERSE_CLAMPED': aud.DISTANCE_MODEL_INVERSE_CLAMPED,
    'EXPONENT': aud.DISTANCE_MODEL_EXPONENT,
    'EXPONENT_CLAMPED': aud.DISTANCE_MODEL_EXPONENT_CLAMPED,
    'LINEAR': aud.DISTANCE_MODEL_LINEAR,
    'LINEAR_CLAMPED': aud.DISTANCE_MODEL_LINEAR_CLAMPED,
    'NONE': aud.DISTANCE_MODEL_INVALID
}


def interpolate(a, b, fac):
    return (fac * b) + ((1-fac) * a)


def alpha_move(a, b, fac):
    if a < b:
        return a + fac
    elif a > b:
        return a - fac
    else:
        return a


# Persistent maps


class SimpleLoggingDatabase(object):
    index: int

    class LineBuffer(object):
        def __init__(self, buffer=[]):
            self.buffer = buffer
            self.index = 0
            self.size = len(self.buffer)

        def read(self):
            line = self.buffer[self.index]
            self.index += 1
            return line

        def write(self, line):
            self.buffer.append(line + "\n")

        def has_next(self):
            return self.index < self.size

        def flush(self, file):
            with open(file, "a") as f:
                f.writelines(self.buffer)

    class Serializer(object):
        def read(self, line_reader):
            raise NotImplementedError()

        def write(self, value, line_writer):
            raise NotImplementedError()

    serializers = {}
    storage_dir = logic.expandPath("//Globals")
    shared_dbs = {}

    @classmethod
    def get_or_create_shared_db(cls, fname):
        db = cls.shared_dbs.get(fname)
        if db is None:
            db = SimpleLoggingDatabase(fname)
            cls.shared_dbs[fname] = db
        return db

    @classmethod
    def get_storage_dir(cls):
        return cls.storage_dir

    @classmethod
    def put_value(cls, key, value, buffer):
        type_name = str(type(value))
        serializer = cls.serializers.get(type_name)
        if not serializer:
            return False
        buffer.write("PUT")
        buffer.write(key)
        buffer.write(type_name)
        serializer.write(value, buffer)

    @classmethod
    def read_existing(cls, fpath, intodic):
        lines = []
        with open(fpath, "r") as f:
            lines.extend(f.read().splitlines())
        buffer = SimpleLoggingDatabase.LineBuffer(lines)
        log_size = 0
        while buffer.has_next():
            op = buffer.read()
            assert op == "PUT"
            key = buffer.read()
            type_id = buffer.read()
            serializer = SimpleLoggingDatabase.serializers.get(type_id)
            value = serializer.read(buffer)
            intodic[key] = value
            log_size += 1
        return log_size

    @classmethod
    def write_put(cls, fname, key, value):
        type_name = str(type(value))
        serializer = cls.serializers.get(type_name)
        if not serializer:
            return  # no serializer for given value type
        if not os.path.exists(cls.get_storage_dir()):
            os.mkdir(cls.get_storage_dir())
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        buffer = SimpleLoggingDatabase.LineBuffer()
        cls.put_value(key, value, buffer)
        buffer.flush(fpath)

    @classmethod
    def read(cls, fname, intodic):
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        if os.path.exists(fpath):
            return cls.read_existing(fpath, intodic)
        else:
            return 0

    @classmethod
    def compress(cls, fname, data):
        buffer = SimpleLoggingDatabase.LineBuffer()
        for key in data:
            value = data[key]
            cls.put_value(key, value, buffer)
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        with open(fpath, "w") as f:
            f.writelines(buffer.buffer)

    def __init__(self, file_name):
        self.fname = file_name
        self.data = {}

        filter(lambda a: a is not remove_globals, bpy.app.handlers.game_post)
        bpy.app.handlers.game_post.append(remove_globals)

        log_size = SimpleLoggingDatabase.read(self.fname, self.data)
        if log_size > (5 * len(self.data)):
            debug("Compressing sld {}".format(file_name))
            SimpleLoggingDatabase.compress(self.fname, self.data)

    def get(self, key, default_value=None):
        return self.data.get(key, default_value)

    def clear(self):
        self.data.clear()

    def put(self, key, value, persist=True):
        self.data[key] = value
        if persist:
            old_value = self.data.get(key)
            changed = old_value != value
            if changed:
                SimpleLoggingDatabase.write_put(self.fname, key, value)


class StringSerializer(SimpleLoggingDatabase.Serializer):

    def write(self, value, line_writer):
        line_writer.write(value)

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else data


class FloatSerializer(SimpleLoggingDatabase.Serializer):

    def write(self, value, line_writer): line_writer.write(str(value))

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else float(data)


class IntegerSerializer(SimpleLoggingDatabase.Serializer):

    def write(self, value, line_writer): line_writer.write(str(value))

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else int(data)


class ListSerializer(SimpleLoggingDatabase.Serializer):

    def write(self, value, line_writer):
        line_writer.write(str(len(value)))
        for e in value:
            tp = str(type(e))
            serializer = SimpleLoggingDatabase.serializers.get(tp)
            if serializer:
                line_writer.write(tp)
                serializer.write(e, line_writer)

    def read(self, line_reader):
        data = []
        count = int(line_reader.read())
        for i in range(0, count):
            tp = line_reader.read()
            serializer = SimpleLoggingDatabase.serializers.get(tp)
            value = serializer.read(line_reader)
            data.append(value)
        return data


class VectorSerializer(SimpleLoggingDatabase.Serializer):
    def write(self, value, line_writer):
        if value is None:
            line_writer.write("None")
        else:
            line = ""
            for i in value:
                line += str(i) + " "
            line_writer.write(line)

    def read(self, line_reader):
        line = line_reader.read()
        if line == "None":
            return None
        data = line.rstrip().split(" ")
        components = [float(d) for d in data]
        return mathutils.Vector(components)


SimpleLoggingDatabase.serializers[str(type(""))] = StringSerializer()
SimpleLoggingDatabase.serializers[str(type(1.0))] = FloatSerializer()
SimpleLoggingDatabase.serializers[str(type(10))] = IntegerSerializer()
SimpleLoggingDatabase.serializers[str(type([]))] = ListSerializer()
SimpleLoggingDatabase.serializers[str(type((0, 0, 0)))] = ListSerializer()
SimpleLoggingDatabase.serializers[str(type(mathutils.Vector()))] = (
    VectorSerializer()
)

# End of persistent maps

LO_AXIS_TO_STRING_CODE = {
    0: "X", 1: "Y", 2: "Z",
    3: "-X", 4: "-Y", 5: "-Z",
}

LO_AXIS_TO_VECTOR = {
    0: mathutils.Vector((1, 0, 0)), 1: mathutils.Vector((0, 1, 0)),
    2: mathutils.Vector((0, 0, 1)), 3: mathutils.Vector((-1, 0, 0)),
    4: mathutils.Vector((0, -1, 0)), 5: mathutils.Vector((0, 0, -1)),
}

LOGIC_OPERATORS = [
    operator.eq,
    operator.ne,
    operator.gt,
    operator.lt,
    operator.ge,
    operator.le
]


# distance between objects or vectors or tuples. None if not computable
def compute_distance(parama, paramb):
    if is_invalid(parama):
        return None
    if is_invalid(paramb):
        return None
    if hasattr(parama, "getDistanceTo"):
        return parama.getDistanceTo(paramb)
    if hasattr(paramb, "getDistanceTo"):
        return paramb.getDistanceTo(parama)
    va = mathutils.Vector(parama)
    vb = mathutils.Vector(paramb)
    return (va - vb).length


def debug(message):
    if not hasattr(bpy.types.Scene, 'logic_node_settings'):
        return
    if not bpy.context or not bpy.context.scene:
        return
    if not bpy.context.scene.logic_node_settings.use_node_debug:
        return
    else:
        print('[Logic Nodes] ' + message)


def xrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == 0 and vec.y == 0 and vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[0], 0, 1.0)
        return True
    else:
        vec = project_vector3(vec, 1, 2)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 1, 2)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[0] += drot
        rotating_object.localOrientation = eulers
        return False


def yrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == 0 and vec.y == 0 and vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[1], 1, 1.0)
        return True
    else:
        vec = project_vector3(vec, 2, 0)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 2, 0)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[1] += drot
        rotating_object.localOrientation = eulers
        return False
    pass


def zrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == 0 and vec.y == 0 and vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[2], 2, 1.0)
        return True
    else:
        # project in 2d, compute angle diff, set euler rot 2
        vec = project_vector3(vec, 0, 1)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 0, 1)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return True
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[2] += drot
        rotating_object.localOrientation = eulers
        return False


def rot_to(
    rot_axis_index,
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    if rot_axis_index == 0:
        return xrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )
    elif rot_axis_index == 1:
        return yrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )
    elif rot_axis_index == 2:
        return zrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )


def move_to(
    moving_object,
    destination_point,
    speed,
    time_per_frame,
    dynamic,
    distance
):
    if dynamic:
        direction = (
            destination_point -
            moving_object.worldPosition)
        dst = direction.length
        if(dst <= distance):
            return True
        direction.z = 0
        direction.normalize()
        velocity = direction * speed
        velocity.z = moving_object.worldLinearVelocity.z
        moving_object.worldLinearVelocity = velocity
        return False
    else:
        direction = (
            destination_point -
            moving_object.worldPosition
            )
        dst = direction.length
        if(dst <= distance):
            return True
        direction.normalize()
        displacement = speed * time_per_frame
        motion = direction * displacement
        moving_object.worldPosition += motion
        return False


def project_vector3(v, xi, yi):
    return mathutils.Vector((v[xi], v[yi]))


def stop_all_sounds(a, b):
    if not hasattr(bpy.types.Scene, 'nl_aud_system'):
        return
    closed_devs = ''
    for dev in bpy.types.Scene.nl_aud_devices:
        bpy.types.Scene.nl_aud_devices[dev].stopAll()
        closed_devs += ' {},'.format(dev)
    debug('Closing Sound Devices:{}'.format(closed_devs[:-1]))
    delattr(bpy.types.Scene, 'nl_aud_devices')
    delattr(bpy.types.Scene, 'nl_aud_system')


def remove_globals(a, b):
    if not hasattr(bpy.types.Scene, 'nl_globals_initialized'):
        return
    delattr(bpy.types.Scene, 'nl_globals_initialized')


def check_game_object(query, scene=None):
    if not scene:
        scene = logic.getCurrentScene()
    else:
        scene = scene
    if (query is None) or (query == ""):
        return
    if not is_invalid(scene):
        # find from scene
        return _name_query(scene.objects, query)


def invalid(ref):
    if ref is None:
        return False
    if not hasattr(ref, "invalid"):
        return False
    return ref.invalid


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


_loaded_userlogic_files = {}


def load_user_logic(module_name):
    full_path = logic.expandPath(
        "//bgelogic/cells/{}.py".format(module_name)
    )
    loaded_value = _loaded_userlogic_files.get(full_path)
    if loaded_value:
        return loaded_value
    import sys
    python_version = sys.version_info
    major = python_version[0]
    minor = python_version[1]
    if (major < 3) or (major == 3 and minor < 3):
        import imp
        loaded_value = imp.load_source(module_name, full_path)
    elif (major == 3) and (minor < 5):
        from importlib.machinery import SourceFileLoader
        loaded_value = SourceFileLoader(module_name, full_path).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loaded_value = module
    _loaded_userlogic_files[module_name] = loaded_value
    return loaded_value


def load_user_module(module_name):
    import sys
    exec("import {}".format(module_name))
    return sys.modules[module_name]


class AudioSystem(object):
    def __init__(self):
        self.active_sounds = []
        self.listener = logic.getCurrentScene().active_camera
        self.old_lis_pos = self.listener.worldPosition.copy()
        bpy.types.Scene.nl_aud_system = self
        if not hasattr(bpy.types.Scene, 'nl_aud_devices'):
            debug('Opening Sound Devices: default3D, default')
            bpy.types.Scene.nl_aud_devices = self.devices = {
                'default3D': aud.Device(),
                'default': aud.Device()
            }
        else:
            self.devices = bpy.types.Scene.nl_aud_devices
        self.device3D = self.devices['default3D']
        self.device = self.devices['default']
        self.device.distance_model = aud.DISTANCE_MODEL_INVALID
        self.device3D.distance_model = self.get_distance_model(
            bpy.context.scene.audio_distance_model
        )
        self.device3D.speed_of_sound = bpy.context.scene.audio_doppler_speed
        self.device3D.doppler_factor = bpy.context.scene.audio_doppler_factor

        filter(lambda a: a is not stop_all_sounds, bpy.app.handlers.game_post)
        bpy.app.handlers.game_post.append(stop_all_sounds)

    def get_distance_model(self, name):
        return DISTANCE_MODELS.get(name, aud.DISTANCE_MODEL_INVERSE_CLAMPED)

    def compute_listener_velocity(self, listener):
        wpos = listener.worldPosition.copy()
        olp = self.old_lis_pos
        vel = (
            (wpos.x - olp.x) * 50,
            (wpos.y - olp.y) * 50,
            (wpos.z - olp.z) * 50
        )
        self.old_lis_pos = wpos
        return vel

    def update(self, network):
        c = logic.getCurrentScene().active_camera
        self.listener = c
        if not self.active_sounds:
            return  # do not update if no sound has been installed
        # update the listener data
        devs = self.devices
        listener_vel = self.compute_listener_velocity(c)
        for d in devs:
            dev = devs[d]
            dev.listener_location = c.worldPosition
            dev.listener_orientation = c.worldOrientation.to_quaternion()
            dev.listener_velocity = listener_vel


class StatefulValueProducer(object):
    def get_value(self): pass
    def has_status(self, status): pass


class LogicNetworkCell(StatefulValueProducer):
    class _Status(object):
        def __init__(self, name):
            self._name = name

        def __repr__(self):
            return self._name

    STATUS_WAITING = _Status("WAITING")
    STATUS_READY = _Status("READY")
    NO_VALUE = _Status("NO_VALUE")

    def __init__(self):
        self._uid = None
        self._status = LogicNetworkCell.STATUS_WAITING
        self._value = None
        self._children = []
        self.network = None
        self.is_waiting = False

#    def create_subcell(self, get_value_call):
#        cell = LogicNetworkSubCell()

    def get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value

    def setup(self, network):
        """
        This is called by the network once, after all the
        cells have been loaded into the tree.
        :return: None
        """
        pass

    def stop(self, network):
        pass

    def _set_ready(self):
        self._status = LogicNetworkCell.STATUS_READY

    def _set_status(self, status):
        """
        Check the current status of the cell. Should return
        True if status equals the current status of the cell.
        :param status:
        :return:
        """
        self._status = status

    def has_status(self, status):
        return status == self._status

    def get_game_object(self, param, scene):
        if str(param) == 'NLO:U_O':
            return self.network._owner
        else:
            return check_game_object(param.split(':')[-1], scene)

    def get_parameter_value(self, param, allow_wait=False, scene=None):
        if str(param).startswith('NLO:'):
            return self.get_game_object(param, scene)
        if isinstance(param, StatefulValueProducer):
            if param.has_status(LogicNetworkCell.STATUS_READY):
                return param.get_value()
            else:
                if not allow_wait:
                    self.is_waiting = True
                return LogicNetwork.STATUS_WAITING
        else:
            return param

    def reset(self):
        """
        Resets the status of the cell to LogicNetwork.STATUS_WAITING.
        A cell may override this to reset other states
        or to keep the value at STATUS_READY if evaluation is required
        to happen only once (or never at all)
        :return:
        """
        self._set_status(LogicNetworkCell.STATUS_WAITING)

    def evaluate(self):
        """
        A logic cell implements this method to do its job. The network
        evaluates a cell until its status becomes
         LogicNetwor.STATUS_READY. When that happens, the cell is
         removed from the update queue.
        :return:
        """
        raise NotImplementedError(
            "{} doesn't implement evaluate".format(self.__class__.__name__)
        )

    def _always_ready(self, status):
        return status is LogicNetworkCell.STATUS_READY

    def _skip_evaluate(self):
        return

    def deactivate(self):
        self.has_status = self._always_ready
        self.evaluate = self._skip_evaluate


class LogicNetworkSubCell(StatefulValueProducer):

    def __init__(self, owner, value_getter):
        self.owner = owner
        self.get_value = value_getter

    def has_status(self, status):
        return self.owner.has_status(status)


class LogicNetwork(LogicNetworkCell):
    def __init__(self):
        LogicNetworkCell.__init__(self)
        self._cells = []
        self._iter = collections.deque()
        self._lastuid = 0
        self._owner = None
        self._max_blocking_loop_count = 0
        self._messages = SimpleLoggingDatabase.get_or_create_shared_db('NL_MessageService')
        self.keyboard = None
        self.mouse = None
        self.keyboard_events = None
        self.active_keyboard_events = None
        self.mouse_events = None
        self.stopped = False
        self.timeline = 0.0
        self._time_then = None
        self.time_per_frame = 0.0
        self._last_mouse_position = [
            logic.mouse.position[0], logic.mouse.position[1]
        ]
        self.mouse_motion_delta = [0.0, 0.0]
        self.mouse_wheel_delta = 0
        self.aud_system_owner = False
        self.init_glob_cats()
        self.audio_system = self.create_aud_system()
        self.sub_networks = []  # a list of networks updated by this network
        self.capslock_pressed = False
        self.evaluated_cells = 0

    def create_aud_system(self):
        if not hasattr(bpy.types.Scene, 'nl_aud_system'):
            self.aud_system_owner = True
            return AudioSystem()
        else:
            return bpy.types.Scene.nl_aud_system

    def init_glob_cats(self):
        if not hasattr(bpy.types.Scene, 'nl_globals_initialized'):
            scene = bge.logic.getCurrentScene()
            cats = bpy.data.scenes[scene.name].nl_global_categories

            msg = ''

            dat = {
                'STRING': 'string_val',
                'FLOAT': 'float_val',
                'INTEGER': 'int_val',
                'BOOLEAN': 'bool_val',
                'FILE_PATH': 'filepath_val'
            }

            for c in cats:
                db = SimpleLoggingDatabase.get_or_create_shared_db(c.name)
                msg += f' {c.name},'
                for v in c.content:
                    val = getattr(v , dat.get(v.value_type, 'FLOAT'), 0)
                    db.put(v.name, val, v.persistent)

            debug(f'Globals Initialized:{msg[:-1]}')
            bpy.types.Scene.nl_globals_initialized = True

    def ray_cast(
        self,
        caster_object,
        ray_origin,
        ray_destination,
        property,
        xray,
        distance
    ):
        now = time.time()
        cached_data = caster_object.get("_NL_ray_cast_data")
        if cached_data is not None:
            data_time = cached_data[0]
            data_origin = cached_data[1]
            data_destination = cached_data[2]
            data_property = cached_data[3]
            data_distance = cached_data[4]
            d_time = now - data_time
            # only if we are in the same frame,
            # otherwise scenegraph might have changed
            if d_time < 0.01:
                if (
                    (data_origin == ray_origin) and
                    (data_destination == ray_destination) and
                    (data_property == property) and
                    (data_distance == distance)
                ):
                    return cached_data[5]
            pass
        obj, point, normal = None, None, None
        if property is not None:
            obj, point, normal = caster_object.rayCast(
                ray_destination,
                ray_origin,
                distance,
                property,
                xray=xray
            )
        else:
            obj, point, normal = caster_object.rayCast(
                ray_destination,
                ray_origin,
                distance,
                xray=xray
            )
        cached_data = (
            now,
            ray_origin,
            ray_destination,
            property,
            distance,
            (obj, point, normal)
        )
        caster_object["_NL_ray_cast_data"] = cached_data
        return obj, point, normal

    def set_mouse_position(self, screen_x, screen_y):
        self.mouse.position = (screen_x, screen_y)
        self._last_mouse_position = [screen_x, screen_y]
        pass

    def get_owner(self):
        return self._owner

    def setup(self):
        self.time_per_frame = 0.0
        for cell in self._cells:
            cell.network = self
            cell.setup(self)
        self._last_mouse_position[:] = logic.mouse.position

    def is_running(self):
        return not self.stopped

    def is_stopped(self):
        return self.stopped

    def stop(self, network=None):
        if self.stopped:
            return
        self._time_then = None
        self.stopped = True
        for cell in self._cells:
            cell.stop(self)
        for m in self._messages.data:
            if m[2] in self._cells:
                self._messages.pop(m, None)

    def _generate_cell_uid(self):
        self._lastuid += 1
        return self._lastuid

    def add_cell(self, cell):
        self._cells.append(cell)
        self._iter.append(cell)
        self._max_blocking_loop_count = len(self._cells) * len(self._cells)
        cell._uid = self._generate_cell_uid()
        return cell

    def evaluate(self):
        now = time.time()
        if self._time_then is None:
            self._time_then = now
        dtime = now - self._time_then
        self._time_then = now
        self.timeline += dtime
        self.time_per_frame = dtime
        if self._owner.invalid:
            debug("Network Owner removed from game. Shutting down the network")
            return True
        self.keyboard = logic.keyboard
        self.mouse = logic.mouse
        # compute mouse translation since last frame (or initialization)
        curr_mpos = self.mouse.position
        last_mpos = self._last_mouse_position
        mpos_delta = self.mouse_motion_delta
        mpos_delta[0] = curr_mpos[0] - last_mpos[0]
        mpos_delta[1] = curr_mpos[1] - last_mpos[1]
        last_mpos[:] = curr_mpos
        # store mouse and keyboard events to be used by cells
        self.keyboard_events = self.keyboard.inputs.copy()
        self.active_keyboard_events = self.keyboard.activeInputs.copy()
        caps_lock_event = self.keyboard_events[bge.events.CAPSLOCKKEY]
        if(caps_lock_event.released):
            self.capslock_pressed = not self.capslock_pressed
        me = self.mouse.inputs
        self.mouse_wheel_delta = 0
        if(me[bge.events.WHEELUPMOUSE].activated):
            self.mouse_wheel_delta = 1
        elif(
            me[bge.events.WHEELDOWNMOUSE].activated
        ):
            self.mouse_wheel_delta = -1
        self.mouse_events = me
        # update the cells
        cells = self._iter
        max_loop_count = len(cells)
        loop_index = 0
        done_cells = []
        while cells:
            if loop_index == self._max_blocking_loop_count:
                debug(
                    "Network found a blocking condition" +
                    " (due to unconnected or non responsive cell)"
                )
                debug("Cells awaiting evaluation: ")
                for c in cells:
                    debug(c)
                debug("Stopping network...")
                self.stop()
                return
            cell = cells.popleft()
            if cell in done_cells:
                continue
            else:
                done_cells.append(cell)
            cell.evaluate()
            self.evaluated_cells += 1
            if not cell.has_status(LogicNetworkCell.STATUS_READY):
                cells.append(cell)
            loop_index += 1
        done_cells = []
        if(loop_index > max_loop_count):
            debug(
                "Wrong sorting alghorithm!",
                loop_index,
                max_loop_count)
        for cell in self._cells:
            cell.reset()
            if cell.has_status(LogicNetworkCell.STATUS_WAITING):
                cells.append(cell)
        # update the sound system
        if self.aud_system_owner:
            self.audio_system.update(self)
        # pulse subnetworks
        for network in self.sub_networks:
            if network._owner.invalid:
                self.sub_networks.remove(network)
            elif network.is_running():
                network.evaluate()
        pass

    def install_subnetwork(self, owner_object, node_tree_name, initial_status):
        # transform the tree name into a NL module name
        valid_characters = (
            "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        stripped_name = "".join(
            [c for c in node_tree_name if c in valid_characters]
        )
        if stripped_name in owner_object:
            debug("Network {} already installed for {}".format(
                    stripped_name, owner_object.name
                ))
            if(initial_status is True):
                owner_object[f'IGNLTree_{node_tree_name}'].stopped = False
        else:
            debug("Installing sub network...")
            initial_status_key = f'NL__{node_tree_name}'
            owner_object[initial_status_key] = initial_status
            module_name = 'bgelogic.NL{}'.format(stripped_name)
            module = load_user_module(module_name)
            module._initialize(owner_object)
            subnetwork = owner_object[f'IGNLTree_{node_tree_name}']
            self.sub_networks.append(subnetwork)


def is_waiting(*args):
    if LogicNetworkCell.STATUS_WAITING in args:
        return True
    return False


def is_invalid(*a):
    for ref in a:
        if ref is None or ref is LogicNetworkCell.STATUS_WAITING or ref == '' :
            return True
        if not hasattr(ref, "invalid"):
            continue
        elif ref.invalid:
            return True
    return False


def not_met(*conditions):
    for c in conditions:
        if (
            c is LogicNetworkCell.STATUS_WAITING or
            c is None or
            c is False
        ):
            return True
    return False


###############################################################################
# Basic Cells
###############################################################################


class ParameterCell(LogicNetworkCell):

    def __init__(self):
        LogicNetworkCell.__init__(self)


class ActionCell(LogicNetworkCell):
    def __init__(self):
        LogicNetworkCell.__init__(self)


class ConditionCell(LogicNetworkCell):
    def __init__(self):
        LogicNetworkCell.__init__(self)


###############################################################################
# Events
###############################################################################


class GEOnInit(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self._set_status(LogicNetworkCell.STATUS_READY)
        self._value = True

    def reset(self):
        self._value = False

    def evaluate(self):
        pass


class OnNextFrame(ConditionCell):

    def __init__(self):
        ConditionCell.__init__(self)
        self.input_condition = None
        self._activated = 0

    def evaluate(self):
        input_condition = self.get_parameter_value(self.input_condition)
        self._set_ready()
        if self._activated == 1:
            self._set_value(True)
            if not input_condition:
                self._activated = 0
        elif input_condition:
            self._set_value(False)
            self._activated = 1
        elif self._activated == 0:
            self._set_value(False)


class ConditionOnUpdate(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self._set_status(LogicNetworkCell.STATUS_READY)
        self._value = True

    def reset(self):
        self._value = True

    def evaluate(self):
        pass


class ConditionValueChanged(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self._previous_value = None
        self._current_value = None
        self.current_value = None
        self.initialize = False
        self.PREVIOUS_VALUE = LogicNetworkSubCell(
            self,
            self.get_previous_value
        )
        self.CURRENT_VALUE = LogicNetworkSubCell(self, self.get_current_value)

    def get_previous_value(self):
        return self._previous_value

    def get_current_value(self):
        return self._current_value

    def reset(self):
        ConditionCell.reset(self)
        self._set_value(False)
        self._previous_value = self._current_value

    def evaluate(self):
        curr = self.get_parameter_value(self.current_value)
        if is_waiting(curr):
            return
        self._set_ready()
        if self.initialize:
            self.initialize = False
            self._previous_value = curr
            self._set_value(False)
        elif self._previous_value != curr:
            self._current_value = curr
            self._set_value(True)


class ConditionValueTrigger(ConditionCell):
    def __init__(self):
        super().__init__()
        self.monitored_value = None
        self.trigger_value = None
        self._last_value = LogicNetworkCell.NO_VALUE

    def evaluate(self):
        monitored_value = self.get_parameter_value(self.monitored_value)
        trigger_value = self.get_parameter_value(self.trigger_value)
        if is_waiting(monitored_value, trigger_value):
            return
        self._set_ready()
        # initialize the value
        if self._last_value is LogicNetworkCell.NO_VALUE:
            self._last_value = monitored_value
            self._set_value(False)
        else:
            value_changed = (monitored_value != self._last_value)
            is_trigger = (monitored_value == trigger_value)
            if value_changed:
                self._last_value = monitored_value
                self._set_value(is_trigger)
            else:
                self._set_value(False)


class ConditionOnce(ConditionCell):

    def __init__(self):
        ConditionCell.__init__(self)
        self.input_condition = None
        self.repeat = None
        self.reset_time = None
        self._consumed = False
        self.time = 0.0

    def evaluate(self):
        condition = self.get_parameter_value(self.input_condition)
        repeat = self.get_parameter_value(self.repeat)
        reset_time = self.get_parameter_value(self.reset_time)
        if is_waiting(repeat, reset_time):
            return
        network = self.network
        tl = network.timeline

        self._set_ready()
        if tl - self.time > reset_time and repeat:
            self._consumed = False
        self.time = tl
        if condition and self._consumed is False:
            self._consumed = True
            self._set_value(True)
            return
        if not_met(condition) and repeat and self._consumed:
            self._consumed = False
        self._set_value(False)


###############################################################################
# Game
###############################################################################


class ActionLoadGame(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.slot = None
        self.path = ''
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def get_game_vec(self, data):
        return mathutils.Euler((data['x'], data['y'], data['z']))

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        slot = self.get_parameter_value(self.slot)
        if is_waiting(slot):
            return
        cust_path = self.get_custom_path(self.path)

        path = (
            logic.expandPath('//Saves/') if self.path == ''
            else cust_path
        )

        scene = logic.getCurrentScene()

        try:
            with open(path + 'save' + str(slot) + '.json') as json_file:
                data = json.load(json_file)
                for obj in data['objects']:
                    if obj['name'] in scene.objects:
                        game_obj = scene.objects[obj['name']]
                    else:
                        debug(
                            'Could not load Object {}: Not in active Scene!'
                            .format(obj['name'])
                        )
                        continue

                    wPos = self.get_game_vec(obj['data']['worldPosition'])
                    wOri = self.get_game_vec(obj['data']['worldOrientation'])
                    wSca = self.get_game_vec(obj['data']['worldScale'])

                    game_obj.worldPosition = wPos
                    game_obj.worldOrientation = wOri.to_matrix()
                    game_obj.worldScale = wSca

                    if obj['type'] == 'dynamic':
                        linVel = self.get_game_vec(
                            obj['data']['worldLinearVelocity']
                        )
                        angVel = self.get_game_vec(
                            obj['data']['worldAngularVelocity']
                        )
                        game_obj.worldLinearVelocity = linVel
                        game_obj.worldAngularVelocity = angVel

                    if obj['type'] == 'light':
                        energy = obj['data']['energy']
                        game_obj.energy = energy

                    if obj['type'] == 'character':
                        wDir = self.get_game_vec(obj['data']['walkDirection'])
                        (
                            bge.constraints
                            .getCharacter(game_obj)
                            .walkDirection
                        ) = wDir

                    for prop in obj['data']['props']:
                        game_obj[prop['name']] = prop['value']
        except Exception:
            debug(
                'Load Game Node: Could Not Find Saved Game on Slot {}!'
                .format(slot)
            )

        self.done = True


class ActionEndGame(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None

    def evaluate(self):
        self._set_ready()
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        logic.endGame()


class ActionRestartGame(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self._set_ready()
        condition = self.get_parameter_value(self.condition)
        if condition:
            logic.restartGame()
        self.done = True


class ActionSaveGame(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.slot = None
        self.path = ''
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('//'):
            return bpy.path.abspath(path)
        elif path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        slot = self.get_parameter_value(self.slot)
        if is_waiting(slot):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            logic.expandPath('//Saves/') if self.path == ''
            else cust_path
        )
        os.makedirs(path, exist_ok=True)

        scene = logic.getCurrentScene()
        data = {
            'objects': []
        }

        objs = data['objects']

        for obj in scene.objects:
            if obj.name == '__default__cam__':
                continue
            props = obj.getPropertyNames()
            prop_list = []
            cha = bge.constraints.getCharacter(obj)
            for prop in props:
                if prop != 'NodeTree':
                    if isinstance(obj[prop], LogicNetwork):
                        continue
                    if isinstance(obj[prop], mathutils.Vector):
                        continue
                    prop_set = {}
                    prop_set['name'] = prop
                    prop_set['value'] = obj[prop]
                    prop_list.append(prop_set)
            loc = obj.worldPosition
            rot = obj.worldOrientation.to_euler()
            sca = obj.worldScale

            if obj.mass:
                lin_vel = obj.worldLinearVelocity
                ang_vel = obj.worldAngularVelocity

                objs.append(
                    {
                        'name': obj.name,
                        'type': 'dynamic',
                        'data': {
                            'worldPosition': {
                                'x': loc.x,
                                'y': loc.y,
                                'z': loc.z
                            },
                            'worldOrientation': {
                                'x': rot.x,
                                'y': rot.y,
                                'z': rot.z
                            },
                            'worldLinearVelocity': {
                                'x': lin_vel.x,
                                'y': lin_vel.y,
                                'z': lin_vel.z
                            },
                            'worldAngularVelocity': {
                                'x': ang_vel.x,
                                'y': ang_vel.y,
                                'z': ang_vel.z
                            },
                            'worldScale': {'x': sca.x, 'y': sca.y, 'z': sca.z},
                            'props': prop_list
                        }
                    }
                )
            if cha:
                wDir = cha.walkDirection

                objs.append(
                    {
                        'name': obj.name,
                        'type': 'character',
                        'data': {
                            'worldPosition': {
                                'x': loc.x,
                                'y': loc.y,
                                'z': loc.z
                            },
                            'worldOrientation': {
                                'x': rot.x,
                                'y': rot.y,
                                'z': rot.z
                            },
                            'worldScale': {'x': sca.x, 'y': sca.y, 'z': sca.z},
                            'walkDirection': {
                                'x': wDir.x,
                                'y': wDir.y,
                                'z': wDir.z
                            },
                            'props': prop_list
                        }
                    }
                )
            else:
                objs.append(
                    {
                        'name': obj.name,
                        'type': 'static',
                        'data': {
                            'worldPosition': {
                                'x': loc.x,
                                'y': loc.y,
                                'z': loc.z
                            },
                            'worldOrientation': {
                                'x': rot.x,
                                'y': rot.y,
                                'z': rot.z
                            },
                            'worldScale': {'x': sca.x, 'y': sca.y, 'z': sca.z},
                            'props': prop_list
                        }
                    }
                )
            data['globalDict'] = logic.globalDict

        with open(path + 'save' + str(slot) + ".json", "w") as file:
            json.dump(data, file, indent=2)

        self.done = True


class ActionStartGame(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.file_name = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self._set_ready()
        condition = self.get_parameter_value(self.condition)
        file_name = self.get_parameter_value(self.file_name)
        if condition:
            logic.startGame(file_name)
        self.done = True


###############################################################################
# Input -> Mouse
###############################################################################


class ConditionMousePressed(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.pulse = False
        self.mouse_button_code = None

    def evaluate(self):
        mouse_button = self.get_parameter_value(self.mouse_button_code)
        if is_waiting(mouse_button):
            return
        self._set_ready()
        mstat = self.network.mouse_events[mouse_button]
        if self.pulse:
            self._set_value(
                mstat.active or
                mstat.activated
            )
        else:
            self._set_value(mstat.activated)


class ConditionMousePressedOn(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.game_object = None
        self.mouse_button = None

    def evaluate(self):
        mouse_button = self.get_parameter_value(self.mouse_button)
        game_object = self.get_parameter_value(self.game_object)
        if is_waiting(mouse_button, game_object):
            return
        self._set_ready()
        if mouse_button is None:
            return
        if is_invalid(game_object):
            return
        mstat = self.network.mouse_events[mouse_button]
        if not mstat.activated:
            self._set_value(False)
            return
        mpos = logic.mouse.position
        camera = logic.getCurrentScene().active_camera
        vec = 10 * camera.getScreenVect(*mpos)
        ray_target = camera.worldPosition - vec
        distance = camera.getDistanceTo(game_object) * 2.0
        t, p, n = self.network.ray_cast(
            camera,
            None,
            ray_target,
            None,
            False,
            distance
        )
        self._set_value(t == game_object)


class ConditionMouseReleased(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.pulse = False
        self.mouse_button_code = None
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        mouse_button = self.get_parameter_value(self.mouse_button_code)
        if is_waiting(mouse_button):
            return
        self._set_ready()
        mstat = self.network.mouse_events[mouse_button]
        if self.pulse:
            self._set_value(
                mstat.released or
                mstat.inactive
            )
        else:
            self._set_value(mstat.released)


class ActionSetMouseCursorVisibility(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.visibility_status = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        visibility_status = self.get_parameter_value(self.visibility_status)
        if is_waiting(visibility_status):
            return
        self._set_ready()
        logic.mouse.visible = visibility_status
        self.done = True


class ActionMouseLook(ActionCell):
    x = None
    y = None
    screen_center = None
    center = None
    mouse = None

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object_x = None
        self.game_object_y = None
        self.inverted = None
        self.sensitivity = None
        self.use_cap_z = None
        self.cap_z = None
        self.use_cap_z = None
        self.cap_y = None
        self.smooth = None
        self._x = 0
        self._y = 0
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.use_local_head = False

    def get_done(self):
        return self.done

    def interpolate(self, a, b, fac):
        return (fac * b) + ((1-fac) * a)

    def get_x_obj(self):
        game_object_x = self.get_parameter_value(self.game_object_x)
        if is_waiting(game_object_x):
            return
        return game_object_x

    def get_y_obj(self):
        game_object_y = self.get_parameter_value(self.game_object_y)
        if is_invalid(game_object_y):
            game_object_y = self.get_x_obj()
        elif game_object_y is not self.get_x_obj():
            self.use_local_head = True
        return game_object_y

    def get_data(self):
        self.x = bge.render.getWindowWidth()//2
        self.y = bge.render.getWindowHeight()//2
        self.screen_center = (
            self.x/bge.render.getWindowWidth(),
            self.y/bge.render.getWindowHeight()
        )
        self.center = mathutils.Vector(self.screen_center)
        self.mouse = logic.mouse

    def evaluate(self):
        self.done = False
        self.get_data()
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object_x = self.get_x_obj()
        game_object_y = self.get_y_obj()
        sensitivity = self.get_parameter_value(self.sensitivity) * 1000
        use_cap_z = self.get_parameter_value(self.use_cap_z)
        use_cap_y = self.get_parameter_value(self.use_cap_y)
        cap_z = self.get_parameter_value(self.cap_z)
        lowercapX = -cap_z.y
        uppercapX = cap_z.x
        cap_y = self.get_parameter_value(self.cap_y)
        lowercapY = -cap_y.x
        uppercapY = cap_y.y
        inverted = self.get_parameter_value(self.inverted)
        smooth = 1 - (self.get_parameter_value(self.smooth) * .99)
        self._set_ready()

        if is_invalid(game_object_x):
            debug('MouseLook Node: Invalid Main Object!')
            return

        mouse_position = mathutils.Vector(self.mouse.position)
        offset = (mouse_position - self.center) * -0.002

        if inverted.get('y', False) is False:
            offset.y = -offset.y
        if inverted.get('x', False) is True:
            offset.x = -offset.x
        offset *= sensitivity

        self._x = offset.x = self.interpolate(self._x, offset.x, smooth)
        self._y = offset.y = self.interpolate(self._y, offset.y, smooth)

        if use_cap_z:
            objectRotation = game_object_x.localOrientation.to_euler()

            if objectRotation.z + offset.x > uppercapX:
                offset.x = 0
                objectRotation.z = uppercapX
                game_object_x.localOrientation = objectRotation.to_matrix()

            if objectRotation.z + offset.x < lowercapX:
                offset.x = 0
                objectRotation.z = lowercapX
                game_object_x.localOrientation = objectRotation.to_matrix()

        game_object_x.applyRotation((0, 0, offset.x), self.use_local_head)

        if use_cap_y:
            objectRotation = game_object_y.localOrientation.to_euler()

            if objectRotation.y + offset.y > uppercapY:
                objectRotation.y = uppercapY
                game_object_y.localOrientation = objectRotation.to_matrix()
                offset.y = 0

            if objectRotation.y + offset.y < lowercapY:
                objectRotation.y = lowercapY
                game_object_y.localOrientation = objectRotation.to_matrix()
                offset.y = 0

        game_object_y.applyRotation((0, (offset.y), 0), True)
        if self.mouse.position != self.screen_center:
            self.mouse.position = self.screen_center
        self.done = True


class ConditionMouseMoved(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.pulse = False

    def evaluate(self):
        self._set_ready()
        mstat = self.network.mouse_events
        if self.pulse:
            self._set_value(
                mstat[bge.events.MOUSEX].active or
                mstat[bge.events.MOUSEX].activated or
                mstat[bge.events.MOUSEY].active or
                mstat[bge.events.MOUSEY].activated
            )
        else:
            self._set_value(
                mstat[bge.events.MOUSEX].activated or
                mstat[bge.events.MOUSEY].activated
            )


class ConditionMouseTargeting(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.game_object = None
        self._mouse_entered_status = False
        self._mouse_exited_status = False
        self._mouse_over_status = False
        self._point = None
        self._normal = None
        self.MOUSE_ENTERED = LogicNetworkSubCell(self, self._get_mouse_entered)
        self.MOUSE_EXITED = LogicNetworkSubCell(self, self._get_mouse_exited)
        self.MOUSE_OVER = LogicNetworkSubCell(self, self._get_mouse_over)
        self.POINT = LogicNetworkSubCell(self, self._get_point)
        self.NORMAL = LogicNetworkSubCell(self, self._get_normal)
        self._last_target = None

    def _get_mouse_entered(self):
        return self._mouse_entered_status

    def _get_mouse_exited(self):
        return self._mouse_exited_status

    def _get_mouse_over(self):
        return self._mouse_over_status

    def _get_point(self):
        return self._point

    def _get_normal(self):
        return self._normal

    def evaluate(self):
        game_object = self.get_parameter_value(self.game_object)
        if is_waiting(game_object):
            return
        self._set_ready()
        if is_invalid(game_object):
            self._mouse_entered_status = False
            self._mouse_exited_status = False
            self._mouse_over_status = False
            self._point = None
            self._normal = None
            return
        scene = game_object.scene
        camera = scene.active_camera
        distance = 2.0 * camera.getDistanceTo(game_object)
        mouse = logic.mouse
        mouse_position = mouse.position
        vec = 10.0 * camera.getScreenVect(*mouse_position)
        ray_target = camera.worldPosition - vec
        # target, point, normal = camera.rayCast(ray_target, None, distance)
        target, point, normal = self.network.ray_cast(
            camera,
            None,
            ray_target,
            None,
            False,
            distance
        )
        if not (target is self._last_target):  # mouse over a new object
            # was target, now it isn't -> exited
            if self._last_target is game_object:
                self._mouse_exited_status = True
                self._mouse_over_status = False
                self._mouse_entered_status = False
                self._point = None
                self._normal = None
            # wasn't target, now it is -> entered
            elif (target is game_object):
                self._mouse_entered_status = True
                self._mouse_over_status = False
                self._mouse_exited_status = False
                self._point = point
                self._normal = normal
            self._last_target = target
        else:  # the target has not changed
            # was target, still target -> over
            if self._last_target is game_object:
                self._mouse_entered_status = False
                self._mouse_exited_status = False
                self._mouse_over_status = True
                self._point = point
                self._normal = normal
            else:  # wans't target, still isn't target -> clear
                self._mouse_entered_status = False
                self._mouse_exited_status = False
                self._mouse_over_status = False
                self._point = None
                self._normal = None


class ActionSetMousePosition(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.screen_x = None
        self.screen_y = None
        self.network = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self.network = network

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        screen_x = self.get_parameter_value(self.screen_x)
        screen_y = self.get_parameter_value(self.screen_y)
        if is_waiting(screen_x, screen_y):
            return
        self._set_ready()
        self.network.set_mouse_position(screen_x, screen_y)
        self.done = True


class ParameterMouseData(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.MX = LogicNetworkSubCell(self, self.getmx)
        self.MY = LogicNetworkSubCell(self, self.getmy)
        self.MDX = LogicNetworkSubCell(self, self.getmdx)
        self.MDY = LogicNetworkSubCell(self, self.getmdy)
        self.MDWHEEL = LogicNetworkSubCell(self, self.getmdwheel)
        self.MXY0 = LogicNetworkSubCell(self, self.getmxyz)
        self.MDXY0 = LogicNetworkSubCell(self, self.getmdxyz)

    def getmx(self):
        return self.network._last_mouse_position[0]

    def getmy(self):
        return self.network._last_mouse_position[1]

    def getmdx(self):
        return self.network.mouse_motion_delta[0]

    def getmdy(self):
        return self.network.mouse_motion_delta[1]

    def getmdwheel(self):
        return self.network.mouse_wheel_delta

    def getmxyz(self):
        mp = self.network._last_mouse_position
        return mathutils.Vector((mp[0], mp[1], 0))

    def getmdxyz(self):
        mp = self.network.mouse_motion_delta
        return mathutils.Vector((mp[0], mp[1], 0))

    def evaluate(self):
        self._set_ready()

    def has_status(self, status):
        return status is LogicNetworkCell.STATUS_READY


class ConditionMouseScrolled(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.wheel_direction = None

    def evaluate(self):
        wd = self.get_parameter_value(self.wheel_direction)
        if is_waiting(wd):
            return
        self._set_ready()
        if wd is None:
            return
        elif wd == 1:  # UP
            self._set_value(self.network.mouse_wheel_delta == 1)
        elif wd == 2:  # DOWN
            self._set_value(self.network.mouse_wheel_delta == -1)
        elif wd == 3:  # UP OR DOWN
            self._set_value(self.network.mouse_wheel_delta != 0)

###############################################################################
# Input -> Gamepad
###############################################################################


class ConditionGamepadButtons(ConditionCell):
    def __init__(self, pulse=False, button=0):
        ConditionCell.__init__(self)
        self.pulse = pulse
        self.button = button
        self.index = None
        self._button_value = None
        self.BUTTON = LogicNetworkSubCell(self, self.get_button)
        self.initialized = False

    def get_button(self):
        return self._button_value

    def evaluate(self):
        self._set_ready()
        index = self.get_parameter_value(self.index)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            debug('Gamepad Button Node: No Joystick at that Index!')
            return
        if is_invalid(joystick):
            return

        if self.button in joystick.activeButtons:
            if not self.initialized:
                self._button_value = True
            else:
                self._button_value = False
            if not self.pulse:
                self.initialized = True

        else:
            self._button_value = False
            self.initialized = False


class ConditionGamepadButtonUp(ConditionCell):
    def __init__(self, pulse=False, button=0):
        ConditionCell.__init__(self)
        self.pulse = pulse
        self.button = button
        self.index = None
        self._last_value = False
        self._up_value = None
        self.BUTTON = LogicNetworkSubCell(self, self.get_button)
        self.initialized = False

    def get_button(self):
        return self._up_value

    def evaluate(self):
        self._set_ready()
        index = self.get_parameter_value(self.index)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            debug('Gamepad Button Node: No Joystick at that Index!')
            return
        if is_invalid(joystick):
            return

        button_down = True if self.button in joystick.activeButtons else False

        if button_down != self._last_value and not button_down:
            self._up_value = True
            if not self.pulse and not self.initialized:
                self.initialized = True
        elif (self._up_value and self.initialized) or button_down:
            self._up_value = False
            self.initialized = False
        elif not (self.initialized and button_down) and self._up_value:
            self._up_value = True

        self._last_value = button_down


class ConditionGamepadSticks(ConditionCell):
    def __init__(self, axis=0):
        ConditionCell.__init__(self)
        self.axis = axis
        self.inverted = None
        self.index = None
        self.sensitivity = None
        self.threshold = None
        self._x_axis_values = None
        self._y_axis_values = None
        self.X = LogicNetworkSubCell(self, self.get_x_axis)
        self.Y = LogicNetworkSubCell(self, self.get_y_axis)

    def get_x_axis(self):
        return self._x_axis_values

    def get_y_axis(self):
        return self._y_axis_values

    def evaluate(self):
        self._set_ready()
        axis = self.get_parameter_value(self.axis)
        if is_invalid(axis):
            debug('Gamepad Sticks Node: Invalid Controller Stick!')
            return
        inverted = self.get_parameter_value(self.inverted)
        index = self.get_parameter_value(self.index)
        sensitivity = self.get_parameter_value(self.sensitivity)
        threshold = self.get_parameter_value(self.threshold)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            debug('Gamepad Sticks Node: No Joystick at that Index!')
            self._x_axis_values = 0
            self._y_axis_values = 0
            return
        if is_invalid(joystick):
            return
        raw_values = joystick.axisValues
        values = []
        if axis == 2:
            raw_values = [raw_values[0], raw_values[1]]
        elif axis == 1:
            raw_values = [raw_values[2], raw_values[3]]
        for x in raw_values:
            if -threshold < x < threshold:
                x = 0
            x *= sensitivity
            values.append((-x if inverted else x))

        x_axis = values[0]
        y_axis = values[1]
        self._x_axis_values = x_axis
        self._y_axis_values = y_axis


class ConditionGamepadTrigger(ConditionCell):
    def __init__(self, axis=0):
        ConditionCell.__init__(self)
        self.axis = axis
        self.index = None
        self.sensitivity = None
        self.threshold = None
        self._value = None
        self.VAL = LogicNetworkSubCell(self, self.get_value)

    def get_x_axis(self):
        return self._value

    def evaluate(self):
        self._set_ready()
        axis = self.get_parameter_value(self.axis)
        if is_invalid(axis):
            debug('Gamepad Trigger Node: Invalid Controller Trigger!')
            return
        index = self.get_parameter_value(self.index)
        sensitivity = self.get_parameter_value(self.sensitivity)
        threshold = self.get_parameter_value(self.threshold)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            debug('Gamepad Trigger Node: No Joystick at that Index!')
            self._x_axis_values = 0
            self._y_axis_values = 0
            return
        if is_invalid(joystick):
            return
        value = joystick.axisValues[4] if axis == 0 else joystick.axisValues[5]

        if -threshold < value < threshold:
            value = 0
        self._value = value * sensitivity


class GEGamepadVibration(ConditionCell):
    def __init__(self, axis=0):
        ConditionCell.__init__(self)
        self.condition = None
        self.index = None
        self.left = None
        self.right = None
        self.time = None
        self.done = None
        self.DONE = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self._set_ready()
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        index = self.get_parameter_value(self.index)
        left = self.get_parameter_value(self.left)
        right = self.get_parameter_value(self.right)
        time = self.get_parameter_value(self.time)
        if is_waiting(index, left, right, time):
            return

        if not logic.joysticks[index]:
            return
        joystick = logic.joysticks[index]
        if not joystick.hasVibration:
            debug('Joystick at index {} has no vibration!'.format(index))
            return

        joystick.strengthLeft = left
        joystick.strengthRight = right
        joystick.duration = int(round(time * 1000))

        joystick.startVibration()
        self.done = True


###############################################################################
# Input -> Keyboard
###############################################################################


class ParameterKeyboardKeyCode(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.key_code = None

    def evaluate(self):
        self._set_ready()
        key_code = self.get_parameter_value(self.key_code)
        self._set_value(key_code)


class ConditionKeyPressed(ConditionCell):
    def __init__(self, pulse=False, key_code=None):
        ConditionCell.__init__(self)
        self.pulse = pulse
        self.key_code = key_code
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        keycode = self.get_parameter_value(self.key_code)
        if is_waiting(keycode):
            return
        self._set_ready()
        keystat = self.network.keyboard_events[keycode]
        if self.pulse:
            self._set_value(
                (
                    keystat.active or keystat.activated
                )
            )
        else:
            self._set_value(keystat.activated)


###############################################################################
# Unordered
###############################################################################


class ParamOwnerObject(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)

    def setup(self, network):
        ParameterCell.setup(self, network)
        self._set_status(LogicNetworkCell.STATUS_READY)
        self._set_value(network.get_owner())

    def reset(self):
        pass

    def evaluate(self):
        pass


class ParameterBoneStatus(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.armature = None
        self.bone_name = None
        self._prev_armature = LogicNetworkCell.NO_VALUE
        self._prev_bone = LogicNetworkCell.NO_VALUE
        self._channel = None
        self._pos = mathutils.Vector((0, 0, 0))
        self._rot = mathutils.Euler((0, 0, 0), "XYZ")
        self._sca = mathutils.Vector((0, 0, 0))
        self.XYZ_POS = LogicNetworkSubCell(self, self._get_pos)
        self.XYZ_ROT = LogicNetworkSubCell(self, self._get_rot)
        self.XYZ_SCA = LogicNetworkSubCell(self, self._get_sca)

    def _get_pos(self):
        return self._pos

    def _get_sca(self):
        return self._sca

    def _get_rot(self):
        return self._rot

    def evaluate(self):
        armature = self.get_parameter_value(self.armature)
        bone_name = self.get_parameter_value(self.bone_name)
        if is_invalid(armature, bone_name):
            return
        self._set_ready()
        channel = None
        if (
            (armature is self._prev_armature) and
            (bone_name == self._prev_bone)
        ):
            channel = self._channel
        else:
            self._prev_armature = armature
            self._prev_bone = bone_name
            self._channel = armature.channels[bone_name]
            channel = self._channel
        if channel.rotation_mode is logic.ROT_MODE_QUAT:
            self._rot[:] = (
                mathutils.Quaternion(channel.rotation_quaternion).to_euler()
            )
        else:
            self._rot[:] = channel.rotation_euler
        self._pos[:] = channel.location
        self._sca[:] = channel.scale


class ParameterCurrentScene(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self._set_ready()

    def get_value(self):
        return logic.getCurrentScene()

    def reset(self): pass
    def evaluate(self): pass


class ParameterParentGameObject(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.game_object = None

    def evaluate(self):
        self._set_ready()
        game_object = self.get_parameter_value(self.game_object)
        if is_invalid(game_object):
            return
        self._set_value(game_object.parent)


class ParameterAxisVector(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.game_object = None

    def evaluate(self):
        obj = self.get_parameter_value(self.game_object)
        front_vector = LO_AXIS_TO_VECTOR[self.axis]
        if is_invalid(obj, front_vector):
            return
        self._set_ready()
        self._set_value(obj.getAxisVect(front_vector))


class ParameterSwitchValue(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.state = None
        self.outcome = False
        self.TRUE = LogicNetworkSubCell(self, self.get_true_value)
        self.FALSE = LogicNetworkSubCell(self, self.get_false_value)

    def get_true_value(self):
        state = self.get_parameter_value(self.state)
        if state:
            return True
        else:
            return False

    def get_false_value(self):
        state = self.get_parameter_value(self.state)
        if state:
            return False
        else:
            return True

    def evaluate(self):
        state = self.get_parameter_value(self.state)
        if is_waiting(state):
            return
        self._set_ready()
        if state:
            self.outcome = True
        self._set_value(self.outcome)


class ParameterObjectProperty(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.game_object = None
        self.property_name = None

    def evaluate(self):
        game_object = self.get_parameter_value(self.game_object)
        property_name = self.get_parameter_value(self.property_name)
        if is_invalid(game_object, property_name):
            return
        self._set_ready()
        if property_name not in game_object:
            game_object[property_name] = None
        else:
            self._set_value(game_object[property_name])


class ParameterGetNodeTreeNodeValue(ParameterCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.tree_name = None
        self.node_name = None
        self.input_slot = None
        self.val = False
        self.OUT = LogicNetworkSubCell(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        tree_name = self.get_parameter_value(self.tree_name)
        node_name = self.get_parameter_value(self.node_name)
        if is_invalid(tree_name, node_name):
            return
        input_slot = self.get_parameter_value(self.input_slot)
        if is_waiting(tree_name):
            return
        self._set_ready()
        self.val = (
            bpy.data.node_groups[tree_name]
            .nodes[node_name]
            .inputs[input_slot]
            .default_value
        )


class ParameterGetNodeTreeNodeAttribute(ParameterCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.val = False
        self.OUT = LogicNetworkSubCell(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        mat_name = self.get_parameter_value(self.mat_name)
        node_name = self.get_parameter_value(self.node_name)
        if is_invalid(mat_name, node_name):
            return
        internal = self.get_parameter_value(self.internal)
        attribute = self.get_parameter_value(self.attribute)
        if is_waiting(mat_name):
            return
        self._set_ready()
        target = (
            bpy.data
            .node_groups[mat_name]
            .nodes[node_name]
        )
        if internal:
            target = getattr(target, internal, target)
        self.val = getattr(target, attribute, None)


class ParameterGetMaterialNodeValue(ParameterCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.input_slot = None
        self.val = False
        self.OUT = LogicNetworkSubCell(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        mat_name = self.get_parameter_value(self.mat_name)
        node_name = self.get_parameter_value(self.node_name)
        if is_invalid(mat_name, node_name):
            return
        input_slot = self.get_parameter_value(self.input_slot)
        if is_waiting(mat_name):
            return
        self._set_ready()
        self.val = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
            .inputs[input_slot]
            .default_value
        )


class ParameterGetMaterialNodeAttribute(ParameterCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.val = False
        self.OUT = LogicNetworkSubCell(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        mat_name = self.get_parameter_value(self.mat_name)
        node_name = self.get_parameter_value(self.node_name)
        if is_invalid(mat_name, node_name):
            return
        internal = self.get_parameter_value(self.internal)
        attribute = self.get_parameter_value(self.attribute)
        if is_waiting(mat_name):
            return
        self._set_ready()
        target = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
        )
        if internal:
            target = getattr(target, internal, target)
        self.val = getattr(target, attribute, None)


class ParameterGetMaterialNode(ParameterCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.val = False
        self.OUT = LogicNetworkSubCell(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        mat_name = self.get_parameter_value(self.mat_name)
        node_name = self.get_parameter_value(self.node_name)
        if is_invalid(mat_name, node_name):
            return
        self._set_ready()
        self.val = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
        )


class ParameterObjectHasProperty(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.game_object = None
        self.property_name = None

    def evaluate(self):
        game_object = self.get_parameter_value(self.game_object)
        property_name = self.get_parameter_value(self.property_name)
        if is_invalid(game_object, property_name):
            debug('Has Property Node: Object or Property Name invalid!')
            return
        self._set_ready()
        self._set_value(
            True if property_name in game_object.getPropertyNames()
            else False
        )


class ParameterDictionaryValue(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.dict = None
        self.key = None

    def evaluate(self):
        dictionary = self.get_parameter_value(self.dict)
        key = self.get_parameter_value(self.key)
        if is_invalid(dictionary, key):
            return
        self._set_ready()
        if key in dictionary:
            self._set_value(dictionary[key])
        else:
            debug("Dict Get Value Node: Key '{}' Not In Dict!".format(key))


class ParameterListIndex(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.items = None
        self.index = None

    def evaluate(self):
        list_d = self.get_parameter_value(self.items)
        index = self.get_parameter_value(self.index)
        if is_invalid(list_d):
            return
        if is_waiting(index):
            return
        self._set_ready()
        if index <= len(list_d) - 1:
            self._set_value(list_d[index])
        else:
            debug('List Index Node: Index Out Of Range!')


class ParameterRandomListIndex(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.items = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_parameter_value(self.items)
        if is_invalid(list_d):
            return
        self._set_ready()
        self._set_value(random.choice(list_d))


class DuplicateList(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.items = None

    def evaluate(self):
        list_d = self.get_parameter_value(self.items)
        if is_invalid(list_d):
            return
        self._set_ready()
        self._set_value(list_d.copy())


class GetActuator(ParameterCell):

    @classmethod
    def act(cls, actuator):
        return actuator

    @classmethod
    def obj(cls, obj_name):
        return obj_name

    def __init__(self):
        ParameterCell.__init__(self)
        self.obj_name = None
        self.act_name = None

    def evaluate(self):
        game_obj = self.get_parameter_value(self.obj_name)
        if is_invalid(game_obj, self.act_name):
            return
        self._set_ready()
        self._set_value(game_obj.actuators[self.act_name])


class GetActuatorByName(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.act_name = None

    def evaluate(self):
        act_name = self.get_parameter_value(self.act_name)
        cont = logic.getCurrentController()
        if is_invalid(act_name):
            return
        if act_name not in cont.actuators:
            debug(f'Controller "{cont}" has no actuator "{act_name}"')
            return
        self._set_ready()
        self._set_value(logic.getCurrentController().actuators[act_name])


class GetActuatorValue(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.actuator = None
        self.field = None

    def evaluate(self):
        actuator = self.get_parameter_value(self.actuator)
        field = self.get_parameter_value(self.field)
        if is_invalid(actuator, field):
            return
        self._set_ready()
        self._set_value(getattr(actuator, field))


class ActivateActuator(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.actuator = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        actuator = str(self.get_parameter_value(self.actuator))
        self._set_ready()
        if is_invalid(actuator):
            return
        controller = logic.getCurrentController()
        if actuator not in controller.actuators:
            debug(f'Controller "{controller}" has no actuator "{actuator}"')
            return
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            controller.deactivate(actuator)
            return
        controller.activate(actuator)
        self.done = True


class DeactivateActuator(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.actuator = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        actuator = str(self.get_parameter_value(self.actuator))
        if is_invalid(actuator):
            return
        controller = logic.getCurrentController()
        if actuator not in controller.actuators:
            return
        self._set_ready()
        controller.deactivate(actuator)
        self.done = True


class ActivateActuatorByName(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.actuator = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        actuator = str(self.get_parameter_value(self.actuator))
        if is_invalid(actuator):
            return
        controller = logic.getCurrentController()
        if actuator not in controller.actuators:
            debug(f'Controller "{controller}" has no actuator "{actuator}"')
            return
        condition = self.get_parameter_value(self.condition)
        self._set_ready()
        if not_met(condition):
            controller.deactivate(actuator)
            return
        controller.activate(actuator)
        self.done = True


class DeactivateActuatorByName(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.actuator = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        actuator = str(self.get_parameter_value(self.actuator))
        if is_invalid(actuator):
            return
        condition = self.get_parameter_value(self.condition)
        controller = logic.getCurrentController()
        if actuator not in controller.actuators:
            return
        self._set_ready()
        if not_met(condition):
            return
        controller.deactivate(actuator)
        self.done = True


class SetActuatorValue(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.actuator = None
        self.field = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        actuator = self.get_parameter_value(self.actuator)
        if is_invalid(actuator):
            return
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        field = self.get_parameter_value(self.field)
        value = self.get_parameter_value(self.value)
        if is_waiting(field, value):
            return
        setattr(actuator, field, value)
        self.done = True


class GetController(ParameterCell):

    @classmethod
    def cont(cls, controller):
        return controller

    @classmethod
    def obj(cls, obj_name):
        return obj_name

    def __init__(self):
        ParameterCell.__init__(self)
        self.obj_name = None
        self.cont_name = None

    def evaluate(self):
        game_obj = self.get_parameter_value(self.obj_name)
        if is_invalid(game_obj):
            debug('Get Controller Node: No Game Object selected!')
            return
        if is_invalid(self.cont_name):
            debug('Get Controller Node: No Controller selected!')
            return
        self._set_ready()
        self._set_value(game_obj.controllers[self.cont_name])


class GetCurrentControllerLB(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(logic.getCurrentController())


class GetSensor(ParameterCell):

    @classmethod
    def sens(cls, sensor):
        return sensor

    @classmethod
    def obj(cls, obj_name):
        return obj_name

    def __init__(self):
        ParameterCell.__init__(self)
        self.obj_name = None
        self.sens_name = None

    def evaluate(self):
        game_obj = self.get_parameter_value(self.obj_name)
        if is_invalid(game_obj):
            debug('Get Sensor Node: No Game Object selected!')
            return
        if is_invalid(self.sens_name):
            debug('Get Sensor Node: No Sensor selected!')
            return
        self._set_ready()
        self._set_value(game_obj.sensors[self.sens_name].positive)


class GetSensorByName(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.obj = None
        self.name = None

    def evaluate(self):
        obj = self.get_parameter_value(self.obj)
        name = self.get_parameter_value(self.name)
        if name in obj.sensors:
            self._set_ready()
            self._set_value(obj.sensors[name].positive)
        else:
            debug("{} has no Sensor named '{}'!".format(obj.name, name))
            return


class GetSensorValueByName(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.obj = None
        self.name = None
        self.field = None

    def evaluate(self):
        obj = self.get_parameter_value(self.obj)
        name = self.get_parameter_value(self.name)
        field = self.get_parameter_value(self.field)
        if name in obj.sensors:
            self._set_ready()
            self._set_value(getattr(obj.sensors[name], field))
        else:
            debug("{} has no Sensor named '{}'!".format(obj.name, name))


class SensorValue(ParameterCell):

    @classmethod
    def sens(cls, sensor):
        return sensor

    @classmethod
    def obj(cls, obj_name):
        return obj_name

    def __init__(self):
        ParameterCell.__init__(self)
        self.obj_name = None
        self.sens_name = None
        self.field = None
        self.val = None
        self.VAL = LogicNetworkSubCell(self, self.get_val)

    def get_val(self):
        return self.val

    def evaluate(self):
        game_obj = self.get_parameter_value(self.obj_name)
        if is_invalid(game_obj):
            debug('Get Sensor Node: No Game Object selected!')
            return
        if is_invalid(self.sens_name):
            debug('Get Sensor Node: No Sensor selected!')
            return
        field = self.get_parameter_value(self.field)
        if is_waiting(field):
            return
        self._set_ready()
        self.val = getattr(game_obj.sensors[self.sens_name], field)


class SensorPositive(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.sensor = None
        self.done = None

    def evaluate(self):
        sens = self.get_parameter_value(self.sensor)
        if is_invalid(sens):
            return
        self._set_ready()
        self._set_value(sens.positive)


class ParameterActiveCamera(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)

    def evaluate(self):
        scene = logic.getCurrentScene()
        self._set_ready()
        if is_invalid(scene):
            debug('Active Camera Node: Invalid Scene!')
            self._set_value(None)
        else:
            self._set_value(scene.active_camera)


class GetGravity(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.collection = None

    def evaluate(self):
        self._set_ready()
        self._set_value(bge.logic.getCurrentScene().gravity)


class GetCollection(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.collection = None

    def evaluate(self):
        collection = self.get_parameter_value(self.collection)
        if is_invalid(collection):
            return
        self._set_ready()
        self._set_value(collection)


class GetCollectionObjects(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.collection = None

    def evaluate(self):
        collection = self.get_parameter_value(self.collection)
        if is_invalid(collection):
            return
        self._set_ready()
        col = bpy.data.collections.get(collection)
        if not col:
            return
        objects = []
        for o in col.objects:
            objects.append(check_game_object(o.name))
        self._set_value(objects)


class GetCollectionObjectNames(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.collection = None

    def evaluate(self):
        collection = self.get_parameter_value(self.collection)
        if is_invalid(collection):
            return
        self._set_ready()
        col = bpy.data.collections.get(collection)
        if not col:
            return
        objects = []
        for o in col.objects:
            if not o.parent:
                objects.append(o.name)
        self._set_value(objects)


class ParameterScreenPosition(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.game_object = None
        self.camera = None
        self.xposition = LogicNetworkSubCell(self, self._get_xposition)
        self.yposition = LogicNetworkSubCell(self, self._get_yposition)
        self._xpos = None
        self._ypos = None

    def _get_xposition(self):
        return self._xpos

    def _get_yposition(self):
        return self._ypos

    def evaluate(self):
        self._set_ready()
        game_object = self.get_parameter_value(self.game_object)
        camera = self.get_parameter_value(self.camera)
        if is_invalid(game_object) or is_invalid(camera):
            self._xpos = None
            self._ypos = None
            self._set_value(None)
            return
        position = camera.getScreenPosition(game_object)
        self._set_value(position)
        self._xpos = position[0]
        self._ypos = position[1]


class ParameterWorldPosition(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.camera = None
        self.screen_x = None
        self.screen_y = None
        self.world_z = None

    def evaluate(self):
        self._set_ready()
        camera = self.get_parameter_value(self.camera)
        screen_x = self.get_parameter_value(self.screen_x)
        screen_y = self.get_parameter_value(self.screen_y)
        world_z = self.get_parameter_value(self.world_z)
        if (
            is_invalid(camera) or
            (screen_x is None) or
            (screen_y is None) or
            (world_z is None)
        ):
            self._set_value(None)
        else:
            direction = camera.getScreenVect(screen_x, screen_y)
            origin = camera.worldPosition
            aim = direction * -world_z
            point = origin + (aim)
            self._set_value(point)


class GECursorBehavior(ActionCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.cursor_object = None
        self.world_z = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self._set_ready()
        camera = logic.getCurrentScene().active_camera
        condition = self.get_parameter_value(self.condition)
        cursor_object = self.get_parameter_value(self.cursor_object)
        world_z = self.get_parameter_value(self.world_z)
        if is_invalid(cursor_object):
            return
        if not_met(condition):
            if cursor_object.visible:
                cursor_object.setVisible(False, True)
            return
        if not cursor_object.visible:
            cursor_object.setVisible(True, True)
        else:
            x = self.network._last_mouse_position[0]
            y = self.network._last_mouse_position[1]
            direction = camera.getScreenVect(x, y)
            origin = camera.worldPosition
            aim = direction * -world_z
            point = origin + aim
            cursor_object.worldOrientation = camera.worldOrientation
            cursor_object.worldPosition = point
        self.done = True


class ParameterPythonModuleFunction(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.module_name = None
        self.module_func = None
        self.use_arg = None
        self.arg = None
        self.val = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.VAL = LogicNetworkSubCell(self, self.get_val)
        self._old_mod_name = None
        self._old_mod_fun = None
        self._module = None
        self._modfun = None

    def get_done(self):
        return self.done

    def get_val(self):
        return self.val

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        mname = self.get_parameter_value(self.module_name)
        mfun = self.get_parameter_value(self.module_func)
        if is_waiting(mname, mfun):
            return
        use_arg = self.get_parameter_value(self.use_arg)
        arg = self.get_parameter_value(self.arg)
        self._set_ready()
        if mname and (self._old_mod_name != mname):
            exec("import {}".format(mname))
            self._old_mod_name = mname
            self._module = eval(mname)
        if self._old_mod_fun != mfun:
            self._modfun = getattr(self._module, mfun)
            self._old_mod_fun = mfun
        if use_arg:
            self.val = self._modfun(arg)
        else:
            self.val = self._modfun()
        self.done = True


class ParameterTime(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.network = None
        self.TIME_PER_FRAME = LogicNetworkSubCell(
            self,
            self.get_time_per_frame
        )
        self.FPS = LogicNetworkSubCell(self, self.get_fps)
        self.TIMELINE = LogicNetworkSubCell(self, self.get_timeline)

    def get_time_per_frame(self):
        return self.network.time_per_frame

    def get_fps(self):
        tpf = self.network.time_per_frame
        if not tpf:
            return 1
        fps = (1 / tpf)
        return fps

    def get_timeline(self):
        return self.network.timeline

    def setup(self, network):
        self.network = network

    def has_status(self, status):
        return status is LogicNetworkCell.STATUS_READY

    def evaluate(self):
        pass


class ParameterObjectAttribute(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.game_object = None
        self.attribute_name = None

    def evaluate(self):
        game_object = self.get_parameter_value(self.game_object)
        attribute_name = self.get_parameter_value(self.attribute_name)
        if is_waiting(game_object, attribute_name):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if not hasattr(game_object, attribute_name):
            debug(
                'Get Object Data Node: {} has no attribute {}!'
                .format(game_object, attribute_name)
            )
            return
        val = getattr(game_object, attribute_name)
        self._set_value(
            val.copy() if isinstance(val, mathutils.Vector)
            else val
        )


class ClampValue(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.value = None
        self.range = None

    def evaluate(self):
        value = self.get_parameter_value(self.value)
        range_ft = self.get_parameter_value(self.range)
        if is_waiting(range_ft):
            return
        if is_invalid(value):
            return
        self._set_ready()
        if range_ft.x == range_ft.y:
            self._set_value(value)
            return
        if value < range_ft.x:
            value = range_ft.x
        if value > range_ft.y:
            value = range_ft.y
        self._set_value(value)


class InterpolateValue(ParameterCell):

    def __init__(self):
        ParameterCell.__init__(self)
        self.value_a = None
        self.value_b = None
        self.factor = None

    def evaluate(self):
        value_a = self.get_parameter_value(self.value_a)
        value_b = self.get_parameter_value(self.value_b)
        factor = self.get_parameter_value(self.factor)
        if is_invalid(value_a, value_b, factor):
            return
        self._set_ready()
        self._set_value((factor * value_b) + ((1-factor) * value_a))


class ParameterArithmeticOp(ParameterCell):
    @classmethod
    def op_by_code(cls, str):
        import operator
        opmap = {
            "ADD": operator.add,
            "SUB": operator.sub,
            "DIV": operator.truediv,
            "MUL": operator.mul
        }
        return opmap.get(str)

    def __init__(self):
        ParameterCell.__init__(self)
        self.operand_a = None
        self.operand_b = None
        self.operator = None

    def get_vec_calc(self, vec, num):
        if len(vec) == 4:
            return mathutils.Vector(
                (
                    self.operator(vec.x, num),
                    self.operator(vec.y, num),
                    self.operator(vec.z, num),
                    self.operator(vec.w, num)
                )
            )
        else:
            return mathutils.Vector(
                (
                    self.operator(vec.x, num),
                    self.operator(vec.y, num),
                    self.operator(vec.z, num)
                )
            )

    def get_vec_vec_calc(self, vec, vec2):
        if len(vec) == 4 and len(vec2) == 4:
            return mathutils.Vector(
                (
                    self.operator(vec.x, vec2.x),
                    self.operator(vec.y, vec2.y),
                    self.operator(vec.z, vec2.z),
                    self.operator(vec.w, vec2.w)
                )
            )
        else:
            return mathutils.Vector(
                (
                    self.operator(vec.x, vec2.x),
                    self.operator(vec.y, vec2.y),
                    self.operator(vec.z, vec2.z)
                )
            )

    def evaluate(self):
        a = self.get_parameter_value(self.operand_a)
        b = self.get_parameter_value(self.operand_b)
        if is_waiting(a, b):
            return
        self._set_ready()
        if (a is None) or (b is None):
            self._set_value(None)
        else:
            if (
                isinstance(a, mathutils.Vector) and
                isinstance(b, mathutils.Vector)
            ):
                self._set_value(self.get_vec_vec_calc(a, b))
                return
            elif isinstance(a, mathutils.Vector):
                self._set_value(self.get_vec_calc(a, b))
                return
            elif isinstance(b, mathutils.Vector):
                debug('Math Node: Only Second Argument is Vector! \
                    Either both or only first can be Vector!')
                return
            self._set_value(self.operator(a, b))


class Threshold(ParameterCell):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        ParameterCell.__init__(self)
        self.value = None
        self.else_z = None
        self.threshold = None
        self.operator = None

    def calc_threshold(self, op, v, t, e):
        if op == 'GREATER':
            return v if v > t else (0 if e else t)
        if op == 'LESS':
            return v if v < t else (0 if e else t)

    def evaluate(self):
        v = self.get_parameter_value(self.value)
        e = self.get_parameter_value(self.else_z)
        t = self.get_parameter_value(self.threshold)
        if is_waiting(v, t):
            return
        value = self.calc_threshold(self.operator, v, t, e)
        self._set_ready()
        if (v is None) or (t is None):
            self._set_value(None)
        else:
            self._set_value(value)


class RangedThreshold(ParameterCell):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        ParameterCell.__init__(self)
        self.value = None
        self.threshold = None
        self.operator = None

    def calc_threshold(self, op, v, t):
        if op == 'OUTSIDE':
            return v if (v < t.x or v > t.y) else 0
        if op == 'INSIDE':
            return v if (t.x < v < t.y) else 0

    def evaluate(self):
        v = self.get_parameter_value(self.value)
        t = self.get_parameter_value(self.threshold)
        if is_waiting(v, t):
            return
        value = self.calc_threshold(self.operator, v, t)
        self._set_ready()
        if (v is None) or (t is None):
            self._set_value(None)
        else:
            self._set_value(value)


class WithinRange(ParameterCell):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        ParameterCell.__init__(self)
        self.value = None
        self.range = None
        self.operator = None

    def calc_range(self, op, v, r):
        if op == 'OUTSIDE':
            return True if (v < r.x or v > r.y) else False
        if op == 'INSIDE':
            return True if (r.x < v < r.y) else False

    def evaluate(self):
        v = self.get_parameter_value(self.value)
        r = self.get_parameter_value(self.range)
        if is_waiting(v, r):
            return
        value = self.calc_range(self.operator, v, r)
        self._set_ready()
        if (v is None) or (r is None):
            self._set_value(None)
        else:
            self._set_value(value)


class GetObInstanceAttr(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.instance = None
        self.attr = None

    def evaluate(self):
        instance = self.get_parameter_value(self.instance)
        attr = self.get_parameter_value(self.attr)
        if is_waiting(instance, attr):
            return
        if not hasattr(instance, attr):
            debug(
                'Get Object Attribute Node: Object has no attr "{}"'.format(
                    attr
                )
            )
            self._set_ready()
            self._set_value(None)
            return
        self._set_ready()
        self._set_value(getattr(instance, attr))


class GetScene(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(logic.getCurrentScene())


class GetTimeScale(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(logic.getTimeScale())


class SetObInstanceAttr(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.instance = None
        self.attr = None
        self.value = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        instance = self.get_parameter_value(self.instance)
        attr = self.get_parameter_value(self.attr)
        value = self.get_parameter_value(self.value)
        if is_waiting(instance, attr, value):
            return
        self._set_ready()
        setattr(instance, attr, value)


class NormalizeVector(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.vector = None

    def evaluate(self):
        vector = self.get_parameter_value(self.vector)
        if is_waiting(vector):
            return
        self._set_ready()
        self._set_value(vector.normalize())


class ParameterActionStatus(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.game_object = None
        self.action_layer = None
        self._action_name = ""
        self._action_frame = 0.0
        self.NOT_PLAYING = LogicNetworkSubCell(self, self.get_not_playing)
        self.ACTION_NAME = LogicNetworkSubCell(self, self.get_action_name)
        self.ACTION_FRAME = LogicNetworkSubCell(self, self.get_action_frame)

    def get_action_name(self):
        return self._action_name

    def get_action_frame(self):
        return self._action_frame

    def get_not_playing(self):
        return not self.get_value()

    def evaluate(self):
        game_object = self.get_parameter_value(self.game_object)
        action_layer = self.get_parameter_value(self.action_layer)
        if is_waiting(game_object, action_layer):
            return
        self._set_ready()
        if is_invalid(game_object):
            self._action_name = ""
            self._action_frame = 0.0
            self._set_value(False)
        else:
            self._set_value(game_object.isPlayingAction(action_layer))
            self._action_name = game_object.getActionName(action_layer)
            self._action_frame = game_object.getActionFrame(action_layer)


class ParameterSimpleValue(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.value = None

    def evaluate(self):
        value = self.get_parameter_value(self.value)
        self._set_ready()
        self._set_value(value)


class ParameterTypeCast(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.to_type = None
        self.value = None

    def typecast_value(self, value, t):
        if t == 'int':
            return int(value)
        elif t == 'bool':
            return bool(value)
        elif t == 'str':
            return str(value)
        elif t == 'float':
            return float(value)

    def evaluate(self):
        value = self.get_parameter_value(self.value)
        to_type = self.get_parameter_value(self.to_type)
        if is_waiting(to_type, value):
            return
        self._set_ready()
        self._set_value(self.typecast_value(value, to_type))


class ParameterVectorMath(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.op = None
        self.vector = None
        self.vector_2 = None
        self.factor = None

    def calc_output_vector(self, op, vec, vec2, fac):
        matvec = vec.copy()
        if op == 'normalize':
            matvec.normalize()
        elif op == 'lerp':
            return matvec.lerp(vec2, fac)
        elif op == 'negate':
            matvec.negate()
        elif op == 'dot':
            return matvec.dot(vec2)
        elif op == 'cross':
            return matvec.cross(vec2)
        elif op == 'project':
            return matvec.project(vec2)
        return matvec

    def evaluate(self):
        op = self.get_parameter_value(self.op)
        vector = self.get_parameter_value(self.vector)
        vector_2 = self.get_parameter_value(self.vector_2)
        factor = self.get_parameter_value(self.factor)
        if op is None:
            return
        if vector is None:
            return
        if vector_2 is None:
            return
        if factor is None:
            return
        self._set_ready()
        self._set_value(self.calc_output_vector(op, vector, vector_2, factor))


class ParameterVector(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_vector = None
        self.input_x = None
        self.input_y = None
        self.input_z = None
        self.output_vector = mathutils.Vector()
        self.OUTX = LogicNetworkSubCell(self, self.get_out_x)
        self.OUTY = LogicNetworkSubCell(self, self.get_out_y)
        self.OUTZ = LogicNetworkSubCell(self, self.get_out_z)
        self.OUTV = LogicNetworkSubCell(self, self.get_out_v)
        self.NORMVEC = LogicNetworkSubCell(self, self.get_normalized_vector)

    def get_out_x(self): return self.output_vector.x
    def get_out_y(self): return self.output_vector.y
    def get_out_z(self): return self.output_vector.z
    def get_out_v(self): return self.output_vector.copy()
    def get_normalized_vector(self): return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        x = self.get_parameter_value(self.input_x)
        y = self.get_parameter_value(self.input_y)
        z = self.get_parameter_value(self.input_z)
        v = self.get_parameter_value(self.input_vector)
        # TODO: zero vector if v is None?
        if not is_invalid(v):
            self.output_vector[:] = v
        if not is_invalid(x):
            self.output_vector.x = x
        if not is_invalid(y):
            self.output_vector.y = y
        if not is_invalid(z):
            self.output_vector.z = z
        self._set_value(self.output_vector)


class ParameterVector2Simple(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_x = None
        self.input_y = None
        self.output_vector = mathutils.Vector()
        self.OUTV = LogicNetworkSubCell(self, self.get_out_v)

    def get_out_v(self): return self.output_vector.copy()
    def get_normalized_vector(self): return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        x = self.get_parameter_value(self.input_x)
        y = self.get_parameter_value(self.input_y)
        if not is_invalid(x):
            self.output_vector.x = x
        if not is_invalid(y):
            self.output_vector.y = y
        self._set_value(self.output_vector)


class ParameterVector2Split(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_v = None
        self.output_v = mathutils.Vector()
        self.OUTX = LogicNetworkSubCell(self, self.get_out_x)
        self.OUTY = LogicNetworkSubCell(self, self.get_out_y)

    def get_out_x(self): return self.output_v.x
    def get_out_y(self): return self.output_v.y

    def evaluate(self):
        self._set_ready()
        vec = self.get_parameter_value(self.input_v)
        if vec is not None:
            self.output_v = vec
        self._set_value(vec)


class ParameterVector3Split(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_v = None
        self.output_v = mathutils.Vector()
        self.OUTX = LogicNetworkSubCell(self, self.get_out_x)
        self.OUTY = LogicNetworkSubCell(self, self.get_out_y)
        self.OUTZ = LogicNetworkSubCell(self, self.get_out_z)

    def get_out_x(self): return self.output_v.x
    def get_out_y(self): return self.output_v.y
    def get_out_z(self): return self.output_v.z

    def evaluate(self):
        self._set_ready()
        vec = self.get_parameter_value(self.input_v)
        if vec is not None:
            self.output_v = vec
        self._set_value(vec)


class ParameterAbsVector3(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_v = None
        self.output_v = mathutils.Vector()
        self.OUTV = LogicNetworkSubCell(self, self.get_out_v)

    def get_out_v(self): return self.output_v

    def evaluate(self):
        self._set_ready()
        vec = self.get_parameter_value(self.input_v)
        vec.x = abs(vec.x)
        vec.y = abs(vec.y)
        vec.z = abs(vec.z)
        if vec is not None:
            self.output_v = vec
        self._set_value(vec)


class ParameterEulerToMatrix(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_e = None
        self.matrix = mathutils.Matrix()
        self.OUT = LogicNetworkSubCell(self, self.get_matrix)

    def get_matrix(self):
        return self.matrix

    def evaluate(self):
        self._set_ready()
        vec = self.get_parameter_value(self.input_e)
        if isinstance(vec, mathutils.Vector):
            vec = mathutils.Euler((vec.x, vec.y, vec.z), 'XYZ')
        self.matrix = vec.to_matrix()


class ParameterMatrixToEuler(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_m = None
        self.euler = mathutils.Euler()
        self.OUT = LogicNetworkSubCell(self, self.get_euler)

    def get_euler(self):
        return self.euler

    def evaluate(self):
        self._set_ready()
        matrix = self.get_parameter_value(self.input_m)
        self.euler = matrix.to_euler()


class ParameterMatrixToVector(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_m = None
        self.vec = mathutils.Vector()
        self.OUT = LogicNetworkSubCell(self, self.get_vec)

    def get_vec(self):
        return self.vec

    def evaluate(self):
        self._set_ready()
        matrix = self.get_parameter_value(self.input_m)
        e = matrix.to_euler()
        self.vec = mathutils.Vector((e.x, e.y, e.z))


class ParameterVector3Simple(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_x = None
        self.input_y = None
        self.input_z = None
        self.output_vector = mathutils.Vector()
        self.OUTV = LogicNetworkSubCell(self, self.get_out_v)

    def get_out_v(self):
        return self.output_vector.copy()

    def get_normalized_vector(self):
        return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        x = self.get_parameter_value(self.input_x)
        y = self.get_parameter_value(self.input_y)
        z = self.get_parameter_value(self.input_z)
        if is_invalid(x):
            return
        self.output_vector.x = x
        self.output_vector.y = y
        self.output_vector.z = z
        self._set_value(self.output_vector)


class ParameterVector4Simple(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_x = None
        self.input_y = None
        self.input_z = None
        self.input_w = None
        self.output_vector = mathutils.Vector((0, 0, 0, 0))
        self.OUTV = LogicNetworkSubCell(self, self.get_out_v)

    def get_out_v(self):
        return self.output_vector.copy()

    def evaluate(self):
        self._set_ready()
        x = self.get_parameter_value(self.input_x)
        y = self.get_parameter_value(self.input_y)
        z = self.get_parameter_value(self.input_z)
        w = self.get_parameter_value(self.input_w)
        if is_invalid(x, y, z, w):
            return
        self.output_vector.x = x
        self.output_vector.y = y
        self.output_vector.z = z
        self.output_vector.w = w
        self._set_value(self.output_vector)


class ParameterColor(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.color = None
        self.output_vector = None
        self.OUTV = LogicNetworkSubCell(self, self.get_out_v)

    def get_out_v(self):
        return self.output_vector.copy()

    def get_normalized_vector(self):
        return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        c = self.get_parameter_value(self.color)
        if is_waiting(c):
            return
        self.output_vector = c


class ParameterColorAlpha(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.color = None
        self.output_vector = None
        self.OUTV = LogicNetworkSubCell(self, self.get_out_v)

    def get_out_v(self):
        return self.output_vector.copy()

    def get_normalized_vector(self):
        return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        c = self.get_parameter_value(self.color)
        if is_waiting(c):
            return
        self.output_vector = c


class ParameterEulerSimple(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.input_x = None
        self.input_y = None
        self.input_z = None
        self.output_euler = mathutils.Euler()
        self.OUTV = LogicNetworkSubCell(self, self.get_out_v)

    def get_out_x(self): return self.output_euler.x
    def get_out_y(self): return self.output_euler.y
    def get_out_z(self): return self.output_euler.z
    def get_out_v(self): return self.output_euler.copy()
    def get_normalized_vector(self): return self.output_euler.normalized()

    def evaluate(self):
        self._set_ready()
        x = self.get_parameter_value(self.input_x)
        y = self.get_parameter_value(self.input_y)
        z = self.get_parameter_value(self.input_z)
        if x is not None:
            self.output_euler.x = x
        if y is not None:
            self.output_euler.y = y
        if z is not None:
            self.output_euler.z = z
        self._set_value(self.output_euler)


class ParameterVector4(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.in_x = None
        self.in_y = None
        self.in_z = None
        self.in_w = None
        self.in_vec = None
        self.out_x = 0
        self.out_y = 0
        self.out_z = 0
        self.out_w = 1
        self.out_vec = mathutils.Vector((0, 0, 0, 1))
        self.OUTX = LogicNetworkSubCell(self, self._get_out_x)
        self.OUTY = LogicNetworkSubCell(self, self._get_out_y)
        self.OUTZ = LogicNetworkSubCell(self, self._get_out_z)
        self.OUTW = LogicNetworkSubCell(self, self._get_out_w)
        self.OUTVEC = LogicNetworkSubCell(self, self._get_out_vec)

    def _get_out_x(self):
        return self.out_x

    def _get_out_y(self):
        return self.out_y

    def _get_out_z(self):
        return self.out_z

    def _get_out_w(self):
        return self.out_w

    def _get_out_vec(self):
        return self.out_vec.copy()

    def get_parameter_value(self, param, default_value):
        if param is None:
            return default_value
        elif hasattr(param, "get_value"):
            value = param.get_value()
            if(value is LogicNetwork.STATUS_WAITING):
                raise "Unexpected error in tree"
            else:
                return value
        else:
            return param

    def evaluate(self):
        self._set_ready()
        x = self.get_parameter_value(self.in_x, None)
        y = self.get_parameter_value(self.in_y, None)
        z = self.get_parameter_value(self.in_z, None)
        w = self.get_parameter_value(self.in_w, None)
        vec = self.get_parameter_value(self.in_vec, None)
        if(vec is not None):
            # out is vec with vec components replaced by non null x,y,z,w
            self.out_x = vec.x if x is None else x
            self.out_y = vec.y if y is None else y
            self.out_z = vec.z if z is None else z
            self.out_w = 1
            if(len(vec) >= 4):
                self.out_w = vec.w if w is None else w
            elif(w is not None):
                self.out_w = w
            self.out_vec[:] = (self.out_x, self.out_y, self.out_z, self.out_w)
        else:
            # in vec is None
            self.out_x = 0 if x is None else x
            self.out_y = 0 if y is None else y
            self.out_z = 0 if z is None else z
            self.out_w = 1 if w is None else w
            self.out_vec[:] = (self.out_x, self.out_y, self.out_z, self.out_w)


class ParameterFindChildByName(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.from_parent = None
        self.child = None
        self.parent = None
        self.CHILD = LogicNetworkSubCell(self, self.get_child)

    def get_child(self):
        parent = self.get_parameter_value(self.from_parent)
        childName = self.get_parameter_value(self.child)
        for x in parent.children:
            if x.name == childName:
                return x
            else:
                return

    def evaluate(self):
        self._set_ready()
        self._set_value(None)

        parent = self.get_parameter_value(self.from_parent)
        child = self.get_parameter_value(self.child)

        if (child is None) or (child == ""):
            return

        if is_waiting(parent, child):
            return
        elif not is_invalid(parent):
            # find from parent
            self._set_value(_name_query(parent.childrenRecursive, child))
            # return


# Condition cells
class ConditionAlways(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.repeat = False
        self._set_status(LogicNetworkCell.STATUS_READY)
        self._value = True

    def reset(self):
        if not self.repeat:
            self._value = False

    def evaluate(self):
        pass


class ObjectPropertyOperator(ConditionCell):
    def __init__(self, operator='EQUAL'):
        ActionCell.__init__(self)
        self.game_object = None
        self.property_name = None
        self.operator = operator
        self.compare_value = None
        self.val = 0
        self.VAL = LogicNetworkSubCell(self, self.get_val)

    def get_val(self):
        return self.val

    def evaluate(self):
        game_object = self.get_parameter_value(self.game_object)
        property_name = self.get_parameter_value(self.property_name)
        compare_value = self.get_parameter_value(self.compare_value)
        operator = self.get_parameter_value(self.operator)
        if is_waiting(property_name, compare_value):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        value = self.val = game_object[property_name]
        if operator > 1:  # eq and neq are valid for None
            if is_invalid(value, compare_value):
                return
        if operator is None:
            return
        self._set_value(LOGIC_OPERATORS[operator](value, compare_value))


class ConditionNot(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.condition = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if is_waiting(condition):
            return
        self._set_ready()
        self._set_value(not condition)


class ConditionLNStatus(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.game_object = None
        self.tree_name = None
        self._running = False
        self._stopped = False
        self.IFRUNNING = LogicNetworkSubCell(self, self.get_running)
        self.IFSTOPPED = LogicNetworkSubCell(self, self.get_stopped)

    def get_running(self):
        return self._running

    def get_stopped(self):
        return self._stopped

    def evaluate(self):
        game_object = self.get_parameter_value(self.game_object)
        tree_name = self.get_parameter_value(self.tree_name)
        if is_waiting(game_object, tree_name):
            return
        self._set_ready()
        self._running = False
        self._stopped = False
        if is_invalid(game_object):
            return
        tree = game_object.get(f'IGNLTree_{tree_name}')
        if tree is None:
            return
        self._running = tree.is_running()
        self._stopped = tree.is_stopped()


class ConditionLogicOp(ConditionCell):
    def __init__(self, operator='GREATER'):
        ConditionCell.__init__(self)
        self.operator = operator
        self.param_a = None
        self.param_b = None
        self.threshold = None

    def evaluate(self):
        a = self.get_parameter_value(self.param_a)
        b = self.get_parameter_value(self.param_b)
        threshold = self.get_parameter_value(self.threshold)
        operator = self.get_parameter_value(self.operator)
        self._set_ready()
        if operator > 1:  # eq and neq are valid for None
            if a is None:
                return
            if b is None:
                return
        if threshold is None:
            threshold = 0
        if threshold > 0 and abs(a - b) < threshold:
            a = b
        if operator is None:
            return
        self._set_value(LOGIC_OPERATORS[operator](a, b))


class ConditionCompareVecs(ConditionCell):
    def __init__(self, operator='GREATER'):
        ConditionCell.__init__(self)
        self.operator = operator
        self.all = None
        self.threshold = None
        self.param_a = None
        self.param_b = None

    def get_vec_val(self, op, a, b, xyz, threshold):
        for ax in ['x', 'y', 'z']:
            av = getattr(a, ax)
            bv = getattr(b, ax)
            av = bv if abs(av - bv) < threshold else av
            if xyz[ax] and not LOGIC_OPERATORS[op](av, bv):
                return False
        return True

    def evaluate(self):
        a = self.get_parameter_value(self.param_a)
        b = self.get_parameter_value(self.param_b)
        all_values = self.get_parameter_value(self.all)
        operator = self.get_parameter_value(self.operator)
        threshold = self.get_parameter_value(self.threshold)
        if is_waiting(a, b, all_values, operator, threshold):
            return
        if (
            not isinstance(a, mathutils.Vector)
            or not isinstance(b, mathutils.Vector)
        ):
            return
        self._set_ready()
        if operator > 1:  # eq and neq are valid for None
            if a is None:
                return
            if b is None:
                return
        if operator is None:
            return
        self._set_value(
            self.get_vec_val(
                operator,
                a,
                b,
                all_values,
                threshold
            )
        )


class ConditionDistanceCheck(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.param_a = None
        self.param_b = None
        self.operator = None
        self.dist = None
        self.hyst = None
        self._check = self._strict_check

    def _strict_check(self, opindex, value, hyst, threshold):
        v = LOGIC_OPERATORS[opindex](value, threshold)
        if v is True:
            self._set_value(True)
        else:
            self._set_value(False)
            self._check = self._hyst_check

    def _hyst_check(self, opindex, value, hyst, threshold):
        if (opindex == 2) or (opindex == 4):
            v = LOGIC_OPERATORS[opindex](value, threshold + hyst)
            if v is True:
                self._set_value(True)
                self._check = self._strict_check
            else:
                self._set_value(False)
        elif (opindex == 3) or (opindex == 5):
            v = LOGIC_OPERATORS[opindex](value, threshold - hyst)
            if v is True:
                self._set_value(True)
                self._check = self._strict_check
            else:
                self._set_value(False)

    def evaluate(self):
        a = self.get_parameter_value(self.param_a)
        b = self.get_parameter_value(self.param_b)
        op = self.get_parameter_value(self.operator)
        dist = self.get_parameter_value(self.dist)
        hyst = self.get_parameter_value(self.hyst)
        if is_waiting(a, b, op, dist, hyst):
            return
        self._set_ready()
        if is_invalid(a):
            return
        if is_invalid(b):
            return
        if op is None:
            return
        if dist is None:
            return
        distance = compute_distance(a, b)
        if distance is None:
            return self._set_value(False)
        if hyst is None:  # plain check, no threshold
            v = LOGIC_OPERATORS[op](distance, dist)
            self._set_value(v)
        else:  # check with hysteresys value, if >, >=, <, <=
            self._check(op, distance, hyst, dist)


class ConditionAnd(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.condition_a = None
        self.condition_b = None

    def evaluate(self):
        ca = self.get_parameter_value(self.condition_a)
        cb = self.get_parameter_value(self.condition_b)
        if is_waiting(ca, cb):
            return
        self._set_ready()
        self._set_value(ca and cb)
    pass


class ConditionAndNot(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.condition_a = None
        self.condition_b = None

    def evaluate(self):
        ca = self.get_parameter_value(self.condition_a)
        cb = not self.get_parameter_value(self.condition_b)
        if is_waiting(ca, cb):
            return
        self._set_ready()
        self._set_value(ca and cb)
    pass


class ConditionNotNone(ConditionCell):

    def __init__(self):
        ConditionCell.__init__(self)
        self.checked_value = None

    def evaluate(self):
        value = self.get_parameter_value(self.checked_value)
        if is_waiting(value):
            return
        self._set_ready()
        self._set_value(value is not None)


class ConditionNone(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.checked_value = None

    def evaluate(self):
        self._set_ready()
        value = self.get_parameter_value(self.checked_value)
        self._set_value(value is None)


class ConditionValueValid(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.checked_value = None

    def evaluate(self):
        self._set_ready()
        value = self.get_parameter_value(self.checked_value)
        self._set_value(not is_invalid(value))


class ConditionOr(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.condition_a = True
        self.condition_b = True

    def evaluate(self):
        ca = self.get_parameter_value(self.condition_a)
        cb = self.get_parameter_value(self.condition_b)
        if is_waiting(ca, cb):
            return
        self._set_ready()
        self._set_value(ca or cb)


class ConditionOrList(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.ca = False
        self.cb = False
        self.cc = False
        self.cd = False
        self.ce = False
        self.cf = False

    def evaluate(self):
        ca = self.get_parameter_value(self.ca)
        cb = self.get_parameter_value(self.cb)
        cc = self.get_parameter_value(self.cc)
        cd = self.get_parameter_value(self.cd)
        ce = self.get_parameter_value(self.ce)
        cf = self.get_parameter_value(self.cf)
        if is_waiting(ca, cb, cc, cd, ce, cf):
            return
        self._set_ready()
        self._set_value(ca or cb or cc or cd or ce or cf)


class ConditionAndList(ConditionCell):

    def __init__(self):
        ConditionCell.__init__(self)
        self.ca = True
        self.cb = True
        self.cc = True
        self.cd = True
        self.ce = True
        self.cf = True

    def evaluate(self):
        ca = self.get_parameter_value(self.ca)
        cb = self.get_parameter_value(self.cb)
        cc = self.get_parameter_value(self.cc)
        cd = self.get_parameter_value(self.cd)
        ce = self.get_parameter_value(self.ce)
        cf = self.get_parameter_value(self.cf)
        if is_waiting(ca, cb, cc, cd, ce, cf):
            return
        self._set_ready()
        self._set_value(ca and cb and cc and cd and ce and cf)


class ActionKeyLogger(ActionCell):
    def __init__(self, pulse=False):
        ActionCell.__init__(self)
        self.condition = None
        self.pulse = pulse
        self._key_logged = None
        self._key_code = None
        self._character = None
        self.KEY_LOGGED = LogicNetworkSubCell(self, self.get_key_logged)
        self.KEY_CODE = LogicNetworkSubCell(self, self.get_key_code)
        self.CHARACTER = LogicNetworkSubCell(self, self.get_character)

    def get_key_logged(self):
        return self._key_logged

    def get_key_code(self):
        return self._key_code

    def get_character(self):
        return self._character

    def reset(self):
        LogicNetworkCell.reset(self)
        self._key_logged = False
        self._key_code = None
        self._character = None

    def evaluate(self):
        self._set_ready()
        condition = self.get_parameter_value(self.condition)
        if not condition:
            return
        network = self.network
        keyboard_status = network.keyboard_events
        left_shift_status = keyboard_status[bge.events.LEFTSHIFTKEY].active
        right_shift_status = keyboard_status[bge.events.RIGHTSHIFTKEY].active
        shift_down = (
            left_shift_status or
            right_shift_status or
            network.capslock_pressed
        )
        active_events = network.active_keyboard_events
        active = (
            'active' if self.pulse
            else 'activated'
        )
        for keycode in active_events:
            event = active_events[keycode]
            if getattr(event, active):
                # something has been pressed
                self._character = bge.events.EventToCharacter(
                    event.type,
                    shift_down
                )
                self._key_code = keycode
                self._key_logged = True


class ConditionTimeElapsed(ConditionCell):

    def __init__(self):
        ConditionCell.__init__(self)
        self.condition = None
        self.delta_time = None
        self._trigger = 0
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        delta_time = self.get_parameter_value(self.delta_time)
        if is_waiting(delta_time):
            return
        self._set_ready()
        now = self.network.timeline

        if not not_met(condition):
            self._trigger = now + delta_time

        if now >= self._trigger:
            self._set_value(True)
        else:
            self._set_value(False)


class ConditionKeyReleased(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.pulse = False
        self.key_code = None
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        keycode = self.get_parameter_value(self.key_code)
        if is_waiting(keycode):
            return
        self._set_ready()
        keystat = self.network.keyboard_events[keycode]
        if self.pulse:
            self._set_value(
                keystat.released or
                keystat.inactive
            )
        else:
            self._set_value(keystat.released)
    pass


class ConditionMouseLeft(ConditionCell):
    def __init__(self, repeat=None):
        ConditionCell.__init__(self)
        self.network = None
        self.repeat = repeat
        self._consumed = False

    def setup(self, network):
        self.network = network

    def reset(self):
        if self._consumed:
            self._set_value(False)
            self._set_status(LogicNetworkCell.STATUS_READY)
        else:
            ConditionCell.reset(self)

    def evaluate(self):
        repeat = self.get_parameter_value(self.repeat)
        if is_waiting(repeat):
            return
        self._set_ready()
        dx = self.network.mouse_motion_delta[0]
        self._set_value(dx > 0)
        if not self.repeat:
            self._consumed = True


class ConditionMouseRight(ConditionCell):
    def __init__(self, repeat=None):
        ConditionCell.__init__(self)
        self.network = None
        self.repeat = repeat
        self._consumed = False

    def setup(self, network):
        self.network = network

    def reset(self):
        if self._consumed:
            self._set_value(False)
            self._set_status(LogicNetworkCell.STATUS_READY)
        else:
            ConditionCell.reset(self)

    def evaluate(self):
        repeat = self.get_parameter_value(self.repeat)
        if is_waiting(repeat):
            return
        self._set_ready()
        dx = self.network.mouse_motion_delta[0]
        self._set_value(dx < 0)
        if not self.repeat:
            self._consumed = True


class ActionRepeater(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.input_value = None
        self.output_cells = []
        self.output_value = None

    def setup(self, network):
        super(ActionCell, self).setup(network)
        for cell in self.output_cells:
            cell.setup(network)

    def evaluate(self):
        self._set_ready()
        condition = self.get_parameter_value(self.condition)
        if not condition:
            return
        input_value = self.get_parameter_value(self.input_value)
        if isinstance(input_value, numbers.Number):
            for e in range(0, input_value):
                self._set_value(e)
                for cell in self.output_cells:
                    cell.evaluate()
        else:
            for e in input_value:
                self._set_value(e)
                for cell in self.output_cells:
                    cell.evaluate()
                pass
            pass
        for cell in self.output_cells:
            cell.reset()
            pass
        pass
    pass


class ConditionCollision(ConditionCell):
    def __init__(self):
        ConditionCell.__init__(self)
        self.game_object = None
        self.use_mat = None
        self.prop = None
        self.material = None
        self._set_value("False")
        self.pulse = False
        self._target = None
        self._point = None
        self._normal = None
        self._collision_triggered = False
        self._consumed = False
        self._last_monitored_object = None
        self._objects = []
        self.TARGET = LogicNetworkSubCell(self, self.get_target)
        self.POINT = LogicNetworkSubCell(self, self.get_point)
        self.NORMAL = LogicNetworkSubCell(self, self.get_normal)
        self.OBJECTS = LogicNetworkSubCell(self, self.get_objects)

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def get_target(self):
        return self._target

    def get_objects(self):
        return self._objects

    def _collision_callback(self, obj, point, normal):
        self._target = obj
        self._point = point
        self._normal = normal
        self._objects.append(obj)
        use_mat = self.get_parameter_value(self.use_mat)
        if use_mat:
            material = self.get_parameter_value(self.material)
            if material:
                for obj in self._objects:
                    bo = obj.blenderObject
                    if material in [slot.material.name for slot in bo.material_slots]:
                        self._collision_triggered = True
                        return
                self._collision_triggered = False
                return
        else:
            prop = self.get_parameter_value(self.prop)
            if prop:
                for obj in self._objects:
                    if prop in obj:
                        self._collision_triggered = True
                        return
                self._collision_triggered = False
                return
        self._collision_triggered = True

    def reset(self):
        LogicNetworkCell.reset(self)
        self._collision_triggered = False
        self._objects = []

    def _reset_last_monitored_object(self, new_monitored_object_value):
        if is_invalid(new_monitored_object_value):
            new_monitored_object_value = None
        if self._last_monitored_object == new_monitored_object_value:
            return
        if not isinstance(new_monitored_object_value, bge.types.KX_GameObject):
            if self._last_monitored_object is not None:
                self._last_monitored_object.collisionCallbacks.remove(
                    self._collision_callback
                )
                self._last_monitored_object = None
        else:
            if self._last_monitored_object is not None:
                self._last_monitored_object.collisionCallbacks.remove(
                    self._collision_callback
                )
            if new_monitored_object_value is not None:
                new_monitored_object_value.collisionCallbacks.append(
                    self._collision_callback
                )
                self._last_monitored_object = new_monitored_object_value
        self._set_value(False)
        self._target = None
        self._point = None
        self._normal = None
        self._collision_triggered = False

    def evaluate(self):
        last_target = self._target
        game_object = self.get_parameter_value(self.game_object)
        self._reset_last_monitored_object(game_object)
        if is_waiting(game_object):
            return
        self._set_ready()
        collision = self._collision_triggered
        if last_target is not self._target:
            self._consumed = False
        if self._consumed:
            self._set_value(False)
            return
        if not self.pulse and collision:
            self._consumed = True
            self._set_value(collision)
        elif self.pulse:
            self._set_value(collision)
        else:
            self._consumed = False
            self._set_value(False)


# Action Cells


class ActionAddObject(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.name = None
        self.reference = None
        self.life = None
        self.done = False
        self.obj = False
        self.OBJ = LogicNetworkSubCell(self, self._get_obj)
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def _get_obj(self):
        return self.obj

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        life = self.get_parameter_value(self.life)
        name = self.get_parameter_value(self.name)
        self._set_ready()
        reference = self.get_parameter_value(self.reference)
        scene = logic.getCurrentScene()
        if is_invalid(life, name, reference, scene):
            return
        self.obj = scene.addObject(name, reference, life)
        self.done = True


class ActionSetGameObjectGameProperty(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object_value = self.get_parameter_value(self.game_object)
        property_name_value = self.get_parameter_value(self.property_name)
        property_value_value = self.get_parameter_value(self.property_value)
        if is_waiting(property_name_value, property_value_value):
            return
        if is_invalid(game_object_value):
            return
        if condition:
            self.done = True
            self._set_ready()
            game_object_value[property_name_value] = property_value_value


class SetMaterial(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.slot = None
        self.mat_name = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        game_object = self.get_parameter_value(self.game_object)
        slot = self.get_parameter_value(self.slot) - 1
        mat_name = self.get_parameter_value(self.mat_name)
        if not_met(condition):
            return
        if is_invalid(game_object):
            return
        if is_waiting(mat_name, slot):
            return
        self._set_ready()
        bl_obj = game_object.blenderObject
        if slot > len(bl_obj.material_slots) - 1:
            debug('Set Material: Slot does not exist!')
            return
        bl_obj.material_slots[slot].material = bpy.data.materials[mat_name]
        self.done = True


class ActionSetNodeTreeNodeValue(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.tree_name = None
        self.node_name = None
        self.input_slot = None
        self.value = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        tree_name = self.get_parameter_value(self.tree_name)
        node_name = self.get_parameter_value(self.node_name)
        input_slot = self.get_parameter_value(self.input_slot)
        value = self.get_parameter_value(self.value)
        if is_waiting(node_name, input_slot, value):
            return
        if is_invalid(tree_name):
            return
        if condition:
            self.done = True
            self._set_ready()
            (
                bpy.data.node_groups[tree_name]
                .nodes[node_name]
                .inputs[input_slot]
                .default_value
            ) = value


class ActionSetNodeTreeNodeAttribute(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.tree_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.value = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        tree_name = self.get_parameter_value(self.tree_name)
        node_name = self.get_parameter_value(self.node_name)
        attribute = self.get_parameter_value(self.attribute)
        internal = self.get_parameter_value(self.internal)
        value = self.get_parameter_value(self.value)
        if is_waiting(node_name, attribute, internal, value):
            return
        if is_invalid(tree_name):
            return
        if condition:
            self._set_ready()
            target = (
                bpy
                .data
                .node_groups[tree_name]
                .nodes[node_name]
            )
            if internal:
                target = getattr(target, internal, target)
            if hasattr(target, attribute):
                setattr(target, attribute, value)
            self.done = True


class ActionSetMaterialNodeValue(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.input_slot = None
        self.value = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        mat_name = self.get_parameter_value(self.mat_name)
        node_name = self.get_parameter_value(self.node_name)
        input_slot = self.get_parameter_value(self.input_slot)
        value = self.get_parameter_value(self.value)
        if is_waiting(node_name, input_slot, value):
            return
        if is_invalid(mat_name):
            return
        if condition:
            self.done = True
            self._set_ready()
            (
                bpy.data.materials[mat_name]
                .node_tree
                .nodes[node_name]
                .inputs[input_slot]
                .default_value
            ) = value


class ActionSetMaterialNodeAttribute(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.value = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        mat_name = self.get_parameter_value(self.mat_name)
        node_name = self.get_parameter_value(self.node_name)
        attribute = self.get_parameter_value(self.attribute)
        internal = self.get_parameter_value(self.internal)
        value = self.get_parameter_value(self.value)
        if is_waiting(node_name, attribute, internal, value):
            return
        if is_invalid(mat_name):
            return
        if condition:
            self._set_ready()
            target = (
                bpy.data.materials[mat_name]
                .node_tree
                .nodes[node_name]
            )
            if internal:
                target = getattr(target, internal, target)
            if hasattr(target, attribute):
                setattr(target, attribute, value)
            self.done = True


class ActionPlayMaterialSequence(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.play_mode = None
        self.play_continue = None
        self.frames = None
        self.fps = None
        self.reverse = False
        self.time = 0.0
        self.on_start = False
        self.running = False
        self.on_finish = False
        self.frame = 0
        self._consumed = False
        self.ON_START = LogicNetworkSubCell(self, self._get_on_start)
        self.RUNNING = LogicNetworkSubCell(self, self._get_running)
        self.ON_FINISH = LogicNetworkSubCell(self, self._get_on_finish)
        self.FRAME = LogicNetworkSubCell(self, self._get_frame)

    def _get_on_start(self):
        return self.on_start
    
    def _get_running(self):
        return self.running
    
    def _get_on_finish(self):
        return self.on_finish
    
    def _get_frame(self):
        return self.frame

    def evaluate(self):
        self.done = False
        self.on_finish = False
        self.on_start = False
        running = self.running
        condition = self.get_parameter_value(self.condition)
        play_continue = self.get_parameter_value(self.play_continue)
        if not_met(condition) and not running:
            return
        self.time += self.network.time_per_frame
        mat_name = self.get_parameter_value(self.mat_name)
        node_name = self.get_parameter_value(self.node_name)
        play_mode = self.get_parameter_value(self.play_mode)
        frames = self.get_parameter_value(self.frames)
        fps = self.get_parameter_value(self.fps)
        if is_waiting(
            mat_name,
            node_name,
            play_mode,
            frames,
            fps
        ):
            return
        rate = 1/fps
        speed = self.time / rate
        self._set_ready()
        if speed < 1:
            return
        self.time -= rate * speed
        player = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
        ).image_user
        start_frame = frames.y if self.reverse else frames.x
        end_frame = frames.x if self.reverse else frames.y
        inverted = (start_frame > end_frame)
        frame = self.frame = player.frame_offset
        reset_cond = (frame <= end_frame) if inverted else (frame >= end_frame)
        if not running:
            if not play_continue and play_mode > 2 or reset_cond:
                player.frame_offset = start_frame if inverted else end_frame
            if not play_continue:
                self.reverse = False
            self.on_start = True
            self._consumed = False
        stops = [3, 4, 5]

        start_cond = (frame > start_frame) if inverted else (frame < start_frame)

        if not condition and play_mode in stops:
            self.on_finish = True
            self.running = False
            return
        if start_cond:
            self.running = True
            player.frame_offset = start_frame
        frame = player.frame_offset
        run_cond = (frame > end_frame) if inverted else (frame < end_frame)
        if run_cond:
            self.running = True
            s = round(speed)
            if inverted:
                if frame - s < end_frame:
                    player.frame_offset = end_frame
                else:
                    player.frame_offset -= s
            else:
                if frame + s > end_frame:
                    player.frame_offset = end_frame
                else:
                    player.frame_offset += s
        elif play_mode == 1 and condition:
            player.frame_offset = start_frame
        elif play_mode == 4:
            player.frame_offset = start_frame
        elif play_mode == 3:
            if running and not self._consumed:
                self.on_finish = True
                self._consumed = True
        elif play_mode == 0 or play_mode == 3:
            if running and not self._consumed:
                self.on_finish = True
                self._consumed = True
            if not condition:
                self.running = False
        elif play_mode == 2 or play_mode == 5:
            if running and not condition:
                self.on_finish = True
            if not condition:
                self.running = False
            self.reverse = not self.reverse
        else:
            if running:
                self.on_finish = True
            self.running = False
        self.done = True


class ActionToggleGameObjectGameProperty(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object_value = self.get_parameter_value(self.game_object)
        property_name_value = self.get_parameter_value(self.property_name)
        property_value_value = self.get_parameter_value(self.property_value)
        if is_waiting(property_name_value, property_value_value):
            return
        if is_invalid(game_object_value):
            return
        self._set_ready()
        if condition:
            value = game_object_value[property_name_value]
            game_object_value[property_name_value] = not value
        self.done = True


class ActionAddToGameObjectGameProperty(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        property_name = self.get_parameter_value(self.property_name)
        property_value = self.get_parameter_value(self.property_value)
        if is_waiting(property_name, property_value):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        value = game_object[property_name]
        game_object[property_name] = (
            value + property_value
        )
        self.done = True


class CopyPropertyFromObject(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.from_object = None
        self.to_object = None
        self.property_name = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        from_object = self.get_parameter_value(self.from_object)
        to_object = self.get_parameter_value(self.to_object)
        if is_invalid(from_object, to_object):
            return
        property_name = self.get_parameter_value(self.property_name)
        if is_waiting(property_name):
            return
        self._set_ready()
        val = from_object.get(property_name)
        if val is not None:
            to_object[property_name] = val
        self.done = True


class ActionClampedAddToGameObjectGameProperty(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.range = None
        self.done = False
        self.OUT = LogicNetworkSubCell(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        game_object = self.get_parameter_value(self.game_object)
        if not_met(condition):
            return
        if is_invalid(game_object):
            return
        property_name = self.get_parameter_value(self.property_name)
        property_value = self.get_parameter_value(self.property_value)
        val_range = self.get_parameter_value(self.range)
        if is_waiting(property_name, property_value):
            return
        self._set_ready()
        value = game_object[property_name]
        new_val = value + property_value
        if new_val > val_range.y:
            new_val = val_range.y
        if new_val < val_range.x:
            new_val = val_range.x
        game_object[property_name] = (
            new_val
        )
        self.done = True


class ValueSwitch(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.conditon = None
        self.val_a = None
        self.val_b = None
        self.out_value = False
        self.VAL = LogicNetworkSubCell(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        val_a = self.get_parameter_value(self.val_a)
        val_b = self.get_parameter_value(self.val_b)
        self._set_ready()
        self.out_value = (
            val_a if condition is True else val_b
        )


class InvertBool(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = LogicNetworkSubCell(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            debug('Inver Bool Node: Value invalid, defaulting to "False"')
            self.out_value = False
            return
        self._set_ready()
        self.out_value = not value


class InvertValue(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = LogicNetworkSubCell(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            debug('Inver Value Node: Value invalid, defaulting to 0')
            self.out_value = 0
            return
        self._set_ready()
        self.out_value = -value


class AbsoluteValue(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = LogicNetworkSubCell(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        if is_invalid(self.value):
            return
        value = self.get_parameter_value(self.value)
        self._set_ready()
        self.out_value = math.fabs(value)


class ActionPrint(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        self._set_ready()
        print(value)
        self.done = True


class ActionCreateVehicle(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.wheels_steering = None
        self.wheels = None
        self.suspension = None
        self.stiffness = None
        self.damping = None
        self.friction = None
        self.done = None
        self.vehicle = None
        self.wheels = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.VEHICLE = LogicNetworkSubCell(self, self.get_vehicle)
        self.WHEELS = LogicNetworkSubCell(self, self.get_wheels)

    def get_done(self):
        return self.done

    def get_vehicle(self):
        return self.vehicle

    def get_wheels(self):
        return self.wheels

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        wheels_steering = self.get_parameter_value(self.wheels_steering)
        wheels = self.get_parameter_value(self.wheels)
        suspension = self.get_parameter_value(self.suspension)
        stiffness = self.get_parameter_value(self.stiffness)
        damping = self.get_parameter_value(self.damping)
        friction = self.get_parameter_value(self.friction)
        if is_waiting(
            game_object, 
            wheels_steering,
            wheels,
            suspension,
            stiffness,
            damping,
            friction
        ):
            return
        self._set_ready()
        orig_ori = game_object.worldOrientation
        game_object.worldOrientation = mathutils.Euler((0, 0, 0), 'XYZ')
        ph_id = game_object.getPhysicsId()
        car = bge.constraints.createVehicle(ph_id)
        down = mathutils.Vector((0, 0, -1))
        axle_dir = mathutils.Vector((0, -1, 0))
        wheels_steering = bpy.data.collections[wheels_steering]
        wheels = bpy.data.collections[wheels]
        for wheel in wheels_steering.objects:
            wheel = check_game_object(wheel.name)
            car.addWheel(
                wheel,
                wheel.worldPosition - game_object.worldPosition,
                down,
                axle_dir,
                suspension,
                abs(wheel.worldScale.x/2),
                True
            )
        for wheel in wheels.objects:
            wheel = check_game_object(wheel.name)
            car.addWheel(
                wheel,
                wheel.worldPosition - game_object.worldPosition,
                down,
                axle_dir,
                suspension,
                abs(wheel.worldScale.x/2),
                False
            )
        for wheel in range(car.getNumWheels()):
            car.setSuspensionStiffness(stiffness, wheel)
            car.setSuspensionDamping(damping, wheel)
            car.setTyreFriction(friction, wheel)
        self.vehicle = car
        game_object.worldOrientation = orig_ori
        self.done = True


class ActionCreateVehicleFromParent(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.suspension = None
        self.stiffness = None
        self.damping = None
        self.friction = None
        self.done = None
        self.vehicle = None
        self.wheels = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.VEHICLE = LogicNetworkSubCell(self, self.get_vehicle)
        self.WHEELS = LogicNetworkSubCell(self, self.get_wheels)

    def get_done(self):
        return self.done

    def get_vehicle(self):
        return self.vehicle

    def get_wheels(self):
        return self.wheels

    def evaluate(self):
        self.done = False
        game_object = self.get_parameter_value(self.game_object)
        if not_met(self.get_parameter_value(self.condition)):
            if game_object.get('vehicle_constraint'):
                self._set_ready()
                self.vehicle = game_object['vehicle_constraint']
            return
        suspension = self.get_parameter_value(self.suspension)
        stiffness = self.get_parameter_value(self.stiffness)
        damping = self.get_parameter_value(self.damping)
        friction = self.get_parameter_value(self.friction)
        if is_waiting(game_object, suspension, stiffness, damping, friction):
            return
        self._set_ready()
        orig_ori = game_object.localOrientation.copy()
        game_object.localOrientation = mathutils.Euler((0, 0, 0), 'XYZ')
        ph_id = game_object.getPhysicsId()
        car = bge.constraints.createVehicle(ph_id)
        down = mathutils.Vector((0, 0, -1))
        axle_dir = game_object.getAxisVect(mathutils.Vector((0, -1, 0)))
        wheels = []
        cs = sorted(game_object.children, key=lambda c: c.name)
        for c in cs:
            if 'FWheel' in c.name:
                c.removeParent()
                car.addWheel(
                    c,
                    c.worldPosition - game_object.worldPosition,
                    down,
                    axle_dir,
                    suspension,
                    abs(c.worldScale.x/2),
                    True
                )
                wheels.append(c)
            elif 'RWheel' in c.name:
                c.removeParent()
                car.addWheel(
                    c,
                    c.worldPosition - game_object.worldPosition,
                    down,
                    axle_dir,
                    suspension,
                    abs(c.worldScale.x/2),
                    False
                )
                wheels.append(c)
        for wheel in range(car.getNumWheels()):
            car.setSuspensionStiffness(stiffness, wheel)
            car.setSuspensionDamping(damping, wheel)
            car.setTyreFriction(friction, wheel)
        game_object.localOrientation = orig_ori
        self.vehicle = game_object['vehicle_constraint'] = car
        self.wheels = wheels
        self.done = True


class VehicleApplyForce(ActionCell):
    def __init__(self, value_type='REAR'):
        ActionCell.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.constraint = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        constraint = self.get_parameter_value(self.constraint)
        if not_met(condition):
            return
        if is_invalid(constraint):
            return
        value = self.get_parameter_value(self.value_type)
        wheelcount = self.get_parameter_value(self.wheelcount)
        power = self.get_parameter_value(self.power)
        if is_waiting(value, wheelcount, power):
            return
        if not condition:
            if self._reset:
                for wheel in range(constraint.getNumWheels()):
                    constraint.applyEngineForce(0, wheel)
                self._reset = False
            return
        if is_invalid(constraint):
            return
        self._reset = True
        self._set_ready()
        if value == 'FRONT':
            for wheel in range(wheelcount):
                constraint.applyEngineForce(power, wheel)
        if value == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.applyEngineForce(power, wheel)
        if value == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.applyEngineForce(power, wheel)
        self.done = True


class VehicleApplyBraking(ActionCell):
    def __init__(self, value_type='REAR'):
        ActionCell.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.constraint = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if is_waiting(condition):
            return
        constraint = self.get_parameter_value(self.constraint)
        value_type = self.get_parameter_value(self.value_type)
        wheelcount = self.get_parameter_value(self.wheelcount)
        power = self.get_parameter_value(self.power)
        if is_waiting(Constraint, value_type, wheelcount, power):
            return

        if not condition:
            if self._reset:
                for wheel in range(constraint.getNumWheels()):
                    constraint.applyBraking(0, wheel)
                self._reset = False
            return
        if is_invalid(constraint):
            return
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                constraint.applyBraking(power, wheel)
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.applyBraking(power, wheel)
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.applyBraking(power, wheel)
        self.done = True


class VehicleApplySteering(ActionCell):
    def __init__(self, value_type='REAR'):
        ActionCell.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.constraint = None
        self.wheelcount = None
        self.power = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        constraint = self.get_parameter_value(self.constraint)
        value_type = self.get_parameter_value(self.value_type)
        wheelcount = self.get_parameter_value(self.wheelcount)
        power = self.get_parameter_value(self.power)
        if is_waiting(Constraint, value_type, wheelcount, power):
            return
        if is_invalid(constraint):
            return
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                constraint.setSteeringValue(power, wheel)
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.setSteeringValue(power, wheel)
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.setSteeringValue(power, wheel)
        self.done = True


class VehicleSetAttributes(ActionCell):
    def __init__(self, value_type='REAR'):
        ActionCell.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.constraint = None
        self.wheelcount = None
        self.set_suspension_compression = False
        self.suspension_compression = False
        self.set_suspension_stiffness = False
        self.suspension_stiffness = False
        self.set_suspension_damping = False
        self.suspension_damping = False
        self.set_tyre_friction = False
        self.tyre_friction = False
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def set_attributes(self, car, wheel, attrs, values):
        if attrs[0] is True:
            car.setSuspensionCompression(values[0], wheel)
        if attrs[1] is True:
            car.setSuspensionStiffness(values[1], wheel)
        if attrs[2] is True:
            car.setSuspensionDamping(values[2], wheel)
        if attrs[3] is True:
            car.setTyreFriction(values[3], wheel)

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        constraint = self.get_parameter_value(self.constraint)
        value_type = self.get_parameter_value(self.value_type)
        wheelcount = self.get_parameter_value(self.wheelcount)
        if is_waiting(constraint, value_type, wheelcount):
            return

        attrs_to_set = [
            self.get_parameter_value(self.set_suspension_compression),
            self.get_parameter_value(self.set_suspension_stiffness),
            self.get_parameter_value(self.set_suspension_damping),
            self.get_parameter_value(self.set_tyre_friction)
        ]
        values_to_set = [
            self.get_parameter_value(self.suspension_compression),
            self.get_parameter_value(self.suspension_stiffness),
            self.get_parameter_value(self.suspension_damping),
            self.get_parameter_value(self.tyre_friction)
        ]
        if is_invalid(constraint):
            return
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        self.done = True


class ActionSetObjectAttribute(ActionCell):
    def __init__(self, value_type='worldPosition'):
        ActionCell.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.xyz = None
        self.game_object = None
        self.attribute_value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        xyz = self.get_parameter_value(self.xyz)
        game_object = self.get_parameter_value(self.game_object)
        attribute = self.get_parameter_value(self.value_type)
        value = self.get_parameter_value(self.attribute_value)
        if is_waiting(xyz, game_object, attribute, value):
            return

        if hasattr(value, attribute):
            value = getattr(value, attribute).copy()
        self._set_ready()
        if not hasattr(game_object, attribute):
            debug(
                'Set Object Data Node: {} has no attribute {}!'
                .format(game_object, attribute)
            )
            return
        data = getattr(game_object, attribute)
        if 'Orientation' in attribute:
            data = data.to_euler()
        for axis in xyz:
            if not xyz[axis]:
                setattr(value, axis, getattr(data, axis))
        setattr(
            game_object,
            attribute,
            value
        )
        if value == 'worldScale':
            game_object.reinstancePhysicsMesh(
                game_object,
                game_object.meshes[0]
            )
        self.done = True


class ActionInstalSubNetwork(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.target_object = None
        self.tree_name = None
        self.initial_status = None
        self._network = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self._network = network

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        target_object = self.get_parameter_value(self.target_object)
        tree_name = self.get_parameter_value(self.tree_name)
        initial_status = self.get_parameter_value(self.initial_status)
        if is_waiting(
            target_object,
            tree_name,
            initial_status
        ):
            return
        self._set_ready()
        if is_invalid(target_object):
            return
        self._network.install_subnetwork(
            target_object,
            tree_name,
            initial_status
        )
        self.done = True


class ActionExecuteNetwork(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.target_object = None
        self.tree_name = None
        self._network = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self._network = network

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        target_object = self.get_parameter_value(self.target_object)
        tree_name = self.get_parameter_value(self.tree_name)
        self._set_ready()
        if is_invalid(target_object):
            return
        added_network = target_object.get(f'IGNLTree_{tree_name}', None)
        if not added_network:
            self._network.install_subnetwork(
                target_object,
                tree_name,
                False
            )
            added_network = target_object.get(f'IGNLTree_{tree_name}', None)
        if condition:
            added_network.stopped = False
        else:
            added_network.stop()
            added_network.stopped = True
            return
        self.done = True


class ActionStartLogicNetwork(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.logic_network_name = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        logic_network_name = self.get_parameter_value(self.logic_network_name)
        if is_waiting(game_object, logic_network_name):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        network = game_object.get(f'IGNLTree_{logic_network_name}')
        if network is not None:
            network.stopped = False
        self.done = True


class ActionStopLogicNetwork(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.logic_network_name = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        logic_network_name = self.get_parameter_value(self.logic_network_name)
        if is_waiting(game_object, logic_network_name):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        network = game_object.get(f'IGNLTree_{logic_network_name}')
        network.stop()
        self.done = True


class ActionFindObject(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.game_object = None

    def evaluate(self):
        self._set_ready()
        game_object = self.get_parameter_value(self.game_object)
        self._set_value(game_object)


class ActionSendMessage(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.from_obj = None
        self.to_obj = None
        self.subject = None
        self.body = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            self._set_value(False)
            return
        from_obj = self.get_parameter_value(self.from_obj)
        to_obj = self.get_parameter_value(self.to_obj)
        subject = self.get_parameter_value(self.subject)
        body = self.get_parameter_value(self.body)
        if is_waiting(from_obj, to_obj, subject, body):
            return
        self._set_ready()
        if body and to_obj:
            from_obj.sendMessage(subject, body=body, to=to_obj)
        elif body:
            from_obj.sendMessage(subject, body=body)
        elif to_obj:
            from_obj.sendMessage(subject, to=to_obj)
        else:
            from_obj.sendMessage(subject)
        self._set_value(True)


class ActionSetGameObjectVisibility(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.visible = None
        self.recursive = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_parameter_value(self.game_object)
        visible = self.get_parameter_value(self.visible)
        recursive = self.get_parameter_value(self.recursive)
        if is_waiting(visible, recursive):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if visible is None:
            return
        if recursive is None:
            return
        game_object.setVisible(visible, recursive)
        self.done = True


class ActionRayPick(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.origin = None
        self.destination = None
        self.property_name = None
        self.xray = None
        self.distance = None
        self.visualize = None
        self._picked_object = None
        self._point = None
        self._normal = None
        self._direction = None
        self.PICKED_OBJECT = LogicNetworkSubCell(self, self.get_picked_object)
        self.POINT = LogicNetworkSubCell(self, self.get_point)
        self.NORMAL = LogicNetworkSubCell(self, self.get_normal)
        self.DIRECTION = LogicNetworkSubCell(self, self.get_direction)
        self.network = None

    def setup(self, network):
        self.network = network

    def get_picked_object(self):
        return self._picked_object

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def get_direction(self):
        return self._direction

    def _compute_direction(self, origin, dest):
        if hasattr(origin, "worldPosition"):
            origin = origin.worldPosition
        if hasattr(dest, "worldPosition"):
            dest = dest.worldPosition
        d = dest - origin
        d.normalize()
        return d

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        origin = self.get_parameter_value(self.origin)
        destination = self.get_parameter_value(self.destination)
        property_name = self.get_parameter_value(self.property_name)
        xray = self.get_parameter_value(self.xray)
        distance = self.get_parameter_value(self.distance)
        visualize = self.get_parameter_value(self.visualize)

        if is_waiting(origin, destination, property_name, distance):
            return
        self._set_ready()
        caster = self.network._owner
        obj, point, normal = None, None, None
        if not property_name:
            obj, point, normal = caster.rayCast(
                destination,
                origin,
                distance,
                xray=xray
            )
        else:
            obj, point, normal = caster.rayCast(
                destination,
                origin,
                distance,
                property_name,
                xray=xray
            )
        direction = self._compute_direction(origin, destination)
        if visualize:
            origin = getattr(origin, 'worldPosition', origin)
            line_dest = direction.copy()
            line_dest.x *= distance
            line_dest.y *= distance
            line_dest.z *= distance
            line_dest = line_dest + origin
            bge.render.drawLine(
                origin,
                line_dest,
                [
                    1,
                    0,
                    0,
                    1
                ]
            )
            if obj:
                bge.render.drawLine(
                    origin,
                    point,
                    [
                        0,
                        1,
                        0,
                        1
                    ]
                )
        self._set_value(obj is not None)
        self._picked_object = obj
        self._point = point
        self._normal = normal
        self._direction = direction


class ActionMousePick(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.distance = None
        self.property = None
        self.xray = None
        self.camera = None
        self._set_value(False)
        self._out_object = None
        self._out_normal = None
        self._out_point = None
        self.OUTOBJECT = LogicNetworkSubCell(self, self.get_out_object)
        self.OUTNORMAL = LogicNetworkSubCell(self, self.get_out_normal)
        self.OUTPOINT = LogicNetworkSubCell(self, self.get_out_point)

    def get_out_object(self):
        return self._out_object

    def get_out_normal(self):
        return self._out_normal

    def get_out_point(self):
        return self._out_point

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        distance = self.get_parameter_value(self.distance)
        property_name = self.get_parameter_value(self.property)
        xray = self.get_parameter_value(self.xray)
        camera = self.get_parameter_value(self.camera)
        if is_waiting(distance, property_name, xray, camera):
            return
        self._set_ready()
        if not condition:
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        if is_invalid(camera):
            return
        mpos = logic.mouse.position
        vec = 10 * camera.getScreenVect(*mpos)
        ray_target = camera.worldPosition - vec
        target, point, normal = self.network.ray_cast(
            camera,
            None,
            ray_target,
            property_name,
            xray,
            distance
        )
        self._set_value(target is not None)
        self._out_object = target
        self._out_normal = normal
        self._out_point = point


class ActionCameraPick(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.camera = None
        self.aim = None
        self.property_name = None
        self.xray = None
        self.distance = None
        self._picked_object = None
        self._picked_point = None
        self._picked_normal = None
        self.PICKED_OBJECT = LogicNetworkSubCell(self, self.get_picked_object)
        self.PICKED_POINT = LogicNetworkSubCell(self, self.get_picked_point)
        self.PICKED_NORMAL = LogicNetworkSubCell(self, self.get_picked_normal)

    def get_picked_object(self):
        return self._picked_object

    def get_picked_point(self):
        return self._picked_point

    def get_picked_normal(self):
        return self._picked_normal

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_parameter_value(self.camera)
        aim = self.get_parameter_value(self.aim)
        property_name = self.get_parameter_value(self.property_name)
        xray = self.get_parameter_value(self.xray)
        distance = self.get_parameter_value(self.distance)
        if is_waiting(camera, aim, property_name, xray, distance):
            return
        self._set_ready()
        if not condition:
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        if is_invalid(camera):
            return
        if is_invalid(aim):
            return
        obj, point, normal = None, None, None
        # assume screen coordinates
        if isinstance(aim, mathutils.Vector) and len(aim) == 2:
            vec = 10 * camera.getScreenVect(aim[0], aim[1])
            ray_target = camera.worldPosition - vec
            aim = ray_target
        if not property_name:
            obj, point, normal = camera.rayCast(aim, None, distance)
        else:
            obj, point, normal = camera.rayCast(
                aim,
                None,
                distance,
                property_name,
                xray=xray
            )
        self._set_value(obj is not None)
        self._picked_object = obj
        self._picked_point = point
        self._picked_normal = normal


class ActionSetActiveCamera(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.camera = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_parameter_value(self.camera)
        if is_waiting(camera):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        scene = logic.getCurrentScene()
        scene.active_camera = camera
        self.done = True


class ActionSetCameraFov(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.camera = None
        self.fov = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_parameter_value(self.camera)
        fov = self.get_parameter_value(self.fov)
        if is_waiting(camera, fov):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        camera.fov = fov
        self.done = True


class ActionSetResolution(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.x_res = None
        self.y_res = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        x_res = self.get_parameter_value(self.x_res)
        y_res = self.get_parameter_value(self.y_res)
        if is_waiting(x_res, y_res):
            return
        self._set_ready()
        bge.render.setWindowSize(x_res, y_res)
        self.done = True


class ActionSetFullscreen(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.use_fullscreen = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        use_fullscreen = self.get_parameter_value(self.use_fullscreen)
        if is_waiting(use_fullscreen):
            return
        self._set_ready()
        bge.render.setFullScreen(use_fullscreen)
        self.done = True


class GESetProfile(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.use_profile = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        use_profile = self.get_parameter_value(self.use_profile)
        if is_waiting(use_profile):
            return
        self._set_ready()
        bge.render.showProfile(use_profile)
        self.done = True


class GEShowFramerate(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.use_framerate = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        use_framerate = self.get_parameter_value(self.use_framerate)
        if is_waiting(use_framerate):
            return
        self._set_ready()
        bge.render.showFramerate(use_framerate)
        self.done = True


class GetVSync(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(bge.render.getVsync())


class GetFullscreen(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(bge.render.getFullScreen())


class GEDrawLine(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.color = None
        self.from_point = None
        self.to_point = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        from_point = self.get_parameter_value(self.from_point)
        to_point = self.get_parameter_value(self.to_point)
        color = self.get_parameter_value(self.color)
        if is_invalid(from_point, to_point, color):
            return
        self._set_ready()
        self._set_value(
            bge.render.drawLine(
                from_point,
                to_point,
                [
                    color.x,
                    color.y,
                    color.z,
                    1
                ]
            )
        )


class GetResolution(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.width = None
        self.height = None
        self.res = None
        self.WIDTH = LogicNetworkSubCell(self, self.get_width)
        self.HEIGHT = LogicNetworkSubCell(self, self.get_height)
        self.RES = LogicNetworkSubCell(self, self.get_res)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_res(self):
        return self.res

    def evaluate(self):
        self._set_ready()
        self.width = bge.render.getWindowWidth()
        self.height = bge.render.getWindowHeight()
        self.res = mathutils.Vector((self.width, self.height))


class ActionSetVSync(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.vsync_mode = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        vsync_mode = self.get_parameter_value(self.vsync_mode)
        if is_waiting(vsync_mode):
            return
        self._set_ready()
        bge.render.setVsync(vsync_mode)
        self.done = True


class InitEmptyDict(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.dict = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.DICT = LogicNetworkSubCell(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.dict

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        self.dict = {}
        self.done = True


class InitNewDict(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.val = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.DICT = LogicNetworkSubCell(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.dict

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        key = self.get_parameter_value(self.key)
        value = self.get_parameter_value(self.val)
        if is_waiting(key, value):
            return
        if not condition:
            return
        self._set_ready()
        self.dict = {str(key): value}
        self.done = True


class SetDictKeyValue(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.val = None
        self.new_dict = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.DICT = LogicNetworkSubCell(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.new_dict

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        dictionary = self.get_parameter_value(self.dict)
        key = self.get_parameter_value(self.key)
        val = self.get_parameter_value(self.val)
        if is_waiting(dictionary, key, val):
            return
        self._set_ready()
        dictionary[key] = val
        self.new_dict = dictionary
        self.done = True


class SetDictDelKey(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.new_dict = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.DICT = LogicNetworkSubCell(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.new_dict

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        dictionary = self.get_parameter_value(self.dict)
        key = self.get_parameter_value(self.key)
        if is_waiting(dictionary, key):
            return
        self._set_ready()
        if key in dictionary:
            del dictionary[key]
        else:
            debug("Dict Delete Key Node: Key '{}' not in Dict!".format(key))
            return
        self.new_dict = dictionary
        self.done = True


class InitEmptyList(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.length = None
        self.items = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.LIST = LogicNetworkSubCell(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.items

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        length = self.get_parameter_value(self.length)
        if is_waiting(length):
            return
        self._set_ready()
        self.items = [None for x in range(length)]
        self.done = True


class InitNewList(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.value = None
        self.value2 = None
        self.value3 = None
        self.value4 = None
        self.value5 = None
        self.value6 = None
        self.items = None
        self.LIST = LogicNetworkSubCell(self, self.get_list)

    def get_list(self):
        return self.items

    def evaluate(self):
        value = self.get_parameter_value(self.value)
        value2 = self.get_parameter_value(self.value2)
        value3 = self.get_parameter_value(self.value3)
        value4 = self.get_parameter_value(self.value4)
        value5 = self.get_parameter_value(self.value5)
        value6 = self.get_parameter_value(self.value6)
        values = [value, value2, value3, value4, value5, value6]
        self.items = []
        self._set_ready()
        for val in values:
            if not is_waiting(val) and not is_invalid(val):
                self.items.append(val)


class AppendListItem(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.items = None
        self.val = None
        self.new_list = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.LIST = LogicNetworkSubCell(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_parameter_value(self.items)
        val = self.get_parameter_value(self.val)
        if is_waiting(list_d, val):
            return
        self._set_ready()
        list_d.append(val)
        self.new_list = list_d
        self.done = True


class SetListIndex(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.items = None
        self.index = None
        self.val = None
        self.new_list = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.LIST = LogicNetworkSubCell(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_parameter_value(self.items)
        index = self.get_parameter_value(self.index)
        val = self.get_parameter_value(self.val)
        if is_invalid(list_d, index, val):
            return
        self._set_ready()
        list_d[index] = val
        self.new_list = list_d
        self.done = True


class RemoveListValue(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.items = None
        self.val = None
        self.new_list = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.LIST = LogicNetworkSubCell(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_parameter_value(self.items)
        val = self.get_parameter_value(self.val)
        if is_invalid(list_d, val):
            return
        self._set_ready()
        if val in list_d:
            list_d.remove(val)
        else:
            debug("List Remove Value Node: Item '{}' not in List!".format(val))
            return
        self.new_list = list_d
        self.done = True


class RemoveListIndex(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.items = None
        self.idx = None
        self.new_list = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.LIST = LogicNetworkSubCell(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_parameter_value(self.items)
        idx = self.get_parameter_value(self.idx)
        if is_invalid(list_d, idx):
            return
        self._set_ready()
        if len(list_d) > idx:
            del list_d[idx]
        else:
            debug("List Index exceeds length!".format(val))
            return
        self.new_list = list_d
        self.done = True


class ActionSetParent(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.child_object = None
        self.parent_object = None
        self.compound = True
        self.ghost = True
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        child_object = self.get_parameter_value(self.child_object)
        parent_object = self.get_parameter_value(self.parent_object)
        compound = self.get_parameter_value(self.compound)
        ghost = self.get_parameter_value(self.ghost)
        self._set_ready()
        if is_invalid(child_object, parent_object, compound, ghost):
            return
        if child_object.parent is parent_object:
            return
        child_object.setParent(parent_object, compound, ghost)
        self.done = True


class ActionRemoveParent(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.child_object = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        child_object = self.get_parameter_value(self.child_object)
        if is_waiting(child_object):
            return
        self._set_ready()
        if is_invalid(child_object):
            return
        if not child_object.parent:
            return
        child_object.removeParent()
        self.done = True


class ActionPerformanceProfile(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.network = None
        self.print_profile = False
        self.check_evaluated_cells = False
        self.check_average_cells_per_sec = False
        self.check_cells_per_tick = False
        self.done = None
        self.data = ''
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.DATA = LogicNetworkSubCell(self, self.get_data)

    def get_done(self):
        return self.done

    def get_data(self):
        return self.data

    def setup(self, network):
        self.network = network

    def evaluate(self):
        self.done = False
        self.data = '----------------------------------Start Profile\n'
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        print_profile = self.get_parameter_value(
            self.print_profile
        )
        check_evaluated_cells = self.get_parameter_value(
            self.check_evaluated_cells
        )
        check_average_cells_per_sec = self.get_parameter_value(
            self.check_average_cells_per_sec
        )
        check_cells_per_tick = self.get_parameter_value(
            self.check_cells_per_tick
        )
        if is_waiting(
            print_profile,
            check_evaluated_cells,
            check_average_cells_per_sec,
            check_cells_per_tick
        ):
            self._set_ready()
            return
        self._set_ready()
        if check_evaluated_cells:
            self.data += 'Evaluated Nodes:\t{}\n'.format(
                self.network.evaluated_cells
            )
        if check_average_cells_per_sec:
            self.data += 'Nodes per Sec (avg):\t{}\n'.format(
                self.network.evaluated_cells / self.network.timeline
            )
        if check_cells_per_tick:
            self.data += 'Nodes per Tick:\t{}\n'.format(
                len(self.network._cells)
            )
        self.data += '----------------------------------End Profile'
        if print_profile:
            print(self.data)
        self.done = True


class ActionEditArmatureConstraint(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.armature = None
        self.constraint_name = None
        self.enforced_factor = None
        self.primary_target = None
        self.secondary_target = None
        self.active = None
        self.ik_weight = None
        self.ik_distance = None
        self.distance_mode = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_parameter_value(self.armature)
        constraint_name = self.get_parameter_value(self.constraint_name)
        enforced_factor = self.get_parameter_value(self.enforced_factor)
        primary_target = self.get_parameter_value(self.primary_target)
        secondary_target = self.get_parameter_value(self.secondary_target)
        active = self.get_parameter_value(self.active)
        ik_weight = self.get_parameter_value(self.ik_weight)
        ik_distance = self.get_parameter_value(self.ik_distance)
        distance_mode = self.get_parameter_value(self.distance_mode)
        if is_waiting(
            armature,
            constraint_name,
            enforced_factor,
            primary_target,
            secondary_target,
            active,
            ik_weight,
            ik_distance,
            distance_mode
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        if invalid(primary_target):
            primary_target = None
        if invalid(secondary_target):
            secondary_target = None
        constraint = armature.constraints[constraint_name]
        if (
            (enforced_factor is not None) and
            (constraint.enforce != enforced_factor)
        ):
            constraint.enforce = enforced_factor
        if constraint.target != primary_target:
            constraint.target = primary_target
        if constraint.subtarget != secondary_target:
            constraint.subtarget = secondary_target
        if constraint.active != active:
            constraint.active = active
        if (ik_weight is not None) and (constraint.ik_weight != ik_weight):
            constraint.ik_weight = ik_weight
        if (
            (ik_distance is not None) and
            (constraint.ik_distance != ik_distance)
        ):
            constraint.ik_distance = ik_distance
        if (
            (distance_mode is not None) and
            (constraint.ik_mode != distance_mode)
        ):
            constraint.ik_mode = distance_mode
        armature.update()
        self.done = True


class ActionEditBone(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.armature = None
        self.bone_name = None
        self.set_translation = None
        self.set_orientation = None
        self.set_scale = None
        self.translate = None
        self.rotate = None
        self.scale = None
        self._eulers = mathutils.Euler((0, 0, 0), "XYZ")
        self._vector = mathutils.Vector((0, 0, 0))
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def _convert_orientation(self, ch, xyzrot):
        eulers = self._eulers
        eulers[:] = xyzrot
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            return eulers.to_quaternion()
        else:
            return xyzrot

    def _set_orientation(self, ch, rot):
        orientation = self._convert_orientation(ch, rot)
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            ch.rotation_quaternion = orientation
        else:
            ch.rotation_euler = orientation

    def _rotate(self, ch, xyzrot):
        orientation = self._convert_orientation(ch, xyzrot)
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            ch.rotation_quaternion = (
                mathutils.Quaternion(ch.rotation_quaternion) * orientation
            )
        else:
            ch.rotation_euler = ch.rotation_euler.rotate(orientation)

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_parameter_value(self.armature)
        bone_name = self.get_parameter_value(self.bone_name)
        set_translation = self.get_parameter_value(self.set_translation)
        set_orientation = self.get_parameter_value(self.set_orientation)
        set_scale = self.get_parameter_value(self.set_scale)
        translate = self.get_parameter_value(self.translate)
        rotate = self.get_parameter_value(self.rotate)
        scale = self.get_parameter_value(self.scale)
        if is_waiting(
            armature,
            bone_name,
            set_translation,
            set_orientation,
            set_scale,
            translate,
            rotate,
            scale
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        if not bone_name:
            return
        # TODO cache the bone index
        bone_channel = armature.channels[bone_name]
        if set_translation is not None:
            bone_channel.location = set_translation
        if set_orientation is not None:
            self._set_orientation(bone_channel, set_orientation)
        if set_scale is not None:
            bone_channel.scale = set_scale
        if translate is not None:
            vec = self._vector
            vec[:] = translate
            bone_channel.location = bone_channel.location + vec
        if scale is not None:
            vec = self._vector
            vec[:] = scale
            bone_channel.scale = bone_channel.scale + vec
        if rotate is not None:
            self._rotate(bone_channel, rotate)
        armature.update()
        self.done = True


class ActionSetBonePos(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.armature = None
        self.bone_name = None
        self.set_translation = None
        self._eulers = mathutils.Euler((0, 0, 0), "XYZ")
        self._vector = mathutils.Vector((0, 0, 0))
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_parameter_value(self.armature)
        bone_name = self.get_parameter_value(self.bone_name)
        set_translation = self.get_parameter_value(self.set_translation)
        self._set_ready()
        if is_invalid(armature, bone_name, set_translation):
            return
        if not bone_name:
            return
        # TODO cache the bone index
        bone_channel = armature.channels[bone_name]
        if set_translation is not None:
            bone_channel.location = set_translation
        else:
            debug('Set Bone Node: Position is None!')
        armature.update()
        self.done = True


class ActionTimeFilter(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.delay = None
        self._triggered = False
        self._triggered_time = None
        self._trigger_delay = None

    def evaluate(self):
        if self._triggered is True:
            self._set_ready()
            delta = self.network.timeline - self._triggered_time
            if delta < self._trigger_delay:
                self._set_value(False)
                return
        condition = self.get_parameter_value(self.condition)
        delay = self.get_parameter_value(self.delay)
        if is_waiting(condition, delay):
            return
        self._set_ready()
        self._set_value(False)
        if delay is None:
            return
        if condition is None:
            return
        if condition:
            self._triggered = True
            self._triggered_time = self.network.timeline
            self._trigger_delay = delay
            self._set_value(True)


class GEBarrier(ActionCell):
    consumed: bool
    trigger: float

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.time = None
        self.consumed = False
        self.trigger = 0

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        time = self.get_parameter_value(self.time)
        if is_waiting(time):
            return

        self._set_ready()

        now = self.network.timeline

        if not not_met(condition):
            if not self.consumed:
                self.consumed = True
                self.trigger = now + time

            if now >= self.trigger:
                self._set_value(True)

        else:
            self._set_value(False)
            self.consumed = False


class ActionTimeDelay(ActionCell):
    consumed: bool
    triggers: list

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.delay = None
        self.triggers = []

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        delay = self.get_parameter_value(self.delay)
        if is_invalid(delay):
            return
        self._set_ready()

        now = self.network.timeline

        if not not_met(condition):
            self.triggers.append(now + delay)

        if not self.triggers:
            self._set_value(False)
            return
        t = self.triggers[0]
        if now >= t:
            self._set_value(True)
            self.triggers.remove(t)
            return
        self._set_value(False)


class ActionSetDynamics(ActionCell):
    def __init__(self):
        self.condition = None
        self.game_object = None
        self.activate = False
        self.ghost = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        ghost = self.get_parameter_value(self.ghost)
        activate = self.get_parameter_value(self.activate)
        if is_waiting(game_object, ghost, activate):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if activate:
            game_object.suspendDynamics(ghost)
        else:
            game_object.restoreDynamics()
        self.done = True


class ActionEndObject(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.scene = None
        self.game_object = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        game_object = self.get_parameter_value(self.game_object)
        if not_met(condition):
            return
        if is_waiting(game_object):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        game_object.endObject()
        self.done = True


class ActionSetTimeScale(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.scene = None
        self.timescale = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        timescale = self.get_parameter_value(self.timescale)
        if is_waiting(timescale):
            return
        self._set_ready()
        if is_invalid(timescale):
            return
        logic.setTimeScale(timescale)
        self.done = True


class ActionSetGravity(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.scene = None
        self.gravity = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        gravity = self.get_parameter_value(self.gravity)
        if is_waiting(gravity):
            return
        self._set_ready()
        if is_invalid(gravity):
            return
        logic.setGravity(gravity)
        self.done = True


class ActionApplyGameObjectValue(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.movement = None
        self.rotation = None
        self.force = None
        self.torque = None
        self.local = False

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        if is_waiting(game_object):
            return
        movement = self.get_parameter_value(self.movement)
        rotation = self.get_parameter_value(self.rotation)
        force = self.get_parameter_value(self.force)
        torque = self.get_parameter_value(self.torque)
        local = self.local
        if is_waiting(movement, rotation, force, torque, local):
            return
        self._set_ready()
        if not condition:
            return
        if is_invalid(game_object):
            return
        if movement:
            game_object.applyMovement(movement, local)
        if rotation:
            if len(rotation) == 3:
                game_object.applyRotation(rotation, local)
            else:
                game_object.applyRotation(rotation.to_euler("XYZ"), local)
        if force:
            game_object.applyForce(force, local)
        if torque:
            game_object.applyTorque(torque, local)


class ActionApplyLocation(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.movement = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        movement = self.get_parameter_value(self.movement)
        local = self.local
        if is_waiting(game_object, movement, local):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if movement:
            game_object.applyMovement(movement, local)
        self.done = True


class ActionApplyRotation(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.rotation = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        rotation = self.get_parameter_value(self.rotation)
        local = self.local
        if is_waiting(game_object, rotation, local):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if rotation:
            if len(rotation) == 3:
                game_object.applyRotation(rotation, local)
            else:
                game_object.applyRotation(rotation.to_euler("XYZ"), local)
        self.done = True


class ActionApplyForce(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.force = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        force = self.get_parameter_value(self.force)
        local = self.local
        if is_waiting(game_object, force):
            return
        self._set_ready()
        game_object.applyForce(force, local)
        self.done = True


class ActionApplyImpulse(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.point = None
        self.impulse = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        point = self.get_parameter_value(self.point)
        impulse = self.get_parameter_value(self.impulse)
        local = self.local
        if hasattr(point, 'worldPosition'):
            point = point.worldPosition
        if is_waiting(point, impulse) or is_invalid(game_object):
            return
        self._set_ready()
        if impulse:
            game_object.applyImpulse(point, impulse, local)
        self.done = True


class ActionCharacterJump(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_parameter_value(self.game_object)
        if is_waiting(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.jump()

        self.done = True


class ActionSaveVariable(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.name = None
        self.val = None
        self.path = ''
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, name, val):
        data = None
        file_path = path + 'variables.json'
        if os.path.isfile(file_path):
            f = open(file_path, 'r')
            data = json.load(f)
            data[name] = val
            f.close()
            f = open(file_path, 'w')
            json.dump(data, f, indent=2)
        else:
            debug('file does not exist - creating...')
            f = open(file_path, 'w')
            data = {name: val}
            json.dump(data, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        name = self.get_parameter_value(self.name)
        val = self.get_parameter_value(self.val)
        if is_waiting(name, val):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)
        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, name, val)
        self.done = True


class ActionSaveVariables(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.val = None
        self.path = ''
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, val):
        path = path + 'variables.json'
        if os.path.isfile(path):
            f = open(path, 'w')
            json.dump(val, f, indent=2)
        else:
            debug('file does not exist - creating...')
            f = open(path, 'w')
            json.dump(val, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        val = self.get_parameter_value(self.val)
        if is_waiting(val):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)
        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, val)
        self.done = True


class ActionLoadVariable(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.name = None
        self.path = ''
        self.var = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.VAR = LogicNetworkSubCell(self, self.get_var)

    def get_done(self):
        return self.done

    def get_var(self):
        return self.var

    def read_from_json(self, path, name):
        self.done = False
        file_path = path + 'variables.json'
        if file_path:
            f = open(file_path, 'r')
            data = json.load(f)
            if name not in data:
                debug('"{}" is not a saved Variabe!')
            self.var = data[name]
            f.close()
        else:
            debug('No saved variables!')

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        name = self.get_parameter_value(self.name)
        if is_waiting(name):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.read_from_json(path, name)
        self.done = True


class ActionLoadVariables(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.path = ''
        self.var = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.VAR = LogicNetworkSubCell(self, self.get_var)

    def get_done(self):
        return self.done

    def get_var(self):
        return self.var

    def read_from_json(self, path):
        self.done = False
        path = path + 'variables.json'
        if not os.path.isfile(path):
            debug('No Saved Variables!')
            return
        f = open(path, 'r')
        data = json.load(f)
        self.var = data
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.read_from_json(path)
        self.done = True


class ActionRemoveVariable(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.name = None
        self.path = ''
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, name):
        data = None
        file_path = path + 'variables.json'
        if os.path.isfile(file_path):
            f = open(file_path, 'r')
            data = json.load(f)
            if name in data:
                del data[name]
            f.close()
            f = open(file_path, 'w')
            json.dump(data, f, indent=2)
            f.close()
        else:
            debug('File does not exist!')

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        name = self.get_parameter_value(self.name)
        if is_waiting(name):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, name)
        self.done = True


class ActionClearVariables(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.path = ''
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path):
        data = None
        file_path = path + 'variables.json'
        if os.path.isfile(file_path):
            data = {}
            f = open(file_path, 'w')
            json.dump(data, f, indent=2)
        else:
            debug('File does not exist - creating...')
            f = open(file_path, 'w')
            data = {}
            json.dump(data, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path)
        self.done = True


class ActionListVariables(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.print_list = None
        self.path = ''
        self.done = None
        self.items = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)
        self.LIST = LogicNetworkSubCell(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.items

    def write_to_json(self, path, p_l):
        data = None
        file_path = path + 'variables.json'
        if os.path.isfile(file_path):
            f = open(file_path, 'r')
            data = json.load(f)
            if len(data) == 0:
                debug('There are no saved variables')
                return
            li = []
            for x in data:
                if p_l:
                    print('{}\t->\t{}'.format(x, data[x]))
                li.append(x)
            self.items = li
        else:
            debug('There are no saved variables')
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/'):
            path = path + '/'
        if path.startswith('./'):
            path = path.split('./', 1)[-1]
            return bpy.path.abspath('//' + path)
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        print_list = self.get_parameter_value(self.print_list)
        if is_waiting(print_list):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, print_list)
        self.done = True


class ActionSetCharacterJump(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.max_jumps = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        max_jumps = self.get_parameter_value(self.max_jumps)
        if is_waiting(game_object, max_jumps):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        physics.maxJumps = max_jumps
        self.done = True


class ActionSetCharacterGravity(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.gravity = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        gravity = self.get_parameter_value(self.gravity)
        if is_waiting(gravity):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        physics.gravity = gravity
        self.done = True


class ActionSetCharacterWalkDir(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.walkDir = None
        self.local = False
        self.active = False
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            if self.active:
                game_object = self.get_parameter_value(self.game_object)
                physics = bge.constraints.getCharacter(game_object)
                physics.walkDirection = mathutils.Vector((0, 0, 0))
                self.active = False
            return
        elif not self.active:
            self.active = True
        game_object = self.get_parameter_value(self.game_object)
        local = self.local
        walkDir = self.get_parameter_value(self.walkDir)
        if is_waiting(game_object, local, walkDir):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if local:
            walkDir = game_object.worldOrientation @ walkDir
        physics = bge.constraints.getCharacter(game_object)
        physics.walkDirection = walkDir
        self.done = True


class ActionSetCharacterVelocity(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.vel = None
        self.time = None
        self.local = False
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        if is_waiting(game_object):
            return
        local = self.local
        physics = bge.constraints.getCharacter(game_object)
        vel = self.get_parameter_value(self.vel)
        time = self.get_parameter_value(self.time)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.setVelocity(vel, time, local)
        self.done = True


class ParameterGetCharacterInfo(ParameterCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.game_object = None
        self.max_jumps = None
        self.cur_jump = None
        self.gravity = None
        self.walk_dir = None
        self.on_ground = None
        self.MAX_JUMPS = LogicNetworkSubCell(self, self.get_max_jumps)
        self.CUR_JUMP = LogicNetworkSubCell(self, self.get_current_jump)
        self.GRAVITY = LogicNetworkSubCell(self, self.get_gravity)
        self.WALKDIR = LogicNetworkSubCell(self, self.get_walk_dir)
        self.ON_GROUND = LogicNetworkSubCell(self, self.get_on_ground)

    def get_max_jumps(self):
        return self.max_jumps

    def get_current_jump(self):
        return self.cur_jump

    def get_gravity(self):
        return self.gravity

    def get_walk_dir(self):
        return self.walk_dir

    def get_on_ground(self):
        return self.on_ground

    def evaluate(self):
        game_object = self.get_parameter_value(self.game_object)
        if is_invalid(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        self._set_ready()
        self.max_jumps = physics.maxJumps
        self.cur_jump = physics.jumpCount
        self.gravity = physics.gravity
        self.walk_dir = physics.walkDirection
        self.on_ground = physics.onGround


class ActionApplyTorque(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.torque = None
        self.local = False
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        torque = self.get_parameter_value(self.torque)
        local = self.local
        if is_waiting(game_object, torque):
            return
        self._set_ready()
        if torque:
            game_object.applyTorque(torque, local)
        self.done = True


class ActionPlayAction(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_name = None
        self.stop = None
        self.frames = None
        self.start_frame = None
        self.end_frame = None
        self.layer = None
        self.priority = None
        self.play_mode = None
        self.layer_weight = None
        self.old_layer_weight = None
        self.speed = None
        self.old_speed = None
        self.blendin = None
        self.blend_mode = None
        self._started = False
        self._running = False
        self._finished = False
        self._frame = 0.0
        self._finish_notified = False
        self.STARTED = LogicNetworkSubCell(self, self._get_started)
        self.FINISHED = LogicNetworkSubCell(self, self._get_finished)
        self.RUNNING = LogicNetworkSubCell(self, self._get_running)
        self.FRAME = LogicNetworkSubCell(self, self._get_frame)

    def _get_started(self):
        return self._started

    def _get_finished(self):
        return self._finished

    def _get_running(self):
        return self._running

    def _get_frame(self):
        return self._frame

    def _reset_subvalues(self):
        self._started = False
        self._finished = False
        self._running = False
        self._frame = 0.0
        self._finish_notified = False

    def _notify_finished(self, obj, layer):
        if not self._finish_notified and self.stop:
            self._finish_notified = True
            self._finished = True
            obj.stopAction(layer)
        else:
            self._finished = False

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        game_object = self.get_parameter_value(self.game_object)
        action_name = self.get_parameter_value(self.action_name)
        start_frame = self.get_parameter_value(self.start_frame)
        end_frame = self.get_parameter_value(self.end_frame)
        layer = self.get_parameter_value(self.layer)
        priority = self.get_parameter_value(self.priority)
        play_mode = self.get_parameter_value(self.play_mode)
        layer_weight = self.get_parameter_value(self.layer_weight)
        speed = self.get_parameter_value(self.speed)
        blendin = self.get_parameter_value(self.blendin)
        blend_mode = self.get_parameter_value(self.blend_mode)
        if is_waiting(
            game_object,
            action_name,
            start_frame,
            end_frame,
            layer,
            priority,
            play_mode,
            layer_weight,
            speed,
            blendin,
            blend_mode
        ):
            return
        if play_mode > 2:
            if not_met(condition):
                self._notify_finished(game_object, layer)
                return
            else:
                play_mode -= 3
        if layer_weight <= 0:
            layer_weight = 0.0
        elif layer_weight >= 1:
            layer_weight = 1.0
        if speed <= 0:
            speed = 0.01
        self._set_ready()
        if is_invalid(game_object):  # can't play
            debug("Play Action Node: Invalid Game Object!")
            self._reset_subvalues()
        else:
            # Condition might be false and the animation running
            # because it was started in a previous evaluation
            playing_action = game_object.getActionName(layer)
            playing_frame = game_object.getActionFrame(layer)
            min_frame = start_frame
            max_frame = end_frame
            if end_frame < start_frame:
                min_frame = end_frame
                max_frame = max_frame
            if (
                (playing_action == action_name) and
                (playing_frame >= min_frame) and
                (playing_frame <= max_frame)
            ):
                self._started = False
                self._running = True
                is_near_end = False
                self._frame = playing_frame
                if (
                    layer_weight != self.old_layer_weight or
                    speed != self.old_speed
                ):
                    next_frame = (
                        playing_frame + speed
                        if
                        playing_frame + speed <= end_frame
                        else
                        0
                    )
                    game_object.stopAction(layer)
                    game_object.playAction(
                        action_name,
                        start_frame,
                        end_frame,
                        layer=layer,
                        priority=priority,
                        blendin=blendin,
                        play_mode=play_mode,
                        speed=speed,
                        layer_weight=1 - layer_weight,
                        blend_mode=blend_mode)
                    game_object.setActionFrame(next_frame, layer)
                # TODO: the meaning of start-end depends
                # also on the action mode
                if end_frame > start_frame:  # play 0 to 100
                    is_near_end = (playing_frame >= (end_frame - 0.5))
                else:  # play 100 to 0
                    is_near_end = (playing_frame <= (end_frame + 0.5))
                if is_near_end:
                    self._notify_finished(game_object, layer)
            elif condition:  # start the animation if the condition is True
                game_object.playAction(
                    action_name,
                    start_frame,
                    end_frame,
                    layer=layer,
                    priority=priority,
                    blendin=blendin,
                    play_mode=play_mode,
                    speed=speed,
                    layer_weight=1 - layer_weight,
                    blend_mode=blend_mode)
                self._started = True
                self._running = True
                self._finished = False
                self._frame = start_frame
                self._finish_notified = False
            else:  # game_object is existing and valid but condition is False
                self._reset_subvalues()
        self.old_layer_weight = layer_weight
        self.old_speed = speed


class ActionStopAnimation(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_layer = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not condition:
            self._set_ready()
            return
        game_object = self.get_parameter_value(self.game_object)
        action_layer = self.get_parameter_value(self.action_layer)
        if is_waiting(game_object, action_layer):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if is_invalid(action_layer):
            return
        game_object.stopAction(action_layer)
        self.done = True


class ActionSetAnimationFrame(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_layer = None
        self.action_frame = None
        self.freeze = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not condition:
            self._set_ready()
            return
        game_object = self.get_parameter_value(self.game_object)
        action_layer = self.get_parameter_value(self.action_layer)
        action_frame = self.get_parameter_value(self.action_frame)
        freeze = self.get_parameter_value(self.freeze)
        action_name = self.get_parameter_value(self.action_name)
        layer_weight = self.get_parameter_value(self.layer_weight)
        self._set_ready()
        if is_invalid(
            game_object,
            action_layer,
            action_frame,
            layer_weight
        ):
            debug('Set Animation Frame Node: Invalid Parameters!')
            return
        is_playing = game_object.isPlayingAction(action_layer)
        same_action = game_object.getActionName(action_layer) == action_name
        action = bpy.data.actions[action_name]
        start_frame = action.frame_range[0]
        end_frame = action.frame_range[1]
        finished = game_object.getActionFrame(action_layer) >= end_frame
        if not (is_playing or same_action) or finished:
            game_object.stopAction(action_layer)
            speed = .000000000000000001 if freeze else 1
            game_object.playAction(
                action_name,
                start_frame,
                end_frame,
                action_layer,
                layer_weight=1-layer_weight,
                speed=speed
            )
        game_object.setActionFrame(action_frame, action_layer)
        self.done = True


class ActionFindScene(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.query = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def has_status(self, status):
        found_scene = self.get_value()
        if (
            (self.condition is None) and
            (found_scene is not None) and
            (not found_scene.invalid) and
            (found_scene is not None)
        ):
            return status is LogicNetworkCell.STATUS_READY
        else:
            return ActionCell.has_status(self, status)

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        query = self.get_parameter_value(self.query)
        if is_waiting(query):
            return
        self._set_ready()
        if self.condition is None:
            scene = _name_query(logic.getSceneList(), query)
            self._set_value(scene)
        scene = _name_query(logic.getSceneList(), query)
        self._set_value(scene)
        self.done = True


class ActionStart3DSoundAdv(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.sound = None
        self.occlusion = None
        self.transition = None
        self.cutoff = None
        self.speaker = None
        self.device = None
        self.loop_count = None
        self.pitch = None
        self.volume = None
        self.attenuation = None
        self.distance_ref = None
        self.cone_angle = None
        self.cone_outer_volume = None
        self.done = None
        self.on_finish = False
        self._clear_sound = 1
        self._sustained = 1
        self._handle = None
        self._handles = {}
        self.DONE = LogicNetworkSubCell(self, self.get_done)
        self.ON_FINISH = LogicNetworkSubCell(self, self.get_on_finish)
        self.HANDLE = LogicNetworkSubCell(self, self.get_handle)

    def get_handle(self):
        return self._handle
    
    def get_on_finish(self):
        return self.on_finish

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        audio_system = self.network.audio_system
        speaker = self.get_parameter_value(self.speaker)
        handles = self._handles
        occlusion = self.get_parameter_value(self.occlusion)
        volume = self.get_parameter_value(self.volume)
        cone_outer_volume = self.get_parameter_value(self.cone_outer_volume)
        pitch = self.get_parameter_value(self.pitch) * logic.getTimeScale()
        attenuation = self.get_parameter_value(self.attenuation)
        self.on_finish = False
        if handles:
            for sound in handles:
                ind = 0
                for handle in handles[sound]:
                    if handle.status:
                        self._set_ready()
                        if ind == 0:
                            self._handle = handle
                        handle.pitch = pitch
                        handle.location = speaker.worldPosition
                        handle.orientation = (
                            speaker
                            .worldOrientation
                            .to_quaternion()
                        )
                        if speaker.mass:
                            handle.velocity = getattr(
                                speaker,
                                'worldLinearVelocity',
                                mathutils.Vector((0, 0, 0))
                            )
                        if occlusion:
                            transition = self.get_parameter_value(
                                self.transition
                            )
                            cam = bge.logic.getCurrentScene().active_camera
                            occluder, point, normal = cam.rayCast(
                                speaker.worldPosition,
                                cam.worldPosition,
                                compute_distance(speaker, cam),
                                xray=False
                            )
                            occluded = False
                            penetration = 1
                            while occluder:
                                if occluder is speaker:
                                    break
                                sound_occluder = occluder.blenderObject.get(
                                    'sound_occluder',
                                    True
                                )
                                if sound_occluder:
                                    occluded = True
                                    block = occluder.blenderObject.get(
                                        'sound_blocking',
                                        .1
                                    )
                                    if penetration > 0:
                                        penetration -= block
                                    else:
                                        penetration = 0
                                    # attenuation *= 1 + block / 2
                                occluder, point, normal = occluder.rayCast(
                                    speaker.worldPosition,
                                    point,
                                    compute_distance(speaker, point),
                                    xray=False
                                )
                            cs = self._clear_sound
                            if occluded and cs > 0:
                                self._clear_sound -= transition
                            elif not occluded and cs < 1:
                                self._clear_sound += transition
                            if self._clear_sound < 0:
                                self._clear_sound = 0
                            sustained = self._sustained
                            if sustained > penetration:
                                self._sustained -= transition / 10
                            elif sustained < penetration:
                                self._sustained += transition / 10
                            mult = (
                                cs * sustained
                                if not ind
                                else (1 - cs) * sustained
                            )
                            # handles[sound][ind].attenuation = attenuation
                            handles[sound][ind].volume = volume * mult
                            handles[sound][ind].cone_volume_outer = (
                                cone_outer_volume *
                                volume *
                                mult
                            )
                        else:
                            handles[sound][ind].volume = volume
                            handles[sound][ind].cone_volume_outer = (
                                cone_outer_volume *
                                volume
                            )
                    elif handle in audio_system.active_sounds:
                        for handle in handles[sound]:
                            audio_system.active_sounds.remove(handle)
                            handles[sound] = []
                        self.on_finish = True
                        continue
                    ind += 1
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        cutoff = self.get_parameter_value(self.cutoff)
        sound = self.get_parameter_value(self.sound)
        device = self.get_parameter_value(self.device)
        loop_count = self.get_parameter_value(self.loop_count)
        distance_ref = self.get_parameter_value(self.distance_ref)
        cone_angle = self.get_parameter_value(self.cone_angle)
        cone_inner_angle = cone_angle.x
        cone_outer_angle = cone_angle.y
        self._set_ready()

        if is_invalid(sound):
            return
        if not hasattr(bpy.types.Scene, 'nl_aud_devices'):
            debug('No Audio Devices initialized!')
            return
        else:
            devs = bpy.types.Scene.nl_aud_devices
        soundpath = logic.expandPath(sound)
        soundfile = aud.Sound.file(soundpath)
        if device not in devs.keys():
            debug(f'Opening Sound Device: {device}')
            devs[device] = aud.Device()
        handle = self._handle = devs[device].play(soundfile)
        if occlusion:
            soundlow = aud.Sound.lowpass(soundfile, 4000*cutoff, .5)
            handlelow = devs[device].play(soundlow)
            self._handles[soundfile] = [handle, handlelow]
        else:
            self._handles[soundfile] = [handle]
        for handle in self._handles[soundfile]:
            handle.relative = False
            handle.location = speaker.worldPosition
            if speaker.mass:
                handle.velocity = getattr(
                    speaker,
                    'worldLinearVelocity',
                    mathutils.Vector((0, 0, 0))
                )
            handle.attenuation = attenuation
            handle.orientation = speaker.worldOrientation.to_quaternion()
            handle.pitch = pitch
            handle.loop_count = loop_count
            handle.volume = volume
            handle.distance_reference = distance_ref
            handle.distance_maximum = 1000
            handle.cone_angle_inner = cone_inner_angle
            handle.cone_angle_outer = cone_outer_angle
            handle.cone_volume_outer = cone_outer_volume * volume
            audio_system.active_sounds.append(handle)
        self.done = True


class ActionStartSound(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.sound = None
        self.loop_count = None
        self.pitch = None
        self.volume = None
        self.done = None
        self.on_finish = False
        self._handle = None
        self._handles = []
        self.DONE = LogicNetworkSubCell(self, self.get_done)
        self.ON_FINISH = LogicNetworkSubCell(self, self.get_on_finish)
        self.HANDLE = LogicNetworkSubCell(self, self.get_handle)

    def get_handle(self):
        return self._handle
    
    def get_on_finish(self):
        return self.on_finish

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        audio_system = self.network.audio_system
        handles = self._handles
        pitch = self.get_parameter_value(self.pitch)
        volume = self.get_parameter_value(self.volume)
        self.on_finish = False
        if handles:
            for handle in handles:
                if not handle.status and handle in audio_system.active_sounds:
                    self._handles.remove(handle)
                    audio_system.active_sounds.remove(handle)
                    self.on_finish = True
                    continue
                self._set_ready()
                handle.volume = volume
                handle.pitch = pitch
            self._handle = handles[-1]
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_parameter_value(self.sound)
        loop_count = self.get_parameter_value(self.loop_count)
        self._set_ready()

        if is_invalid(sound):
            return
        if not hasattr(bpy.types.Scene, 'nl_aud_devices'):
            debug('No Audio Devices initialized!')
            return
        else:
            devs = bpy.types.Scene.nl_aud_devices
        soundpath = logic.expandPath(sound)
        soundfile = aud.Sound.file(soundpath)
        handle = self._handle = devs['default'].play(soundfile)
        self._handles.append(handle)
        handle.relative = True
        handle.pitch = pitch
        handle.loop_count = loop_count
        handle.volume = volume
        audio_system.active_sounds.append(handle)
        self.done = True


class ActionStopSound(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_parameter_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.stop()


class ActionStopAllSounds(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        if not hasattr(bpy.types.Scene, 'nl_aud_devices'):
            debug('No Audio Devices to close.')
            return
        self._set_ready()
        for dev in bpy.types.Scene.nl_aud_devices:
            bpy.types.Scene.nl_aud_devices[dev].stopAll()


class ActionPauseSound(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_parameter_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.pause()


class ActionResumeSound(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_parameter_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.resume()


class ReceiveMessage(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.subject = None
        self.received = False
        self.body = ''
        self.target = None
        self.OUT = LogicNetworkSubCell(self, self.get_received)
        self.BODY = LogicNetworkSubCell(self, self.get_body)
        self.TARGET = LogicNetworkSubCell(self, self.get_target)

    def get_received(self):
        return self.received
    
    def get_body(self):
        return self.body
    
    def get_target(self):
        return self.target

    def evaluate(self):
        subject = self.get_parameter_value(self.subject)
        if is_invalid(subject):
            return
        self._set_ready()
        messages = self.network._messages
        rec = subject in messages.data
        if rec:
            self.received = True
            dat = messages.data[subject]
            self.body = dat[0]
            self.target = dat[1]
            return
        self.target = None
        self.body = ''
        self.received = False


class ParameterGetGlobalValue(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.data_id = None
        self.key = None
        self.default = None

    def evaluate(self):
        data_id = self.get_parameter_value(self.data_id)
        key = self.get_parameter_value(self.key)
        default = self.get_parameter_value(self.default)
        if is_waiting(data_id, key, default):
            return
        self._set_ready()
        db = SimpleLoggingDatabase.get_or_create_shared_db(data_id)
        self._set_value(db.get(key, default))


class ActionListGlobalValues(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.condition = None
        self.data_id = None
        self.print_d = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        data_id = self.get_parameter_value(self.data_id)
        print_d = self.get_parameter_value(self.print_d)
        if is_waiting(data_id, print_d):
            return
        self._set_ready()
        db = SimpleLoggingDatabase.get_or_create_shared_db(data_id)
        if print_d:
            print(f'[Logic Nodes] Global category "{data_id}":')
            for e in db.data:
                print('{}\t->\t{}'.format(e, db.data[e]))
            print('END ------------------------------------')
        self._set_value(db.data)


class ParameterFormattedString(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.format_string = None
        self.value_a = None
        self.value_b = None
        self.value_c = None
        self.value_d = None

    def evaluate(self):
        format_string = self.get_parameter_value(self.format_string)
        value_a = self.get_parameter_value(self.value_a)
        value_b = self.get_parameter_value(self.value_b)
        value_c = self.get_parameter_value(self.value_c)
        value_d = self.get_parameter_value(self.value_d)
        if is_waiting(format_string, value_a, value_b, value_c, value_d):
            return
        self._set_ready()
        if format_string is None:
            return
        result = format_string.format(value_a, value_b, value_c, value_d)
        self._set_value(result)


class ActionSetGlobalValue(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.data_id = None
        self.key = None
        self.value = None
        self.persistent = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        data_id = self.get_parameter_value(self.data_id)
        persistent = self.get_parameter_value(self.persistent)
        key = self.get_parameter_value(self.key)
        value = self.get_parameter_value(self.value)
        if is_waiting(data_id, persistent, key, value):
            return
        self._set_ready()
        if self.condition is None or condition:
            if data_id is None:
                return
            if persistent is None:
                return
            if key is None:
                return
            db = SimpleLoggingDatabase.get_or_create_shared_db(data_id)
            db.put(key, value, persistent)
            if self.condition is None:
                self.deactivate()
        self.done = True


class CreateMessage(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.subject = None
        self.body = None
        self.target = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        subject = self.get_parameter_value(self.subject)
        messages = self.network._messages
        if not_met(condition):
            if subject in messages.data:
                if messages.data[subject][2] is self:
                    messages.data.pop(subject, None)
            self._set_ready()
            return
        body = self.get_parameter_value(self.body)
        target = self.get_parameter_value(self.target)
        if is_waiting(body, target):
            return
        if is_invalid(subject):
            return
        self._set_ready()
        messages.put(subject, [body, target, self], False)
        self.done = True


class ActionRandomInt(ActionCell):
    def __init__(self):
        self.max_value = None
        self.min_value = None
        self._output = 0
        self.OUT_A = LogicNetworkSubCell(self, self._get_output)

    def _get_output(self):
        return self._output

    def evaluate(self):
        min_value = self.get_parameter_value(self.min_value)
        max_value = self.get_parameter_value(self.max_value)
        if is_waiting(max_value, min_value):
            return
        if min_value > max_value:
            s = min_value
            min_value = max_value
            max_value = s
        self._set_ready()
        if min_value == max_value:
            min_value = -sys.maxsize
            max_value = sys.maxsize

        self._output = random.randint(min_value, max_value)


class ActionRandomFloat(ActionCell):
    def __init__(self):
        self.max_value = None
        self.min_value = None
        self._output = 0
        self.OUT_A = LogicNetworkSubCell(self, self._get_output)

    def _get_output(self):
        return self._output

    def evaluate(self):
        min_value = self.get_parameter_value(self.min_value)
        max_value = self.get_parameter_value(self.max_value)
        if is_waiting(min_value, max_value):
            return
        if min_value > max_value:
            s = min_value
            min_value = max_value
            max_value = s
        self._set_ready()
        if min_value == max_value:
            min_value = sys.float_info.min
            max_value = sys.float_info.max

        delta = max_value - min_value
        self._output = min_value + (delta * random.random())


class ActionTranslate(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.moving_object = None
        self.local = None
        self.vect = None
        self.speed = None
        self._t = None
        self._old_values = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        moving_object = self.get_parameter_value(self.moving_object)
        vect = self.get_parameter_value(self.vect)
        dx = vect.x
        dy = vect.y
        dz = vect.z
        speed = self.get_parameter_value(self.speed)
        local = self.get_parameter_value(self.local)
        if is_waiting(
            vect,
            dx,
            dy,
            dz,
            speed,
            local
        ):
            return
        if is_invalid(moving_object):
            return
        self._set_ready()
        if dx is None:
            return
        if dy is None:
            return
        if dz is None:
            return
        if speed is None:
            return
        if local is None:
            return
        new_values = (moving_object, dx, dy, dz, speed, local)
        if new_values != self._old_values:
            start_pos = (
                moving_object.localPosition if
                local else moving_object.worldPosition
            )
            end_pos = mathutils.Vector((
                start_pos.x + dx, start_pos.y + dy, start_pos.z + dz
            ))
            distance = (start_pos - end_pos).length
            time_to_destination = distance / speed
            t_speed = 1.0 / time_to_destination
            self._old_values = new_values
            self._start_pos = start_pos.copy()
            self._end_pos = end_pos.copy()
            self._d_pos = (end_pos - start_pos)
            self._t_speed = t_speed
            self._t = 0.0
        t = self._t
        dt = self._t_speed * self.network.time_per_frame
        t += dt
        if t >= 1.0:
            self._set_value(True)
            self._t = 0.0
            if local:
                moving_object.localPosition = self._end_pos.copy()
            else:
                moving_object.worldPosition = self._end_pos.copy()
        else:
            npos = self._start_pos + (self._d_pos * t)
            if local:
                moving_object.localPosition = npos
            else:
                moving_object.worldPosition = npos
            self._t = t
            self._set_value(False)


class SetGamma(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].view_settings.gamma = value
        self.done = True


class SetExposure(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].view_settings.exposure = value
        self.done = True


class SetEeveeAO(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_gtao = value
        self.done = True


class SetEeveeBloom(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_bloom = value
        self.done = True


class SetEeveeSSR(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_ssr = value
        self.done = True


class SetEeveeVolumetrics(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].eevee.use_volumetric_lights = value
        self.done = True


class SetEeveeSMAA(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_eevee_smaa = value
        self.done = True


class SetEeveeSMAAQuality(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        value = self.get_parameter_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_eevee_smaa = value
        self.done = True


class SetLightEnergy(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.lamp = None
        self.energy = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_parameter_value(self.lamp)
        energy = self.get_parameter_value(self.energy)
        if is_waiting(lamp, energy):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        light.energy = energy
        self.done = True


class SetLightShadow(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.lamp = None
        self.use_shadow = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_parameter_value(self.lamp)
        use_shadow = self.get_parameter_value(self.use_shadow)
        if is_waiting(lamp, use_shadow):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        light.use_shadow = use_shadow
        self.done = True


class SetLightColor(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.lamp = None
        self.color = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_parameter_value(self.lamp)
        color = self.get_parameter_value(self.color)
        if is_waiting(lamp, color):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        light.color = color
        self.done = True


class GetLightEnergy(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.lamp = None
        self.energy = 0
        self.ENERGY = LogicNetworkSubCell(self, self.get_energy)

    def get_energy(self):
        return self.energy

    def evaluate(self):
        lamp = self.get_parameter_value(self.lamp)
        if is_waiting(lamp):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        self.energy = light.energy


class GetLightColor(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        self.lamp = None
        self.color = 0
        self.COLOR = LogicNetworkSubCell(self, self.get_color)

    def get_color(self):
        return self.color

    def evaluate(self):
        lamp = self.get_parameter_value(self.lamp)
        if is_waiting(lamp):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        self.color = light.color


# Action "Move To": an object will follow a point
class ActionMoveTo(ActionCell):

    def __init__(self):
        ActionCell.__init__(self)
        # list of parameters of this action
        self.condition = None
        self.moving_object = None
        self.destination_point = None
        self.speed = None
        self.dynamic = None
        self.distance = None

    def evaluate(self):  # the actual execution of this cell
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        moving_object = self.get_parameter_value(self.moving_object)
        destination_point = self.get_parameter_value(self.destination_point)
        speed = self.get_parameter_value(self.speed)
        distance = self.get_parameter_value(self.distance)
        dynamic = self.get_parameter_value(self.dynamic)
        if hasattr(destination_point, 'worldPosition'):
            destination_point = destination_point.worldPosition
        if is_waiting(
            moving_object,
            destination_point,
            speed,
            distance,
            dynamic
        ):
            return
        self._set_ready()
        self._set_value(move_to(
            moving_object,
            destination_point,
            speed,
            self.network.time_per_frame,
            dynamic,
            distance))


class ActionTrackTo(ActionCell):
    def __init__(self):
        self.condition = None
        self.moving_object = None
        self.target_object = None
        self.rot_axis = 2
        self.front_axis = 0
        self.speed = 20

    def evaluate(self):
        self._set_value(False)
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return self._set_ready()
        moving_object = self.get_parameter_value(self.moving_object)
        target_object = self.get_parameter_value(self.target_object)
        speed = self.get_parameter_value(self.speed)
        rot_axis = self.get_parameter_value(self.rot_axis)
        front_axis = self.get_parameter_value(self.front_axis)
        if is_waiting(speed, rot_axis, front_axis):
            return
        if is_invalid(moving_object):
            return
        if is_invalid(target_object):
            return
        self._set_ready()
        if rot_axis is None:
            return
        if front_axis is None:
            return
        if rot_axis == 0:
            self._set_value(
                xrot_to(
                    moving_object,
                    target_object,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 1:
            self._set_value(
                yrot_to(
                    moving_object,
                    target_object,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 2:
            self._set_value(
                zrot_to(
                    moving_object,
                    target_object,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )


class ActionRotateTo(ActionCell):
    def __init__(self):
        self.condition = None
        self.moving_object = None
        self.target_point = None
        self.rot_axis = 2
        self.front_axis = 0

    def evaluate(self):
        self._set_value(False)
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        moving_object = self.get_parameter_value(self.moving_object)
        target_point = self.get_parameter_value(self.target_point)
        if hasattr(target_point, 'worldPosition'):
            target_point = target_point.worldPosition
        rot_axis = self.get_parameter_value(self.rot_axis)
        front_axis = self.get_parameter_value(self.front_axis)
        if is_waiting(moving_object, target_point, rot_axis, front_axis):
            return
        self._set_ready()
        if rot_axis == 0:
            self._set_value(
                xrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    0,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 1:
            self._set_value(
                yrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    0,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 2:
            self._set_value(
                zrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    0,
                    self.network.time_per_frame
                )
            )


class ActionNavigateWithNavmesh(ActionCell):

    class MotionPath(object):
        def __init__(self):
            self.points = []
            self.cursor = 0
            self.destination = None

        def next_point(self):
            if self.cursor < len(self.points):
                return self.points[self.cursor]
            else:
                return None

        def destination_changed(self, new_destination):
            return self.destination != new_destination

        def advance(self):
            self.cursor += 1
            return self.cursor < len(self.points)

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.moving_object = None
        self.rotating_object = None
        self.navmesh_object = None
        self.destination_point = None
        self.move_dynamic = None
        self.linear_speed = None
        self.reach_threshold = None
        self.look_at = None
        self.rot_axis = None
        self.front_axis = None
        self.rot_speed = None
        self._motion_path = None

    def evaluate(self):
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        moving_object = self.get_parameter_value(self.moving_object)
        rotating_object = self.get_parameter_value(self.rotating_object)
        navmesh_object = self.get_parameter_value(self.navmesh_object)
        destination_point = self.get_parameter_value(self.destination_point)
        move_dynamic = self.get_parameter_value(self.move_dynamic)
        linear_speed = self.get_parameter_value(self.linear_speed)
        reach_threshold = self.get_parameter_value(self.reach_threshold)
        look_at = self.get_parameter_value(self.look_at)
        rot_axis = self.get_parameter_value(self.rot_axis)
        front_axis = self.get_parameter_value(self.front_axis)
        rot_speed = self.get_parameter_value(self.rot_speed)
        if is_invalid(
            destination_point,
            move_dynamic,
            linear_speed,
            reach_threshold,
            look_at,
            rot_axis,
            front_axis,
            rot_speed
        ):
            return
        if is_invalid(moving_object, navmesh_object):
            return
        if is_invalid(rotating_object):
            rotating_object = None
        self._set_ready()
        if (
            (self._motion_path is None) or
            (self._motion_path.destination_changed(destination_point))
        ):
            points = navmesh_object.findPath(
                moving_object.worldPosition,
                destination_point
            )
            motion_path = ActionNavigateWithNavmesh.MotionPath()
            motion_path.points = points[1:]
            motion_path.destination = destination_point
            self._motion_path = motion_path
        next_point = self._motion_path.next_point()
        if next_point:
            tpf = self.network.time_per_frame
            if look_at and (rotating_object is not None):
                rot_to(
                    rot_axis,
                    rotating_object,
                    next_point,
                    front_axis,
                    rot_speed,
                    tpf
                )
            reached = move_to(
                moving_object,
                next_point,
                linear_speed,
                tpf,
                move_dynamic,
                reach_threshold
            )
            if reached:
                has_more = self._motion_path.advance()
                if not has_more:
                    self._set_value(True)


class ActionFollowPath(ActionCell):
    class MotionPath(object):
        def __init__(self):
            self.points = []
            self.cursor = 0
            self.loop = False
            self.loop_start = 0

        def next_point(self):
            if self.cursor < len(self.points):
                return self.points[self.cursor]
            else:
                return None

        def advance(self):
            self.cursor += 1
            if self.cursor < len(self.points):
                return True
            else:
                if self.loop:
                    self.cursor = self.loop_start
                    return True
                return False

    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.moving_object = None
        self.rotating_object = None
        self.path_parent = None
        self.loop = None
        self.navmesh_object = None
        self.move_dynamic = None
        self.linear_speed = None
        self.reach_threshold = None
        self.look_at = None
        self.rot_speed = None
        self.rot_axis = None
        self.front_axis = None
        self._motion_path = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            self._motion_path = None
            self._set_ready()
            return
        moving_object = self.get_parameter_value(self.moving_object)
        rotating_object = self.get_parameter_value(self.rotating_object)
        path_parent = self.get_parameter_value(self.path_parent)
        navmesh_object = self.get_parameter_value(self.navmesh_object)
        move_dynamic = self.get_parameter_value(self.move_dynamic)
        linear_speed = self.get_parameter_value(self.linear_speed)
        reach_threshold = self.get_parameter_value(self.reach_threshold)
        look_at = self.get_parameter_value(self.look_at)
        rot_axis = self.get_parameter_value(self.rot_axis)
        front_axis = self.get_parameter_value(self.front_axis)
        rot_speed = self.get_parameter_value(self.rot_speed)
        loop = self.get_parameter_value(self.loop)
        if is_invalid(
            path_parent,
            move_dynamic,
            linear_speed,
            reach_threshold,
            look_at,
            rot_axis,
            front_axis,
            loop
        ):
            return
        if is_invalid(rot_speed):
            rot_speed = 0
        if loop is None:
            return
        if is_invalid(moving_object):
            return
        if is_invalid(navmesh_object):
            navmesh_object = None
        self._set_ready()
        self._set_value(False)
        if (self._motion_path is None) or (self._motion_path.loop != loop):
            self.generate_path(
                moving_object.worldPosition,
                path_parent,
                navmesh_object,
                loop
            )
        next_point = self._motion_path.next_point()
        if next_point:
            tpf = self.network.time_per_frame
            if look_at:
                rot_to(
                    rot_axis,
                    rotating_object,
                    next_point,
                    front_axis,
                    rot_speed,
                    tpf
                )
            reached = move_to(
                moving_object,
                next_point,
                linear_speed,
                tpf,
                move_dynamic,
                reach_threshold
            )
            if reached:
                has_more = self._motion_path.advance()
                if not has_more:
                    self._set_value(True)
                    self.done = True

    def generate_path(self, start_position, path_parent, navmesh_object, loop):
        children = sorted(path_parent.children, key=lambda o: o.name)
        if not children:
            return self._motion_path.points.clear()
        path = ActionFollowPath.MotionPath()
        path.loop = loop
        points = path.points
        self._motion_path = path
        if not navmesh_object:
            points.append(mathutils.Vector(start_position))
            if loop:
                path.loop_start = 1
            for c in children:
                points.append(c.worldPosition.copy())
        else:
            last = children[-1]
            mark_loop_position = loop
            for c in children:
                subpath = navmesh_object.findPath(
                    start_position,
                    c.worldPosition
                )
                if c is last:
                    points.extend(subpath)
                else:
                    points.extend(subpath[:-1])
                if mark_loop_position:
                    path.loop_start = len(points)
                    mark_loop_position = False
                start_position = c.worldPosition
            if loop:
                subpath = navmesh_object.findPath(
                    last.worldPosition,
                    children[0].worldPosition
                )
                points.extend(subpath[1:])


class ParameterDistance(ParameterCell):
    def __init__(self):
        ParameterCell.__init__(self)
        self.parama = None
        self.paramb = None

    def evaluate(self):
        parama = self.get_parameter_value(self.parama)
        paramb = self.get_parameter_value(self.paramb)
        if is_waiting(parama, paramb):
            return
        self._set_ready()
        self._set_value(compute_distance(parama, paramb))


class ActionReplaceMesh(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.target_game_object = None
        self.new_mesh_name = None
        self.use_display = None
        self.use_physics = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        self._set_ready()
        if not condition:
            return
        target = self.get_parameter_value(self.target_game_object)
        mesh = self.get_parameter_value(self.new_mesh_name)
        display = self.get_parameter_value(self.use_display)
        physics = self.get_parameter_value(self.use_physics)
        if is_invalid(target):
            return
        if mesh is None:
            return
        if display is None:
            return
        if physics is None:
            return
        target.replaceMesh(mesh, display, physics)
        if physics:
            target.reinstancePhysicsMesh()
        self.done = True


class RemovePhysicsConstraint(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.object = None
        self.name = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not condition:
            return
        obj = self.get_parameter_value(self.object)
        if is_invalid(obj):
            return
        name = self.get_parameter_value(self.name)
        if is_invalid(name):
            return
        self._set_ready()
        bge.constraints.removeConstraint(obj[name].getConstraintId())
        self.done = True


class AddPhysicsConstraint(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.target = None
        self.child = None
        self.name = None
        self.constraint = None
        self.use_world = None
        self.pivot = None
        self.use_limit = None
        self.axis_limits = None
        self.linked_col = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not_met(condition):
            return
        target = self.get_parameter_value(self.target)
        child = self.get_parameter_value(self.child)
        name = self.get_parameter_value(self.name)
        constraint = self.get_parameter_value(self.constraint)
        pivot = self.get_parameter_value(self.pivot)
        use_limit = self.get_parameter_value(self.use_limit)
        use_world = self.get_parameter_value(self.use_world)
        axis_limits = self.get_parameter_value(self.axis_limits)
        linked_col = self.get_parameter_value(self.linked_col)
        if is_invalid(
            target,
            child,
            name,
            constraint,
            pivot,
            use_limit,
            use_world,
            axis_limits,
            linked_col
        ):
            return
        self._set_ready()
        flag = 0 if linked_col else 128
        if use_world:
            pivot.x -= target.localPosition.x
            pivot.y -= target.localPosition.y
            pivot.z -= target.localPosition.z
        if use_limit:
            target[name] = bge.constraints.createConstraint(
                target.getPhysicsId(),
                child.getPhysicsId(),
                constraint,
                pivot_x=pivot.x,
                pivot_y=pivot.y,
                pivot_z=pivot.z,
                axis_x=axis_limits.x,
                axis_y=axis_limits.y,
                axis_z=axis_limits.z,
                flag=flag
            )
        else:
            target[name] = bge.constraints.createConstraint(
                target.getPhysicsId(),
                child.getPhysicsId(),
                constraint,
                pivot_x=pivot.x,
                pivot_y=pivot.y,
                pivot_z=pivot.z,
                flag=flag
            )
        self.done = True


class ActionAlignAxisToVector(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.game_object = None
        self.vector = None
        self.axis = None
        self.factor = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        self._set_ready()
        if not_met(condition):
            return
        game_object = self.get_parameter_value(self.game_object)
        v = self.get_parameter_value(self.vector)
        axis = self.get_parameter_value(self.axis)
        factor = self.get_parameter_value(self.factor)
        if is_invalid(game_object):
            return
        if axis is None:
            return
        if factor is None:
            return
        v = getattr(v, 'worldPosition', v).copy()
        if not self.local:
            v -= game_object.worldPosition
        if axis > 2:
            matvec = v.copy()
            matvec.negate()
            v = matvec
            axis -= 3
        game_object.alignAxisToVect(v, axis, factor)
        self.done = True


class ActionUpdateBitmapFontQuads(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.game_object = None
        self.text = None
        self.grid_size = None
        self.condition = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):  # no status waiting, test
        self.done = False
        condition = self.get_parameter_value(self.condition)
        if not condition:
            return self._set_ready()
        self._set_ready()
        game_object = self.get_parameter_value(self.game_object)
        text = eval(self.get_parameter_value(self.text))
        grid_size = self.get_parameter_value(self.grid_size)
        if is_invalid(game_object):
            return
        if text is None:
            text = ""
        if grid_size is None:
            return
        uv_size = 1.0 / grid_size
        mesh = game_object.meshes[0]
        quad_count = int(mesh.getVertexArrayLength(0) / 4)
        text_size = len(text)
        char_index = 0
        ASCII_START = 32
        for i in range(0, quad_count):
            row = 0
            column = 0
            if char_index < text_size:
                ascii_code = ord(text[char_index])
                grid_code = ascii_code - ASCII_START
                row = int(grid_code / grid_size)
                column = int(grid_code % grid_size)
                char_index += 1
            v0 = mesh.getVertex(0, i * 4)
            v1 = mesh.getVertex(0, i * 4 + 1)
            v2 = mesh.getVertex(0, i * 4 + 2)
            v3 = mesh.getVertex(0, i * 4 + 3)
            xmin = uv_size * column
            xmax = uv_size * (column + 1)
            ymax = 1.0 - (uv_size * row)
            ymin = 1.0 - (uv_size * (row + 1))
            v0.u = xmin
            v0.v = ymin
            v1.u = xmax
            v1.v = ymin
            v2.u = xmax
            v2.v = ymax
            v3.u = xmin
            v3.v = ymax
        self.done = True


class ActionSetCurrentScene(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.condition = None
        self.scene_name = None
        self.done = None
        self.OUT = LogicNetworkSubCell(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_parameter_value(self.condition)
        self._set_ready()
        if not condition:
            return
        scene_name = self.get_parameter_value(self.scene_name)
        if scene_name is None:
            return
        current_scene = logic.getCurrentScene()
        current_scene_name = current_scene.name
        if current_scene_name != scene_name:
            logic.addScene(scene_name)
            current_scene.end()
        self.done = True


class ActionStringOp(ActionCell):
    def __init__(self):
        ActionCell.__init__(self)
        self.opcode = None
        self.condition = None
        self.input_string = None
        self.input_param_a = None
        self.input_param_b = None

    def evaluate(self):
        self._set_ready()
        code = self.get_parameter_value(self.opcode)
        condition = self.get_parameter_value(self.condition)
        input_string = self.get_parameter_value(self.input_string)
        input_param_a = self.get_parameter_value(self.input_param_a)
        input_param_b = self.get_parameter_value(self.input_param_b)
        if not condition:
            return
        if input_string is None:
            return
        input_string = str(input_string)
        if code == 0:  # postfix
            self._set_value(input_string + str(input_param_a))
        elif code == 1:  # prefix
            self._set_value(str(input_param_a) + input_string)
        elif code == 2:  # infix
            self._set_value(
                str(input_param_a) +
                input_string +
                str(input_param_b)
            )
        elif code == 3:  # remove last
            self._set_value(input_string[:-1])
        elif code == 4:  # remove first
            self._set_value(input_string[1:])
        elif code == 5:  # replace a with b in string
            self._set_value(
                input_string.replace(
                    str(input_param_a),
                    str(input_param_b)
                )
            )
        elif code == 6:  # upper case
            self._set_value(input_string.upper())
        elif code == 7:  # lower case
            self._set_value(input_string.lower())
        elif code == 8:  # remove range
            self._set_value(
                input_string[:input_param_a] +
                input_string[input_param_b:]
            )
        elif code == 9:  # insert at
            self._set_value(
                input_string[:input_param_b] +
                str(input_param_a) +
                input_string[input_param_b:]
            )
        elif code == 10:  # length
            self._set_value(len(input_string))
        elif code == 11:  # substring
            self._set_value(input_string[input_param_a:input_param_b])
        elif code == 12:  # first index of
            self._set_value(input_string.find(str(input_param_a)))
        elif code == 13:  # last index of
            self._set_value(input_string.rfind(str(input_param_a)))
        pass
    pass


class ParameterMathFun(ParameterCell):

    @classmethod
    def signum(cls, a): return (a > 0) - (a < 0)

    @classmethod
    def curt(cls, a):
        if a > 0:
            return a**(1./3.)
        else:
            return -(-a)**(1./3.)

    def __init__(self):
        ParameterCell.__init__(self)
        self.a = None
        self.b = None
        self.formula = ""
        self._previous_values = [None, None]
        self._formula_globals = globals()
        self._formula_locals = {
            "exp": math.exp,
            "pow": math.pow,
            "log": math.log,
            "log10": math.log10,
            "acos": math.acos,
            "asin": math.asin,
            "atan": math.atan,
            "atan2": math.atan2,
            "cos": math.cos,
            "hypot": math.hypot,
            "sin": math.sin,
            "tan": math.tan,
            "degrees": math.degrees,
            "radians": math.radians,
            "acosh": math.acosh,
            "asinh": math.asinh,
            "atanh": math.atanh,
            "cosh": math.cosh,
            "sinh": math.sinh,
            "tanh": math.tanh,
            "pi": math.pi,
            "e": math.e,
            "ceil": math.ceil,
            "sign": ParameterMathFun.signum,
            "abs": math.fabs,
            "floor": math.floor,
            "mod": math.fmod,
            "sqrt": math.sqrt,
            "curt": ParameterMathFun.curt,
            "str": str,
            "int": int,
            "float": float
        }

    def evaluate(self):
        self._set_ready()
        a = self.get_parameter_value(self.a)
        b = self.get_parameter_value(self.b)
        olds = self._previous_values
        do_update = (
            (a != olds[0]) or
            (b != olds[1])
        )
        if do_update:
            formula_locals = self._formula_locals
            formula_locals["a"] = a
            formula_locals["b"] = b
            out = eval(self.formula, self._formula_globals, formula_locals)
            olds[0] = a
            olds[1] = b
            self._set_value(out)
