# Mongodb数据json转化错误nalytics(TypeError: ObjectId('') is not JSON serializable)

------
https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable/16586274

```python

import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# 使用 （analytics是要处理的数据列表)
JSONEncoder().encode(analytics)

# It's also possible to use it in the following way.
json.encode(analytics, cls=JSONEncoder)

```
