#!/usr/local/bin/python3

'''
Program Name:   Refresher

Synopsis: Program is used to automate the change to the dynamic IP address set within .ovpn files.

Functionality:

    (1) Pull the current public IPv4 address on your network
    (2) Compare the pull address with the address in each .ovpn file
    (3) If different, change the address
    (4) Send an email to user with the new updated files attached

Requirements:

    (1) Request module to download webpages
    (2) Beautifulsoup modules to parse through webpage
    (3) Command Line argument to specify email address
    (4) Modify files and save updated version
    (5) Possible modules to send an email to the user with attached files

Usage: ./refresher.py -r user@example.com
Required:
-r:         Recipient Address
'''

import sys
import getopt
import bs4
import requests
import os
import re

commands = ["-r"]

recipient_address = ""
public_address = ""
current_address = ""

'''Prints out the usage of the program to the user'''
def usage():
    print("Usage:   ./refresher.py -r user@example.com")
    print("Required:")
    print("-r:      Recipient Address")
    print("")
    sys.exit()

'''Gathers command line argument'''
def options(arguments):

    global recipient_address

    try:
        opts, args = getopt.getopt(arguments[1], "-r")
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for opt in args:
        if opt == "-r":
            recipient_address = args

'''Function will pull IPv4 address and configure variable for address'''
def public_pull():

    global public_address

    response = requests.get("https://www.iplocation.net/find-ip-address")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    address_element = soup.select("div > div > div > div > div > p > span")
    public_address = str(address_element[0].getText())

'''Function wll now find all .ovpn files and store them in an array to be opened'''
def find_ovpn():

    ovpn_file = []

    # Running system command to find all files
    os.system("find / -type f | grep \".ovpn\" > output.txt")
    file = open("output.txt", "r")
    open_file = file.readlines()

    # Appending each line of the file to the array
    for line in open_file:
        ovpn_file.append(line)

    # This will remove the output file generated and also close the file
    os.system("rm -f output.txt")
    file.close()

    return ovpn_file

'''Function will find address regex within the objects'''
def expression_checker(object):

    global current_address

    # Building regex to search for "remote x.x.x.x 1194"
    address_regex = re.compile(r"(remote)\s(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s(1194)")
    search = address_regex.search(object)

    # Sets the current address found
    current_address = search.group(2)

    # Checks to see if current address is different from public
    if current_address != public_address:
        return True
    return False

'''Function to email user with the updated files'''
def email_me(attachments):





def main():

    public_pull()
    #options(sys.argv)

   # if len(sys.argv) < 2:
    #    usage()

    files = find_ovpn()

    for file in files:
        if expression_checker(open(file.rstrip("\n"),"r").read()):
            os.system("sed -i \"s/remote %s 1194/remote %s 1194/g\" %s" %(current_address, public_address, file))


#main()