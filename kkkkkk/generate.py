import copy
import json

endpoint =  {
    "name": "/test",
    "description": "",
    "method": "GET",
    "endpoint": "/testf",
    "data_source": {
      "cluster_id": 3778994
    },
    "params": [
      {
        "name": "id",
        "type": "integer",
        "required": 1,
        "default": "",
        "description": ""
      }
    ],
    "settings": {
      "timeout": 5000,
      "row_limit": 50
    },
    "sql_file": "sql/GET-testf.sql",
    "type": "sql_endpoint",
    "return_type": "json"
  }

result = []
for i in range(1000):
    t = copy.deepcopy(endpoint)
    t["name"] = f"/test{i}"
    t["endpoint"] = f"/test{i}"
    result.append(t)

print(json.dumps(result, indent=" "))

