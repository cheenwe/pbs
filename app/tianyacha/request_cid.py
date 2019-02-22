# test.py
#
# coding=utf-8
import requests
import os, sys,time, json, random, datetime
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


# 当前文件的路径
pwd = os.getcwd()
project_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
sys.path.append(project_path)

from api.rest_api import RestApi

import urllib3
urllib3.disable_warnings()
api = RestApi()

# 清输入你的 cookie
MY_COOKIE = "xxxxxxxxxxxx"


def create_tyc_company(data):
	try:
		api.tyc_company(data)
	except Exception as e:
		print (" api request fail 	. 	.		. ", format(e)) # 接口请求失败


def check_text_by_title(data_text, css):
	return data_text.select(css)[0].get('title')


def check_by_text(data_text, css):
	return data_text.select(css)[0].getText()

def check_one_company(url, data_text):

	code = url
	print('code:'+code)

	#  公司logo    logo             string
	company_logo = data_text.find_all('div', class_="logo -w100")
	print(company_logo)
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

		data_all = {'code': code, 'logo': logo, 'name': name, 'phone': phone, 'mail': mail, 'url': url, 'address': address , 'intro': intro, 'old_name': old_name, 'update_date': update_date, 'boss_name': boss_name, 'reg_money': reg_money, 'set_date': set_date, 'status': status, 'reg_number': reg_number,'credit_code': credit_code, 'company_code': company_code, 'tax_code': tax_code, 'category_id': category_id, 'end_time': end_time, 'industry_id': industry_id, 'tax': tax, 'allow_time': allow_time, 'pay_money': pay_money, 'all_people': all_people, 'insured_people': insured_people, 'organ': organ, 'reg_address': reg_address, 'en_name': en_name, 'operate_scope': operate_scope}
		create_tyc_company(data_all)
		print('====================================上传成功==============================================')

		pass
	except Exception as e:
		print(e)


# 进入每个公司详情页面
def search_one_company(company_url):

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
	cookies= MY_COOKIE


	rs = requests.get(company_url, headers=headers, cookies=cookies, verify=False)
	rs.encoding = 'utf-8'
	data = BeautifulSoup(rs.text, "lxml")

	company_logo = data.find_all('div', class_="logo -w100")

	if len(company_logo)> 0:
		check_one_company(company_url, data)
	else:
		current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print(current_time)
		print("需要手工验证, 1")
		input_str = input("");
		if input_str == "1":
			print("Received input is : ", input_str  )
	# print(data)



def GetUid():
	try:
		r = api.tyc_request_cid()
		return (json.loads(r)["data"])
	except Exception as e:
		log.error("api request fail: %s", format(e))

# https://www.tianyancha.com/company/3179683797
while True:
	uid = GetUid()
	print(uid)
	company_url = 'https://www.tianyancha.com/company/'+uid
	print(company_url)
	search_one_company(company_url)
	time.sleep(random.randint(2,3))

