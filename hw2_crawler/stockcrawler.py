import sys
import mechanize
import pandas as pd
from bs4 import BeautifulSoup

class stockCrawler(object):
	"""docstring for ClassName"""
	def __init__(self):
		self.all_l=[]
		self.year = sys.argv[1]
		self.month = sys.argv[2]

	def crawler(self,year,month):
		br = mechanize.Browser()
		url = "http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report"+str(year)+str(month)+"/"+str(year)+str(month)+"_F3_1_8_6214.php?STK_NO=6214&myear="+str(year)+"&mmon="+str(month)
		res = br.open(url)
		soup = BeautifulSoup(res)
		for a in soup.find_all( attrs={"bgcolor": "#FFFFFF"} ):
			data_l = []
			for t in [0,1,3,4,5,6,8]:
				data_l.append(a.contents[t].string)
			self.all_l.append(data_l)    

	def storage(self):
		rowname = ['Date','Trade Volume','Opening Price','Highest Price','Lowest Price','Closing Price','Transaction']
		df = pd.DataFrame(self.all_l, columns=rowname)
		with open('data.csv', 'w') as f:
			df.to_csv(f)

	def run(self):
		self.crawler(self.year,self.month)
		self.storage()

def main():
	try:
		stockcrawler = stockCrawler()
		stockcrawler.run()
		print('creat data.csv succuess')
	except:
		print('''please format year and month  e.x 2014 07 if don't work the website have no data''')

if __name__ == '__main__' :
    main()




