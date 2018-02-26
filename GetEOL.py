import requests
import json

token_url = 'https://cloudsso.cisco.com/as/token.oauth2?grant_type=client_credentials'
Client_ID = '9z2umga2y7ysgfc9h4kjhhsd'
Client_Secret = '34j3WSXpnHAdfxmc5tAyCScA'
resp = requests.post(token_url, auth=(Client_ID, Client_Secret)).json()


#list of Product ID's . We just assumed that we have already extracted them from devices
pid_list = ['WS-C3550-24-SMI' ,'DS-C9513','DS-X9232-256K9']

def geteolinfo (pid_list):
	for PID in pid_list:
		url = 'https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/' + PID +'?responseencoding=json'
		string = 'Bearer '+ resp['access_token']
		header = {'Authorization': string}
		resp_eol = requests.get (url, headers=header)
		data = resp_eol.json()
		print ('PID : ' + PID)
		print ('Last date of support :' + data['EOXRecord'][0]['LastDateOfSupport']['value'])



geteolinfo(pid_list)