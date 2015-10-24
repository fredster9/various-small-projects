## Takes sitemap.xml file and outputs each URL into CSV with date updated in next column
## initialize from command line with 'python xml_crawl_FD.py

from xml.dom import minidom
import csv, sys

reload(sys)
sys.setdefaultencoding('utf8')

## ENTER YOUR SITEMAP FILE LOCATION HERE
SITEMAP_FILE = "sitemap_092815.xml"

smfile = open(SITEMAP_FILE, "r")
doc = minidom.parse(smfile)
smfile.close()

def printNode(node):
  url_tag = doc.getElementsByTagName("url")
  print url_tag

  out = []

  for x in url_tag:
      url = x.getElementsByTagName("loc")[0]
      updated = x.getElementsByTagName("lastmod")[0]
      output = url.firstChild.data, updated.firstChild.data
      print "URL: %s, UPDATED: %s" % (url.firstChild.data, updated.firstChild.data)
      out.append(output)

  OUTPUT_FILENAME = (SITEMAP_FILE+".csv")
  output_file = open(OUTPUT_FILENAME, "wb")
  wr = csv.writer(output_file, dialect="excel")
  wr.writerows(out)

printNode(doc)

