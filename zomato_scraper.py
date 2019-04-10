from bs4 import BeautifulSoup
import requests,pprint,time
from selenium import webdriver

# Here I use webdriver for scrap data
driver = webdriver.Chrome()
driver.get('https://www.zomato.com/ncr')

page = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
detail_for_place=[]


# This Function will give us Name of location, Total restaurnants and link of restuarnants
# I will use it in TASK1 And TASK2
def scrapt_all_detail(page):
	soup = BeautifulSoup(page,"html.parser")
	segment_div=soup.find('div', class_='ui segment row')
	a_tag=segment_div.find_all('a')
	for i in a_tag:
		dict={'Name_of_location': "" , 'Total_restaurnants': "", 'link':''}
		location=i.get_text().split('(')
		dict['Name_of_location']=location[0].strip()
		dict['Total_restaurnants']=location[1].strip()[0:-1]
		dict['link']=i['href']
		detail_for_place.append(dict)
	return detail_for_place
scrapted_data=scrapt_all_detail(page)
# pprint.pprint(scrapted_data)


#task 1 
# In this task I analyse the total restaurnants by location
def analyse_locilities(location):
	list_by_location=[]
	id=1
	for i in location:
		dic={'Name_of_location':'','Total_restaurnants':'','id':0}
		dic['Name_of_location']=i['Name_of_location']
		dic['Total_restaurnants']=i['Total_restaurnants']
		dic['id']=id
		id+=1
		list_by_location.append(dic)
	return list_by_location
analysis_places=analyse_locilities(scrapted_data)
# pprint.pprint(analysis_places)


#task 2
print('\n\n<========Enter the id for entering for the particular location==========>\n\n')
user_input=int(input())
print('\n\nPlease wait...\n\n')
time.sleep(2)
print('Thanks\n')

# This funtion is finding link of a webside. I will use it to find the task 2's output
def scrapt_restaurnants_link(url):
	driver = webdriver.Chrome()
	driver.get(url)
	page = driver.execute_script("return document.documentElement.outerHTML")
	driver.quit()
	soup = BeautifulSoup(page,"html.parser")
	zone_div=soup.find('div',class_='subzone-content')

	subzone=zone_div.find_all('div')
	dict={}
	for i in subzone:
		fontsize=i.find("div",class_="fontsize1 semi-bold mt2")
		cat_subzone=i.find('div',class_='cat-subzone-res ptop0 ml15 mr20')
		try:
			res_loca=(fontsize.get_text()).strip()
			pd=cat_subzone.find('div',class_='pb5 bt ptop0 ta-right')
			see_more=pd.find('a')['href']
			dict[res_loca]=see_more
		except:
			continue
	return dict

screpted_link=scrapt_restaurnants_link(scrapted_data[user_input-1]['link'])
# pprint.pprint(screpted_link)


# This code will print all key of dictionary that is in screpted_link
a=[]
for key in screpted_link:
	a.append(key)
print('Enter the type of restaurnant for the following list',a,'\nThe input should be match with the item given in the below list\n\n\n')
user_input=input()
# print(screpted_link[user_input])


# Analysise all details of a restaurnant.
def open_the_type_restaurnants(type):
	all_details=[]
	id=0
	driver = webdriver.Chrome()
	driver.get(type)
	page = driver.execute_script("return document.documentElement.outerHTML")
	driver.quit()
	soup=BeautifulSoup(page,"html.parser")
	ui_card=soup.find('div',class_='ui cards')
	artcl=ui_card.find_all('article')
	for i in artcl:
		name_location=[]
		name_location_dic={}
		name=i.find_all('a',class_='result-title hover_feedback zred bold ln24 fontsize0 ')
		location=i.find_all('a',class_='ln24 search-page-text mr10 zblack search_result_subzone left')
		review=i.find('span').get_text()
		name_location_dic['Review']=review
		rps_range=i.find('div', class_='res-cost clearfix')
		price_range=rps_range.find('span',class_='col-s-11 col-m-12 pl0').get_text()
		rating_div=i.find('div', class_='ta-right floating search_result_rating col-s-4 clearfix')
		rating=rating_div.find('div').get_text().strip()
		id+=1
		name_location_dic['Restaurnant_id']=id
		for j in name:
			name_location_dic['Name']=j.get_text().strip()
		for j in location:
			name_location_dic['Location']=j.get_text().strip()
		name_location_dic['Rating']=rating
		name_location_dic['Price Range']=price_range
		all_details.append(name_location_dic)

	return all_details
pprint.pprint(open_the_type_restaurnants(screpted_link[user_input]))
# open_the_type_restaurnants('https://www.zomato.com/ncr/caf%C3%A9s-in-pitampura?ref_page=subzone')

