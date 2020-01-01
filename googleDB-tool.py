#!/usr/bin/python
# -*- coding: utf8 -*-

# ################################################################################  
# ## Redistributions of source code must retain the above copyright notice
# ## DATE: 2011-11-27
# ## AUTHOR: SecPoint ApS  
# ## MAIL: info@secpoint.com  
# ## SITE: http://www.secpoint.com  
# ##
# ## LICENSE: BSD http://www.opensource.org/licenses/bsd-license.php
# ################################################################################  
# ## 1.0 initial release
# ## 1.1 google query generating option (-q)
# ## 1.2 generating HTML output
# ## 1.3 added support for multiple sites generation (-m option)
# ## 1.5 friendly output and examples, database update

from optparse import OptionParser
import os.path
from urllib import quote_plus
 
VERSION = '1.5'

SAMPLES="""
Command line examples:
    1-generate list of search strings for finding login pages
    ./googleDB-tool.py "login_pages.txt"  

    2-generate list of Google queries for finding login pages
    ./googleDB-tool.py "login_pages.txt" -q

    3-same as 2, but in HTML format
    ./googleDB-tool.py "login_pages.txt" -q -t

    4-same as 3, but save to "OUT.html"
    ./googleDB-tool.py "login_pages.txt" -q -t -o "OUT.html"

    5-generate queries as in 4, but only for site.com
    ./googleDB-tool.py "login_pages.txt" -q -t -o "OUT.html" -s site.com

    6-all of the above, for multiple sites from "sites.txt" list
 ./googleDB-tool.py "login_pages.txt" -q -t -o OUT.html -s site.com -m sites.txt

    """


def get_strings(src_file):
    """getting strings from file"""
    res = []
    try:
        res = open(src_file,'r').readlines()
        res = [x.strip() for x in res]
    except:
        res = []
    return res

def append_sitename(strs,site):
    """adding site name to strings"""
    strs = [x+' site:'+site for x in strs]
    return strs

def gen_google_query(strs):
    """generating Google query strings for each line"""
    qs=[]
    gstring = "http://www.google.com/search?q="
    for x in strs:
            qs.append(gstring+quote_plus(x))
    return [strs,qs]

def gen_html_output(strs,q):
    """generating pretty HTML output"""
    res = []
    res.append('<html>\n')
    res.append('<head><title>GoogleDB queries strings</title></head>\n')
    res.append('<body>\n')
    res.append('\t<ul>\n')
    for (x,v) in zip(strs,q):
        res.append('\t\t<li><a href="%s">%s</a></li>\n'%(v,x))
    res.append('\t</ul>\n')
    res.append('</body>\n</html>')
    return res

def save_output(strs,out_f):
    """saving/printing results"""
    res = "\n".join(strs)

    if out_f:
        try:
            open(out_f,'w').write(res)
        except:
            print "Error! Couldn't save output file!"
            exit()
    else:
        print res

def main():
    """Parsing options and starting engine"""
    parser = OptionParser(usage="%prog <sourcefile> [-s site] [-q] [-t] [-f outfile]", 
              version="SecPoint.com %prog "+VERSION,
              epilog="SecPoint.com Google Penetration Testing Hack Database v. "+VERSION)
    parser.add_option("-o", "--output", dest="filename",
                      help="save output to file", metavar="FILE")
    parser.add_option("-s", "--site", dest="sitename",
                      help="generate queries for the SITE", metavar="SITE")
    parser.add_option("-m", "--multiple", dest="listfilename",
                      help="generate queries for multiple sites listed in LISTFILE", metavar="LISTFILE")
    parser.add_option("-q", "--query",
                      action="store_true", dest="gen_query", default=False,
                      help="generate google query urls for each line")
    parser.add_option("-t", "--html",
                      action="store_true", dest="gen_html", default=False,
                      help="generate output in HTML format (implies -q)")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print """SecPoint.com Google Penetration Testing Hack Database

 The Portable Penetrator - Wifi Recovery - Vulnerability Scanner
 http://www.secpoint.com/portable-penetrator.html
        """
        parser.print_help()
        print SAMPLES
        exit()
        #parser.error("please set source file (could be found in 'db' dir)")
    #all options 
    site_name = options.sitename
    gen_html = options.gen_html
    gen_query = options.gen_query
    out_file = options.filename
    multlist_file = options.listfilename
    db_dir = os.path.join(os.path.dirname(__file__),'db')
    source_file = os.path.join(db_dir,args[0])
    if not os.path.isfile(source_file):
        parser.error("could not find source file! Please check if it exists in 'db' dir")

    #starting!
    strs = get_strings(source_file)
    if not strs:
        print "Can't get data from your source file!"
        exit()
    queries = []
    if site_name and multlist_file:
        print "Please use -s OR -m switches alone!"
        exit()    
    if site_name:
        strs = append_sitename(strs,site_name)
    if multlist_file:
        if not os.path.isfile(multlist_file):
            print "Could not find file from -m switch!"
            exit()
        mlst = open(multlist_file).read().split('\n')
        strsnew = [] #using multiple sites to create queries
        for i in mlst:
            strsnew.extend(append_sitename(strs,i))
        strs = strsnew    
    if gen_query:
        [strs,queries] = gen_google_query(strs)
    if gen_html:
        if not gen_query: #if not previuosly generated
            [strs,queries] = gen_google_query(strs)
        strs = gen_html_output(strs,queries)
    else:
        if queries:   
            strs = queries

    save_output(strs,out_file)


if __name__ == "__main__":
    main()
