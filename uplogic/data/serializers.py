from uplogic.data import GlobalDB
from mathutils import Vector


class StringSerializer(GlobalDB.Serializer):

    def write(self, value, line_writer):
        line_writer.write(value)

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else data


class FloatSerializer(GlobalDB.Serializer):

    def write(self, value, line_writer): line_writer.write(str(value))

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else float(data)


class IntegerSerializer(GlobalDB.Serializer):

    def write(self, value, line_writer): line_writer.write(str(value))

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else int(data)


class ListSerializer(GlobalDB.Serializer):

    def write(self, value, line_writer):
        line_writer.write(str(len(value)))
        for e in value:
            tp = str(type(e))
            serializer = GlobalDB.serializers.get(tp)
            if serializer:
                line_writer.write(tp)
                serializer.write(e, line_writer)

    def read(self, line_reader):
        data = []
        count = int(line_reader.read())
        for i in range(0, count):
            tp = line_reader.read()
            serializer = GlobalDB.serializers.get(tp)
            value = serializer.read(line_reader)
            data.append(value)
        return data


class VectorSerializer(GlobalDB.Serializer):
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
        return Vector(components)
