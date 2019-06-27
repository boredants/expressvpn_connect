"""This script grabs a list of all the recommended Express VPN sites,
picks one at random and connects to it"""

import sys, time, subprocess, random, os.path as o
from insults import insults

path = '/usr/bin/expressvpn'

def main():
    """User makes choices here"""
    if o.exists(path):
        pass
    else:
        print('ExpressVPN is not installed.  Exiting...')
        time.sleep(1)
        sys.exit(2)

    print('ExpressVPN Connection Script')
    print('1.  Connect')
    print('2.  Disconnect')
    print('3.  Exit\n')

    choice = input('Choose an option number: ')

    if choice == '1':
        connect()
    elif choice == '2':
        disconnect()
    elif choice == '3':
        goodbye()
    else:
        print(choice + ' --- Really?')
        insults()
        sys.exit(5)

def connect():
    """The connect function - most of the heavy lifting"""
    output = subprocess.check_output("expressvpn status", shell=True)
    if "Connected to" in output.decode("utf-8"):
        print('You are currently connected...  Exiting...')
        time.sleep(1)
        sys.exit(3)
    else:
        #Get a list of all recommended sites
        vpnSites = subprocess.Popen(('expressvpn', 'list', 'all'), \
            stdout=subprocess.PIPE)
        vpnOutput = subprocess.check_output(('grep', 'Y$'), stdin=vpnSites.stdout)
        vpnSites.wait()

        #vpnoutput is returned as a byte value, so we have to decode it
        vpnDecoded = vpnOutput.decode("utf-8")

        #Create an empty list
        vpnList = []

        #Populate the list
        for line in vpnDecoded.split('\n'):
            vpnList.append(line)

        #Choose a random entry, split the line on a single-space character
        #and return the first element (the abbreviation for the site we
        #will connect to)
        vpnChoice = random.choice(vpnList).split(' ')[0]

        #Connect
        subprocess.call(['expressvpn', 'connect', vpnChoice])

def disconnect():
    """The disconnect function"""
    output = subprocess.check_output("expressvpn status", shell=True)
    if "Not" in output.decode("utf-8"):
        print('You are not currently connected...  Exiting...')
        time.sleep(1)
        sys.exit(4)
    else:
        subprocess.call(['expressvpn', 'disconnect'])
        time.sleep(1)
        sys.exit(0)

def goodbye():
    """Saying goodbye"""
    time.sleep(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
