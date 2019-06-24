# coding=utf-8
import requests
import os, sys,time, json, random
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


# 当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)

from api.rest_api import RestApi
# from proxy.proxy import NewProxyIp

# 初始化
api = RestApi()
# daili = NewProxyIp("1")[0]
# print(daili)


file_name_load = "./company_url/new/"

# def create_tyc_company(data):
# 	try:
# 		api.tyc_company(data)
# 	except Exception as e:
# 		print (" api request fail 	. 	.		. ", format(e)) # 接口请求失败


# def create_tyc_cid(data):
# 	try:
# 		api.tyc_cid(data)
# 	except Exception as e:
# 		print (" api request fail 	. 	.		. ", format(e)) # 接口请求失败



def write_file(data_list,company_url_id,city,page,count,serach_url):

	file_name = file_name_load+str(count)+"_"+city+".csv"
	with open(file_name, 'a+', encoding='utf-8') as f:
		writer = f.write(company_url_id+","+serach_url+'\n')

def CheckDir(dir):
    if not os.path.exists(dir):
      os.makedirs(dir)
    pass




############################




def check_text_by_title(data_text, css):
	return data_text.select(css)[0].get('title')


def check_by_text(data_text, css):
	return data_text.select(css)[0].getText()


def check_one_company(url, data_text, city):

	code = url
	print('code:'+code)

	city = city
	print('城市:'+city)

	#  公司logo    logo             string
	company_logo = data_text.find_all('div', class_="logo -w100")
	for x in company_logo:
		logo = x.find_all('img')[0].get('data-src')
		print('logo:'+logo)

	# 公司名称     name             string
	name = data_text.find_all('h1', class_="name")[0].getText().strip()
	print('名称:'+name)

	# 电话        phone            string.
	if "暂无信息" not in data_text.select('div.f0>div.in-block>span:nth-of-type(2)')[0].getText():
		phone = data_text.select('div.f0>div.in-block>span:nth-of-type(2)')[0].getText().strip()
		print( "电话:"+phone)
	else:
		phone ="-"
		print( "电话:暂无信息" )

	# 邮箱        mail             string 
	if "暂无信息" not in data_text.select('div.f0>div.in-block>span:nth-of-type(2)')[1].getText():
		mail = data_text.select('div.f0>div.in-block>span:nth-of-type(2)')[1].getText().strip()
		print( "邮箱:"+mail)
	else:
		mail ="-"

		print( "邮箱:暂无信息")
 
	# 网址        url              string
	if "暂无信息" in data_text.select('div.f0>div.in-block')[2].getText():
		print( "网址:暂无信息")

		url = "-"
	else:
		url = data_text.select('div.f0>div.in-block>a')[0].get("href")
		print( "网址:"+url)

	# 地址        address          string
	if "暂无信息" not in data_text.select('div.f0>div.in-block')[3].getText():
		address = data_text.select('div.f0>div.in-block')[3].getText().split('附近公司')[0].split('：')[1]
		print( "地址:"+address)
	else:
		print( "地址:暂无信息")
		address = '-'

	# 简介        intro            string
	if "暂无信息" in data_text.find_all('div', class_="summary")[0].getText():
		print( "简介:暂无信息")
		intro = '-'
	else:
		summary = data_text.find_all('div', class_="summary")
		for x in summary:
			intro = x.find_all('script')[0].getText().strip()
		print( "简介:"+intro )

	# 公司曾用名   old_name         string
	old_name_css = '#company_web_top > div.box.-company-box > div.content > div.tag-list-content > div:nth-child(2)'
	in_old_name = check_by_text(data_text, old_name_css)
	if "曾用名" in in_old_name:
		old_name = in_old_name.split("曾用名")[1]
	else:
		old_name = "-"
	print('公司曾用名:'+old_name)

	# 更新时间     update_date      date
	update_date_css = '#company_web_top > div.footer > div.refesh.float-left > span.updatetimeComBox'
	update_date = check_by_text(data_text, update_date_css)
	print('更新时间:'+update_date)

	try:

		# 法人        boss_name        string
		boss_css = '#_container_baseInfo > table:nth-child(1) > tbody > tr:nth-child(1) > td.left-col.shadow'
		boss = check_by_text(data_text, boss_css)
		if "-" in boss:
			boss_name = "-"
		else:
			boss_name_css = '#_container_baseInfo > table:nth-child(1) > tbody > tr:nth-child(1) > td.left-col.shadow > div > div:nth-child(1) > div.humancompany > div.name > a'
			boss_name = check_by_text(data_text, boss_name_css)
		print('法人:'+boss_name)

		# 注册资本     reg_money        string
		reg_money_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(1) > td:nth-child(2) > div'
		reg_money = check_text_by_title(data_text, reg_money_css)
		print('注册资本:'+reg_money)

		# 成立日期     set_date         string
		set_date_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(1) > td:nth-child(4) > div'
		set_date = check_text_by_title(data_text, set_date_css)
		print('成立日期:'+set_date)

		# 经营状态     status           string
		status_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(2) > td:nth-child(2)'
		status = check_by_text(data_text, status_css)
		print('经营状态:'+status)

		# 工商注册号    reg_number       string
		reg_number_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(2) > td:nth-child(4)'
		reg_number = check_by_text(data_text, reg_number_css)
		print('工商注册号:'+reg_number)

		# 统一社会信用代码 credit_code    string
		credit_code_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(3) > td:nth-child(2)'
		credit_code = check_by_text(data_text, credit_code_css)
		print('统一社会信用代码:'+credit_code)

		# 组织机构代码    company_code   string
		# company_code
		company_code_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(3) > td:nth-child(4)'
		company_code = check_by_text(data_text, company_code_css)
		print('组织机构代码:'+company_code)

		# 纳税人识别号   tax_code        string
		# tax_code
		tax_code_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(4) > td:nth-child(2)'
		tax_code = check_by_text(data_text, tax_code_css)
		print('纳税人识别号:'+tax_code)

		# 公司类型      category_id     integer
		# category_id
		category_id_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(4) > td:nth-child(4)'
		category_id = check_by_text(data_text, category_id_css)
		print('公司类型:'+category_id)

		# 营业期限      end_time        string
		# end_time
		end_time_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(5) > td:nth-child(2)'
		end_time = check_by_text(data_text, end_time_css)
		print('营业期限:'+end_time)

		# 行业         industry_id     integer
		# industry_id
		industry_id_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(5) > td:nth-child(4)'
		industry_id = check_by_text(data_text, industry_id_css)
		print('行业:'+industry_id)

		# 纳税人资质    tax              string
		# tax
		tax_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(6) > td:nth-child(2)'
		tax = check_by_text(data_text, tax_css)
		print('纳税人资质:'+tax)

		# 核准日期      allow_time       string
		# allow_time
		allow_time_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(6) > td:nth-child(4)'
		allow_time = check_by_text(data_text, allow_time_css)
		print('核准日期:'+allow_time)

		# 实缴资本      pay_money        string
		# pay_money
		pay_money_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(7) > td:nth-child(2)'
		pay_money = check_by_text(data_text, pay_money_css)
		print('实缴资本:'+pay_money)

		# 人员规模      all_people       string
		# all_people
		all_people_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(7) > td:nth-child(4)'
		all_people = check_by_text(data_text, all_people_css)
		print('人员规模:'+all_people)

		# 参保人数      insured_people   string
		# insured_people
		insured_people_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(8) > td:nth-child(2)'
		insured_people = check_by_text(data_text, insured_people_css)
		print('参保人数:'+insured_people)

		# 登记机关      organ            string
		# organ
		organ_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(8) > td:nth-child(4)'
		organ = check_by_text(data_text, organ_css)
		print('登记机关:'+organ)

		# 注册地址      reg_address      string
		# reg_address
		reg_address_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(9) > td:nth-child(2)'
		reg_address = check_by_text(data_text, reg_address_css)
		print('注册地址:'+reg_address)

		# 英文名称      en_name          string
		# en_name
		en_name_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(9) > td:nth-child(4)'
		en_name = check_by_text(data_text, en_name_css)
		print('英文名称:'+en_name)

		# 经营范围      operate_scope            string
		# operate_scope
		operate_scope_css = '#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(10) > td:nth-child(2) > span > span > span.js-full-container.hidden'
		operate_scope = check_by_text(data_text, operate_scope_css)
		print('经营范围:'+operate_scope)

		data_all = {'code': code, 'city':city, 'logo': logo, 'name': name, 'phone': phone, 'mail': mail, 'url': url, 'address': address , 'intro': intro, 'old_name': old_name, 'update_date': update_date, 'boss_name': boss_name, 'reg_money': reg_money, 'set_date': set_date, 'status': status, 'reg_number': reg_number,'credit_code': credit_code, 'company_code': company_code, 'tax_code': tax_code, 'category_id': category_id, 'end_time': end_time, 'industry_id': industry_id, 'tax': tax, 'allow_time': allow_time, 'pay_money': pay_money, 'all_people': all_people, 'insured_people': insured_people, 'organ': organ, 'reg_address': reg_address, 'en_name': en_name, 'operate_scope': operate_scope}
		create_tyc_company(data_all)
		print('====================================上传成功==============================================')

		pass
	except Exception as e:
		print(e)
	
	


	

# 进入每个公司详情页面
def search_one_company(company_url, city):
	
	s=requests.session()
	headers={
		'Accept':'application/json, text/javascript, */*; q=0.01',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.9',
		'Connection':'keep-alive',
		'Host':'www.tianyancha.com',
		'Referer':company_url,
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
		'X-Requested-With':'XMLHttpRequest',
    }
	cookies={}
			   

	rs = requests.get(company_url, headers=headers, cookies=cookies, verify=False)
	rs.encoding = 'utf-8'
	data = BeautifulSoup(rs.text, "lxml")
	# print(data)
	check_one_company(company_url, data, city)


	time.sleep(random.randint(1,3))



##########################




# 进入每个城市
def function_city(serach_url):

	s=requests.session()
	headers={

	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Host':'www.tianyancha.com',
	'Referer':serach_url,
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest',

    }

	cookies={
	'__insp_norec_sess':'true',
	'__insp_nv':'true',
	'__insp_slim':'1550636701674',
	'__insp_ss':'1550636230628',
	'__insp_targlpt':'5aSp55y85p_lLeWVhuS4muWuieWFqOW3peWFt1/kvIHkuJrkv6Hmga/mn6Xor6Jf5YWs5Y_45p_l6K_iX_W3peWVhuafpeivol/kvIHkuJrkv6HnlKjkv6Hmga/ns7vnu58=',
	'__insp_targlpu':'aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20v',
	'__insp_wid':'677961980',
	'_ga':'GA1.2.531930070.1549963995',
	'_gat_gtag_UA_123487620_1':' 1',
	'_gid':' GA1.2.1888142622.1550636231',
	'aliyungf_tc':'AQAAAKcYbRoeBgMAFtfsdL+PLY4fFqrV',
	'auth_token':'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjYyMTM4MzI5MCIsImlhdCI6MTU1MDI4ODA0MywiZXhwIjoxNTY1ODQwMDQzfQ.vWPFCn0QQYzg4Zh0gjtdcMHtnOA8en7e5f23jgFlu9B56x2YC_-03j0NgRK3iXAqQ6a9__KTjBATbVQnWSNj0A',
	'cloud_token':'d6fcbdfebfab4b07b6c87b89d0fa9a1b',
	'csrfToken':'_ktjwVHq2fEEaUuw1cwLf39j',
	'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758':' 1550636701',
	'Hm_lvt_e92c8d65d92d534b0fc290df538b4758':'1550288031,1550636230,1550636239,1550636271',
	'ssuid':'4915086116',
	'tyc-user-info':'%7B%22claimEditPoint%22%3A%220%22%2C%22myAnswerCount%22%3A%220%22%2C%22myQuestionCount%22%3A%220%22%2C%22explainPoint%22%3A%220%22%2C%22privateMessagePointWeb%22%3A%220%22%2C%22nickname%22%3A%22%E5%BB%BA%E5%AE%81%E5%85%AC%E4%B8%BB%22%2C%22integrity%22%3A%220%25%22%2C%22privateMessagePoint%22%3A%220%22%2C%22state%22%3A%220%22%2C%22announcementPoint%22%3A%220%22%2C%22isClaim%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22discussCommendCount%22%3A%221%22%2C%22monitorUnreadCount%22%3A%224%22%2C%22onum%22%3A%220%22%2C%22claimPoint%22%3A%220%22%2C%22token%22%3A%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjYyMTM4MzI5MCIsImlhdCI6MTU1MDI4ODA0MywiZXhwIjoxNTY1ODQwMDQzfQ.vWPFCn0QQYzg4Zh0gjtdcMHtnOA8en7e5f23jgFlu9B56x2YC_-03j0NgRK3iXAqQ6a9__KTjBATbVQnWSNj0A%22%2C%22pleaseAnswerCount%22%3A%220%22%2C%22redPoint%22%3A%220%22%2C%22bizCardUnread%22%3A%220%22%2C%22vnum%22%3A%220%22%2C%22mobile%22%3A%2216621383290%22%7D',
	'TYCID':'344ad1602ea911e9b28e5db4b6efd162',
	'undefined':'344ad1602ea911e9b28e5db4b6efd162',
	}
	
	rs = requests.get(serach_url, headers=headers, cookies=cookies, verify=False)
	rs.encoding = 'utf-8'
	data_list_city = BeautifulSoup(rs.text, "lxml")

	# print(data)
	return data_list_city

# 拿到各个公司的url city url 
def company_city_url_new(company_list,city,page,count,serach_url):
	list_city_url = company_list.select('div.content>div.header')
	for company_one_url in list_city_url:
		company_url = company_one_url.find_all('a')[0].get('href')
		company_url_id = company_url.split("company/")[1]
		print(company_url+"=="+city+"===="+page)

		# data = {'city': city,'cid': company_url_id,'url': serach_url}

		# create_tyc_cid(data)

		write_file(company_url,company_url_id,city,page,count,serach_url)

		# search_one_company(company_url, city)




#####################################




	
# 拿到各个城市url
def city_url(data_):


	
	# 各个省份数据
	city_urls_new = data_.find_all('a', class_="link-hover-click overflow-width")
	
	count = 0
	code = [110101,110102,110105,110106,110107,110108,110109,110111,110112,110113,110114,110115,110116,110117,110118,110119,110228,110229]
	for x in city_urls_new:
		count = count + 1
		company_city_urls_new = x.get('href')
		city = x.getText()
		for x_code in code:
			for x_ot in range(1,11):
				for p in range(1,250):
					# https://www.tianyancha.com/search/os1-ot2/p2?base=bj&areaCode=110101
					serach_url = (company_city_urls_new.split('?')[0]+"/os1-ot"+str(x_ot)+"/p"+str(p)+"?"+company_city_urls_new.split('?')[1])+"&areaCode="+str(x_code)
					company_list = function_city(serach_url)
					
					page = "p"+str(p)

					company_city_url_new(company_list,city,page,count,serach_url)




		# print(company_city_urls_new)
		# if count >= 1:
		# 	for p in range(1,6):
		# 		serach_url = (company_city_urls_new.split('?')[0]+"/p"+str(p)+"?"+company_city_urls_new.split('?')[1])
		# 		company_list = function_city(serach_url)
		# 		page = "p"+str(p)
		# 		company_city_url_new(company_list,city,page,count)

	# 各个地区数据
	# city_urls = data_.select('div.row>div.col-11>div.item>a')
	# count = 0
	# for x in city_urls:
	# 	count = count + 1
	# 	company_city_urls_new = x.get('href')
	# 	city = x.getText()
	# 	print(company_city_urls_new)
	# 	if count >= 1:
	# 		for p in range(1,6):
	# 			# https://www.tianyancha.com/search/os1-ot2?base=bj&areaCode=110101
	# 			serach_url = (company_city_urls_new.split('?')[0]+"/p"+str(p)+"?"+company_city_urls_new.split('?')[1])
	# 			company_list = function_city(serach_url)
	# 			page = "p"+str(p)
	# 			company_city_url_new(company_list,city,page,count)


# 主页面url
url="https://www.tianyancha.com"
# 用户登录
def open_page(url):

	CheckDir(file_name_load)
	s=requests.session()
	headers={

	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Connection':'keep-alive',
	'Host':'www.tianyancha.com',
	'Referer':'https://www.tianyancha.com/',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest',

    }

	cookies={

	'__insp_norec_sess':'true',
	'__insp_nv':'true',
	'__insp_slim':'1550636238858',
	'__insp_ss':'1550636230628',
	'__insp_targlpt':'5aSp55y85p_lLeWVhuS4muWuieWFqOW3peWFt1/kvIHkuJrkv6Hmga/mn6Xor6Jf5YWs5Y_45p_l6K_iX_W3peWVhuafpeivol/kvIHkuJrkv6HnlKjkv6Hmga/ns7vnu58=',
	'__insp_targlpu':'aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20v',
	'__insp_wid':'677961980',
	'_ga':'GA1.2.531930070.1549963995',
	'_gat_gtag_UA_123487620_1':' 1',
	'_gid':' GA1.2.1888142622.1550636231',
	'aliyungf_tc':'AQAAAKcYbRoeBgMAFtfsdL+PLY4fFqrV',
	'auth_token':'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjYyMTM4MzI5MCIsImlhdCI6MTU1MDI4ODA0MywiZXhwIjoxNTY1ODQwMDQzfQ.vWPFCn0QQYzg4Zh0gjtdcMHtnOA8en7e5f23jgFlu9B56x2YC_-03j0NgRK3iXAqQ6a9__KTjBATbVQnWSNj0A',
	'cloud_token':'d6fcbdfebfab4b07b6c87b89d0fa9a1b',
	'csrfToken':'_ktjwVHq2fEEaUuw1cwLf39j',
	'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758':' 1550636239',
	'Hm_lvt_e92c8d65d92d534b0fc290df538b4758':'1549963994,1550288031,1550636230,1550636239',
	'ssuid':'4915086116',
	'tyc-user-info':'%7B%22claimEditPoint%22%3A%220%22%2C%22myAnswerCount%22%3A%220%22%2C%22myQuestionCount%22%3A%220%22%2C%22explainPoint%22%3A%220%22%2C%22privateMessagePointWeb%22%3A%220%22%2C%22nickname%22%3A%22%E5%BB%BA%E5%AE%81%E5%85%AC%E4%B8%BB%22%2C%22integrity%22%3A%220%25%22%2C%22privateMessagePoint%22%3A%220%22%2C%22state%22%3A%220%22%2C%22announcementPoint%22%3A%220%22%2C%22isClaim%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22discussCommendCount%22%3A%221%22%2C%22monitorUnreadCount%22%3A%224%22%2C%22onum%22%3A%220%22%2C%22claimPoint%22%3A%220%22%2C%22token%22%3A%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNjYyMTM4MzI5MCIsImlhdCI6MTU1MDI4ODA0MywiZXhwIjoxNTY1ODQwMDQzfQ.vWPFCn0QQYzg4Zh0gjtdcMHtnOA8en7e5f23jgFlu9B56x2YC_-03j0NgRK3iXAqQ6a9__KTjBATbVQnWSNj0A%22%2C%22pleaseAnswerCount%22%3A%220%22%2C%22redPoint%22%3A%220%22%2C%22bizCardUnread%22%3A%220%22%2C%22vnum%22%3A%220%22%2C%22mobile%22%3A%2216621383290%22%7D',
	'TYCID':'344ad1602ea911e9b28e5db4b6efd162',
	'undefined':'344ad1602ea911e9b28e5db4b6efd162',
	
	}

	rs = requests.get(url, headers=headers, cookies=cookies, verify=False)
	rs.encoding = 'utf-8'
	data = BeautifulSoup(rs.text, "lxml")
	# print(data)
	city_url(data)

	

# 入口
open_page(url)



# 手动拼接方式
# for p in range(1,6):
# 	serach_url = 'https://www.tianyancha.com/search/p'+str(p)+'?base=bj'
# 	data_text_city = function_city(serach_url)
# 	city = "北京"
# 	page = "p"+str(p)
# 	company_city_url_new(data_text_city,city,page)
