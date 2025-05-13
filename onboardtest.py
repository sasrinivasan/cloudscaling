from cloudscalinglib.xiqrestlib import *
from cloudscalinglib.outputfilegenexosv3 import *


if __name__ == "__main__":
    apiurl="https://ws3-api.qa.xcloudiq.com/"
    xiquser="sasrinivasan+scaling@extremenetworks.com"
    xiqpass="Extreme@123"
    authurl="https://ws3-api.qa.xcloudiq.com/login"
    
    filename = "./devicecfg/apscaling.csv"
    
postAdvanceOnboard(apiurl, authurl, xiquser, xiqpass, csv_file_path="./devicecfg/test.csv")
    
    
   