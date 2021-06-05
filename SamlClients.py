import datetime
import getopt
import json
import os
import re
import sys

import requests
import urllib3

base_url = os.environ.get('PF_ADMIN_URL', 'https://localhost:9999')
pf_admin_user = os.environ.get('PF_ADMIN_USER', 'Administrator')
pf_admin_pswd = os.environ.get('PF_ADMIN_PSWD', '1Password')

headers = {
    'X-XSRF-Header': 'PingFederate',
    'Content-Type': 'application/json'
}

samlclients_path = os.path.dirname(os.path.realpath(__file__)) + "/PFConnections"
now = datetime.datetime.today()
nTime = now.strftime("%Y%m%d%H%M%S")

# PingFederate BaseURL's
metadataurl = base_url + "/pf-admin-api/v1/metadataUrls"
idpurl = base_url + "/pf-admin-api/v1/sp/idpConnections"
spurl = base_url + "/pf-admin-api/v1/idp/spConnections"

# Export URL
metadataurlpath = samlclients_path + '/SAML/MetadataURL' + nTime
idpclientpath = samlclients_path + '/SP/IDPSAMLClients' + nTime
spclientpath = samlclients_path + '/IDP/SPSAMLClients' + nTime

# Import URL
import_metadataurl_path = samlclients_path + '/SAML'
import_idpsamlclients_path = samlclients_path + '/SP'
import_spsamlclients_path = samlclients_path + '/IDP'

def json_request(request,url,payload):
    req_resp=requests.request(request,url,headers=headers,data=payload,auth=(pf_admin_user, pf_admin_pswd), verify=False)
    return req_resp.json(),req_resp.status_code

# get SAML connections data by making get call to admin api
def export_response(export_path,import_url):
        export_payload = {}
        os.makedirs(export_path)
        function = json_request("GET",import_url,export_payload)
        filedata=function[0]
        for n in range(len(filedata['items'])):
            body = filedata['items'][n]
            name = body['name']
            updatedName = re.sub('[^A-Za-z0-9 ]+', '-', name)
            storing_metadataurl = export_path + '/pf-' + updatedName + '.json'
            with open(storing_metadataurl, 'w+') as write_file:
                json.dump(body, write_file, sort_keys=True, indent=4)
            print('pf-' + name + ".json" + " " + "is created"+", Status Code:: "+str(function[1]))
        return function[1]


def import_response(import_path,import_url):
    try:
        file_path = max([os.path.join(import_path, d)
                    for d in os.listdir(import_path)],
                    key=os.path.getmtime)
        print("\nLatestfileDataLocation :: ", file_path)
        files = os.listdir(file_path)
        for ind in range(len(files)):
            filename = file_path + '/' + files[ind]
            print('' + filename)
            with open(filename, 'r') as input:
                import_payload = json.load(input)
                res=json.dumps(import_payload)
                respone=json_request("POST",import_url,res)
                print(respone[1])
            return (respone[1])
    except:
        return("FilePath Not found, export the connections and then try import")
        print("FilePath Not found, export the connections and then try import")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'eix', ['export', 'import', 'exportimport', ])
    except getopt.GetoptError:
        print('Invalid input, exiting the script')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-e', '--export'):
            export_response(export_path=metadataurlpath, import_url=metadataurl)
            export_response(export_path=idpclientpath, import_url=idpurl)
            export_response(export_path=spclientpath, import_url=spurl)
        elif opt in ("-i", "--import"):
            import_response(import_path=import_metadataurl_path,import_url=metadataurl)
            import_response(import_path=import_idpsamlclients_path, import_url=idpurl)
            import_response(import_path=import_spsamlclients_path, import_url=spurl)
        elif opt in ("-x", "--exportimport"):
            export_response(export_path=metadataurlpath, import_url=metadataurl)
            export_response(export_path=idpclientpath, import_url=idpurl)
            export_response(export_path=spclientpath, import_url=spurl)
            import_response(import_path=import_metadataurl_path, import_url=metadataurl)
            import_response(import_path=import_idpsamlclients_path, import_url=idpurl)
            import_response(import_path=import_spsamlclients_path, import_url=spurl)


if __name__ == "__main__":
    # disables Unverified HTTPs warning
    urllib3.disable_warnings()
    main(sys.argv[1:])