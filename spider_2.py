import os
import json
import time
import sys
import signal
import urllib.request
import urllib.error
from urllib.parse import urlparse

from multiprocessing import Pool
from user_agent import generate_user_agent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TimeLimitError(Exception):
    def __init__(self, value):
        Exception.__init__()
        self.value = value

    def __str__(self):
        return self.value

def handler(signum,frame):
	raise TimeLimitError('Time limit exceeded');

	

def get_image_link(keyword,filepath,num_request = 500):
	number_of_scroll = int (num_request/400) + 1;
	img_urls = set();
	driver = webdriver.Chrome();
	url = "https://www.google.com/search?q="+keyword+"&source=lnms&tbm=isch";
	driver.get(url);
	img_dir = filepath + keywords + '/';
	if not os.path.exists(img_dir):
		os.makedirs(img_dir);
	for _ in range(number_of_scroll):
		for __ in range(10):
		    # multiple scrolls needed to show all 400 images
		    driver.execute_script("window.scrollBy(0, 1000000)")
		    time.sleep(2)
		# to load next 400 images
		time.sleep(5)
		try:
		    driver.find_element_by_xpath("//input[@value='Show more results']").click()
		except Exception as e:
		    print("sorry I couldn't find the solution")
		    break;
	imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
	count = 1;
	print(len(imges));
	signal.signal(signal.SIGALRM,handler);
	for img in imges:
		img_url = json.loads(img.get_attribute('innerHTML'))["ou"];
		img_urls.add(img_url);
		print(count);
		try:
			req = urllib.request.Request(img_url,headers = {"User-Agent": generate_user_agent()});
			signal.alarm(5);
			response = urllib.request.urlopen(req);
			
		except TimeLimitError as e:
			print("Time limit Exceed for downloading this image");
			continue;

		except:
			print("I couldn't download from {0}".format(img_url));
		finally:
			signal.alarm(0);

		data = response.read();
		file_path = img_dir + '{0}.jpg'.format(count);
		with open(file_path,'wb') as wf:
			wf.write(data);
		count += 1;














if __name__ == '__main__':
	keywords = sys.argv[1];
	download_dir = './image'
	get_image_link(keywords,download_dir);