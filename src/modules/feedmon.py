'''
Created on 24.08.2013

@author: tintin
'''
from feedparser import feedparser
from future.Future import Future
import pprint
import datetime
import modules.QA_Logger as QA_Logger
LOG = QA_Logger.getLogger(name="feedmon")

class FeedMon(object):
    
    def __init__(self,feeds={},match_fields=[],hours=0, minutes=0):
        self.feeds=feeds
        self.match_fields=match_fields
        self.hours=hours
        self.minutes=minutes
    
    def addFeed(self,name,uri):
        LOG.debug("FeedMon - addFeed - %s:%s"%(name,uri))
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
        LOG.debug("FeedMon - fetch()")
        hours=self.hours
        minutes=self.minutes
        now = datetime.datetime.now()
        dt_now = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
        future_calls = [Future(feedparser.parse,rss_url) for rss_url in self.feeds.values()]
        entries = []
        feed=None
        for future_obj in future_calls:
            try:
                feed = future_obj()
                LOG.debug("* fetching %s"%feed.href)
                # check feed date
                if hours or minutes:
                    feed_last_update = feed.get("updated_parsed") or feed.get('feed',{}).get("updated_parsed")
                    feed_last_update = datetime.datetime(feed_last_update.tm_year, feed_last_update.tm_mon, feed_last_update.tm_mday, feed_last_update.tm_hour, feed_last_update.tm_min)
                    if (dt_now-feed_last_update) > datetime.timedelta(minutes=minutes,hours=hours):
                        LOG.info("skipping %s - not within timespan (%s:%s)"%(feed.href,hours, minutes))
                        continue
                # check entries date
                filtered_feed = []
                for f in feed['items']:
                    if hours or minutes:
                        e_published =f.get('published_parsed')
                        if e_published:
                            # check published date if available
                            e_published = datetime.datetime(e_published.tm_year, e_published.tm_mon, e_published.tm_mday, e_published.tm_hour, e_published.tm_min)
                            if (dt_now-e_published) > datetime.timedelta(minutes=minutes,hours=hours):
                                continue
                    filtered_feed.append(f) 
                entries.extend( filtered_feed )
            except TypeError, te:
                LOG.error("failed to load rss feed: %s"%feed.href)
                LOG.debug(repr(te))
 
        self.feedentries=entries
        LOG.debug("FeedMon - fetch() - Done!")
        return self.entries()
    
    def entries(self):
        for e in self.feedentries:
            yield e
    
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
        # split needl by " AND " and make sure all phrases in the AND line match within one entry
        return [e for e in haystack if any( all(ph.lower() in str(e).lower() for ph in n.split(" AND ") ) for n in needle )]
          
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