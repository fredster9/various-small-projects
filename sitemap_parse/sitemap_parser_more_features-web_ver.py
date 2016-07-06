
from xml.dom.minidom import parseString
import csv, sys, urllib2, json
import pandas as pd
import matplotlib.pyplot as plt, mpld3

## To handle any special char issues - maybe less relevant if not exporting to CSV
reload(sys)
sys.setdefaultencoding('utf8')

urls = (
	  '/', 'hello',
	  '/xml', 'xml_proj',
      '/chart', 'chartpg',
	  )

class hello:
	def GET(self):
		return "Hello, world."

class xml_proj:
	def GET(self):
		#return render.xml_proj(name="Fred")
		template = env.get_template('xml_proj.html')
		return template.render()

	def POST(self):
		## read in form response
		data = web.input()
		## Access element by name
		sm_url = data.sitemap
		print "RAW URL", sm_url
		#template = env.get_template('chartpg.html')
		#return template.render(sm_url)
#
# class chartpg:
# 	def GET(self, sm_url):
# 		print "in chartpg GET"
# 		print "SM URL", sm_url

		sitemap = urllib2.urlopen(sm_url)
		#print "RESPONSE", sitemap
		doc = parseString(sitemap.read())
		print "DOC", doc

		url_tag = doc.getElementsByTagName("url")

		## List for accumulating url and last mod values
		out = []

		## For every <url></url> object/node in url_tag (which will be every one in the sitemap) extract the URL and last modified date
		for x in url_tag:
			url = x.getElementsByTagName("loc")[0]
			updated = x.getElementsByTagName("lastmod")[0]
			## This gets the values and not the whole object
			output = url.firstChild.data, updated.firstChild.data
			#print "URL: %s, UPDATED: %s" % (url.firstChild.data, updated.firstChild.data)
			## Append to list
			out.append(output)

		## Create pandas dataframe with the headers below and all the rows from the out list
		df = pd.DataFrame(out, columns=["URL", "Last_Mod"])
		## Convert Last_Mod to datetime for accessing month, etc.
		df.Last_Mod = pd.to_datetime(df.Last_Mod, format= "%Y-%m-%d")

		# ## Changed code because pandas 0.13 doesn't have dt.accessor and I can't figure out how to upgrade it on DO
		df['Year'] = df.Last_Mod.apply(lambda x: x.year)
		df['Month'] = df.Last_Mod.apply(lambda x: x.month)
		df['Week'] = df.Last_Mod.apply(lambda x: x.week)
		# df['Year'] = df.Last_Mod.dt.year
		# df['Month'] = df.Last_Mod.dt.month
		# df['Week'] = df.Last_Mod.dt.week

		yr_mon = df.groupby(['Year', 'Month'])
		yrmonplt = yr_mon.size()
		fig = plt.figure()
		fid = yrmonplt.plot(kind='bar')
		plt.title('Updates by Month')
		json01 = json.dumps(mpld3.fig_to_dict(fig))
		print json01
		template = env.get_template('chartpg.html')
		#print "TEMPLATE", template
		#return template.render(name='Fred', jsonobj=json01)

		yr_week = df.groupby(['Year', 'Month', 'Week'])
		yrweekplt = yr_week.size()
		fig2 = plt.figure()
		fid = yrweekplt.plot(kind='bar')
		plt.title('Updates by Week')
		json02 = json.dumps(mpld3.fig_to_dict(fig2))
		print json02
		template = env.get_template('chartpg.html')
		print "TEMPLATE", template
		return template.render(name='Fred', jsonobj1=json01, jsonobj2=json02)

application = web.application(urls, globals()).wsgifunc()