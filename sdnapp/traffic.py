import sys
import json
import os

W1="192.168.1.2"
W2="192.168.2.2"
W3="192.168.3.2"
W4="192.168.4.2"

E1="192.168.1.1"
E2="192.168.2.1"
E3="192.168.3.1"
E4="192.168.4.1"


# 1 for VoIP
# 2 for UDP
# 3 for tcp



#call code using python GenerateTraffic.py C/S(client/server) ipaddress Type
#Info for iperf:
# TCP and UDP tests
# Set port (-p)
# Setting TCP options: No delay, MSS, etc.
# Setting UDP bandwidth (-b)
# Setting socket buffer size (-w)
# Reporting intervals (-i)
# Setting the iPerf buffer (-l)
# Bind to specific interfaces (-B)
# IPv6 tests (-6)
# Number of bytes to transmit (-n)
# Length of test (-t)
# Parallel streams (-P)
# Setting DSCP/TOS bit vectors (-S)
# Change number output format (-f)

def VOIP(site,ipaddress):
    if site == 'client':
        os.system("iperf -c "+ ipaddress +" -u  -mss 160 -b 65000 -f -b 65000 -S 184 -P 4 -fk -i 10 -t 300")
    else:
        os.system("iperf -s -u -b 65000 -S 184 -P 4 -fk -i 10")
    return


def SystemBackUps(site,ipaddress):
    if site == 'client':
        os.system("iperf -c "+ipaddress+" -w 6000")
    else:
        os.system("iperf -s -w 10000")
    return


def Gaming(site,ipaddress):
    if site == 'client':
        os.system("iperf -c "+ipaddress+" -u -b 10m")
    else:
        os.system("iperf -s -u -i 1")
    return

def address(ipaddress):
    if ipaddress == 'E1':
        return E1;
    elif ipaddress == 'E2':
        return E2;
    elif ipaddress == 'E3':
        return E3;
    elif ipaddress == 'E4':
        return E4;
    elif ipaddress == 'W1':
        return  W1;
    elif ipaddress == 'W2':
        return W2;
    elif ipaddress == 'W3':
        return W3;
    elif ipaddress == 'W4':
        return W4;

ipToLsp= {
    "192.168.1.1" : 'GROUP_EIGHT_NY_SF_LSP1',
    "192.168.2.1" : 'GROUP_EIGHT_NY_SF_LSP2',
    "192.168.3.1" : 'GROUP_EIGHT_NY_SF_LSP3',
    "192.168.4.1" : 'GROUP_EIGHT_NY_SF_LSP4',
    "192.168.1.2" : 'GROUP_EIGHT_SF_NY_LSP1',
    "192.168.2.2" : 'GROUP_EIGHT_SF_NY_LSP2',
    "192.168.3.2" : 'GROUP_EIGHT_SF_NY_LSP3',
    "192.168.4.2" : 'GROUP_EIGHT_SF_NY_LSP4',
}

routes= {
    'GROUP_EIGHT_NY_SF_LSP1' : ['new york','miami','chicago','san francisco'],
    'GROUP_EIGHT_NY_SF_LSP2' : ['new york','miami','chicago','dallas','san francisco'],
    'GROUP_EIGHT_NY_SF_LSP3' : ['new york','chicago','','dallas','san francisco'],
    'GROUP_EIGHT_NY_SF_LSP4' : ['new york','miami','dallas','san francisco'],
    'GROUP_EIGHT_SF_NY_LSP1' : ['san francisco','chicago','new york'],
    'GROUP_EIGHT_SF_NY_LSP2' : ['san francisco','dallas','miami','new york'],
    'GROUP_EIGHT_SF_NY_LSP3' : ['san francisco','houston','tampa','new york'],
    'GROUP_EIGHT_SF_NY_LSP4' : ['san francisco','dallas','chicago','new york']
}

def writelspjson():
    jsonobj = []

    lspdict = {}
    for key in routes:
        #print key,
        value = {}
        value['flow'] = "off"
        value['traffic'] = "video"
        value['path'] = routes[key]
        #print value
        lspdict[key] = value;
    print lspdict
        #jsonobj.append(lspdict)

    with open('static/lspinfo.json', 'w') as outfile:
        json.dump(lspdict, outfile)

'''
    jsondict = [{'name' : 'GROUP_EIGHT_NY_SF_LSP3',
                'flow' : 'off',
                'traffic' : 'video',
                'path' : routes['GROUP_EIGHT_NY_SF_LSP3']}]
'''

if __name__ == "__main__":

    writelspjson();

    site = sys.argv[1];
    ip = sys.argv[2];
    traffic = sys.argv[3];

    #print ipToLsp[ip]
    #print traffic

    if (sys.argv[1])=="voip" :
            VOIP(sys.argv[2],address(sys.argv[3]));
    elif (sys.argv[1])=="video" :
            SystemBackUps(sys.argv[2],address(sys.argv[3]));
    elif (sys.argv[1])=="gaming" :
            Gaming(sys.argv[2],address(sys.argv[3]));
