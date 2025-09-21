import requests
import json

url = "https://stream.wikimedia.org/v2/stream/recentchange"

headers = {
    'User-Agent': 'LinkedDataSandbox/0.1 (https://github.com/wallberg/linked-data-sandbox)'
}

with requests.get(url, stream=True, headers=headers) as resp:
    resp.raise_for_status()
    for line in resp.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data: '):
                data = decoded_line[6:]
                event = json.loads(data)
                # print(event)
                print("========")
                # if change['user'] == 'InternetArchiveBot':
                # print('{user} edited {title_url}'.format(**event))
                for key, value in event.items():
                    if key == 'meta':
                        for mkey, mvalue in value.items():
                            print(f'  meta.{mkey=}, {mvalue=}')
                    else:
                        print(f' {key=}, {value=}')
