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


###
#test /v0.2/VerifyFaceImage
###
print('** testing /v0.2/VerifyFaceImage **')

url = "{}{}".format(server, '/v0.2/VerifyFaceImage')
headers = {'Api-Key': args.api_key}
qdata = base64_data['o-AUDREY-1']
cdata = [base64_data[v] for v in ['o-AUDREY-1', 'o-AUDREY-2', 'o-AUDREY-3']]
data = {    
    "queryData":qdata,
    "candidateDataArray":cdata     
}
response = requests.post(url.format(server), headers = headers, data=json.dumps(data), proxies=proxies, verify=False)
print('response:')
print(response.text)
print('')
