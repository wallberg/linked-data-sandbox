import requests
import json

from kafka import KafkaProducer

url = "https://stream.wikimedia.org/v2/stream/recentchange"

headers = {
    'User-Agent': 'LinkedDataSandbox/0.1 (https://github.com/wallberg/linked-data-sandbox)'
}

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'wikidata-activitystream'

with requests.get(url, stream=True, headers=headers) as resp:
    resp.raise_for_status()
    for line in resp.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('data: '):
                data = decoded_line[6:]
                event = json.loads(data)
                # print(event)
                # if change['user'] == 'InternetArchiveBot':
                # print('{user} edited {title_url}'.format(**event))
                if event['wiki'] == 'wikidatawiki':
                    print("========")
                    for key, value in event.items():
                        if key == 'meta':
                            for mkey, mvalue in value.items():
                                print(f'  meta.{mkey=}, {mvalue=}')
                        else:
                            print(f' {key=}, {value=}')

                producer.send(topic, event)
                producer.flush()
