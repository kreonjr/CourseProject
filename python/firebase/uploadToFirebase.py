"""
uploadToFirebase.py

Reads the final output of the tag mining algorithms and uploads it to 
the firebase project's database, to update the frontend dashboard

Created on November 2nd, 2021 4:44pm

@author: creonc2
"""
import requests
import json

url = "https://us-central1-topic-thunder-a7103.cloudfunctions.net/updateDatabase"

f = open('../text_mining/firebase-output.json',)
data = json.load(f)
payload = json.dumps(data)

headers = {
  'x-api-key': '8efa1e88-d80c-45ee-850e-9d78bc81f9bb',
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)

if(response.status_code == 200):
    print(response.text)
else:
    print("Something went wrong with the update: ", response.text)