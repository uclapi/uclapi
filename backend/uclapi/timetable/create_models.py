file_string = open("Full_DDL.sql").read()
# file_string = open("test.txt").read()


a = """
    class Meta:
        managed = False
        db_table = '####'
        _DATABASE = 'roombookings'
"""

def find_all(word, string):
    index_starts = []
    stripped_length = 0
    while string.find(word) != -1:
        index_starts.append(stripped_length + string.find(word))
        string = string[string.find(word) + 12:]
        stripped_length = (index_starts[-1] + 12)
    return index_starts


data = {}


def strip_prefix(string, prefix):
    if not string:
        return ""
    while string[0] == prefix:
        string = string[1:]
    return string

import json

for index in find_all("CREATE TABLE", file_string):
    start = index
    while file_string[index] != "(":
        index += 1
    table_name = file_string[start + 12: index]

    counter = 1
    start = index
    index += 1
    while counter and index < len(file_string):
        if file_string[index] == "(":
            counter += 1
        elif file_string[index] == ")":
            counter -= 1
        index += 1
    table_fields = file_string[start + 1: index - 1].split("\n")
    table_fields = list(map(lambda k: strip_prefix(strip_prefix(k, ","), " "), table_fields))
    data[strip_prefix(table_name.replace("\n", ""), " ")] = table_fields

def find_prefix(right):
    name_map = {
        "text": "VARCHAR2",
        "integer": "NUMBER",
        "date": "DATE",
        "char": "CHAR",
        "float": "FLOAT"
    }
    for name in name_map:
        if right.startswith(name_map[name]):
            return name_map[name]


def get_field_type(right):
    if find_prefix(right) == "NUMBER":
        return "BigIntegerField()"
    if find_prefix(right) == "DATE":
        return "DateField()"
    if find_prefix(right) == "CHAR":
        return "CharField(max_length=1)"
    if find_prefix(right) == "VARCHAR2":
        i = 0
        while right[i] != "(":
            i += 1
        max_char = int(right[i + 1: -1].split(" ")[0])
        return "TextField(max_length={})".format(max_char)
    if find_prefix(right) == "FLOAT":
        return "FloatField()"

def map_field(right):
    return get_field_type(right)

def format_table_name(name):
    return name[0] + name[1:].lower()

for table_name, fields in data.items():
    ret_str = ""
    ret_str += "class {}(models.Model):\n".format(format_table_name(table_name[11:-1]))
    for field in fields:
        if not field:
            continue
        field_name, *rest = field.split(" ")
        rest = ' '.join(rest)
        right_hand = map_field(rest)
        ret_str += "    {} = models.{}\n".format(field_name.lower(), right_hand)
    ret_str += a.replace("####", table_name[:-1])
    # print(ret_str)
