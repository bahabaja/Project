import paramiko
import time
import nmap

iprange = open('/root/Desktop/range.txt', 'r')
range = str(iprange.readline())

def networkscanner(range):
    nm = nmap.PortScanner()
    activeiplist = []
    nm.scan(range,'22')

    for item in nm.all_hosts():
        x = nm[item].state()
        if ( x == 'up'):
            activeiplist.append(item)
        return (activeiplist)

activeiplist = networkscanner(range)

def opensshcon(activeiplist):
    try :
        for item in activeiplist:
            username = 'admin'
            password = 'cisco'
            session = paramiko.SSHClient()
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            session.connect(item , username = username, password = password)
            connection = session.invoke_shell()
            connection.send('terminal length 0\n')
            time.sleep(1)
            connection.send('show ip interface brief\n')
            time.sleep(1)
            output = connection.recv(1000)
            print ( output + '\n')
            session.close()
    except paramiko.AuthenticationException:
        print ('Invalid username or password')

networkscanner(range)
opensshcon(activeiplist)