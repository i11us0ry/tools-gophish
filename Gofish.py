import re
import os
import sys
import csv
import requests
import optparse
from gophish import Gophish
from gophish.models import *

requests.packages.urllib3.disable_warnings()

API_KEY = ""   #33335
url = ""

api = Gophish(API_KEY, host=url, verify=False)

banner = '''
	参考语句：

	01、创建发件邮箱（指定目录）:python3 Gofish.py --createSP --dir C:\\Users\\gophish\\smtp
	02、创建发件邮箱（指定文件）:python3 Gofish.py --createSP --ifile C:\\Users\\gophish\\smtp\\1.csv
	03、删除发件邮箱（所有邮箱）:python3 Gofish.py --deleteSP 0
	04、删除发件邮箱（指定ID值）:python3 Gofish.py --deleteSP 81-85,87,88-90
	05、获取发件邮箱（所有邮箱）:python3 Gofish.py --getSP 0
	06、获取发件邮箱（指定ID值）:python3 Gofish.py --getSP 81-85,87,88-90
	07、创建发件目标（指定目录）:python3 Gofish.py --createG --dir C:\\Users\\gophish\\groups
	08、获取发件目标（所有目标）:python3 Gofish.py --getG 0
	09、获取发件目标（指定ID值）:python3 Gofish.py --getG 20-25,27,28-30
	10、删除发件目标（所有目标）:python3 Gofish.py --deleteG 0
	11、获取发件目标（指定ID值）:python3 Gofish.py --deleteG 20-25,27,28-30
	12、创建钓鱼任务（指定文件）:python3 Gofish.py --createC --ifile C:\\Users\\gophish\\campaigns\\1.csv
	13、获取钓鱼任务（所有任务）:python3 Gofish.py --getC 0
	14、获取钓鱼任务（指定ID值）:python3 Gofish.py --getC 45-47,50
	15、删除钓鱼任务（所有任务）:python3 Gofish.py --deleteC 0
	16、删除钓鱼任务（指定ID值）:python3 Gofish.py --deleteC 45-49,50
	17、完成钓鱼任务（所有任务）:python3 Gofish.py --complete 0
	18、获取钓鱼任务（指定ID值）:python3 Gofish.py --complete 51-53
	19、导出钓鱼任务（所有任务）:python3 Gofish.py --saveResults 0 --ofile allResults
	20、导出钓鱼任务（中招用户）:python3 Gofish.py --saveResults 1 --ofile submitData_or_clickLink

'''

class GophishPY():
	def __init__(self):
		self.csv_data = ""
		self.files_name = []

		parser = optparse.OptionParser()
		parser.add_option("--createSP", action="store_true", dest="createSP", help="create Sending Profiles")
		parser.add_option("--createG", action="store_true", dest="createG", help="create groups")
		parser.add_option("--createC", action="store_true", dest="createC", help="create campaigns")

		parser.add_option("--deleteSP", dest="deleteSP", help="delete Sending Profiles")
		parser.add_option("--deleteG", dest="deleteG", help="delete groups")
		parser.add_option("--deleteC", dest="deleteC", help="delete campaigns")

		parser.add_option("--getSP", dest="getSP", help="get Sending Profiles")
		parser.add_option("--getG", dest="getG", help="get groups")
		parser.add_option("--getC", dest="getC", help="get campaigns")

		parser.add_option("--complete", dest="complete", help="complete campaigns")

		parser.add_option("--saveResults", dest="saveResults", help="save Results")

		parser.add_option("--dir", dest="dir", help="指定目录")
		parser.add_option("--ifile", dest="ifile", help="指定文件")
		parser.add_option("--ofile", dest="ofile", help="输出文件")


		parser.add_option("--helps", action="store_true", dest="helps", help="参考语法")

		self.options, self.args = parser.parse_args()
		self.main()

	def main(self):
		# create sendig profiles
		if self.options.createSP != None:
			print("------------------create sendig profiles------------------")
			print()
			# 根据指定目录下的文件创建 sendig profiles
			if self.options.dir != None:
				self.get_files_name(self.options.dir)
				for fn in self.files_name:
					with open(fn[0],encoding="utf-8") as openCsv:
						reader = csv.reader(openCsv)
						header = next(reader)
						for row in reader:
							try:
								name, host, address, username, password = row[0],row[1],row[2],row[3],row[4]
								print("creating sendig profile:" + name)
								self.create_sending_profile(name, host, address, username, password)
							except:
								print("任务失败，请检擦语法是否正确！")
			# 根据指定文件创建 sendig profiles
			elif self.options.ifile != None:
				with open(self.options.ifile,encoding="utf-8") as openCsv:
					reader = csv.reader(openCsv)
					header = next(reader)
					for row in reader:
						try:
							name, host, address, username, password = row[0],row[1],row[2],row[3],row[4]
							print("creating sendig profile" + name)
							self.create_sending_profile(name, host, address, username, password)
						except:
							print("任务失败，请检擦语法是否正确！")
			else:
				print("任务失败，请检擦语法是否正确！")

		# create groups
		elif self.options.createG != None:
			print("------------------create groups------------------")
			print()
			# 根据指定文件创建 groups
			if self.options.dir != None:
				self.get_files_name(self.options.dir)
				for fn in self.files_name:
					with open(fn[0],encoding="utf-8") as openCsv:
						reader = csv.reader(openCsv)
						header = next(reader)
						targets = []
						for row in reader:
							first_name, last_name, email, position = row[0],row[1],row[2],row[3]
							targets.append(User(first_name=first_name, last_name=last_name, email=email, position=position))
						try:
							print("creating groups:" + fn[1])
							self.create_group(fn[1], targets)
						except:
							print("任务失败，请检擦语法是否正确！")
			else:
				print("任务失败，请检擦语法是否正确！")

		# create Campaigns
		elif self.options.createC != None:
			print("------------------ reate camplains -----------------")
			print()
			# 根据指定文件创建 Campaigns
			if self.options.ifile != None:
				with open(self.options.ifile,encoding="utf-8") as openCsv:
					reader = csv.reader(openCsv)
					header = next(reader)
					for row in reader:
						try:
							name, groups, page, template, smtp, url = row[0],row[1],row[2],row[3],row[4],row[5]
							print("creating Campaigns:" + name)
							self.create_campaign(name, groups, page, template, smtp, url)
						except:
							print("任务失败，请检擦语法是否正确！")
			else:
				print("任务失败，请检擦语法是否正确！")

		# delete sending profiles
		elif self.options.deleteSP != None:
			print("------------------ delete sending profiles ------------------")
			print()
			ids = []
			if self.options.deleteSP == "0":
				smtps = self.get_sending_profiles()
				for smtp in smtps:
					ids.append(smtp.id)
			else:
				ids = self.get_id(self.options.deleteSP)
			for id in ids:
				print("deleting sending profiles:"+str(id))
				self.delete_sending_profile(id)

		# delete groups
		elif self.options.deleteG != None:
			print("------------------ delete groups ------------------")
			print()
			ids = []
			if self.options.deleteG == "0":
				groups = self.get_groups()
				for group in groups:
					ids.append(group.id)
			else:
				ids = self.get_id(self.options.deleteG)
			for id in ids:
				print("deleting groups:"+str(id))
				self.delete_group(id)

		# delete campaigns
		elif self.options.deleteC != None:
			print("------------------ delete campaigns ------------------")
			print()
			ids = []
			if self.options.deleteC == "0":
				campaigns = self.get_campaigns()
				for campaign in campaigns:
					ids.append(campaign.id)
			else:
				ids = self.get_id(self.options.deleteC)
			for id in ids:
				print("deleting campaigns:"+str(id))
				self.delete_campaign(id)


		# get campaigns
		elif self.options.getC != None:
			campaigns = []
			if self.options.getC == "0":
				campaigns = self.get_campaigns()
			else:
				ids = self.get_id(self.options.getC)
				for id in ids:
					campaign = self.get_campaign(id)
					campaigns.append(campaign)
			print("campaign.id      campaign.name")
			print("------------------------------------------------------------------")
			for campaign in campaigns:
				print(str(campaign.id)+"               "+campaign.name)
			print("------------------------------------------------------------------")

		# get groups
		elif self.options.getG != None:
			groups = []
			if self.options.getG == "0":
				groups = self.get_groups()
			else:
				ids = self.get_id(self.options.getG)
				for id in ids:
					group = self.get_group(id)
					groups.append(group)
			print("group.id      group.name")
			print("------------------------------------------------------------------")
			for group in groups:
				print(str(group.id)+"             "+group.name)
			print("------------------------------------------------------------------")

		# get sending profiles
		elif self.options.getSP != None:
			smtps = []
			if self.options.getSP == "0":
				smtps = self.get_sending_profiles()
			else:
				ids = self.get_id(self.options.getSP)
				for id in ids:
					smtp = self.get_sending_profile(id)
					smtps.append(smtp)
			print("smtp.id  smtp.name  smtp.from_address")
			print("------------------------------------------------------------------")
			for smtp in smtps:
				print(str(smtp.id)+"       "+smtp.name+"           "+smtp.from_address)
			print("------------------------------------------------------------------")

		# complete campaign
		elif self.options.complete != None:
			print("------------------complete " + self.options.complete + " campaign------------")
			print()
			ids = []
			if self.options.complete == '0':
				campaigns = self.get_campaigns()
				for campaign in campaigns:
					ids.append(campaign.id)
			else:
				ids = self.get_id(self.options.complete)
			for id in ids:
				print("complete campaign:"+str(id))
				try:
					self.complete_campaign(id)
				except:
					print("任务失败，请检擦语法是否正确！")

		# save Results
		elif self.options.saveResults != None:
			print("------------------save Results-------------------")
			print()
			data = []
			if self.options.saveResults == "0":
				campaigns = self.get_campaigns()
				for campaign in campaigns:
					for results in campaign.results:
						data.append(results)
			elif self.options.saveResults == "1":
				campaigns = self.get_campaigns()
				for campaign in campaigns:
					for results in campaign.results:
						if results.status == "Clicked Link" or results.status == "Submitted Data":
							data.append(results)
			self.save_results(data)

		elif self.options.helps != None:
			print(banner)

		else:
			print("任务失败，请检擦语法是否正确！")


	# 处理id
	def get_id(self,ids):
		id = []
		if "," in ids:
			ids = ids.split(",")
			for i in range(0,len(ids)):
				if "-" in ids[i]:
					ids[i] = ids[i].split("-")
					for idsi in range(int(ids[i][0]),int(ids[i][1])+1):
						id.append(idsi)
				else:
					id.append(int(ids[i]))
		elif "-" in ids:
			ids = ids.split("-")
			for idsi in range(int(ids[0]),int(ids[1])+1):
				id.append(idsi)
		else:
			id.append(int(ids))
		return id

	# 保存 results
	def save_results(self, datas):
		headers = ["first_name", "last_name", "email", "position", "status"]
		rows = []
		file = self.options.ofile
		file = file+".csv"
		for data in datas:
			rows.append([data.first_name,data.last_name,data.email,data.position,data.status])
		with open(file,"w",newline='') as wCsv:
			f_csv = csv.writer(wCsv)
			f_csv.writerow(headers)
			f_csv.writerows(rows)

	# 获取文件名
	def get_files_name(self,path):
		for file in os.listdir(path):
			file_path = os.path.join(path, file)
			self.files_name.append([file_path, file])

	'''
	sending_profile ??????
	id (int) The smtp ID
	name (str) The smtp name
	interface_type (str) The type of SMTP connection (for now, always use SMTP)
	host (str) The host:port of the SMTP server
	from_address (str) The address to send emails from (e.g. John Doe <johndoe@example.com>)
	ignore_cert_errors (bool) Whether or not to ignore SSL certificate validation errors (set to true in the case of self-signed certificates)
	modified_date (optional: datetime.datetime) The datetime this SMTP profile was previously modified
	'''
	def get_sending_profile(self, id):
		smtp = api.smtp.get(smtp_id=id)
		return smtp

	def get_sending_profiles(self):
		smtps = api.smtp.get()
		return smtps

	def create_sending_profile(self, name, host, address, username, password):
		smtp = SMTP(name=name)
		smtp.host = host
		smtp.from_address = address
		smtp.interface_type = "SMTP"
		smtp.ignore_cert_errors = True
		smtp.username = username
		smtp.password = password
		smtp = api.smtp.post(smtp)

	def delete_sending_profile(self, id):
		api.smtp.delete(smtp_id=id)

	'''
	Landing_Pages ?????
	id (int) The page ID
	html (str) The page HTML
	name (str) The page name
	modified_date (optional: datetime.datetime) The scheduled time for page launch
	capture_credentials (bool default:False) Whether or not the landing page should capture credentials
	capture_passwords (bool default:False) Whether or not the landing page should capture passwords
	redirect_url (str) The URL to redirect targets to after they submit data
	'''
	def get_Landing_Pages(self):
		pages = api.pages.get()
		return pages

	def get_Landing_Page(self, id):
		page = api.pages.get(page_id=id)
		return page

	def create_Landing_Page(self, name, html, capture, url=""):
		if capture == "data":
			page = Page(name=name, html=html, capture_credentials=True, redirect_url=url)
		elif capture == "pass":
			page = Page(name=name, html=html, capture_passwords=True, redirect_url=url)
		else:
			page = Page(name=name, html=html, redirect_url=url)
		page = api.pages.post(page)

	def delete_Landing_Page(self, id):
		api.pages.delete(page_id=id)

	'''
	Template ??????
	id (int) The template ID
	name (str) The template name
	html (str) The template HTML
	text (str) The template HTML
	modified_date (optional: datetime.datetime) The scheduled time for template launch
	attachments (list(models.Attachment)) The optional email attachments
	'''
	def get_Templates(self):
		templates = api.templates.get()
		return templates

	def get_Template(self, id):
		template = api.templates.get(template_id=id)
		return template

	def create_Template(self, name, html):
		template = Template(name=name,html=html)
		template = api.templates.post(template)
		return template

	def delete_Template(self, id):
		api.Template.delete(template_id=id)

	'''
	groups ???????
	id (int) The user ID
	first_name (str) The first name
	last_name (str) The last name
	email (str) The email address
	position (str) The position (job role)
	'''
	def get_groups(self):
		groups = api.groups.get()
		return groups

	def get_group(self, id):
		group = api.groups.get(group_id=id)
		return group

	# ???? groups
	'''
	targets = [
	    User(first_name='John', last_name='Doe', email='johndoe@example.com'),
	    User(first_name='Jane', last_name='Doe', email='janedoe@example.com')
	    ]
	'''
	def create_group(self, name, targets):
		group = Group(name=name, targets=targets)
		group = api.groups.post(group)
		return group

	def delete_group(self, id):
		api.groups.delete(group_id=id)

	# campaign.results
	'''
	id (int) The result ID
	first_name (str) The first name
	last_name (str) The last name
	email (str) The email address
	position (str) The position (job role)
	ip (str) The last seen IP address
	latitude (float) The latitude of the ip
	longitude (float) The longitude of the ip
	status (str) The users status in the campaign
		Email Sent
		Sending
		Error
		Email Opened
		Clicked Link
		Submitted Data
	'''
	def get_campaigns(self):
		campaigns = api.campaigns.get()
		return campaigns

	def get_campaign(self, id):
		campaign = api.campaigns.get(campaign_id=id)
		return campaign

	def create_campaign(self, name, groups, page, template, smtp, url):
		groups = [Group(name=groups)]
		page = Page(name=page)
		template = Template(name=template)
		smtp = SMTP(name=smtp)
		url = url
		campaign = Campaign(name=name, groups=groups, page=page, template=template, smtp=smtp, url=url)
		campaign = api.campaigns.post(campaign)
		return campaign

	def delete_campaign(self, id):
		api.campaigns.delete(campaign_id=id)

	def complete_campaign(self, id):
		api.campaigns.complete(campaign_id=id)

if __name__ == "__main__":
	GP = GophishPY()

