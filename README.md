FeedMon
=======

monitor rss/atom feeds for specified keywords

will scan a set of security related rss-feeds by default. See usage.


Purpose: spot vulnerabilities/exploits for installed software early. E.g. feed dpkg --get-selections (debian) as a comma separated list to feedmon.



Dependencies
============
* feedparser (https://code.google.com/p/feedparser/)
* Future-Threads (http://code.activestate.com/recipes/84317/)


Usage
=====

	! - missing search keywords (arguments)
	
	
	Usage: feedmon.py  [OPTIONS] [Argument(s) ...]
	
	Mandatory arguments to long options are mandatory for short options too.
	
	  -r <value>, --rss-fields=<value>           restrict search to supplied fields only.
	                                             *** DEFAULT='summary,summary_detail,title,title_detail'
	  -f <value>, --rss-feeds=<value>            feed uris (feed1,feed2,...).
	                                             *** DEFAULT='http://www.exploit-db.com/rss.xml,http://www.securiteam.com/securiteam.rss,http://www             .securityfocus.com/rss/vulnerabilities.xml,http://seclists.org/rss/bugtraq.rss,http://seclists.org/rss/fulldisclosure.rss,http://rss.packetstor             msecurity.com/files/,http://www.heise.de/security/news/news-atom.xml,http://feeds.feedburner.com/ZDI-Published-Advisories,http://feeds.feedburn             er.com/ZDI-Upcoming-Advisories,http://www.eeye.com/resources/media-center/rss?rss=Zero-Day-Tracker,http://www.cert.at/all.warnings.all.rss_2.0.             xml,http://www.kb.cert.org/vulfeed'
	  -h,         --help                         This help.
	  -x <value>, --keywordsfile=<value>         load keywords from file (NL separated).
	                                             *** DEFAULT='None'
	  -s <value>, --hours=<value>                only check feeds newer than xx hours .
	                                             *** DEFAULT='96'
	  -v <value>, --verbosity=<value>            Enable verbose output.
	                                             *** DEFAULT='20'
	  -m,         --minutes                      only check feeds newer than xx hours .
	

	                                             
	                                             
Use-Cases
=========

Search security feeds for 'kernel','squid'

	#> feedmon.py kernel squid
	
	[2013-08-25 01:21:00,931] INFO - RSS-Fields set for scanning: ['summary', 'summary_detail', 'title', 'title_detail'] 
	[2013-08-25 01:21:00,931] INFO - RSS-Feeds: ['http://www.exploit-db.com/rss.xml', 'http://www.securiteam.com/securiteam.rss', 'http://www.securityfocus.com/rss/vulnerabilities.xml', 'http://seclists.org/rss/bugtraq.rss', 'http://seclists.org/rss/fulldisclosure.rss', 'http://rss.packetstormsecurity.com/files/', 'http://www.heise.de/security/news/news-atom.xml', 'http://feeds.feedburner.com/ZDI-Published-Advisories', 'http://feeds.feedburner.com/ZDI-Upcoming-Advisories', 'http://www.eeye.com/resources/media-center/rss?rss=Zero-Day-Tracker', 'http://www.cert.at/all.warnings.all.rss_2.0.xml', 'http://www.kb.cert.org/vulfeed'] 
	[2013-08-25 01:21:11,128] WARNING - {'summary_detail': {'base': u'http://www.securiteam.com/securiteam.rss', 'type': u'text/html', 'language': None, 'value': u'Microsoft windows kernel unspecified memory object handling race condition local privilege escalation (2013-1294) vulnerability.'}, 'published_parsed': time.struct_time(tm_year=2013, tm_mon=7, tm_mday=4, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=185, tm_isdst=0), 'links': [{'href': u'http://www.securiteam.com/windowsntfocus/5TP2W15ALA.html', 'type': u'text/html', 'rel': u'alternate'}], 'title': u'Microsoft Windows Kernel  Memory Object Handling Race Condition Local Privilege Escalation (2013-1294) Vulnerability', 'summary': u'Microsoft windows kernel unspecified memory object handling race condition local privilege escalation (2013-1294) vulnerability.', 'guidislink': False, 'title_detail': {'base': u'http://www.securiteam.com/securiteam.rss', 'type': u'text/plain', 'language': None, 'value': u'Microsoft Windows Kernel  Memory Object Handling Race Condition Local Privilege Escalation (2013-1294) Vulnerability'}, 'link': u'http://www.securiteam.com/windowsntfocus/5TP2W15ALA.html', 'published': u'Thu, 04 Jul 2013 00:00 GMT', 'id': u'http://www.securiteam.com/windowsntfocus/5TP2W15ALA.html'} 
	[2013-08-25 01:21:11,128] WARNING - {'summary_detail': {'base': u'http://www.securityfocus.com/rss/vulnerabilities.xml', 'type': u'text/html', 'language': None, 'value': u"Linux Kernel 'mmc_ioctl_cdrom_read_data()' Function Local Information Disclosure Vulnerability"}, 'published_parsed': time.struct_time(tm_year=2013, tm_mon=8, tm_mday=24, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=5, tm_yday=236, tm_isdst=0), 'links': [{'href': u'http://www.securityfocus.com/bid/60375', 'type': u'text/html', 'rel': u'alternate'}], 'title': u"Vuln: Linux Kernel 'mmc_ioctl_cdrom_read_data()' Function Local Information Disclosure Vulnerability", 'summary': u"Linux Kernel 'mmc_ioctl_cdrom_read_data()' Function Local Information Disclosure Vulnerability", 'title_detail': {'base': u'http://www.securityfocus.com/rss/vulnerabilities.xml', 'type': u'text/plain', 'language': None, 'value': u"Vuln: Linux Kernel 'mmc_ioctl_cdrom_read_data()' Function Local Information Disclosure Vulnerability"}, 'link': u'http://www.securityfocus.com/bid/60375', 'published': u'2013-08-24'} 
	[2013-08-25 01:21:11,135] WARNING - {'summary_detail': {'base': u'http://rss.packetstormsecurity.com/files/', 'type': u'text/html', 'language': None, 'value': u'FreeBSD Security Advisory - When initializing the SCTP state cookie being sent in INIT-ACK chunks, a buffer allocated from the kernel stack is not completely initialized. Fragments of kernel memory may be included in SCTP packets and transmitted over the network. For each SCTP session, there are two separate instances in which a 4-byte fragment may be transmitted. This memory might contain sensitive information, such as portions of the file cache or terminal buffers. This information might be directly useful, or it might be leveraged to obtain elevated privileges in some way. For example, a terminal buffer might include an user-entered password.'}, 'published_parsed': time.struct_time(tm_year=2013, tm_mon=8, tm_mday=23, tm_hour=23, tm_min=59, tm_sec=22, tm_wday=4, tm_yday=235, tm_isdst=0), 'links': [{'href': u'http://packetstormsecurity.com/files/122933/FreeBSD-SA-13.10.sctp.txt', 'type': u'text/html', 'rel': u'alternate'}], 'tags': [], 'title': u'FreeBSD Security Advisory - sctp Kernel Memory Disclosure', 'comments': u'http://packetstormsecurity.com/files/122933/FreeBSD-Security-Advisory-sctp-Kernel-Memory-Disclosure.html', 'summary': u'FreeBSD Security Advisory - When initializing the SCTP state cookie being sent in INIT-ACK chunks, a buffer allocated from the kernel stack is not completely initialized. Fragments of kernel memory may be included in SCTP packets and transmitted over the network. For each SCTP session, there are two separate instances in which a 4-byte fragment may be transmitted. This memory might contain sensitive information, such as portions of the file cache or terminal buffers. This information might be directly useful, or it might be leveraged to obtain elevated privileges in some way. For example, a terminal buffer might include an user-entered password.', 'guidislink': False, 'title_detail': {'base': u'http://rss.packetstormsecurity.com/files/', 'type': u'text/plain', 'language': None, 'value': u'FreeBSD Security Advisory - sctp Kernel Memory Disclosure'}, 'link': u'http://packetstormsecurity.com/files/122933/FreeBSD-SA-13.10.sctp.txt', 'published': u'Fri, 23 Aug 2013 23:59:22 GMT', 'id': u'http://packetstormsecurity.com/files/122933/FreeBSD-SA-13.10.sctp.txt'} 
	[2013-08-25 01:21:11,135] WARNING - {'summary_detail': {'base': u'http://www.eeye.com/resources/media-center/rss?rss=Zero-Day-Tracker', 'type': u'text/html', 'language': None, 'value': u'Symantec Backup Exec System Recovery contains a vulnerability in the way the CD/DVD driver present in GEARAspiWDM.sys handles IOCTL inputs.  Successful exploitation may result in remote code execution.'}, 'links': [{'href': u'http://www.eeye.com/resources/security-center/research/zero-day-tracker/2011/17273', 'type': u'text/html', 'rel': u'alternate'}], 'published_parsed': time.struct_time(tm_year=2011, tm_mon=5, tm_mday=12, tm_hour=7, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=132, tm_isdst=0), 'title': u'Symantec Backup Exec System Recovery 8.5 Kernel Pointer Dereference', 'summary': u'Symantec Backup Exec System Recovery contains a vulnerability in the way the CD/DVD driver present in GEARAspiWDM.sys handles IOCTL inputs.  Successful exploitation may result in remote code execution.', 'guidislink': False, 'title_detail': {'base': u'http://www.eeye.com/resources/media-center/rss?rss=Zero-Day-Tracker', 'type': u'text/plain', 'language': None, 'value': u'Symantec Backup Exec System Recovery 8.5 Kernel Pointer Dereference'}, 'link': u'http://www.eeye.com/resources/security-center/research/zero-day-tracker/2011/17273', 'published': u'Thu, 12 May 2011 07:00:00 GMT', 'id': u'http://www.eeye.com/resources/security-center/research/zero-day-tracker/2011/17273'} 
	[2013-08-25 01:21:11,141] WARNING - {'summary_detail': {'base': u'http://www.eeye.com/resources/media-center/rss?rss=Zero-Day-Tracker', 'type': u'text/html', 'language': None, 'value': u'Trend Micro Maximum Security 2011 contains a local privilege escalation vulnerability that is caused by a pointer overwrite vulnerability. This could be leveraged to allow an attacker to gain kernel-level privileges and execute arbitrary code.'}, 'links': [{'href': u'http://www.eeye.com/resources/security-center/research/zero-day-tracker/2010/20101102', 'type': u'text/html', 'rel': u'alternate'}], 'published_parsed': time.struct_time(tm_year=2010, tm_mon=11, tm_mday=2, tm_hour=7, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=306, tm_isdst=0), 'title': u'Trend Micro Titanium Maximum Security 2011 Local Kernel Level Privilege Escalation', 'summary': u'Trend Micro Maximum Security 2011 contains a local privilege escalation vulnerability that is caused by a pointer overwrite vulnerability. This could be leveraged to allow an attacker to gain kernel-level privileges and execute arbitrary code.', 'guidislink': False, 'title_detail': {'base': u'http://www.eeye.com/resources/media-center/rss?rss=Zero-Day-Tracker', 'type': u'text/plain', 'language': None, 'value': u'Trend Micro Titanium Maximum Security 2011 Local Kernel Level Privilege Escalation'}, 'link': u'http://www.eeye.com/resources/security-center/research/zero-day-tracker/2010/20101102', 'published': u'Tue, 02 Nov 2010 07:00:00 GMT', 'id': u'http://www.eeye.com/resources/security-center/research/zero-day-tracker/2010/20101102'} 
	[2013-08-25 01:21:11,142] INFO - --DONE-- 
		
	
Search specific rss feeds for 'kernel'

	#> feedmon.py --rss-feeds=http://myownfeed.com/rss kernel

