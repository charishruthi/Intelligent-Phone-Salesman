'''
ner_client.py
Author: Anantharaman Narayana Iyer
Date: 18 Dec 2014
Client class that is a proxy to the NER in the server
'''
import requests
import json
import os

service_url = "http://jnresearch.com/"
upload_url = service_url + "upload_file"
prod_bigrams_url = service_url + "get_brand_product_bigrams"

def upload_file(fn, pw, group):
    comps = os.path.split(fn) # get the components of file name
    headers = {'content-type': 'application/json'}
    r = requests.post(upload_url, data = json.dumps({"data": open(fn, 'rb').read(), "password": pw, "group": group, "filename": comps[1]}), headers = headers) #
    if r.text.isdigit():
        return int(r.text)
    return None
    

class RerClient(object):
    def __init__(self, password, group):
        self.group = group
        self.password = password
        self.headers = {'content-type': 'application/json'}
        return

    def upload(self, fn):
        ret = upload_file(fn, self.password, self.group)
        return ret

    def get_brand_product_bigrams_dict(self):
        r = requests.post(prod_bigrams_url, data = json.dumps({"password": self.password, "group": self.group}), headers = self.headers) #
        return json.loads(r.text)


if __name__ == "__main__":
    # run the code below from different systems - replace the pw and groups - use g100, g101, g102, g103
    ner = NerClient("1PI11CS196", "g104")
    ret = ner.get_brand_product_bigrams_dict()
    #fn = r"my_file_name_for_uploading"
    #ret = ner.upload(fn) # web service for upload
    print ret
