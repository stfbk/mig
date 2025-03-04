import requests
import time
import json
import argparse
from pprint import pprint

def read_suite(path):
    with open(path) as f:
        return json.load(f)
    
def read_file(path):
    with open(path) as f:
        return f.read()

def prepare_test(testPath, sessionsPath):
    test = read_suite(testPath)
    sessions = {}

    # collect session names
    names = set()
    for t in test['tests']:
        for s in t['test']['sessions']:
            names.add(s)

    # retrieve session
    for s in names:
        sessions[s] = read_file('{}/{}'.format(sessionsPath, s))

    return {
        'test': json.dumps(test),
        'sessions': sessions
    }


def send_request(url, test, onlyValidate):
    req = requests.post("{}/execute".format(url) + ('onlyValidate' if onlyValidate else ''), json=test)
    
    # check status code
    if req.status_code != 200:
        print("Request failed")
        return False    

    # check error
    res = req.json()
    if not res['success']:
        print("Error in parsing: " + res['error'])
        return False
        
    return True

def poll_result(url):
    while True:
        req = requests.post(url + "/result")

        # check status code
        if req.status_code != 200:
            print("Request failed")
            return False
        
        # check result
        res = req.json()
        if res['finished']:
            return res['tests']

        # wait
        time.sleep(3)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help="The test suite")
    parser.add_argument('sessions', help="The folder containing the sessions")
    parser.add_argument('--only-validate', action='store_true', default=False, help='Only validate the test suite')
    parser.add_argument('--url', help='The url of MIG-T', default='http://localhost:3000')

    args = parser.parse_args()

    data = prepare_test(args.path, args.sessions)
    if not send_request(args.url, data, args.only_validate):
        print("Error in sending test suite to MIG-T")
        return
    
    if not args.only_validate:
        result = poll_result(args.url)
        if result is False:
            print("Error in retrieving the result")
            return
        pprint(result)

if __name__ == '__main__':
    main()
