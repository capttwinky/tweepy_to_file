#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  twtofile.py
#

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from ssl import SSLError

import json
import os

class ToFileListener(StreamListener):
    """ A listener handles tweets that are received from the stream. 
    This listener writes the json encoded tweets to a given file and 
    prints the count of stored tweets on stdout.
    """
    def __init__(self, fname, truncate = False):
        ''' fname = string file path and name to write to
            truncate = integer, if set, return at most this number of 
                lines from the end of the file          
        '''
        self.fname = fname
        if os.path.exists(self.fname):
            with open(self.fname) as ofile:
                strw = [line for line in ofile.readlines() if line]
        if truncate is not False and isinstance(truncate, int):
            if truncate == 0 or truncate is True:
                strw = ''
            else:
                strw = strw[:-1*truncate]
            with open(self.fname,'w') as wfile:
                wfile.write(''.join(strw))
        self.cntr = len(strw)

    def on_data(self, data):
        with open(self.fname,'a') as wfile:
            wfile.write('{0}\n'.format(data))
        self.cntr +=1
        print self.cntr
        return True

    def on_error(self, status):
        print status


def filtertofile(fname, to_track, oauth_data):
    ''' fname := name of file to output json data to
    to_track := actual query to write result of
    oauth_data := https://dev.twitter.com/docs/auth/obtaining-access-tokens
    
    '''
    if not hasattr(to_track,'append'):
        to_track = [str(to_track)]
    l = ToFileListener(fname)
    auth = OAuthHandler(oauth_data['consumer_key'], oauth_data['consumer_secret'])
    auth.set_access_token(oauth_data['access_token'], oauth_data['access_token_secret'])
    keep_going = True
    while keep_going:
        try:
            print 'startloop!'
            stream = Stream(auth, l)    
            stream.filter(track=to_track)
        except SSLError as e:
            print 'timeout!'
        except Exception as e:
            keep_going = False
            raise e

if __name__ == '__main__':
    '''oauth_data.json  := 
    {'consumer_key':'xxxxxxxxx',
     'consumer_secret':'xxxxxxxxx',
     'access_token':'xxxxxxxxx',
     'access_token_secret':'xxxxxxxxx'}
     with values obtained from following instructions on 
     https://dev.twitter.com/docs/auth/obtaining-access-tokens
     
     haiku search and haiku.json output files are obviously just examples.
     
     '''
        
    with open('oauth_data.json') as ofile:
        oauth_data = json.loads(ofile.read())
        
    filtertofile('haiku.json','haiku',oauth_data)
