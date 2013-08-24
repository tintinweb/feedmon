FeedMon
=======

monitor rss/atom feeds for specified keywords

will scan a set of security related rss-feeds by default. See usage.


Dependencies
============
* feedparser (https://code.google.com/p/feedparser/)
* Future-Threads (http://code.activestate.com/recipes/84317/)


Usage
=====


	! - missing search keywords (arguments)
	
		
	Usage: main.py  [OPTIONS] [Argument(s) ...]
	
	Mandatory arguments to long options are mandatory for short options too.
	
	  -r <value>, --rss-fields=<value>           restrict search to supplied fields only.
	                                             *** DEFAULT='summary,summary_detail,title,title_detail'
	  -f <value>, --rss-feeds=<value>            feed uris (feed1,feed2,...).
	                                             *** DEFAULT='http://www.exploit-db.com/rss.xml,http://www.securiteam.com/securiteam.rss,http://www.securityfocus.com/rss/vulnerabilities.xml,http://seclists.org/rss/bugtraq.rss,http://seclists.org/rss/fulldisclosure.rss,http://rss.packetstormsecurity.com/files/,http://feeds.feedburner.com/ZDI-Published-Advisories,http://feeds.feedburner.com/ZDI-Upcoming-Advisories,http://www.eeye.com/resources/media-center/rss?rss=Zero-Day-Tracker,http://www.cert.at/all.warnings.all.rss_2.0.xml,http://www.kb.cert.org/vulfeed'
	  -h,         --help                         This help.
	  -v <value>, --verbosity=<value>            Enable verbose output.
	                                             *** DEFAULT='20'
	                                             
	                                             
Use-Cases
=========

Search security feeds for 'kernel','squid'

	#> main.py kernel squid
	
Search specific rss feeds for 'kernel'

	#> main.py --rss-feeds=http://myownfeed.com/rss kernel

