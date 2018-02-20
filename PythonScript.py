import re
import paramiko
import time
import nmap


# Files used for this script
iprange = open('/root/Desktop/range.txt', 'r')
passlist = open('/home/debian/Desktop/Python Project Files/passwords.txt', 'r')
# An empty and temporary file that this script uses to denote adjacencies
tempfile = open('/home/debian/cdptempoutput.txt', 'w')

# Regular expressions needed for extracting necessary information from command outputs
version_pattern = re.compile('Version ([\d\w\(\)\.]+)')
os_pattern = re.compile('(NX\-OS|IOS|IOS\-XR)')
range_pattern = re.compile('(\d+.\d+.\d+.\d+\/\d+)')
hostname_pattern = re.compile('(.*#)')
neighbor_pattern = re.compile('(.*?)\..*')
modulename_pattern = re.compile('(NAME:.*?)\,')

# Get the range from range.txt file and add each range into a list
def getrange(iprange):
    range = []
    for line in iprange:
        iprange.readlines()
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
            print (nm[host].hostname())
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


#Main function for SSH connections, entering commands and returning their ouputs in required format
def opensshcon(activeiplist, passwordlist):
    for item in activeiplist:
        username = 'admin'
        for item2 in passwordlist:
            try:
                session = paramiko.SSHClient()
                session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                session.connect(item, username=username, password=item2)
                connection = session.invoke_shell()
                print('Interactive SSH Connection established')
                print('--------------------------------------\n')
                connection.send('terminal length 0\n')
                time.sleep(1)
                connection.send('show version\n')
                time.sleep(1)
                output = connection.recv(3000)
                hwversion = version_pattern.search(output).group(1)
                osversion = os_pattern.search(output).group(1)
                print('Operating system version is : ' + osversion)
                print('Hardware version is : ' + hwversion)
                print('Management IP address is : ' + item)
                print('Password is : ' + item2)
                connection.send('show inventory\n')
                time.sleep(1)
                output1 = connection.recv(6000)
                modname = modulename_pattern.findall(output1)
                modnamex = ','.join([str(a)[6:][1:][:-1] for a in modname])
                print('Modules are : ' + modnamex)
                connection.send('show cdp neighbors\n')
                time.sleep(1)
                output2 = connection.recv(4000)
                hostname = hostname_pattern.findall(output2)
                print('Hostname is : ' + str(hostname[0])[:-1])
                neighbors = neighbor_pattern.findall(output2)
                nghbrs = ','.join([str(d) for d in neighbors])
                print('Connected neighbors are : ' + nghbrs)
                connection.send('show interface description\n')
                time.sleep(1)
                output3 = connection.recv(1000)
                print('Interface status and descritpion')
                print('**************************************\n')
                interfaces = output3.split('\n')
                temp1 = interfaces[1:][:-1]
                for int in temp1:
                    print (int)

                print('++++++++++++++++++++++++++++++++++++++\n')
                # Adds adjacencies to the empty temporary file
                for i in neighbors:
                    tempfile.write((str(hostname[0])[:-1]) + ',' + i + '\n')

                session.close()

            except paramiko.ssh_exception.AuthenticationException:
                continue


networkscanner(range)
opensshcon(activeiplist, passwordlist)