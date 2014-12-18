

if __name__=="__main__":
    import modules.QA_Logger as QA_Logger
    LOG = QA_Logger.getLogger(name="feedmon")
    import modules.SimpleOptparse as SimpleOptparse
    from modules.feedmon import FeedMon
        
    
    optDef = {  
            (('--help',         '-h'),     "This help"):                                   False,
            (('--verbosity',    '-v'),     "Enable verbose output"):                       QA_Logger.QA_Logger.L_INFO,
            (('--rss-fields',   '-r'),     "restrict search to supplied fields only"):     "summary,summary_detail,title,title_detail",
            (('--rss-feeds',    '-f'),     "feed uris (feed1,feed2,...)"):                 "http://www.exploit-db.com/rss.xml,http://www.securiteam.com/securiteam.rss,http://www.securityfocus.com/rss/vulnerabilities.xml,http://seclists.org/rss/bugtraq.rss,http://seclists.org/rss/fulldisclosure.rss,http://rss.packetstormsecurity.com/files/,http://www.heise.de/security/news/news-atom.xml,http://feeds.feedburner.com/ZDI-Published-Advisories,http://feeds.feedburner.com/ZDI-Upcoming-Advisories,http://www.eeye.com/resources/media-center/rss?rss=Zero-Day-Tracker,http://www.cert.at/all.warnings.all.rss_2.0.xml,http://www.kb.cert.org/vulfeed",
            (('--hours',        '-s'),     "only check feeds newer than xx hours, default=disabled "):       0,
            (('--minutes',      '-m'),     "only check feeds newer than xx hours, default=disabled "):       0,
            (('--keywordsfile', '-x'),     "load keywords from file (NL separated)"):    None,
          }
    options,arguments=SimpleOptparse.parseOpts(optDef)
    LOG.setLevel(int(options['verbosity']))
        
    if not len(arguments):
        print "! - missing search keywords (arguments)"
        print SimpleOptparse.buildUsageString(optDef)
        exit()
        
    if options['rss-fields']:
        options['rss-fields']=options['rss-fields'].split(",")
        LOG.info("RSS-Fields set for scanning: %s"%options['rss-fields'])
    if options['rss-feeds']:
        options['rss-feeds']=options['rss-feeds'].split(",")
        LOG.info("RSS-Feeds: %s"%options['rss-feeds'])
    if options['keywordsfile']:
        f = open(options['keywordsfile'],'r')
        arguments = f.read().split('\n')
        f.close()

    # start the magic    
    fmon = FeedMon(hours=int(options['hours']),minutes=int(options['minutes']))
    
    fmon.addFeeds(options['rss-feeds'])
    fmon.fetch()            
    fmon.setMatchFields(options['rss-fields'])
    
    keywords = arguments
    
    warnings = 0
    LOG.debug("searching for keywords in rss feed entries...")
    for e in fmon.search(keywords): 
        warnings +=1
        LOG.warning(e)
    
    LOG.info("--DONE--")
    exit(warnings)
    
