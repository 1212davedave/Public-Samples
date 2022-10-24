# webscrape for the website https://agency.nationwide.com/index.html

from bs4 import BeautifulSoup
import requests
import csv

url = "https://agency.nationwide.com/index.html"
baseurl = "https://agency.nationwide.com/"
session = requests.Session()
response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
states = []

filename = "C:\\Path\\To\\File\\datadump.txt" # This is the directory and filename for the output file in csv
for link in soup.findAll('a', attrs={'class': 'Directory-listLink'}):
	states.append(link.get('href'))
states.remove("washington-dc")
cityLinks = ["https://agency.nationwide.com/washington-dc"]
for state in states:
	response2 = session.get(baseurl + state)
	soup2 = BeautifulSoup(response2.content, 'html.parser')
	for link2 in soup2.findAll('span', attrs={'class': 'Directory-listLinkText'}):
		city = str(link2.contents[0]).lower()
		newurl = str(baseurl + city + "-" + state)
		cityLinks.append(newurl)
for link in cityLinks:
	response3 = session.get(link)
	soup3 = BeautifulSoup(response3.content, 'html.parser')
	for article in soup3.findAll('article', attrs={'class': 'Teaser Teaser--directory'}):
		try:
			row
		except NameError:
				row = {
					"agency": None,
					"name": None,
					"phone": None,
					"address1": None,
					"address2": None,
					"city": None,
					"state": None,
					"zip": None,
				}
		else:
			del row
			row = {
				"agency": None,
				"name": None,
				"phone": None,
				"address1": None,
				"address2": None,
				"city": None,
				"state": None,
				"zip": None,
			}
		if (article.find('span', text=True, attrs={'class': 'LocationName'})) is not None:
			for agency in article.find('span', text=True, attrs={'class': 'LocationName'}):
				row["agency"] = agency
		if (article.find('div', attrs={'class': 'Teaser-agentName'})) is not None:
			for name in article.find('div', attrs={'class': 'Teaser-agentName'}):
				row["name"] = name
		if (article.find('span', attrs={'id': 'telephone'})) is not None:
			for phone in article.find('span', attrs={'id': 'telephone'}):
				row["phone"] = phone
		if (article.find('span', attrs={'class': 'c-address-street-1'})) is not None:
			for street1 in article.find('span', attrs={'class': 'c-address-street-1'}):
				row["address1"] = street1
		if (article.find('span', attrs={'class': 'c-address-street-2'})) is not None:
			for street2 in article.find('span', attrs={'class': 'c-address-street-2'}):
				row["address2"] = street2
		if (article.find('span', attrs={'class': 'c-address-city'})) is not None:
			for city in article.find('span', attrs={'class': 'c-address-city'}):
				row["city"] = city
		if (article.find('abbr', attrs={'class': 'c-address-state'})) is not None:
			for state1 in article.find('abbr', attrs={'class': 'c-address-state'}):
				row["state"] = state1
		if (article.find('span', attrs={'class': 'c-address-postal-code'})) is not None:
			for zip in article.find('span', attrs={'class': 'c-address-postal-code'}):
				row["zip"] = zip
		rowlist = list(row.values())
		with open(filename, 'a+') as file:
			filewriter = csv.writer(file)
			filewriter.writerow(rowlist)
		file.close()

