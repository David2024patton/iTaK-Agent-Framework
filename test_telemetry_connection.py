"""Simple telemetry connection test.

This script directly tests the OTLP connection to the VPS
without needing to run a full agent.
"""

import requests
import random
import time

# Generate unique trace ID
tid = ''.join([hex(random.randint(0,15))[2:] for _ in range(32)])
sid = ''.join([hex(random.randint(0,15))[2:] for _ in range(16)])

data = {
    'resourceSpans': [{
        'resource': {'attributes': [{'key': 'service.name', 'value': {'stringValue': 'itak-telemetry'}}]},
        'scopeSpans': [{
            'spans': [{
                'traceId': tid,
                'spanId': sid,
                'name': 'iTaK Framework Test',
                'kind': 1,
                'startTimeUnixNano': str(int(time.time()*1e9)),
                'endTimeUnixNano': str(int((time.time()+5)*1e9)),
                'attributes': [
                    {'key': 'test.type', 'value': {'stringValue': 'iTaK-Framework-Connection-Test'}},
                    {'key': 'test.timestamp', 'value': {'stringValue': time.strftime('%Y-%m-%d %H:%M:%S')}},
                    {'key': 'framework.version', 'value': {'stringValue': '0.1.0'}}
                ]
            }]
        }]
    }]
}

print("=" * 70)
print("iTaK TELEMETRY CONNECTION TEST")
print("=" * 70)
print(f"Target: http://145.79.2.67:4318/v1/traces")
print(f"Trace ID: {tid}")
print("=" * 70)

try:
    r = requests.post('http://145.79.2.67:4318/v1/traces', json=data, timeout=10)
    print(f"\n✅ SUCCESS!")
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
    
    if r.status_code == 200:
        print("\n" + "=" * 70)
        print("TELEMETRY IS WORKING!")
        print("=" * 70)
        print(f"\nView in Grafana:")
        print(f"1. Go to: http://145.79.2.67:3456/")
        print(f"2. Navigate to: Explore -> Tempo")
        print(f"3. Paste Trace ID: {tid}")
        print(f"4. Or search for: service.name = 'itak-telemetry'")
        print("=" * 70)
    else:
        print(f"\n⚠️  Unexpected status code: {r.status_code}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nTroubleshooting:")
    print("1. Check VPS is accessible: ping 145.79.2.67")
    print("2. Verify collector is running: ssh root@145.79.2.67 'docker ps'")
    print("3. Check firewall allows port 4318")
