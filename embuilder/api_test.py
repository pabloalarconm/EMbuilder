import requests
from os import listdir, getcwd
from os.path import isfile, join
import sys
from pyperseo.functions import get_files
import json

mypath = getcwd() + "/embuilder/data/"

def post_call(route,body,mypath,filename,format):
    headers={"accept": "application/json", "Content-Type": "application/json"}
    try:
        response = requests.post(url = "http://127.0.0.1:8000/"+ route, headers = headers,json = body)
        response.encoding = response.apparent_encoding
        try:
            f = open(mypath + filename + "." + format, "x")
            f.write(response.text)
        except FileExistsError:
            f = open(mypath + filename + "." + format, "w")
            f.write(response.text)
        finally:
            f.close()
    except requests.ConnectionError as c:
        print("Error Connecting:",c)
    except requests.RequestException as e:
        print("Something Else: ",e)

files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
all_files = [ff for ff in files if ff.endswith(str(".json"))]
if len(all_files) == 0: print("No resources are present at {} path with .{} format.".format(mypath,"json"))

for filex in all_files:
    filename = filex.split(".json")[0]
    with open(mypath + filex) as json_file:
        json_content = json.load(json_file)

    if sys.argv[1] == "yarrrml":
        post_call(route = sys.argv[1], body=json_content, mypath=mypath,
         filename=filename, format="yaml")
    elif sys.argv[1] == "shex":
        post_call(route = sys.argv[1], body=json_content, mypath=mypath,
         filename=filename, format="shex")
    elif sys.argv[1] == "obda":
        post_call(route = sys.argv[1], body=json_content, mypath=mypath,
         filename=filename, format="obda")
    elif sys.argv[1] == "sparql":
        post_call(route = sys.argv[1], body=json_content, mypath=mypath,
         filename=filename, format="ttl")
    else:
        sys.exit('Wrong argument passed, you need to provide an argument as "yarrrml" or "shex" to define to method')
