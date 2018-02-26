import re
import paramiko
import time
import nmap

# Files used for this script
iprange = open('/root/Desktop/range.txt', 'r')
passlist = open('/home/debian/Desktop/Python Project Files/passwords.txt', 'r')
# Two empty and temporary files that this script uses to denote adjacencies and whole output
tempfile1 = open('/home/debian/cdptempoutput.txt', 'w')
tempfile2 = open('/home/debian/scriptoutput.txt', 'w')

# Regular expressions needed for extracting necessary information from command outputs
hw_version_pattern = re.compile('Cisco\s\d+')
os_version_pattern = re.compile('Version ([\d\w\(\)\.]+)')
os_pattern = re.compile('(NX\-OS|IOS|IOS\-XR)')
range_pattern = re.compile('(\d+.\d+.\d+.\d+\/\d+)')
hostname_pattern = re.compile('(.*) uptime')
neighbor_pattern = re.compile('(.*?)\..*')
module_pattern = re.compile('(.*Slot|Slot)( .*):(\n*\s*)(.*)')
# pid_pattern = re.compile('(PID:.*?)\,')
pid_1_pattern = re.compile('(PID:)(.*?)\,')
interface_pattern = re.compile('(.*\d) *(up|down|admin down) *(up|down) *(.*)')


# Get the range from range.txt file and add each range into a list
def getrange(iprange):
    range = []
    for line in iprange:
        range1 = range_pattern.findall(line)
        range = range + range1
    return (range)


# For each range, we use nmap scanner to check if related IP's are active and related ports are open
def networkscanner(range):
    nm = nmap.PortScanner()
    activeiplist = []
    for item in range:
        nm.scan(item, '22')
        for host in nm.all_hosts():
            x = nm[host].state()
            y = nm[host]['tcp'][22]['state']
            if (x == 'up') & (y == 'open'):
                activeiplist.append(host)
    return (activeiplist)


# Get the passwords from password.txt file
def getpasswords(passlist):
    passwordlist = []
    for line in passlist:
        line = line.strip()
        if line:
            passwordlist.append(line)
    return (passwordlist)


range = getrange(iprange)
passwordlist = getpasswords(passlist)
activeiplist = networkscanner(range)


# Main function for SSH connections, entering commands and returning their ouputs in required format
def opensshcon(activeiplist, passwordlist):
    for item in activeiplist:
        username = 'admin'
        for item2 in passwordlist:
            try:
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(item, username=username, password=item2)
                connection = session.invoke_shell()
                connection.send('terminal length 0\n')
                time.sleep(1)
                connection.send('show version\n')
                time.sleep(1)
                output = connection.recv(3000)
                hostname = hostname_pattern.findall(output)
                print('------------------------------------------------------------------\n')
                print('Interactive SSH Connection established to ' + str(hostname[0]) + '\n')
                print('------------------------------------------------------------------')
                tempfile2.write('------------------------------------------------------------------\n')
                tempfile2.write('Interactive SSH Connection established to ' + str(hostname[0]) + '\n')
                tempfile2.write('------------------------------------------------------------------\n')

                hwversion = hw_version_pattern.search(output).group()
                osversion = os_version_pattern.search(output).group(1)
                ostype = os_pattern.search(output).group(1)
                print('Hostname :' + str(hostname[0]))
                print('Hardware version : ' + hwversion)
                print('Operating system : ' + ostype)
                print('Operating system version : ' + osversion)
                print('Management IP address : ' + item)
                print('Password : ' + item2 + '\n')
                tempfile2.write('Hostname :' + str(hostname[0]) + '\n')
                tempfile2.write('Hardware version : ' + hwversion + '\n')
                tempfile2.write('Operating system : ' + ostype + '\n')
                tempfile2.write('Operating system version : ' + osversion + '\n')
                tempfile2.write('Management IP address : ' + item + '\n')
                tempfile2.write('Password : ' + item2 + '\n')

                connection.send('show diag\n')
                time.sleep(2)
                output1 = connection.recv(15000)
                modname = module_pattern.findall(output1)

                for i in (xrange(0, len(modname))):
                    print('Slot name   : ' + modname[i][0] + modname[i][1])
                    print('Slot status : ' + modname[i][3] + '\n')
                    tempfile2.write('Slot name   : ' + modname[i][0] + modname[i][1] + '\n')
                    tempfile2.write('Slot status : ' + modname[i][3] + '\n')
                    tempfile2.write('\n')

                connection.send('show cdp neighbors\n')
                time.sleep(1)
                output2 = connection.recv(4000)
                neighbors = neighbor_pattern.findall(output2)
                nghbrs = ','.join([str(d) for d in neighbors])

                print('Connected neighbors are : ' + nghbrs + '\n')
                tempfile2.write('Connected neighbors are : ' + nghbrs + '\n')

                connection.send('show interface description\n ')
                time.sleep(1)
                output3 = connection.recv(3000)
                print('Interface status and description')
                print('********************************\n')
                tempfile2.write('Interface status and description' + '\n')
                tempfile2.write('********************************\n' + '\n')
                interfaces = output3.split('\n')
                temp1 = interfaces[1:][:-1]
                interfaceinfo = []
                for line in temp1:
                    ints = interface_pattern.findall(line)
                    interfaceinfo = interfaceinfo + ints
                for i in (xrange(0, len(interfaceinfo))):
                    print('Interface name is :' + interfaceinfo[i][0])
                    print('Interface status is :' + interfaceinfo[i][1])
                    print('Interface protocol is :' + interfaceinfo[i][2])
                    print('Interface description is :' + interfaceinfo[i][3] + '\n')
                    tempfile2.write('Interface name is :' + interfaceinfo[i][0] + '\n')
                    tempfile2.write('Interface status is :' + interfaceinfo[i][1] + '\n')
                    tempfile2.write('Interface protocol is :' + interfaceinfo[i][2] + '\n')
                    tempfile2.write('Interface description is :' + interfaceinfo[i][3] + '\n')
                    tempfile2.write('\n')

                # Add adjacencies to the empty temporary file
                for i in neighbors:
                    tempfile1.write((str(hostname[0])) + ',' + i + '\n')

                session.close()

            except paramiko.ssh_exception.AuthenticationException:
                continue


networkscanner(range)
opensshcon(activeiplist, passwordlist)
tempfile1.close()
tempfile2.close()