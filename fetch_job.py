
import requests
a = requests.get("https://remotive.com/api/remote-jobs")
if a.ok == True:
    a = a.json()
print(a)
a = requests.get("https://remotive.com/api/remote-jobs")
if a.ok == True:
    a = a.json()
print(a)
