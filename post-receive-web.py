#!/usr/bin/python
import sys
import subprocess
import json
import requests

def get_commits(old, new):
    p = subprocess.Popen(['git', 'log', '--pretty=format:"%H %cn %ce %s"', '--reverse',
                          '{}..{}'.format(old, new)], stdout=subprocess.PIPE)
    return p.stdout.read().strip('"').split()

if __name__ == '__main__':
    lines = sys.stdin.readlines()
    for line in lines:
        old, new, ref = line.strip().split(' ')
        keys = ['hashref', 'name', 'email', 'message']
        values = get_commits(old, new)
        commit = dict(zip(keys, values))
        commit['branch'] = ref.split('/')[-1]
        url = ''
        headers = {'content-type': 'application/json'}
        res = requests.post(url, data=json.dumps(commit), headers=headers)
