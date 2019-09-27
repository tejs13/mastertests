import requests
import time

data = {"field0": "asfsaf",
        "field1": "models.CharField(max_length=200)",
        "field2": "models.CharField(max_length=200)",
        "field3": "models.CharField(max_length=200)",
        "field4": "models.CharField(max_length=200)",
        "field5": "models.CharField(max_length=200)",
        "field6": "models.CharField(max_length=200)",
        "field7": "models.CharField(max_length=200)",
        "field8": "models.CharField(max_length=200)",
        "field9": "models.CharField(max_length=200)",
        "field10": "models.CharField(max_length=200)",
        "field11": "models.CharField(max_length=200",
        "field12": "models.CharField(max_length=200",
        "field13": "models.CharField(max_length=200)",
        "field14": "models.CharField(max_length=200)",
        "field15": "models.CharField(max_length=200)",
        "field16": "models.CharField(max_length=200)",
        "field17": "models.CharField(max_length=200)",
        "field18": "models.CharField(max_length=200)",
        "field19": "models.CharField(max_length=200)",
        "field20": "models.CharField(max_length=200)",
        "field21": "models.CharField(max_length=200)",
        "field22": "models.CharField(max_length=200)",
        "field23": "models.CharField(max_length=200)",
        "field24": "models.CharField(max_length=200)",
        "field25": "models.CharField(max_length=200)",
        "field26": "models.CharField(max_length=200)",
        "field27": "models.CharField(max_length=200)",
        "field28": "models.CharField(max_length=200)",
        "field29": "models.CharField(max_length=200)",
        "field30": "models.CharField(max_length=200)",
        "field31": "models.CharField(max_length=200)",
        "field32": "models.CharField(max_length=200)",
        "field33": "models.CharField(max_length=200)",
        "field34": "models.CharField(max_length=200)",
        "field35": "models.CharField(max_length=200)",
        "field36": "models.CharField(max_length=200)",
        "field37": "models.CharField(max_length=200)",
        "field38": "models.CharField(max_length=200)",
        "field39": "models.CharField(max_length=200)",
        "field40": "models.CharField(max_length=200)",
        "field41": "models.CharField(max_length=200)",
        "field42": "models.CharField(max_length=200)",
        "field43": "models.CharField(max_length=200)",
        "field44": "models.CharField(max_length=200)",
        "field45": "models.CharField(max_length=200)",
        "field46": "models.CharField(max_length=200)",
        "field47": "models.CharField(max_length=200)",
        "field48": "models.CharField(max_length=200)",
        "field49": "models.CharField(max_length=200)",
        }
data2 = {"name": "new",
         "code": "new"
         }

headers = {'content-type': 'application/json',
           'Authorization': 'Token 73e782001ab3e2846f00141e4ba910fe38704a65'
           }
start = time.time()
for i in range(100):
    r = requests.post('http://127.0.0.1:8000/master/api.exe', json=data, headers=headers)
    print(i)

print("execution time", time.time() - start)
