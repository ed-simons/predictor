
import json

# These code snippets use an open-source library. http://unirest.io/python
# response = unirest.get("https://api-football-v1.p.mashape.com/fixtures/league/2",
#   headers={
#     "X-Mashape-Key": "373pmkisjSmshA8AnqLLWdONNgDPp1aejcgjsnoZZjd4yJPpHX",
#     "Accept": "application/json"
#   }
# )
# 
# Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
# Connection: keep-alive
# Content-Type: application/json
# Date: Thu, 16 Aug 2018 22:35:11 GMT
# Expires: Thu, 19 Nov 1981 08:52:00 GMT
# Pragma: no-cache
# Server: Mashape/5.0.6pwd

# Transfer-Encoding: chunked

class Season:
    def __init__(self):
        pass

    def league(self):
        """
        /fixtures/league/{league_id}
        """
        return json.load(open('league.json'))