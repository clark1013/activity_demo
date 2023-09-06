import copy
import json

endpoint =   {
    "name": "/test",
    "description": "",
    "method": "GET",
    "endpoint": "/test",
    "data_source": {
      "cluster_id": 10422944594530052187
    },
    "params": [],
    "settings": {
      "timeout": 30000,
      "row_limit": 1000,
      "cache_enabled": 0,
      "cache_ttl": 0,
      "enable_pagination": 0
    },
    "tag": "Default",
    "batch_operation": 0,
    "sql_file": "sql/GET-test.sql",
    "type": "sql_endpoint",
    "return_type": "json"
  }


result = []
for i in range(200):
    t = copy.deepcopy(endpoint)
    t["name"] = f"/test{i}"
    t["endpoint"] = f"/test{i}"
    result.append(t)

print(json.dumps(result, indent=" "))
