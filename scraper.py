# Libraries
import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib.request
from flask import Flask,render_template,request
import os
from flask import send_file
import random

app = Flask(__name__)

@app.route('/',methods=["GET","POST"])
def scrape():
    if request.method=="POST":
        try:
            fe=request.form
            role=fe['role']
            place=fe['place']

            Shine,Shine2 = shine(place,role)
            Indeed,Indeed2 = indeed(place,role)
            Times,Times2 = times(place,role)

            webs=['shine','indeed','Times Jobs']

            all_jobs=[Shine,Indeed,Times]

            add_to_excel(webs,all_jobs)

            all_jobs2=[Shine2,Indeed2,Times2]

            return render_template('result.html',all_jobs=all_jobs2)
        except:
            return render_template('result.html',all_jobs=None)



    return render_template('index.html')

@app.route('/down',methods=["GET","POST"])
def down ():
    # add_to_excel(webs,all_jobs)
    if request.method=="POST":

        
        path = "jobs.xlsx"
        return send_file(path, as_attachment=True)

def indeed(place,role):

  job=''
  role=role.split(' ')
  for i in role:
    if i != role[-1]:
      job+=i+'+'
    else:
      job+=i  

  url = urllib.request.urlopen(f'https://www.indeed.co.in/jobs?q={job}&l={place}')
  soup = BeautifulSoup(url,'html.parser') 
  a=soup.find_all('td', attrs={'id': 'resultsCol'})
  jobs=[]
  b=soup.find_all('a', attrs={'class': 'jobtitle turnstileLink'})

  for i in a:
      loc = i.find_all('div', attrs={'class':'recJobLoc'})
      title=i.find_all('a', attrs={'class':'jobtitle turnstileLink'})
      date='not provided'
      comp = i.find_all('span', attrs={'class':'company'})
      desc = i.find_all('div', attrs={'class':'summary'})
      href=i.find_all('a', attrs={'class':'jobtitle turnstileLink'})
      tel='-'
      mail='-'
      web='-'
      skills='-'
      exp='-'
      sal='-'
      
      for o in range(0,len(b)):
          jobs.append([title[o].text.strip(),date,comp[o].text.strip(),tel,mail,web,loc[o]['data-rc-loc'],comp[o].text.strip(),skills,desc[o].text.strip(),sal,exp,'https://www.indeed.com'+ href[o]['href']])
      print(len(jobs))
  return pd.DataFrame(jobs),jobs




def shine(place,role):
  
    job=''
    role=role.split(' ')
    for i in role:
        if i != role[-1]:
            job+=i+'-'
        else:
            job+=i  


    fhand = urllib.request.urlopen(f'https://www.shine.com/job-search/{job}-jobs-in-{place}')
    soup = BeautifulSoup(fhand,'html.parser') 
    jobs2=[]
    j=0
    regex = re.compile('^search_listing')
    content_lis = soup.find_all('li', attrs={'class': regex})

    for i in content_lis:

        if i!=None:

            
            title = i.find_all('li', attrs={'class': 'snp cls_jobtitle'})[0].text
            date = i.find_all('li', attrs={'class': 'time share_links jobDate'})          
            employer = i.find_all('li', attrs={'class': 'snp_cnm cls_cmpname cls_jobcompany'})         
            tel='-'
            mailid='-'
            web=i.find_all('li', attrs={'class': 'snp_cnm cls_cmpname cls_jobcompany'})[0].text
            loc=i.find_all('em')[0].text
            web=i.find_all('li', attrs={'class': 'snp_cnm cls_cmpname cls_jobcompany'})[0].text
            skill=[]
            skills = i.find_all('div', attrs={'class': 'sk jsrp cls_jobskill'})[0]
            skill=skills.text
            desc = i.find_all('li', attrs={'class': 'srcresult'})
            salary='-'
            exp = i.find_all('span', attrs={'class': 'snp_yoe cls_jobexperience'})[0].text.strip()
            link = i.find('a', attrs={'class': 'cls_searchresult_a searchresult_link'})
        
            jobs2.append([title.strip(),date[j].get_text().strip(),employer[j].get_text().strip(),tel,mailid,web.strip(),loc.strip(),web.strip(),skill,desc[j].get_text().strip(),salary,exp,'https://www.shine.com'+ link['href']])
    print(len(jobs2))
    return pd.DataFrame(jobs2),jobs2
    

def times(place,role):
        
    jobs3 = []
    job=''
    role=role.split(' ')
    for i in role:
        if i != role[-1]:
            job+=i+'+'
        else:
            job+=i  



    url = urllib.request.urlopen(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={job}&txtLocation=+{place}')
    soup = BeautifulSoup(url,'html.parser') 

    # a=soup.find_all('ul', attrs={'class': 'new-joblist'})
    # print(a)


    regex = re.compile('^new-joblist')
    content_lis = soup.find_all('ul', attrs={'class': regex})
    # print(content_lis)
    no=0
    for i in content_lis:
        while no<25:

            title = i.find_all('strong', attrs={'class': 'blkclor'})[no].text

            date = '-'
            
            company_name=i.find_all('h3', attrs={'class': 'joblist-comp-name'})[no].text.strip()
            
            tel = '-'

            mail = '-'

            web = '-'

            set1=i.find_all('ul', attrs={'class': 'top-jd-dtl clearfix'})[no].text
            set12=set1.split()
            e1 = set12[0].strip('card_travel')
            e2 = set12[2]

            Location = set12[-1]

            company_name=i.find_all('h3', attrs={'class': 'joblist-comp-name'})[no].text.strip()
            Desc = i.find_all('ul', attrs={'class': 'list-job-dtl clearfix'})[no].text
            Desc = Desc.split('KeySkills:')

            
            Skills =Desc[1].strip()

            Desc1 = Desc[0].strip()

            sal ='-'    

            exp= f'{e1} - {e2}'

            
            Link = i.find_all('a', href=re.compile('^https://www.timesjobs.com/job-detail/'))[no]
            Link = str(Link).split('"')
            fLink=Link[1]

            jobs3.append([title,date,company_name,tel,mail,web,Location,company_name,Skills,Desc1,sal,exp,fLink])
            no+=1
    print(len(jobs3))
    return pd.DataFrame(jobs3),jobs3
        



def add_to_excel(webs,all_jobs):
    ra=random.randint(0,10000)
    # filename=f'Jobs{ra}.xlsx'
    filename='jobs.xlsx'
    
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    number=0
    for jobs in all_jobs:
        jobs.columns=['Job Title','	Date','	Recruiter name','	Tel','	Mailid','	Website ','	Location','	Company	','Skills','	Desc','	Salary','	Experince','	Link']

        jobs.to_excel(writer, sheet_name=webs[number])
        
        print(f'{webs[number]} added to excel file')

        number+=1



    writer.save()
    
    
    # return send_file(filename, attachment_filename=filename)
    


# if __name__=="__main__":
#   place='bangalore'
#   role='Java'
#   Shine = shine(place,role)
#   Indeed = indeed(place,role)
#   webs=['shine','indeed']
#   all_jobs=[Shine,Indeed]
#   add_to_excel(webs,all_jobs)
  

        

        #  try other websites //  hosting

   




if __name__ == "__main__":
    app.run(debug=True)
