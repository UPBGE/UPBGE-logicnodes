from .globaldb import GlobalDB
from .serializers import StringSerializer
from .serializers import FloatSerializer
from .serializers import IntegerSerializer
from .serializers import ListSerializer
from .serializers import VectorSerializer
from mathutils import Vector


GlobalDB.serializers[str(type(""))] = StringSerializer()
GlobalDB.serializers[str(type(1.0))] = FloatSerializer()
GlobalDB.serializers[str(type(10))] = IntegerSerializer()
GlobalDB.serializers[str(type([]))] = ListSerializer()
GlobalDB.serializers[str(type((0, 0, 0)))] = ListSerializer()
GlobalDB.serializers[str(type(Vector()))] = (
    VectorSerializer()
)
