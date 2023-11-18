#!/usr/bin/env python3

import json

from sseclient import SSEClient as EventSource

url = 'https://stream.wikimedia.org/v2/stream/recentchange'
for event in EventSource(url):
    if event.event == 'message':
        try:
            change = json.loads(event.data)
        except ValueError:
            pass
        else:
            # print("========")
            # if change['user'] == 'InternetArchiveBot':
            print('{user} edited {title_url}'.format(**change))
            # for key, value in change.items():
            #     print(f' {key=}, {value=}')
