#!/usr/bin/env python
"""
A Flickr tag bot
"""

import argparse
import flickrapi
import json
import logging as l
import os
import sys
import traceback

from myflickr import API_KEY, NAMESPACE_DEFAULT

SCRIPT_DESC = "poll machine tags from flickr"

def main ():
    """ Unleash the bot! """

    global args
    global l

    flickr = flickrapi.FlickrAPI(API_KEY)
    resp = flickr.machinetags_getPairs(namespace=args.namespace, format="json")
    if resp[:14] == "jsonFlickrApi(":
        jstr = resp[14:-1]
        j = json.loads(jstr)
        ptags = [(p['_content'], p['usage']) for p in j['pairs']['pair']]
        for ptag in ptags:
            print "%s is used on %s photos in Flickr" % ptag


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=SCRIPT_DESC, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument ("-n", "--namespace", default=NAMESPACE_DEFAULT, help="namespace to use in requesting machine tags")
        parser.add_argument ("-v", "--verbose", action="store_true", default=False, help="verbose output")
        args = parser.parse_args()
        if args.verbose:
            l.basicConfig(level=l.DEBUG)
        else:
            l.basicConfig(level=l.WARNING)
        main()
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print "ERROR, UNEXPECTED EXCEPTION"
        print str(e)
        traceback.print_exc()
        os._exit(1)
