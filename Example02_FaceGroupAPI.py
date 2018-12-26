import requests
import json
import base64
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('api_key', help='the key for accessing APIs')
parser.add_argument('--server_url', type=str,
    help='The server url (port included)', default='https://iot.cht.com.tw/api/face')
parser.add_argument('--http_proxy', type=str,
    help='http proxy', default=None)
parser.add_argument('--https_proxy', type=str,
    help='https proxy', default=None)

args = parser.parse_args(sys.argv[1:])
server = args.server_url
proxies = {
  "http": args.http_proxy,
  "https": args.https_proxy,
}


# read all images and get the corresponding base64-encoded data
img_names = ['o-AUDREY-1', 'o-AUDREY-2', 'o-AUDREY-3', 'friends']
files = {name: open("images/{}.jpg".format(name), "rb") for name in img_names}
base64_data = {name: base64.b64encode(files[name].read()).decode('utf-8') for name in img_names}
headers = {'Api-Key': args.api_key}

'''
1) POST /v0.2/FaceGroup
create a FaceGroup
'''

create_group_url = '{}/v0.2/FaceGroup'
data_dicts = {"groupName": "requests-test-group"}
data = json.dumps(data_dicts)
response = requests.post(create_group_url.format(server), headers = headers, data=data, proxies=proxies)
rdata = json.loads(response.text)
print("===== 1) POST /v0.2/FaceGroup =====")
print(rdata)
print()
groupId = rdata['groupId']  #remember this for testing later

'''
2) GET /v0.2/FaceGroup
get all FaceGroups
'''
get_facegroups_url = '{}/v0.2/FaceGroup'                                          
response = requests.get(get_facegroups_url.format(server), headers = headers, proxies=proxies)
rdata = json.loads(response.text)
print("===== 2) GET /v0.2/FaceGroup =====")
print(rdata)
print()

'''
3) POST /v0.2/FaceGroup/{groupId}
add a face to a FaceGroup
'''

add_face_url = '{}/v0.2/FaceGroup/{}'
data = {
    "imgData":base64_data['o-AUDREY-1'],
    "roiRect": {
        "left": 3,
        "top": 3,
        "right": 999,
        "bottom": 999
    },
    "faceMetadata": "o-AUDREY-1"
}
data = json.dumps(data)
response = requests.post(add_face_url.format(server, groupId), headers = headers, data=data, proxies=proxies)
rdata = json.loads(response.text)                
print("===== 3) POST /v0.2/FaceGroup/{groupId} =====")
print(rdata)
print()
groupedFaceId = rdata['groupedFaceId']

'''
4) GET /v0.2/FaceGroup/{groupId}
get information a bout a FaceGroup
'''
get_facegroup_url = '{}/v0.2/FaceGroup/{}'                                            
response = requests.get(get_facegroup_url.format(server, groupId), headers = headers, proxies=proxies)
rdata = json.loads(response.text)
print("===== 4) GET /v0.2/FaceGroup/{groupId} =====")
print(rdata)
print()

'''
5) POST /v0.2/FaceGroup/{groupId}/Match
match face to FaceGroup
'''
match_face_url = '{}/v0.2/FaceGroup/{}/Match'
data = {
    "queryData":base64_data['o-AUDREY-2'],    
    "roiRect": {
        "left": 3,
        "top": 3,
        "right": 999,
        "bottom": 999
    },
    "topK": 3,
    "allFaces": False
}
data = json.dumps(data)
response = requests.post(match_face_url.format(server, groupId), headers = headers, data=data, proxies=proxies)
rdata = json.loads(response.text)
print("===== 5) POST /v0.2/FaceGroup/{groupId}/Match =====")
print("TEST-1")
print(rdata)
print()

data = {
    "queryData":base64_data['friends'],
    "roiRect": {
        "left": 50,
        "top": 50,
        "right": 300,
        "bottom": 300
    },
    "topK": 1,
    "allFaces": True
}
data = json.dumps(data)
response = requests.post(match_face_url.format(server, groupId), headers = headers, data=data, proxies=proxies)
rdata = json.loads(response.text)
print("TEST-2")
print(rdata)
print()

'''
6) DELETE /v0.2/FaceGroup/{groupId}/Face/{groupedFaceId}
delete a face
'''
delete_face_url = '{}/v0.2/FaceGroup/{}/Face/{}'
response = requests.delete(delete_face_url.format(server, groupId, groupedFaceId), headers = headers, proxies=proxies)
rdata = json.loads(response.text)                
print("===== 6) DELETE /v0.2/FaceGroup/{groupId}/Face/{groupedFaceId} =====")
print(rdata)
print()

'''
7) DELETE /v0.2/FaceGroup/{groupId}
delete a facegroup
'''
delete_group_url = '{}/v0.2/FaceGroup/{}'
response = requests.delete(delete_group_url.format(server, groupId), headers=headers, data='', proxies=proxies)
rdata = json.loads(response.text)
print("===== 7) DELETE /v0.2/FaceGroup/{groupId} =====")
print(rdata)
print()