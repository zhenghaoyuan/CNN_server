import os;
import time;
import sys;
import re;
import logging;
import urllib.request;
import urllib.error;
from PIL import Image
from multiprocessing import Pool
from user_agent import generate_user_agent



def download_page(url):
	try:
		headers = {}
		headers['user-agent'] = generate_user_agent();
		headers['Referer'] = 'https://www.google.com';
		req = urllib.request.Request(url,headers = headers);
		resp = urllib.request.urlopen(req);
		return str(resp.read());
	except Exception as e:
		print('error while downloading the page');
		return None;


def parse_page(url):
	page_content = download_page(url);
	if page_content:
		link_list = re.findall('"ou":"(.*?)"',page_content);
		print(link_list);
		if len(link_list) == 0:
			#print('get no link from page\n');
			return set();
		else:
			return set(link_list);
	else:
		return set();

def download_pages(keywords,download_dir):

	img_dir = download_dir + '/' + keywords + '/';
	if not os.path.exists(img_dir):
		os.makedirs(img_dir);

	url = 'https://www.google.com/search?q=' + keywords + '&source=lnms&tbm=isch'
	image_links = parse_page(url);
	time.sleep(2);
	print("start downloading...");
	count = 1;
	for link in image_links:
		try:
			if link.endswith(".jpg") or link.endswith(".jpeg") or link.endswith(".png"):
				#print("downloading from source" + " " + link);
				req = urllib.request.Request(link,headers = {"User-Agent": generate_user_agent()});
				response = urllib.request.urlopen(req);
				data = response.read();
				if link.endswith(".jpg"):
					file_path = img_dir + '{0}.jpg'.format(count);
				elif link.endswith(".jpeg"):
					file_path = img_dir + '{0}.jpeg'.format(count);
				else:
					file_path = img_dir + '{0}.png'.format(count);
				with open(file_path,'wb') as wf:
					wf.write(data);
				#check if the image is valid or not
				print(file_path);
				im = Image.open(file_path);
				try:
					im.verify();

					if im.format != 'JPEG' and im.format != 'PNG':
						print(im.format);
						os.remove(file_path);
				except:
					print("wrong");
					os.remove(file_path);
				count += 1;
		except:
			#print(link);
			print("couldn't find");



if __name__ == '__main__':
	keywords = sys.argv[1];
	download_dir = './image'
	download_pages(keywords,download_dir);
