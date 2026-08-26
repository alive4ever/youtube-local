from youtube.util import INNERTUBE_CLIENTS, fetch_url
import json
import time

def get_po_token(client, identifier=''):
    if not identifier:
        return None
    print(f'Generating po_token for {identifier}')
    start_time = time.perf_counter()
    client_context = INNERTUBE_CLIENTS[client]['INNERTUBE_CONTEXT']
    try:
        http_resp = fetch_url('http://localhost:4416/ping')
        ping_result = json.loads(http_resp.decode())
        print(f"Using bgutil server {ping_result['version']}")
        payload = {
                'content_binding': identifier,
                'bypass_cache': True,
                'innertube_context': client_context,
                }
        result = fetch_url('http://localhost:4416/get_pot', report_text=f'Getting po_token for {identifier} via bgutil server', headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        result_json = json.loads(result.decode())
        po_token = result_json['poToken']
        end_time = time.perf_counter()
        print(f'Got po_token for {identifier} via bgutil server in { end_time - start_time:.2f} s')
        return po_token
    except Exception as err:
        print('Unable to generate po_token. Make sure that bgutil server is running on localhost:4416. Refer to https://github.com/Brainicism/bgutil-ytdlp-pot-provider for more details.')
        return None
