from bs4 import BeautifulSoup
import requests
import re
import datetime as DT
import uuid
import json

def gen_uid():
    return str(uuid.uuid4())


class JobsBGAPI:
    @staticmethod
    def is_internship(id):
        job = requests.get('https://www.jobs.bg/job/'+ str(id)).text
        return 'Стаж' in job

    @staticmethod
    def get_offer_info(id, company):
        job = requests.get('https://www.jobs.bg/job/'+ str(id)).text
        document = BeautifulSoup(job, 'html.parser')
        name = str(document.find_all('b')[0])
        company_id = company
        description = str(document.find_all('td')[13])
        location = ''
        try:
            location = re.search('Месторабота ([а-яa-zА-ЯA-Z]*);', str(document.find_all('td')[10]), re.IGNORECASE).group(1)
        except:
            location = 'not set'
        date = str(DT.datetime.today())
        available = True
        duration = 'по договорка'
        email = 'contact_us@headstarter.eu'
        hours_per_day = '4-7ч.' # 'До 4ч.' || '4-7ч.' || '8ч.'
        age_required = '16+' # '16-18' || '18+' || '16+'
        tag_id = -1
        views = 0
        return {
            'name': name,
            'company_id': company_id,
            'description': description,
            'location': location,
            'date': date,
            'available': available,
            'duration': duration,
            'email': email,
            'hours_per_day': hours_per_day,
            'age_required': age_required,
            'tag_id': tag_id,
            'views': views
        }
        
    @staticmethod
    def get_company_info(id, fields):
        company = requests.get('https://www.jobs.bg/company/'+ str(id)).text
        document = BeautifulSoup(company, 'html.parser')
        response = {}
        response['uid'] = gen_uid()
        response['id'] = id
        
        if 'logo' in fields:
            for logo in document.findAll('img'):
                if 'https://assets.jobs.bg/assets/logo/' in logo['src']:
                    response['logo'] = logo['src']
                    break
        if 'name' in fields:
            response['name'] = re.search('Jobs.bg - Обяви за работа от (.*)', str(document.title), re.IGNORECASE | re.MULTILINE | re.DOTALL).group(1)[:-8]
        if 'description' in fields:
            response['description'] = str(document.findAll(attrs = {'class':'sectionTitle'})[0].findNext('div'))
        if 'website' in fields:
            response['website'] = ''
        if 'contacts' in fields:
            response['contacts'] = str(document.findAll(attrs = {'class':'sectionTitle'})[1].findNext('div'))
        if 'offers' in fields:
            response['offers'] = [re.search('([0-9]+)', x['href'], re.IGNORECASE | re.MULTILINE | re.DOTALL).group(1) for x in document.findAll(attrs = {'class':'joblink'})]
        
        return response
    
    @staticmethod
    def get_top50_companies(log):
        top50 = requests.get('https://www.jobs.bg/top50.php').text
        document = BeautifulSoup(top50, 'html.parser')
        companies = document.find_all('tr')[1:-2][::2]
        for i in range(len(companies)):
            print('#'+str(i + 1)+' ... resolving ...')
            id = re.search('company/([0-9]+)', str(companies[i].findChildren()[3]), re.IGNORECASE | re.MULTILINE | re.DOTALL).group(1)
            
            company = JobsBGAPI.get_company_info(id, ['offers', 'name', 'logo', 'description', 'website', 'contacts'])
            company['index'] = str(i + 1)
            
            print(json.dumps(company), file=log.companies)
            print('RESOLVED')
            print('#'+str(i + 1)+'\'s offers ... resolving ...')
            for x in company['offers']:
                print(json.dumps(JobsBGAPI.get_offer_info(x, company['id'])), file=log.jobs)
            print('RESOLVED')
    
    @staticmethod
    def get_companies(log, companies):
        for i in range(len(companies)):
            print('#'+str(i + 1)+' ... resolving ...')
            id = companies[i]
            
            company = JobsBGAPI.get_company_info(id, ['offers', 'name', 'logo', 'description', 'website', 'contacts'])
            company['index'] = str(i + 1)
            
            print(json.dumps(company), file=log.companies)
            print('RESOLVED')
            print('#'+str(i + 1)+'\'s offers ... resolving ...')
            for x in company['offers']:
                if JobsBGAPI.is_internship(x):
                    print(json.dumps(JobsBGAPI.get_offer_info(x, company['id'])), file=log.jobs)
            print('RESOLVED')

class Resources:
    def __init__(self):
        self.companies = open("companies.txt", "a")
        self.jobs = open("jobs.txt", "a")
    def __del__(self):
        self.companies.close()
        self.jobs.close()

log = Resources()

# JobsBGAPI.get_top50_companies(log)
JobsBGAPI.get_companies(log, ["10362","111592","129619","17851","189033","210809","22149","224541","225123","22705","244499","249870","259177","265977","266581","34630","38730","40143","41944","92073"])

del log