from embuilder.builder import EMB
import json

with open("data/data_test.json") as json_file:
    data = json.load(json_file)

yarrrml = EMB(data["config"], data["prefixes"],data["triplets"])

test_yarrrml = yarrrml.transform_ShEx()
print(test_yarrrml)
test_obda = yarrrml.transform_OBDA()
print(test_obda)
test_sparql = yarrrml.transform_SPARQL()
print(test_sparql)
test_shex = yarrrml.transform_YARRRML()
print(test_shex)