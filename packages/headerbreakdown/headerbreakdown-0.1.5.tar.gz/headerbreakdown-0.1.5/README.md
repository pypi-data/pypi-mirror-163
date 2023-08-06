# HeaderBreakdown
converts a collection of HTTP headers into a dictionary structure for automated analysis; creates parsed and analyzed objects; accepts strings, lists, or dictionaries of header values

### Installation
```
pip install headerbreakdown
or
pip3 install headerbreakdown
or
python3 -m pip install headerbreakdown
```

### Example Output
```
{
    "_direction": "response",
    "_httpversion": "HTTP/1.1",
    "_responsecode": "302",
    "_responsephrase": "Found",
    "location": {
        "key": "Location",
        "value": [
            "https://www.google.com/?gws_rd=ssl"
        ]
    },
    "cachecontrol": {
        "key": "Cache-Control",
        "value": [
            "private"
        ]
    },
    "contenttype": {
        "key": "Content-Type",
        "value": [
            "text/html; charset=UTF-8"
        ],
        "subvalues": [
            "charset=UTF-8",
            "text/html"
        ],
        "microvalues": [
            {
                "microkey": "charset",
                "microvalue": "UTF-8"
            }
        ]
    },
    "date": {
    ...
```

### Example Usage
```
from headerbreakdown import HeaderBreakdown as hb
import json
# header with multiple Host and User-Agent values
someheader = "GET /?gws_rd=ssl HTTP/1.1\r\nHost: www.google.com\r\nHost: www.bing.com\r\nHost: www.yahoo.com\r\nConnection: keep-alive\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/99.0\r\nCookie: 1P_JAR=2021-03-13-04"
# create the object
h = hb(someheader)
# print only the parsed version of the header
print(h.parsed)
# print the analyzed version with subvalues, minivalues, and microkeys and microvalues
print(h.analyzed)
# print as json
print(json.dumps(h.analyzed, indent=4))
# etc
```

### Available Attributes

| attribute | type | description |
| -- | -- | -- |
| **parsed** | dict | main structure of parsed header information |
| **analyzed** | dict | main structure of parsed and analyzed header information with subvalues, minivalues, and microkeys and microvalues |
| \_direction | string | request or response |
| \_method | list | request verb;  length of one, unless an illegal header is present |
| \_host | list | request host;  length of one, unless an illegal header is present |
| \_path | list | request path;  length of one, unless an illegal header is present |
| \_httpversion | string | HTTP version being used |
| \_responsecode | string | response code number only, as a string |
| \_responsephrase | string | response phrase only |
| \_keys | list | normalized keys in the analyzed object (same as obj.keys() but omits the sub/mini/micro items) |
- Note that `method` and `path` are also presented as normalized keys alongside other request header keys (`host` will also be present)

### Releases and Updates
- 2022-08-11
	- minor edits and comments for readability
	- made `hb_unittest.py` and commented out `unit_tests()` in headerbreakdown.py
- 2022-08-10
	- converted method and path to lists to accomodate illegal headers such as multiple methods and paths
	- fixed attributes to only set if not already present
		- prevents "requestrequest" or "responseresponse" for `_direction` if illegal headers are set
- 2022-03-25
	- complete overhaul
	- accepts strings, lists, and dictionaries as input
	- simplified output dict structure
	- standardized keys
	- removed json outputs
	- TO DO - convert metadata string attributes to lists (smuggling)
- 2021-04-06
	- added nested_direction_json/output, ex. {"headers":{"request":{...}}}
	- so direction gets captured and headers do not get overwritten if processing a capture with both sides of the communication
	- the nested_direction_* attributes will be type None when processing a single, direction-ambiguous header (ex. "Set-Cookie: k1=v1;k2=v2")
- 2021-04-01
	- minor fix for HTTP/ detection
- 2021-03-23
	- minor edits, added summary and nested_output/nested_json attributes, ex. {"headers":{...}}
- 2021-03-13
	- first release
