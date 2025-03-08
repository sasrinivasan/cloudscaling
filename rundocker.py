import paramiko

def runSwitchEmulator(ip, username, password, port_mapping="9050:9050", container_name="sathish_exos", image_name="iqemu-exos", script_path="/bin/bash poc.sh", serial="1:700", hac="ws3r1.qa.xcloudiq.com", tls="yes", sshd="yes", prefix="SA", debug="true", telegraf="1", monitor_enable="0", restport="9050", iqversion="1.9.8", iqmd5sum="5e991aefe670f381993a9a9a342f55c3", macbase="00:ab:04:00:00:00", osversion="33.2.1.11", connrate="1:5", model="X435-24P-4S", scale="x435-medium"):
    """
    Logs in to the server and runs the specified Docker command.

    Parameters:
    ip (str): The IP address of the server.
    username (str): The username for SSH login.
    password (str): The password for SSH login.
    port_mapping (str): The port mapping for Docker.
    container_name (str): The name of the Docker container.
    image_name (str): The name of the Docker image.
    script_path (str): The path to the script to run inside the container.
    serial (str): The serial parameter.
    hac (str): The HAC parameter.
    tls (str): The TLS parameter.
    sshd (str): The SSHD parameter.
    prefix (str): The prefix parameter.
    debug (str): The debug parameter.
    telegraf (str): The telegraf parameter.
    monitor_enable (str): The monitor enable parameter.
    restport (str): The restport parameter.
    iqversion (str): The IQ version parameter.
    iqmd5sum (str): The IQ MD5 sum parameter.
    macbase (str): The MAC base parameter.
    osversion (str): The OS version parameter.
    connrate (str): The connection rate parameter.
    model (str): The model parameter.
    scale (str): The scale parameter.
    """
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server
        ssh.connect(ip, username=username, password=password)
        print(f"Connected to {ip}")

        # Construct the Docker command
        docker_command = (
            f"docker run -d -p {port_mapping} --name {container_name} {image_name} {script_path} "
            f"serial={serial} hac={hac} tls={tls} sshd={sshd} prefix={prefix} debug={debug} "
            f"telegraf={telegraf} monitor_enable={monitor_enable} restport={restport} iqversion={iqversion} "
            f"iqmd5sum={iqmd5sum} macbase={macbase} osversion={osversion} connrate={connrate} model={model} scale={scale}"
        )
        print(f"Running command: {docker_command}")

        # Execute the Docker command
        stdin, stdout, stderr = ssh.exec_command(docker_command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            print(f"Output: {output}")
        if error:
            print(f"Error: {error}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the SSH connection
        ssh.close()
        print("Connection closed")

if __name__ == "__main__":
    ip = "10.64.192.17"
    username = "root"
    password = "password"
    port_mapping = "9050:9050"
    container_name = "sathish_exos_donotdelete"
    image_name = "iqemu-exos"
    script_path = "/bin/bash poc.sh"
    serial = "0:700"
    hac = "ws3r1.qa.xcloudiq.com"
    tls = "yes"
    sshd = "yes"
    prefix = "EOND"
    debug = "true"
    telegraf = "1"
    monitor_enable = "0"
    restport = "9050"
    iqversion = "1.9.8"
    iqmd5sum = "5e991aefe670f381993a9a9a342f55c3"
    macbase = "00:ab:04:00:00:00"
    osversion = "33.2.1.11"
    connrate = "1:5"
    model = "X435-24P-4S"
    scale = "x435-medium"

    runSwitchEmulator(ip, username, password, port_mapping, container_name, image_name, script_path, serial, hac, tls, sshd, prefix, debug, telegraf, monitor_enable, restport, iqversion, iqmd5sum, macbase, osversion, connrate, model, scale)