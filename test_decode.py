import base64
import re

# A sample CBMi string from a Google news link
url = "https://news.google.com/rss/articles/CBMiigFBVV95cUxOVDMxeU5wLWV6cXdTcHk5T0k2d0VDbnRoT3BSNUFULW9DYmh1VTdSUy1aU3k5cksta1dXTV9DU0Joa2Rib19WLWV4alc5OW5DYkU0d2lrcUVKR0I0NGpkOVRvSVkyR1hXU2JybG1DUmc3emt3ajJmcDB2WlFtcUpBd0V4Q3NJU1lma2c?oc=5"
cbmi = url.split("articles/")[1].split("?")[0]

try:
    # Padding if necessary
    padding = 4 - (len(cbmi) % 4)
    if padding != 4:
        cbmi += "=" * padding
    
    decoded = base64.urlsafe_b64decode(cbmi)
    # The decoded string is a protobuf. We can just extract any http URL using regex
    urls = re.findall(b'https?://[^\x00-\x1F\x7F-\x9F]+', decoded)
    print("Found URLs in Base64:", urls)
except Exception as e:
    print("Error:", e)

