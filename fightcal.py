from lxml import html
import requests
import praw
import HTMLParser
import re
from ConfigParser import SafeConfigParser
import sys, os
import time

def postcal():
    
    # load config file
    containing_dir = os.path.abspath(os.path.dirname(sys.argv[0]))	
    cfg_file = SafeConfigParser()
    path_to_cfg = os.path.join(containing_dir, 'fightcal.cfg')
    cfg_file.read(path_to_cfg)

    # log into reddit
    print 'logging in...'
    r = praw.Reddit(user_agent=cfg_file.get('reddit', 'user_agent'))
    r.login(cfg_file.get('reddit', 'username'), cfg_file.get('reddit', 'password'))
	
    # get subreddit
    subreddit = r.get_subreddit('XXX')

    # Shedog calender URL
    page = requests.get('http://www.sherdog.com/events/')

    # creates a list of events:
    print 'scraping'
    tree = html.fromstring(page.text)
    ufc_month = tree.xpath('//*[@id="ufc_tab"]/ul[2]/li/a/span/span[@class="month"]/text()')	
    ufc_day = tree.xpath('//*[@id="ufc_tab"]/ul[2]/li/a/span/span[@class="day"]/text()')
    ufc_event = tree.xpath('//*[@id="ufc_tab"]/ul[2]/li/a/text()[2]')
    ufc_link = tree.xpath('//*[@id="ufc_tab"]/ul[2]/li/a/@href')
    bellator_month = tree.xpath('//*[@id="bellator_tab"]/ul[2]/li/a/span/span[@class="month"]/text()')	
    bellator_day = tree.xpath('//*[@id="bellator_tab"]/ul[2]/li/a/span/span[@class="day"]/text()')
    bellator_event = tree.xpath('//*[@id="bellator_tab"]/ul[2]/li/a/text()[2]')
    bellator_link = tree.xpath('//*[@id="bellator_tab"]/ul[2]/li/a/@href')	
    wsof_month = tree.xpath('//*[@id="wsof_tab"]/ul[2]/li/a/span/span[@class="month"]/text()')	
    wsof_day = tree.xpath('//*[@id="wsof_tab"]/ul[2]/li/a/span/span[@class="day"]/text()')
    wsof_event = tree.xpath('//*[@id="wsof_tab"]/ul[2]/li/a/text()[2]')
    wsof_link = tree.xpath('//*[@id="wsof_tab"]/ul[2]/li/a/@href')	
    
    # organizes lists of events with formatting:
    print 'organizing...'
    merged_list = "* Event Calendar"
    
    merged_list = merged_list + "\n* **UFC**" 
    merged_list = merged_list + "\n* " + ufc_month[0] + " " + ufc_day[0] + ": " + "[" + ufc_event[0].strip() + "](//sherdog.com" + ufc_link[0] + ")"
    merged_list = merged_list + "\n* " + ufc_month[1] + " " + ufc_day[1] + ": " + "[" + ufc_event[1].strip() + "](//sherdog.com" + ufc_link[1] + ")"

    merged_list = merged_list + "\n* **Bellator**"    
    merged_list = merged_list + "\n* " + bellator_month[0] + " " + bellator_day[0] + ": " + "[" + bellator_event[0].strip() + "](//sherdog.com" + bellator_link[0] + ")"	
    merged_list = merged_list + "\n* " + bellator_month[1] + " " + bellator_day[1] + ": " + "[" + bellator_event[1].strip() + "](//sherdog.com" + bellator_link[1] + ")"	

    merged_list = merged_list + "\n* **WSOF**" 
    merged_list = merged_list + "\n* " + wsof_month[0] + " " + wsof_day[0] + ": " + "[" + wsof_event[0].strip() + "](//sherdog.com" + wsof_link[0] + ")"		
    merged_list = merged_list + "\n* " + wsof_month[1] + " " + wsof_day[1] + ": " + "[" + wsof_event[1].strip() + "](//sherdog.com" + wsof_link[1] + ")"

    merged_list = merged_list + "\n* ^Last ^updated ^" + (time.strftime("%m/%d")) + " ^@ ^" + (time.strftime("%H:%M:%S"))

    # uncomment to print list in console for testing
    #print merged_list
    
    # delimiters
    start_delimiter = "[](/start)"
    end_delimiter = "[](/end)"
											
    # parse and replace sidebar contents
    print 'parsing...'
    current_sidebar = subreddit.get_settings()['description']
    current_sidebar = HTMLParser.HTMLParser().unescape(current_sidebar)
    replace_pattern = re.compile('%s.*?%s' % (re.escape(cfg_file.get('reddit', 'start_delimiter')), re.escape(cfg_file.get('reddit', 'end_delimiter'))), re.IGNORECASE|re.DOTALL|re.UNICODE)
    new_sidebar = re.sub(replace_pattern,
					    '%s\\n\\n%s\\n%s' % (cfg_file.get('reddit', 'start_delimiter'), merged_list, cfg_file.get('reddit', 'end_delimiter')),
					    current_sidebar)
    # updates sidebar contents
    print 'posting...'
    subreddit.update_settings(description=new_sidebar)
	
    # uncomment to print edited sidebar in console for testing
    #print new_sidebar  
