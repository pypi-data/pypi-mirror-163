# PyPI package `aioairq`

Python library for asynchronous data access to local air-Q devices.

## Retrieve data from air-Q

```python
import asyncio
from aioairq import AirQ

address = "123ab_air-q.local"
password = "airqsetup"
airq = AirQ(address, password)

loop = asyncio.get_event_loop()

data = loop.run_until_complete(airq.data)
average = loop.run_until_complete(airq.average)
config = loop.run_until_complete(airq.config)
```
