import sys
import PIL.Image as image
import PIL.ImageChops as imagechops
import time,re,random
import io
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from getInfo import getInfo
from dbService import DBService

#获取浏览器驱动
def get_webdriver(name):
        if name.lower() == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
            return webdriver.PhantomJS(desired_capabilities=dcap)

        elif name.lower() == "chrome":
            return webdriver.Chrome(executable_path=r"C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")

#输入查询词，点击按钮
def input_params(driver,name):
        driver.get("http://www.gsxt.gov.cn/index")
        element = WebDriverWait(driver,10).until(lambda the_driver:the_driver.find_element_by_id('keyword'))
        element.send_keys(name)
        time.sleep(0.5)
        element = WebDriverWait(driver,10).until(lambda the_driver:the_driver.find_element_by_id('btn_query'))
        element.click()
        time.sleep(0.5)

def get_merge_image(filename,location_list):   
	im = image.open(filename)    
	new_im = image.new('RGB', (260,116))    
	im_list_upper=[]    
	im_list_down=[]    
	for location in location_list:        
		if location['y']==-58:            
			pass            
			im_list_upper.append(im.crop((abs(location['x']),58,abs(location['x'])+10,116)))        
		if location['y']==0:           
			pass            
			im_list_down.append(im.crop((abs(location['x']),0,abs(location['x'])+10,58)))    
		new_im = image.new('RGB', (260,116))    
	x_offset = 0    
	for im in im_list_upper:        
		new_im.paste(im, (x_offset,0))        
		x_offset += im.size[0]    
	x_offset = 0    
	for im in im_list_down:        
		new_im.paste(im, (x_offset,58))        
		x_offset += im.size[0]    
	return new_im
	
def get_image(driver,div):    
	#找到图片所在的div    
	background_images=driver.find_elements_by_xpath(div)    
	location_list=[]    
	imageurl=''   
	for background_image in background_images: 
		# print(re.findall('background-position: (.*)px (.*)px;',background_image.get_attribute('style')))
		location={}        
		# 在html里面解析出小图片的url地址，还有长高的数值        
		location['x']=int(re.findall('background-position: (.*)px (.*)px;',background_image.get_attribute('style'))[0][0])      
		location['y']=int(re.findall('background-position: (.*)px (.*)px;',background_image.get_attribute('style'))[0][1])        
		location_list.append(location)
		try: 
			imageurl=re.findall('url\(\"(.*)\"\)', background_image.get_attribute('style'))[0]
		except:
			imageurl=re.findall('url\((.*)\)', background_image.get_attribute('style'))[0]
		# print(imageurl)     
	imageurl=imageurl.replace("webp","jpg")
	# print(imageurl) 
	jpgfile=io.BytesIO(urllib.request.urlopen(imageurl).read())    
	#重新合并图片     
	image=get_merge_image(jpgfile,location_list )    
	return image


##比较两张图片的像素点RGB值，相差超过50，即认为是缺口位置
def is_similar(image1,image2,x,y):    
    pass    
    pixel1=image1.getpixel((x,y))    
    pixel2=image2.getpixel((x,y))    
    for i in range(0,3):        
    	if abs(pixel1[i]-pixel2[i])>=50:            
    		return False    
    return True

def get_diff_location(image1,image2):  
 	i=0    
 	for i in range(0,260):        
 		for j in range(0,116):            
 			if is_similar(image1,image2,i,j)==False:                
 				return  i


##生成鼠标轨迹，待优化
def get_track(length):    
	//the important alorithmn



def hackgeetest(driver):
	#等待图片元素加载出来
	WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']").is_displayed())    
	WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_bg gt_show']").is_displayed())    
	WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='gt_cut_fullbg gt_show']").is_displayed())
	#下载图片，并重新拼接
	image1=get_image(driver,"//div[@class='gt_cut_fullbg_slice']")
	# image1.show()
	image2=get_image(driver,"//div[@class='gt_cut_bg_slice']")
	# image2.show()
	
	#计算缺口位置
	loc=get_diff_location(image1,image2) 
	track_list=get_track(loc)

	#找到滑动的圆球    
	element=driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
	location=element.location
	y=location['y']
	#鼠标点击元素并按住不放    
	print ("第一步,点击元素" )   
	ActionChains(driver).click_and_hold(on_element=element).perform()    
	time.sleep(0.15)  
  
	print("第二步,拖动元素")   
	for track in track_list:
		y=y+random.randint(0,1)
		ActionChains(driver).move_to_element_with_offset(to_element=element,xoffset=track[0]+22,yoffset=y).perform()
		ActionChains(driver).click_and_hold().perform()
		time.sleep(track[1])

	print('第三步,释放鼠标')
	ActionChains(driver).release(on_element=element).perform()
	time.sleep(0.8)

	element=WebDriverWait(driver,30).until(lambda the_driver:the_driver.find_element_by_class_name('gt_info_text'))
	result = element.text
	print(result)
	return result

def get_search_list(driver):
	#提取条目url,爬取工商信息
	
	#等待搜索结果加载
	WebDriverWait(driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='pagination']"))  

	# print(driver.page_source)
	soup = BeautifulSoup(driver.page_source,'html.parser')
	tag=soup.find('div',class_='pagination')
	atag=tag.find_all('a')
	# pages=int(re.findall('javascript:turnOverPage\((.*)\)',atag[-1].attrs['href'])[0]) 
	# print(pages)
	# 打印第一页
	print('get_search_item....')
	search_list=[]
	for sp in soup.find_all('a',attrs={'class':'search_list_item'}):
		# print(re.sub('\s+','\n',sp.get_text()))
		search_item={}
		domain='http://www.gsxt.gov.cn'
		search_item['name']=sp.h1.get_text().strip()
		li=sp.find_all('span',attrs={'class':'g3'})
		search_item['regNo']=li[0].get_text().strip();
		search_item['holder']=li[1].get_text().strip();
		search_item['foundingTime']=li[2].get_text().strip();	
		search_item['url']=domain+sp.attrs['href']	
		search_list.append(search_item)
	#访问并打印剩余的页面
	# for page in range(pages-1):
	# 	element=WebDriverWait(driver, 30).until(lambda the_driver: the_driver.find_element_by_xpath("//div[@class='pagination']/form/a[last()-1]"))  
	# 	element.click()
	# 	soup = BeautifulSoup(driver.page_source,'html.parser')
	# 	for sp in soup.find_all('a',attrs={'class':'search_list_item'}):
	# 		# print(re.sub('\s+','\n',sp.get_text()))
	# 		search_item={}
	# 		search_item['name']=sp.h1.get_text().strip()
	# 		li=sp.find_all('span',attrs={'class':'g3'})
	# 		search_item['regNo']=li[0].get_text().strip();
	# 		search_item['holder']=li[1].get_text().strip();
	# 		search_item['foundingTime']=li[2].get_text().strip();
	# 		search_item['url']=domain+sp.attrs['href']	
	# 		search_list.append(search_item)
	return search_list

def spiderinfo(searchword,webdriver=1):
	#这里的文件路径是webdriver的文件路径  
	if webdriver==1:
		driver = get_webdriver("chrome")
	else:
		driver = get_webdriver("phantomjs")
	input_params(driver,searchword)
	#driver.get("localhost:8000/")
	flag=True
	while flag:
		result=hackgeetest(driver)
		if '通过' in result:
			time.sleep(1)
			print('success')
			#获取工商企业数据，仅获取第一家
			search_list=get_search_list(driver)
			# g=getInfo(search_list[0]['url'])
			# g.run()
			db=DBService()
			for item in search_list:
				db.insert(1,(item['name'],item['regNo'],item['url'],int(time.time())))
			driver.quit()
			return search_list
		elif '吃' in result:
			print('fail')
			time.sleep(3)
		else:
			print("reload")
			input_params(driver,searchword)
	
if __name__=="__main__":
	spiderinfo("阿里巴巴")

	

