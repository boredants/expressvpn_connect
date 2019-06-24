"""This script grabs a list of all the recommended Express VPN sites,
picks one at random and connects to it"""

import sys, time, subprocess, random
from insults import insults

def main():
    """User makes choices here"""
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

def connect():
    """The connect function - most of the heavy lifting"""
    output = subprocess.check_output("expressvpn status", shell=True)
    if "Connected to" in output.decode("utf-8"):
        print('You are currently connected...  Exiting...')
        time.sleep(1)
        sys.exit()
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

        #Another way
        #Build the connection string for the  final subprocess call
        #args = 'expressvpn connect ' + vpnChoice
        #Connect
        #subprocess.call(args, shell=True)

def disconnect():
    """The disconnect function"""
    output = subprocess.check_output("expressvpn status", shell=True)
    if "Not" in output.decode("utf-8"):
        print('You are not currently connected...  Exiting...')
        time.sleep(1)
        sys.exit()
    else:
        subprocess.call(['expressvpn', 'disconnect'])
        time.sleep(1)
        sys.exit()

def goodbye():
    """Saying goodbye"""
    time.sleep(1)
    sys.exit()

if __name__ == "__main__":
    main()

#output = subprocess.check_output("expressvpn status", shell=True)
#if "Not" in output.decode("utf-8"):
#    print("You are not connected.")