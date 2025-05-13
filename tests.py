from cloudscalinglib.xiqrestlib import *
from cloudscalinglib.outputfilegenexosv3 import *


if __name__ == "__main__":
    apiurl="https://ws3-api.qa.xcloudiq.com/"
    xiquser="sasrinivasan+scaling@extremenetworks.com"
    xiqpass="Extreme@123"
    authurl="https://ws3-api.qa.xcloudiq.com/login"
    
    filename = "./devicecfg/apscaling.csv"
    
    
    
    generateOnboardCsvWithAP(
        apiurl=apiurl,
        authurl=authurl,
        xiquser=xiquser,
        xiqpass=xiqpass,
        device_type="EXOS",
        num_devices=600,
        model="x435-24s",
        serial_prefix="SA",
        serial_start=1,
        output_file=filename,
        num_aps=6000,
        ap_per_switch=10,
        ap_start_serial="04101900460421",
        ap_model="AP410C"
    )
    ap_base_serial = "04101900460421"
    ap_base_mac = "062978AB2090"
    total_ap = 6000  # Total number of APs available
    num_aps = 10    # Number of APs per switch

    write_output_files(
        prefix="SA", 
        num_files=600, 
        base_mac="00:ab:00:00:00:00", 
        output_dir="./output", 
        inputcsvfile=filename,
        base_serial="04101900460421",
        ap_base_serial=ap_base_serial,
        ap_base_mac=ap_base_mac,
        num_aps=num_aps,  # Number of APs per switch
        total_ap=total_ap  # Total number of APs available
    )
postAdvanceOnboard(apiurl, authurl, xiquser, xiqpass, csv_file_path="./devicecfg/apscaling.csv")
    
    
   