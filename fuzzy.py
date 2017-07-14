from clarifai.rest import ClarifaiApp
import sys
import selenium
import urllib2
import urllib
import unicodedata
from selenium import webdriver
from xvfbwrapper import Xvfb
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import os
import re

links=[]
score=[]

#WebdriverWait myWait = new WebdriverWait(driver,10);

app = ClarifaiApp("agJExNhNHN5f26_R0-sJEkRVilekOjgUpJn84pdJ", "vYUAe5vX_7r_LYLsjNRRb8Izv4QDzN9C1cXWiF_-")

model = app.models.get("general-v1.3")

######### add your own address here !
address = "/home/pratik/Desktop/fuzzy/"+sys.argv[1]
#########

data=model.predict_by_filename(filename=address)
siz = len(data['outputs'][0]['data']['concepts'])
strng=""
for i in range(0,2):
	strng=strng+ " "+data['outputs'][0]['data']['concepts'][i]['name']

#display=Xvfb()
#display.start()

driver = webdriver.Chrome()	
driver.get("https://www.amazon.in")

element = driver.find_element_by_id("twotabsearchtextbox")
element.send_keys(strng)
element.submit()


for i in range(0,3):
	name="result"+'_'+str(i)
	try:
		element = WebDriverWait(driver, 30).until(
			EC.presence_of_element_located((By.ID, name))
			)
	finally:
		element = driver.find_element_by_xpath('//*[@id="'+name+'"]/div/div/div/div[1]/div/div/a')
		url_a= element.get_attribute('href')
		links.append(url_a)
		element = driver.find_element_by_xpath('//*[@id="'+name+'"]/div/div/div/div[1]/div/div/a/img')
		url= element.get_attribute('src')
		driver1 = webdriver.Chrome()
		driver1.get(url_a)


		try:
			element = WebDriverWait(driver1, 30).until(
				EC.presence_of_element_located((By.ID, "imgTagWrapperId"))
				)
		finally:
			element = driver1.find_element_by_xpath('//*[@id="imgTagWrapperId"]/img')
			url= element.get_attribute('src')
			newurl=str(url)
			print newurl
			urllib.urlretrieve(newurl,"img/"+str(i)+".jpg")
			driver1.quit()


				
var=os.popen('pyssim test.jpg "img/*"').read()
i=0
for each in  var.split('\n'):
	arr=each.split(' ')
	if len(arr)>1:
		score.append(arr[3])
		i=i+1
mydict={}

for i in range	(0,len(links)):
	mydict[str(links[i])]=score[i]

driver.quit()

#display.stop()
count=0
driver2= webdriver.Chrome()
driver2.execute_script("window.open('');")
for key, value in sorted(mydict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    print "%s: %s" % (key, value)
    if count<2:
    	driver2.switch_to.window(driver2.window_handles[count])
    	driver2.get(key)
    	count = count+1
    else:
    	break