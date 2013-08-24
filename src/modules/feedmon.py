'''
Created on 24.08.2013

@author: tintin
'''
from feedparser import feedparser
from future.Future import Future
import pprint

class FeedMon(object):
    
    def __init__(self,feeds={},match_fields=[]):
        self.feeds=feeds
        self.match_fields=match_fields
    
    def addFeed(self,name,uri):
        self.feeds[name]=uri
        
    def addFeeds(self,var):
        if isinstance(var,list):
            new_feeds = dict(zip(range(len(var)),var))
        elif isinstance(var,dict):
            pass
        elif isinstance(var,basestring):
            new_feeds={'str_0',var}
        else:
            raise Exception("incompatible feed var: %s"%repr(var))
            
        self.feeds.update(new_feeds)
        
    def fetch(self):
        future_calls = [Future(feedparser.parse,rss_url) for rss_url in self.feeds.values()]
        feeds = [future_obj() for future_obj in future_calls]
        entries = []
        for feed in feeds:
            entries.extend( feed[ "items" ] )
        self.feedentries=entries
        
        return self.entries()
    
    def entries(self):
        for e in self.feedentries:
            yield e
            
    def sort(self):
        sorted_entries = sorted(self.feedentries, key=lambda entry: entry["updated"])
        sorted_entries.reverse() # for most recent entries first
    
    
    def setMatchFields(self,lst):
        """provide a list of rss feed keys to match on __contains__ (in) otherwise match all (slow)"""
        self.match_fields.extend(lst)
                    
    def __str__(self):
        return "\n".join( [str(e) for e in self.feedentries])
    
    def __repr__(self):
        return pprint.pformat(self.feedentries)
    
    def extract_fields(self, fields):
        res = []
        for i,e in enumerate(self.feedentries):
            # get all matching fields for this entry
            res_d = {}
            for extract_field in [f for f in fields if e.has_key(f)]:
                res_d[extract_field]=e[f]
            res_d['id']=i
            res.append(res_d)
        return res
            
    
    def __contains__(self, needle):
        return len(self.search(needle))
   
    def _search(self,needle,haystack):
        if isinstance(needle,basestring):
            needle=[needle]
        
        return [e for e in haystack if any(n in str(e).lower() for n in needle )]
          
    def search(self,needle, haystack=None): 
        haystack = haystack or self.feedentries
        if len(self.match_fields):
            haystack = self.extract_fields(self.match_fields)
            results = self._search(needle, haystack)
            # get original entries from search (note extract_fields adds an 'id' key to the resulting dict with the corresponding feedentries id
            return [ self.feedentries[e['id']] for e in results if e.has_key('id')]
        
        return self._search(needle, haystack)
    
     

if __name__=="__main__":
        
    feeder = FeedMon()
    
    feeds = ["http://www.exploit-db.com/rss.xml",
             "http://www.securiteam.com/securiteam.rss",
             "http://www.securityfocus.com/rss/vulnerabilities.xml",
             "http://seclists.org/rss/bugtraq.rss",
             ] 
    feeder.addFeeds(feeds)
    feeder.fetch()            
    feeder.setMatchFields(['summary','summary_detail','title','title_detail'])
    print "kernel" in feeder
    for e in feeder.search("kernel"): print e