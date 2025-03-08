###################################################
# Author:Sathish Kumar Srinivasan
# Contact: sasrinivasan@extremenetworks.com
#
#
####################################################
import time
import logging
import requests
import inspect
import datetime
import logging as logger
import os
import csv
import pycountry
import random


okRespCodeList=[200,202]
snsList=[]

apiurl="apiurl"
xiquser="xiquser"
xiqpass="xiqpass"
authurl="authurl"
'''
apiurl="https://g2-api.qa.xcloudiq.com/"
xiquser="sasrinivasan@extremenetworks.com"
xiqpass="Aerohive123"
authurl="https://g2-api.qa.xcloudiq.com/login"
'''

polname=""

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

def CheckRestError(status_code=500,response=""):
    respOK=True
    callerfunction=str(inspect.stack()[1].function)


    if status_code not in okRespCodeList:
        logging.error("Unexpected response from REST server- Response  is %s",response)
        
        logging.error("Calling Function is %s",callerfunction)
        respOK=False
    return respOK

def CreateLogReport(logname='Logs_'):
    filename= logname +"_"+ datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+'.log'
    if not os.path.exists("Testlog"):
        os.makedirs("Testlog")
        
    
    logging.basicConfig(
    filename='./Testlog/'+filename,
    level=logging.INFO, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
     )


# Login to XIQ with user/pass and get  a bearer/auth token. This is needed for further REST requests
def xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass):
    accessToken=None
    auth_token_header_value = None

    data = { "username": xiquser, "password": xiqpass }
    auth_response = requests.post(authurl, json=data,headers=headers)
    statusCode=auth_response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=auth_response.text)
  
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("Authentication  successfull. Access token is:")
        logger.debug(auth_response.text)

        #authToken=json.dumps(auth_response.text)["access_token"]
        auth_token=auth_response.json()
        accessToken=auth_token["access_token"]
        auth_token_header_value = "Bearer %s" % accessToken
    
    
    return auth_token_header_value

#Returns a dictionary with VIQ, license info
#{'devices': 10, 'standalone': True, 'expired': True, 'customer_id': 'CMJJ-39NQ-YQMH-VUQP', 'vhm_id': 'VHM-ZMLJFVIJ', 'owner_id': 4362, 'licenses': [{'id': 4229912, 'create_time': '2022-03-04T09:06:13.000+0000', 'update_time': '2022-03-04T09:06:13.000+0000', 'status': 'BUY', 'active_date': '2022-03-04T09:06:13.000+0000', 'expire_date': '2023-03-04T00:00:00.000+0000', 'entitlement_key': 'IZSF9-JBMLW-A4WLP-2YQLE-CYHAT-QJDEA', 'entitlement_type': 'PERMANENT', 'mode': 'BUY', 'devices': 10, 'activated': 0, 'available': 0}]}
def get_xiqviqinfo(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="account/viq",auth_token="None"):
    url=apiurl+path
    
    ViqInfo={}
    if auth_token=="None":
        logger.info("get_xiqviqinfo-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("get_xiqdeviceList-XIQ added list of devices:")
        logger.debug(response.json())
        ViqInfo=response.json()
    
    return ViqInfo

def post_xiqOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:onboard",deviceType="exos",field="sns",snsList=[],auth_token="None"):
    url=apiurl+path
    onboardeddeviceList=None
    
    OnBoarded=False
    
    onboardDeviceDict={deviceType:{ "sns": []}}
    
    if auth_token=="None":
        logger.info("post_xiqOnboardDevices-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
        
    logger.info(f"Onboarding devices with serial numbers:{snsList}")
    for serialno in snsList:
        onboardDeviceDict[deviceType][field].append(serialno)
    
    data=onboardDeviceDict
    #print (data)
    headers={'accept': 'application/json',"Authorization": auth_token}
    response = requests.post(url, json=data,headers=headers)

    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.info("Devices added to XIQ")

        OnBoarded=True

    return OnBoarded

#Returns a dictionary list of  onboarded  devices
def get_xiqdeviceListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices?page=1&limit=100&deviceTypes=REAL&deviceTypes=DIGITAL_TWIN&async=false",auth_token="None"):
    url=apiurl+path
    DeviceInfo={}
    if auth_token=="None":
        logger.info("get_xiqdeviceListDict-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("get_xiqdeviceList-XIQ added list of devices:")
        logger.debug(response.json())
        DeviceInfo=response.json()
    
    return DeviceInfo

#Returns a dictionary list of  clients connected to  onboarded devices
def get_xiqclientListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="clients/active?page=1&limit=10000", auth_token="None"):
    url=apiurl+path
    ClientInfo={}
    if auth_token=="None":
        logger.info("get_xiqclientListDict-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("get_xiqclientListDict-List of connected clients")
        logger.debug(response.json())
        ClientInfo=response.json()
    #print(UserInfo)
    return ClientInfo

# Given a device serial  number, fetch onboarded device ID
def get_xiqDeviceId(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn="",auth_token="None"):
    DeviceId=None
    
    if auth_token=="None":
        logger.info("get_xiqDeviceId-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    deviceInfoDict=get_xiqdeviceListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token=auth_token)

    logger.info("get_xiqDeviceId:List of devices\t" +str(deviceInfoDict))
    deviceList=deviceInfoDict['data']
    for device in deviceList:
        if device['serial_number']== sn:
            DeviceId=device['id']
    return DeviceId


# Poll device status periodically till it reaches a state Managed in given time
#Start time- Inital sleep, increment time- periodic poll time, endtime- final time before returning failure

def CheckDeviceStatusPeriodic(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn="",auth_token="None",starttime=30,incrementtime=10,endtime=600):
    deviceStatus="NOT_PRESENT"
    connecttime=starttime
    poll=True
    if auth_token=="None":
        logger.info("get_xiqDeviceId-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    logger.info(f"Sleeping for {starttime} before checking device status")
    time.sleep(starttime)

    while poll==True:
        
        deviceInfoDict=get_xiqdeviceListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token=auth_token)

        logger.info("get_xiqDeviceId:List of devices\t" +str(deviceInfoDict))
        deviceList=deviceInfoDict['data']

        if (deviceList == []):
            logger.error(f"Get device API did not return any devices - Issue similar to XIQ-14386.")
            poll=False
            break

        for device in deviceList:
 
            if (device['serial_number']== sn) and (device["device_admin_state"]=="MANAGED"):
                
                
                logger.info(f"Device status is Managed- Time taken {connecttime} seconds")
                poll=False
                deviceStatus="MANAGED"
                

                break
                
            elif (connecttime >= endtime):
                    logger.error(f"Device state did not change to managed in {endtime} seconds.")
                    logger.info(device)
                    poll=False
                    break
            else:
                #devicestate=device["device_admin_state"]
                #logger.info(f"Current state of device with serial number {sn} is {devicestate} ")
                logger.info(f"Time elapsed {connecttime} sec.Sleeping for {incrementtime} seconds before next poll")
                time.sleep(incrementtime)
                connecttime=connecttime+incrementtime
                    

    return deviceStatus

# Delete Devices from XIQ
def post_xiqDelOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:delete",snsList=[],auth_token="None"):
    url=apiurl+path
    data = {"ids":[]}
    Deleted=False
    if auth_token=="None":
        logger.info("post_xiqDelOnboardDevice-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    for serialno in snsList:
        devid=""
        devid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=serialno,auth_token=auth_token)
        if devid !="None":
            data["ids"].append(devid)
    
    #print(data)

    logger.info("From post_xiqDelOnboardDevices- Devices ID list:\t",data)

  
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response = requests.post(url, json=data,headers=headers)
    #print(response)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)

    if responseOK!=False: 
        #print(auth_response.text)
        logger.debug("Devices deleted from XIQ")

        Deleted=True

    return  Deleted



def xiqsendclitodevice(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:cli",deviceType="exos",cliList=[],snsList=[],auth_token="None"):

    cliResp={}
    url=apiurl+path
    cliRespJson={}
   
     
    cliDict = {"devices":{"ids":[]},"clis":[]}
    
    cliExecTImeDict={"devices":{"ids":[]},"clis":[],"execTime":[]}

    if auth_token=="None":
        logger.info("xiqsendclitodevice-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    for serialno in snsList:
        id=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=serialno,auth_token=auth_token)
        cliDict["devices"]["ids"].append(id)
        cliExecTImeDict["devices"]["ids"].append(id)
        
    for cli in cliList:
        cliDict["clis"].append(cli)
        cliExecTImeDict["clis"].append(cli)
        #Dict for CLIresp time

    #print(cliDict)
    headers={'accept': 'application/json',"Authorization": auth_token,}
    #Start clock tick
    cli_begin_time = datetime.datetime.now()
    logger.debug(f"CLI dictionary is {cliDict}")
    response = requests.post(url, json=cliDict,headers=headers)
    #End it after getting resp from XIQ
    cli_endtime=datetime.datetime.now()-cli_begin_time
    cliExecTImeDict["execTime"].append(cli_endtime)

    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)

    
    if responseOK!=False:
        
        logger.debug(f"CLI executed for devices")
        cliRespJson=response.json()
        
    return cliRespJson,cliExecTImeDict

#Returns a dictionary list of  policies
def get_xiqpolicyListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="network-policies?page=1&limit=30",auth_token="None"):
    url=apiurl+path
    #print(url)
    PolicyInfo={}

    if auth_token=="None":
        logger.info("Auth token not passed- Generating new token")
        accessToken,auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    headers={'accept': 'application/json',"Authorization": auth_token,}
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        #print(auth_response.text)
        logger.debug("get_xiqpolicyListDic-List of policies")
        logger.debug(response.json())
        PolicyInfo=response.json()
    #print(UserInfo)
    return PolicyInfo

def get_xiqpolicyId(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,polname="Wired",auth_token="None"):
    PolicyId=None
    
    if auth_token=="None":
        logger.info("Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    policyInfoDict=get_xiqpolicyListDict(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,auth_token=auth_token)
    
    logger.debug("get_xiqDeviceId:List of policy\t" +str(policyInfoDict))
    policyList=policyInfoDict['data']
    for pol in policyList:
        if pol['name']== polname:
            PolicyId=pol['id']

    return PolicyId
#assign a policy to device
def put_xiqpoldevice(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,snsList=[],polname="None",auth_token="None"):
    
    if auth_token=="None":
        logger.info("Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token

    headers={'accept': 'application/json',"Authorization": auth_token,}
    
    polstatusdict={}
    
    for serialno in snsList:
        deviceid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=serialno,auth_token=auth_token)
        policyid=get_xiqpolicyId(apiurl=apiurl,polname=polname,authurl=authurl,auth_token=auth_token)
        logger.info(f"Policy id {policyid} will be associated with {deviceid} with serialno {serialno}")
        url=apiurl+"devices/"+str(deviceid)+"/network-policy?networkPolicyId="+str(policyid)
       
        response=requests.put(url,headers=headers)
        polstatusdict["serial_no"]=serialno
        polstatusdict["device_id"]=deviceid
        polstatusdict["policy_id"]=policyid
        polstatusdict["put_url"]=url
        polstatusdict["policy assignment status"]=response

    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
   
    if responseOK!=False:
        
        logger.debug(f"{polname} assigned to devices in {snsList}" )
        logger.info(polstatusdict)

    return responseOK

    # update policy


def post_xiqupdatepolicy(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, path="deployments",
                         snsList=[],imageupdate=False, auth_token="None"):
    url = apiurl + path
    polUpdateResponseJson = {}
    if imageupdate==False:
        poldict = {
            "devices": {
                "ids": [

                ]
            },
            "policy": {
                "enable_complete_configuration_update": "true"

            }
        }
    elif imageupdate==True:
        poldict = {
            "devices": {
                "ids": [

                ]
            },
            "policy": {
                "enable_complete_configuration_update": "true",
                "firmware_upgrade_policy": {
                "enable_enforce_upgrade": "true"
           
                },
                "firmware_activate_option": {
                "activation_delay_seconds": 60,
                }

            }
        }
        



    if auth_token == "None":
        logger.info("Auth token not passed- Generating new token")
        auth_token = xiqlogin(authurl=authurl, xiquser=xiquser, xiqpass=xiqpass)
    else:
        auth_token = auth_token

    for serialno in snsList:
        id = get_xiqDeviceId(apiurl=apiurl, authurl=authurl, sn=serialno, auth_token=auth_token,
                             xiquser=xiquser, xiqpass=xiqpass)
        poldict["devices"]["ids"].append(id)
        logger.info(f"Policy json is {poldict}")

    headers = {'accept': 'application/json', "Authorization": auth_token, }

    logger.info(f"Policy dictionary is {poldict}")
    
    response = requests.post(url, json=poldict, headers=headers)

    statusCode = response.status_code
    responseOK = CheckRestError(status_code=statusCode, response=response.text)

    if responseOK != False:
        logger.debug(f"policy update successfull")
        polUpdateResponseJson = response.json()

    return polUpdateResponseJson
 


def get_policyupdatestatus(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="deployments/status?deviceIds=",auth_token="None",sn=""):
    
    
    PolStatusInfo={}
    if auth_token=="None":
        logger.info("get_policyupdatestatus-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    
    devid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=sn,auth_token=auth_token)
    
    url=apiurl+path+str(devid)
    logger.info(f"Update status post url {url}")
    headers={'accept': 'application/json',"Authorization": auth_token,}
    
    response=requests.get(url, headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)
    
    if responseOK!=False:
        
        logger.debug(f"policy update status info for device with {sn} is {response.json()}")
        
        PolStatusInfo=response.json()
    
    return PolStatusInfo

# Poll policy update status periodically for a given device IDs
#Start time- Inital sleep, increment time- periodic poll time, endtime- final time before returning failure

def CheckPolicyStatusPeriodic(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn="",auth_token="None",starttime=10,incrementtime=30,endtime=900):
    policyupdateStatus=False
    connecttime=starttime
    poll=True
    if auth_token=="None":
        logger.info("CheckPolicyStatusPeriodic-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    devid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=sn,auth_token=auth_token)
    logger.info(f"Sleeping for {starttime} before checking policy update status")
    time.sleep(starttime)

    while poll==True:
        
        
        polstatusInfoDict=get_policyupdatestatus(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="deployments/status?deviceIds=",auth_token=auth_token,sn=sn)
        


        if (polstatusInfoDict[str(devid)]['finished']== True) and (polstatusInfoDict[str(devid)]["is_finished_successful"]==True):
                               
                logger.info(f"Policy update for device with serial {sn} is successful")
                logger.info(f"Policy updated completed in {connecttime-starttime} seconds")
                poll=False
                policyupdateStatus=True
                break
                
        elif (connecttime >= endtime):
                logger.error(f"Policy did not update in {endtime} seconds.")
                logger.info(polstatusInfoDict)
                poll=False
                
                break
        else:
            logger.info(f"Time elapsed {connecttime} sec.Sleeping for {incrementtime} seconds before next poll")
            time.sleep(incrementtime)
            connecttime=connecttime+incrementtime
                

    return policyupdateStatus

def post_xiqRebootOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,sn="",auth_token="None",path="/devices/:reboot"):
    url=apiurl+path
    data = {"ids":[]}
    Rebooted=False
    if auth_token=="None":
        logger.info("CheckPolicyStatusPeriodic-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    devid=get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=sn,auth_token=auth_token)
        
    
        
    data["ids"].append(devid)
    logger.info("From post_xiqRebootOnboardDevices- Devices ID list:\t",data)
    
    
    logger.info("From post_xiqRebootOnboardDevices\t",data) 
    headers={'accept': 'application/json',"Authorization": auth_token,}
    response = requests.post(url, json=data,headers=headers)
    statusCode=response.status_code
    responseOK=CheckRestError(status_code=statusCode,response=response.text)


    if responseOK!=False: 
        #print(auth_response.text)
        logger.info("Devices  Rebooted")

        Rebooted=True



    return  Rebooted
#Sends CLI to device, receivces response, splits the reponse based on newlines and checks lines for patterns.
#only single CLI in CLIList is supported currently- this is a API infra limitation for switching devices
def executeandcheckClioutput(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:cli",deviceType="exos",cliList=[],snsList=[],auth_token="None",checkList=[]):
    CheckValidCLiExecution=False
    if auth_token=="None":
        logger.info("CheckPolicyStatusPeriodic-Auth token not passed- Generating new token")
        auth_token=xiqlogin(authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    else:
        auth_token=auth_token
    devid=str(get_xiqDeviceId(apiurl=apiurl,authurl=authurl,sn=snsList[0],auth_token=auth_token))

    cliresp={}
    cliExecTIme={}
    cliresp,cliExecTIme=xiqsendclitodevice(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:cli",deviceType="exos",cliList=cliList,snsList=snsList,auth_token=auth_token)
    logger.info(f"Cli response is {cliresp}")
    clioutput=cliresp['device_cli_outputs'][devid][0]['output']
    splitout=clioutput.split("\n")

    testList=[]

    for checkString in checkList:
        if checkString in clioutput:
            
            logger.info(f"{checkString} found in {cliList[0]}.")
            testList.append("True")
            
        else:
            logger.error(f"{checkString} not found in {cliList[0]}.")
            testList.append("False")
    
    if len(testList) == len(checkList) and  "False" not in testList :
        CheckValidCLiExecution=True
    else:
        CheckValidCLiExecution=False
            

    return CheckValidCLiExecution
#returns location tree
def getxiqLocationTree (apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, path="locations/tree?expandChildren=true", auth_token="None"):
    url = apiurl + path
    LocationInfo = {}

    if auth_token == "None":
        logger.info("get_xiqlocations-Auth token not passed- Generating new token")
        auth_token = xiqlogin(authurl=authurl, xiquser=xiquser, xiqpass=xiqpass)
    else:
        auth_token = auth_token

    headers = {'accept': 'application/json', "Authorization": auth_token}
    response = requests.get(url, headers=headers)
    statusCode = response.status_code
    responseOK = CheckRestError(status_code=statusCode, response=response.text)

    if responseOK != False:
        logger.debug("get_xiqlocations-List of locations")
        logger.debug(response.json())
        LocationInfoTree = response.json()

    return LocationInfoTree
#return a location id given a name
def getxiqLocationID(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, location_name="", auth_token="None"):
    locations = getxiqLocationTree(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, auth_token=auth_token)
    location_id = None

    def find_location_id(locations, location_name):
        for location in locations:
            if location['name'] == location_name:
                return location['id']
            if 'children' in location and location['children']:
                child_id = find_location_id(location['children'], location_name)
                if child_id:
                    return child_id
        return None

    location_id = find_location_id(locations, location_name)

    if location_id is None:
        logger.error(f"Location with name '{location_name}' not found.")
    else:
        logger.info(f"Location ID for '{location_name}' is {location_id}")

    return location_id
   

#creates a site by in xiq. Lattitude and longitude are fetched from worldcities.csv
def postxiqCreateSite(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, parent_name="", site_name="", city="", address="", address2="", state="", postal_code="", csvfile="worldcities.csv", auth_token="None"):
    # Get the parent ID
    parent_id = getxiqLocationID(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, location_name=parent_name, auth_token=auth_token)
    if parent_id is None:
        logger.error(f"Parent location with name '{parent_name}' not found.")
        return None

    # Lookup worldcities.csv for city details
    city_details = {}
    with open(csvfile, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['city'] == city:
                city_details = row
                break

    if not city_details:
        logger.error(f"City '{city}' not found in {csvfile}.")
        return None

    country_name = city_details['country']
    country = pycountry.countries.get(name=country_name)
    if not country:
        logger.error(f"Country '{country_name}' not found in pycountry library.")
        return None

    country_code = country.numeric
    latitude = float(city_details['lat'])
    longitude = float(city_details['lng'])

    # Generate random postal code
    postal_code = str(random.randint(100000, 999999))

    # Prepare the data for the POST request
    data = {
        "parent_id": parent_id,
        "name": f"{city}_site",
        "address": {
            "address": f"{city} {address}",
            "address2": f"{city} {address2}",
            "city": city,
            "state": city_details['admin_name'],
            "postal_code": postal_code
        },
        "country_code": country_code,
        "latitude": latitude,
        "longitude": longitude
    }

    # Get the auth token if not provided
    if auth_token == "None":
        logger.info("create_site-Auth token not passed- Generating new token")
        auth_token = xiqlogin(authurl=authurl, xiquser=xiquser, xiqpass=xiqpass)
    else:
        auth_token = auth_token

    headers = {'accept': 'application/json', "Authorization": auth_token, 'Content-Type': 'application/json'}
    url = apiurl + "locations/site"
    response = requests.post(url, json=data, headers=headers)
    statusCode = response.status_code
    responseOK = CheckRestError(status_code=statusCode, response=response.text)

    if responseOK != False:
        logger.info(f"Site '{site_name}' created successfully.")
        return response.json()
    else:
        logger.error(f"Failed to create site '{site_name}'.")
        return None
    
#delete location and its child recursively.If location name is org, it will delete all locations
def deletexiqLocation(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, location_name="", auth_token="None"):
    # Get the location ID
    location_id = getxiqLocationID(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, location_name=location_name, auth_token=auth_token)
    print(location_id)
    if location_id is None:
        logger.error(f"Location with name '{location_name}' not found.")
        return None

    # Prepare the URL for the DELETE request
    url = f"{apiurl}locations/{location_id}?force_delete=true"

    # Get the auth token if not provided
    if auth_token == "None":
        logger.info("delete_xiqLocation-Auth token not passed- Generating new token")
        auth_token = xiqlogin(authurl=authurl, xiquser=xiquser, xiqpass=xiqpass)
    else:
        auth_token = auth_token

    headers = {'accept': '*/*', "Authorization": auth_token}
    response = requests.delete(url, headers=headers)
    statusCode = response.status_code
    responseOK = CheckRestError(status_code=statusCode, response=response.text)

    if responseOK != False:
        logger.info(f"Location '{location_name}' deleted successfully.")
        return response.json()
    else:
        logger.error(f"Failed to delete location '{location_name}'.")
        return None
    
#extracts random cities from worldcities.csv
def extract_random_cities(csv_file_path="worldcities.csv", num_cities=10):
    cities = []

    # Read the CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Extract the relevant data
        for row in reader:
            city_info = {
                'latitude': row['lat'],
                'longitude': row['lng'],
                'country': row['country'],
                'admin_name': row['admin_name']
            }
            cities.append({row['city']: city_info})

    # Select a random subset of cities
    if num_cities > len(cities):
        num_cities = len(cities)
    random_cities = random.sample(cities, num_cities)

    return random_cities

#create building within a site
def postxiqCreateBuilding(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, parent_name="", site_name="", building_number=1, city="", address="", address2="", state="", postal_code="", latitude=0, longitude=0, auth_token="None"):
    # Get the parent ID
    parent_id = getxiqLocationID(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, location_name=parent_name, auth_token=auth_token)
    if parent_id is None:
        logger.error(f"Parent location with name '{parent_name}' not found.")
        return None

    # Generate building name and address
    building_name = f"{site_name}_building {building_number}"
    building_address = f"{city} {address}_building {building_number}"
    building_address2 = f"{city} {address2}_building {building_number}"

    # Generate random latitude and longitude within 30 km range
    lat_variation = random.uniform(-0.27, 0.27)  # Approx 30 km in latitude
    lon_variation = random.uniform(-0.27, 0.27)  # Approx 30 km in longitude
    building_latitude = latitude + lat_variation
    building_longitude = longitude + lon_variation

    # Prepare the data for the POST request
    data = {
        "parent_id": parent_id,
        "name": building_name,
        "address": {
            "address": building_address,
            "address2": building_address2,
            "city": city,
            "state": state,
            "postal_code": postal_code
        },
        "latitude": building_latitude,
        "longitude": building_longitude
    }

    # Get the auth token if not provided
    if auth_token == "None":
        logger.info("postxiqCreateBuilding-Auth token not passed- Generating new token")
        auth_token = xiqlogin(authurl=authurl, xiquser=xiquser, xiqpass=xiqpass)
    else:
        auth_token = auth_token

    headers = {'accept': 'application/json', "Authorization": auth_token, 'Content-Type': 'application/json'}
    url = apiurl + "locations/building"
    response = requests.post(url, json=data, headers=headers)
    statusCode = response.status_code
    responseOK = CheckRestError(status_code=statusCode, response=response.text)

    if responseOK != False:
        logger.info(f"Building '{building_name}' created successfully.")
        return response.json()
    else:
        logger.error(f"Failed to create building '{building_name}'.")
        return None

def postxiqCreateFloor(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, parent_name="", building_name="", floor_number=1, environment="AUTO_ESTIMATE", db_attenuation=0, measurement_unit="FEET", installation_height=0, map_size_width=0, map_size_height=0, map_name="", auth_token="None"):
    # Get the parent ID
    parent_id = getxiqLocationID(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, location_name=parent_name, auth_token=auth_token)
    if parent_id is None:
        logger.error(f"Parent location with name '{parent_name}' not found.")
        return None

    # Generate floor name
    floor_name = f"{building_name}_floor {floor_number}"

    # Prepare the data for the POST request
    data = {
        "parent_id": parent_id,
        "name": floor_name,
        "environment": environment,
        "db_attenuation": db_attenuation,
        "measurement_unit": measurement_unit,
        "installation_height": installation_height,
        "map_size_width": map_size_width,
        "map_size_height": map_size_height,
        "map_name": map_name
    }

    # Get the auth token if not provided
    if auth_token == "None":
        logger.info("postxiqCreateFloor-Auth token not passed- Generating new token")
        auth_token = xiqlogin(authurl=authurl, xiquser=xiquser, xiqpass=xiqpass)
    else:
        auth_token = auth_token

    headers = {'accept': 'application/json', "Authorization": auth_token, 'Content-Type': 'application/json'}
    url = apiurl + "locations/floor"
    response = requests.post(url, json=data, headers=headers)
    statusCode = response.status_code
    responseOK = CheckRestError(status_code=statusCode, response=response.text)

    if responseOK != False:
        logger.info(f"Floor '{floor_name}' created successfully.")
        return response.json()
    else:
        logger.error(f"Failed to create floor '{floor_name}'.")
        return None
#create number of buildings and floors for all sites
def createBuildingsAndFloorsForSites(apiurl, authurl, xiquser, xiqpass, num_buildings, num_floors, auth_token="None"):
    # Get the list of locations (including the root)
    locations = getxiqLocationTree(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, auth_token=auth_token)
    
    if not locations:
        logger.error("No locations found.")
        return None

    # Process only the child nodes (sites)
    for root in locations:
        if 'children' in root:
            for site in root['children']:
                site_name = site['name']
                parent_name = site_name
                city = site['name']
                address = "Main St"
                address2 = "Second St"
                state = "State"
                postal_code = "000000"
                latitude = 0.0  # Default latitude, replace with actual value if available
                longitude = 0.0  # Default longitude, replace with actual value if available

                # Create buildings for the site
                for building_number in range(1, num_buildings + 1):
                    building_response = postxiqCreateBuilding(
                        apiurl=apiurl,
                        authurl=authurl,
                        xiquser=xiquser,
                        xiqpass=xiqpass,
                        parent_name=parent_name,
                        site_name=site_name,
                        building_number=building_number,
                        city=city,
                        address=address,
                        address2=address2,
                        state=state,
                        postal_code=postal_code,
                        latitude=latitude,
                        longitude=longitude,
                        auth_token=auth_token
                    )

                    if building_response:
                        building_name = f"{site_name}_building {building_number}"
                        # Create floors for the building
                        for floor_number in range(1, num_floors + 1):
                            postxiqCreateFloor(
                                apiurl=apiurl,
                                authurl=authurl,
                                xiquser=xiquser,
                                xiqpass=xiqpass,
                                parent_name=building_name,
                                building_name=building_name,
                                floor_number=floor_number,
                                environment="AUTO_ESTIMATE",
                                db_attenuation=0,
                                measurement_unit="FEET",
                                installation_height=10,
                                map_size_width=100,
                                map_size_height=100,
                                #map_name=f"{building_name}_map",
                                auth_token=auth_token
                            )
#generate device csv
def generateOnboardCsv (device_type, num_devices, model="x435-24s", serial_prefix="DEV", serial_start=0, output_dir="."):
    # Fetch all available locations using getxiqLocationTree
    locations = getxiqLocationTree(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, auth_token="None")
    
    if not locations:
        logger.error("No locations found.")
        return None

    # Extract unique names for floors
    floor_locations = []
    for root in locations:
        if 'children' in root:
            for site in root['children']:
                if 'children' in site:
                    for building in site['children']:
                        if 'children' in building:
                            for floor in building['children']:
                                if floor['type'] == "FLOOR":
                                    floor_locations.append(floor['unique_name'])

    if not floor_locations:
        logger.error("No floor locations found.")
        return None

    # Generate device details
    devices = []
    for i in range(num_devices):
        serial_number = f"{serial_prefix}-{serial_start + i:06d}"
        ip_address = f"192.168.0.{(i % 254) + 1}"  # Ensure IP addresses are within a valid range
        location = floor_locations[i % len(floor_locations)]
        device = {
            "SerialNumber": serial_number,
            "IPAddress": ip_address,
            "DeviceFamily": device_type,
            "User": "admin",
            "Password": "Extreme@123",
            "InletConnect": "false",
            "SSHConnect": "false",
            "InletServerIP": "10.64.194.54",
            "InletServerPort": "8090",
            "Model": model,
            "Location": location
        }
        devices.append(device)

    # Write device details to CSV file
    output_file = os.path.join(output_dir, "devices.csv")
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=devices[0].keys())
        writer.writeheader()
        writer.writerows(devices)

    logger.info(f"CSV file generated: {output_file}")
    return output_file
#onboard devices with location
def postAdvanceOnboard(apiurl, authurl, xiquser, xiqpass, csv_file_path, auth_token="None"):
    # Fetch all available locations using getxiqLocationTree
    locations = getxiqLocationTree(apiurl=apiurl, authurl=authurl, xiquser=xiquser, xiqpass=xiqpass, auth_token=auth_token)
    
    if not locations:
        logger.error("No locations found.")
        return None

    # Create a dictionary to map location names to their details
    location_map = {}
    for root in locations:
        if 'children' in root:
            for site in root['children']:
                if 'children' in site:
                    for building in site['children']:
                        if 'children' in building:
                            for floor in building['children']:
                                if floor['type'] == "FLOOR":
                                    location_map[floor['unique_name']] = {
                                        'location_id': floor['id'],
                                        'latitude': floor.get('latitude', 0),
                                        'longitude': floor.get('longitude', 0)
                                    }

    if not location_map:
        logger.error("No floor locations found.")
        return None

    # Read the CSV file and construct the JSON payload
    devices_by_type = {
        "extreme": [],
        "exos": [],
        "voss": [],
        "wing": [],
        "dell": [],
        "dt": []
    }

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            device_type = row['DeviceFamily'].lower()
            if device_type in devices_by_type:
                location = location_map.get(row['Location'], {})
                device = {
                    "serial_number": row['SerialNumber'],
                    "location": {
                        "location_id": location.get('location_id', 0),
                        "x": 0,
                        "y": 0,
                        "latitude": location.get('latitude', 0),
                        "longitude": location.get('longitude', 0)
                    },
                    "network_policy_id": 0,  # Replace with actual network policy ID if available
                    "hostname": row['SerialNumber']
                }
                devices_by_type[device_type].append(device)

    # Construct the final JSON payload
    payload = {k: v for k, v in devices_by_type.items() if v}
    payload["unmanaged"] = True

    # Get the auth token if not provided
    if auth_token == "None":
        logger.info("postAdvanceOnboard-Auth token not passed- Generating new token")
        auth_token = xiqlogin(authurl=authurl, xiquser=xiquser, xiqpass=xiqpass)
    else:
        auth_token = auth_token

    headers = {'accept': 'application/json', "Authorization": auth_token, 'Content-Type': 'application/json'}
    url = apiurl + "devices/:advanced-onboard?async=false"
    response = requests.post(url, json=payload, headers=headers)
    statusCode = response.status_code
    responseOK = CheckRestError(status_code=statusCode, response=response.text)

    if responseOK != False:
        logger.info("Devices advanced onboarded successfully.")
        return response.json()
    else:
        logger.error("Failed to advanced onboard devices.")
        return None



    
   
if __name__=="__main__":
    print("In XIQ rest main")
    
    apiurl="https://ws3-api.qa.xcloudiq.com/"
    xiquser="sasrinivasan+scaling@extremenetworks.com"
    xiqpass="Extreme@123"
    authurl="https://ws3-api.qa.xcloudiq.com/login"
    #auth=xiqlogin(authurl=authurl,xiquser="sasrinivasan+scaling@extremenetworks.com",xiqpass="Extreme@123")
    #print(auth)
    #sns=["EXT-000000","EXT-000001","EXT-000002","EXT-000003","EXT-000004","EXT-000005","EXT-000006","EXT-000007","EXT-000008","EXT-000009","EXT-000010","EXT-000011","EXT-000012","EXT-000013","EXT-000014","EXT-000015","EXT-000016","EXT-000017","EXT-000018","EXT-000019","EXT-000020","EXT-000021","EXT-000022","EXT-000023","EXT-000024","EXT-000025","EXT-000026","EXT-000027","EXT-000028","EXT-000029","EXT-000030","EXT-000031","EXT-000032","EXT-000033","EXT-000034","EXT-000035","EXT-000036","EXT-000037","EXT-000038","EXT-000039","EXT-000040","EXT-000041","EXT-000042","EXT-000043","EXT-000044","EXT-000045","EXT-000046","EXT-000047","EXT-000048","EXT-000049","EXT-000050","EXT-000051","EXT-000052","EXT-000053","EXT-000054","EXT-000055","EXT-000056","EXT-000057","EXT-000058","EXT-000059","EXT-000060","EXT-000061","EXT-000062","EXT-000063","EXT-000064","EXT-000065","EXT-000066","EXT-000067","EXT-000068","EXT-000069","EXT-000070","EXT-000071","EXT-000072","EXT-000073","EXT-000074","EXT-000075","EXT-000076","EXT-000077","EXT-000078","EXT-000079","EXT-000080","EXT-000081","EXT-000082","EXT-000083","EXT-000084","EXT-000085","EXT-000086","EXT-000087","EXT-000088","EXT-000089","EXT-000090","EXT-000091","EXT-000092","EXT-000093","EXT-000094","EXT-000095","EXT-000096","EXT-000097","EXT-000098","EXT-000099","EXT-000100","EXT-000101","EXT-000102","EXT-000103","EXT-000104","EXT-000105","EXT-000106","EXT-000107","EXT-000108","EXT-000109","EXT-000110","EXT-000111","EXT-000112","EXT-000113","EXT-000114","EXT-000115","EXT-000116","EXT-000117","EXT-000118","EXT-000119","EXT-000120","EXT-000121","EXT-000122","EXT-000123","EXT-000124","EXT-000125","EXT-000126","EXT-000127","EXT-000128","EXT-000129","EXT-000130","EXT-000131","EXT-000132","EXT-000133","EXT-000134","EXT-000135","EXT-000136","EXT-000137","EXT-000138","EXT-000139","EXT-000140","EXT-000141","EXT-000142","EXT-000143","EXT-000144","EXT-000145","EXT-000146","EXT-000147","EXT-000148","EXT-000149","EXT-000150","EXT-000151","EXT-000152","EXT-000153","EXT-000154","EXT-000155","EXT-000156","EXT-000157","EXT-000158","EXT-000159","EXT-000160","EXT-000161","EXT-000162","EXT-000163","EXT-000164","EXT-000165","EXT-000166","EXT-000167","EXT-000168","EXT-000169","EXT-000170","EXT-000171","EXT-000172","EXT-000173","EXT-000174","EXT-000175","EXT-000176","EXT-000177","EXT-000178","EXT-000179","EXT-000180","EXT-000181","EXT-000182","EXT-000183","EXT-000184","EXT-000185","EXT-000186","EXT-000187","EXT-000188","EXT-000189","EXT-000190","EXT-000191","EXT-000192","EXT-000193","EXT-000194","EXT-000195","EXT-000196","EXT-000197","EXT-000198","EXT-000199","EXT-000200","EXT-000201","EXT-000202","EXT-000203","EXT-000204","EXT-000205","EXT-000206","EXT-000207","EXT-000208","EXT-000209","EXT-000210","EXT-000211","EXT-000212","EXT-000213","EXT-000214","EXT-000215","EXT-000216","EXT-000217","EXT-000218","EXT-000219","EXT-000220","EXT-000221","EXT-000222","EXT-000223","EXT-000224","EXT-000225","EXT-000226","EXT-000227","EXT-000228","EXT-000229","EXT-000230","EXT-000231","EXT-000232","EXT-000233","EXT-000234","EXT-000235","EXT-000236","EXT-000237","EXT-000238","EXT-000239","EXT-000240","EXT-000241","EXT-000242","EXT-000243","EXT-000244","EXT-000245","EXT-000246","EXT-000247","EXT-000248","EXT-000249","EXT-000250","EXT-000251","EXT-000252","EXT-000253","EXT-000254","EXT-000255","EXT-000256","EXT-000257","EXT-000258","EXT-000259","EXT-000260","EXT-000261","EXT-000262","EXT-000263","EXT-000264","EXT-000265","EXT-000266","EXT-000267","EXT-000268","EXT-000269","EXT-000270","EXT-000271","EXT-000272","EXT-000273","EXT-000274","EXT-000275","EXT-000276","EXT-000277","EXT-000278","EXT-000279","EXT-000280","EXT-000281","EXT-000282","EXT-000283","EXT-000284","EXT-000285","EXT-000286","EXT-000287","EXT-000288","EXT-000289","EXT-000290","EXT-000291","EXT-000292","EXT-000293","EXT-000294","EXT-000295","EXT-000296","EXT-000297","EXT-000298","EXT-000299","EXT-000300","EXT-000301","EXT-000302","EXT-000303","EXT-000304","EXT-000305","EXT-000306","EXT-000307","EXT-000308","EXT-000309","EXT-000310","EXT-000311","EXT-000312","EXT-000313","EXT-000314","EXT-000315","EXT-000316","EXT-000317","EXT-000318","EXT-000319","EXT-000320","EXT-000321","EXT-000322","EXT-000323","EXT-000324","EXT-000325","EXT-000326","EXT-000327","EXT-000328","EXT-000329","EXT-000330","EXT-000331","EXT-000332","EXT-000333","EXT-000334","EXT-000335","EXT-000336","EXT-000337","EXT-000338","EXT-000339","EXT-000340","EXT-000341","EXT-000342","EXT-000343","EXT-000344","EXT-000345","EXT-000346","EXT-000347","EXT-000348","EXT-000349","EXT-000350","EXT-000351","EXT-000352","EXT-000353","EXT-000354","EXT-000355","EXT-000356","EXT-000357","EXT-000358","EXT-000359","EXT-000360","EXT-000361","EXT-000362","EXT-000363","EXT-000364","EXT-000365","EXT-000366","EXT-000367","EXT-000368","EXT-000369","EXT-000370","EXT-000371","EXT-000372","EXT-000373","EXT-000374","EXT-000375","EXT-000376","EXT-000377","EXT-000378","EXT-000379","EXT-000380","EXT-000381","EXT-000382","EXT-000383","EXT-000384","EXT-000385","EXT-000386","EXT-000387","EXT-000388","EXT-000389","EXT-000390","EXT-000391","EXT-000392","EXT-000393","EXT-000394","EXT-000395","EXT-000396","EXT-000397","EXT-000398","EXT-000399","EXT-000400","EXT-000401","EXT-000402","EXT-000403","EXT-000404","EXT-000405","EXT-000406","EXT-000407","EXT-000408","EXT-000409","EXT-000410","EXT-000411","EXT-000412","EXT-000413","EXT-000414","EXT-000415","EXT-000416","EXT-000417","EXT-000418","EXT-000419","EXT-000420","EXT-000421","EXT-000422","EXT-000423","EXT-000424","EXT-000425","EXT-000426","EXT-000427","EXT-000428","EXT-000429","EXT-000430","EXT-000431","EXT-000432","EXT-000433","EXT-000434","EXT-000435","EXT-000436","EXT-000437","EXT-000438","EXT-000439","EXT-000440","EXT-000441","EXT-000442","EXT-000443","EXT-000444","EXT-000445","EXT-000446","EXT-000447","EXT-000448","EXT-000449","EXT-000450","EXT-000451","EXT-000452","EXT-000453","EXT-000454","EXT-000455","EXT-000456","EXT-000457","EXT-000458","EXT-000459","EXT-000460","EXT-000461","EXT-000462","EXT-000463","EXT-000464","EXT-000465","EXT-000466","EXT-000467","EXT-000468","EXT-000469","EXT-000470","EXT-000471","EXT-000472","EXT-000473","EXT-000474","EXT-000475","EXT-000476","EXT-000477","EXT-000478","EXT-000479","EXT-000480","EXT-000481","EXT-000482","EXT-000483","EXT-000484","EXT-000485","EXT-000486","EXT-000487","EXT-000488","EXT-000489","EXT-000490","EXT-000491","EXT-000492","EXT-000493","EXT-000494","EXT-000495","EXT-000496","EXT-000497","EXT-000498","EXT-000499"]
    #post_xiqOnboardDevices (apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,path="devices/:onboard",deviceType="voss",field="sns",snsList=sns,auth_token=auth)
    #loc=getxiqLocationTree(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass)
    #print(loc)
    #locationid=getxiqLocationID(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,location_name="New Delhi")
    #print(locationid)
    #site=postxiqCreateSite(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,parent_name
    #="Calzedonia",site_name="New Delhi",city="New Delhi",address="Via new delhi",address2="Via new delhi",state="New Delhi",postal_code="000000")
    #print(site)

    #deletexiqLocation(apiurl=apiurl,authurl=authurl,xiquser=xiquser,xiqpass=xiqpass,location_name="Eon Digital")
    #cities = extract_random_cities()
    #print(cities)

    # Extract random cities
    '''cities = extract_random_cities(csv_file_path="worldcities.csv", num_cities=2)

    # Create sites for each city
    for city_dict in cities:
        for city, details in city_dict.items():
            postxiqCreateSite(
                apiurl=apiurl,
                authurl=authurl,
                xiquser=xiquser,
                xiqpass=xiqpass,
                parent_name="EonDigital",
                site_name=f"{city}_site",
                city=city,
                address="Main St",
                address2="Second St",
                state=details['admin_name'],
                postal_code="000000",
                csvfile="worldcities.csv"
            )
    # Number of buildings and floors to create
    num_buildings = 1
    num_floors = 1

    # Create buildings and floors for the sites
    createBuildingsAndFloorsForSites(
        apiurl=apiurl,
        authurl=authurl,
        xiquser=xiquser,
        xiqpass=xiqpass,
        num_buildings=num_buildings,
        num_floors=num_floors
    )


    # Generate CSV file for VOSS devices
    generateOnboardCsv(device_type="EXOS", num_devices=700, model="X435-24P-4S", serial_prefix="EOND", serial_start=0, output_dir=".")'''

    postAdvanceOnboard(apiurl, authurl, xiquser, xiqpass, csv_file_path="devices.csv")
