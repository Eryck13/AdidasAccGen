import json
import requests
from time import sleep
import datetime
import random
from bs4 import BeautifulSoup as bs


def main():#'✓'
    
    print('Welcome to Adidas account generator!')
    url = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MiAccount-Register/'
    
    #User Input
    proxychoice = input('Will you be using proxies? Please enter "Yes" or "No": ')
    user = input('Please enter the name for your domain with: ')
    domain = input('Insert a domain with @: ')
    passw = input('Please enter a password for all your accounts: ')
    amount = input('Please enter the amount of accounts you would like to make: ')
    print('\n')
    
    #Open firstnames.txt and read from the file
    ranfname = open('firstnames.txt', 'rt').read().splitlines()
    #Replace any extra spaces in the list
    ranfname = [ranfname.replace(' ', '') for ranfname in ranfname]     
    
    #Open lastnames.txt and read from the file
    ranlname = open('lastnames.txt', 'rt').read().splitlines()
    #Replace any extra spaces in the list
    ranlname = [ranlname.replace(' ', '') for ranlname in ranlname]     
   
    with open('proxiesadidas.txt', 'r') as r:
       proxylist = r.read().splitlines()

 
                  
    for i in range(int(amount)): 
        
                #Randomize a bunch of stuff
                bday = random.randint(1,30)
                bmonth = random.randint(1,12)
                byear = random.randint(1970,1999)
                session = requests.Session()
                randtime = random.randint(1,3) 
               
                #If user Inputs "Yes" we select a random proxy
                if proxychoice == 'Yes':
                    proxy = random.choice(proxylist)
                
                #More random selection of stuff
                domainfinal = user + str(random.randint(1,10000)) + domain
                passwfinal = passw + str(random.randint(1,10000))
                ranfname2 = random.choice(ranfname)
                ranlname2 = random.choice(ranlname)
                
                session.headers = {'origin':'https://www.adidas.com',"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
                
                #Final account format will look like this(User@insertdomain)
                accs = domainfinal + ":" + passwfinal + ":" + ranfname2 + ":" + ranlname2
                
                #Get requests to find the session
                find = session.get(url)
                print("Starting Account Creation....")
                
                if find.status_code == 200:
                  print('[',datetime.datetime.utcnow(),']','Session Found!')
                #sleep(1)
                
                #Assigning check to the whole text content of the get request and then parse through html
                check = bs(find.text, "html.parser")
                
                #Parse through the html until we find the corresponding name dwfrm_mipersonalinfo_securekey
                keyfind = check.find_all("input",{"name":"dwfrm_mipersonalinfo_securekey"})
                
                #Key is our secure token as adidas calls it, we check the "value" field and assign the value of dwfrm_mipersonalinfo_securekey to the variable "key" 
                key = keyfind[0]["value"]
                
                #Parse through the html until we find the ID of dwfrm_mipersonalinfo
                var = check.find_all("form",{"id":"dwfrm_mipersonalinfo"})
                
                #V1 gets assigned to the whole "action" field
                v1 = var[0]["action"]
                
                #We parse through v1's string and find the unique variable after Register/ and split it and assign it to varend
                varend = v1.split("Register/")[1]
                
                #Headers 
                session.headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	                                "Accept-Encoding":"gzip, deflate, br",
	                                "Accept-Language":"en-US,en;q=0.9",
	                                "Cache-Control":"max-age=0",
	                                "Connection":"keep-alive",
	                                "Content-Type":"application/x-www-form-urlencoded",
	                                "Host":"www.adidas.com",
	                                "Origin":"https://www.adidas.com",
	                                "Referer":"https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MiAccount-Register/",
	                                "Upgrade-Insecure-Requests":"1",
	                                "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
                                    }
                #Appending the starting url to the variable we just parsed EX: (https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MiAccount-Register/ +C19394949) 
                url2 = url + varend
                
                #Our payload for step 1
                load1 = {'dwfrm_mipersonalinfo_firstname':ranfname2,
                    'dwfrm_mipersonalinfo_lastname':ranlname2,
                    'dwfrm_mipersonalinfo_customer_birthday_dayofmonth':str(bday),
                    'dwfrm_mipersonalinfo_customer_birthday_month':str(bmonth),         
                    'dwfrm_mipersonalinfo_customer_birthday_year':str(byear),
                    'dwfrm_mipersonalinfo_step1':'Next',
                    'dwfrm_mipersonalinfo_securekey':key
                    }
                
                #Post request for Step 1
                post1 = session.post(url2,data=load1)
                
                #sleep(1)
                
                #Condition for step 2 
                if post1.status_code == 200 and "New password" and "Confirm password" in post1.text:
                        print('[',datetime.datetime.utcnow(),']','Step 1 Passed!')
                        
                        #Headers
                        headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
	                                                'Upgrade-Insecure-Requests': '1',
	                                                'Host': 'www.adidas.com',
	                                                'Origin': 'https://www.adidas.com',
	                                                'Referer': url2}
               
                        #We then repeat the same parsing steps as step 1
                        check2 = bs(post1.text, "html.parser")
                        keyfind2 = check2.find_all("input",{"name":"dwfrm_milogininfo_securekey"})
                        key2 = keyfind2[0]["value"]
                
                        var2 = check2.find_all("form",{"id":"dwfrm_milogininfo"})
                        v2 = var2[0]["action"]
                        varend2 = v2.split("Register/")[1]
                        
                        #Appending the starting url to the variable we just parsed EX: (https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MiAccount-Register/ +C193975757)
                        url3 = url + varend2
                        
                        #Our payload for step 2
                        load2 = {'dwfrm_milogininfo_email': domainfinal,
				        'dwfrm_milogininfo_password': passwfinal,
				        'dwfrm_milogininfo_newpasswordconfirm': passwfinal,
				        'dwfrm_milogininfo_step2': 'Next',
				        'dwfrm_milogininfo_securekey': key2
                        }
                        
                        #Post request for Step 2
                        post2 = session.post(url3,data=load2,headers=headers2)
                        
                        #sleep(1)
                        
                        #Condition for step 3
                        if post2.status_code == 200:
                                print('[',datetime.datetime.utcnow(),']','Step 2 Passed!')
                                
                                #Repeat the same parsing that we did for step 1,2
                                check3 = bs(post2.text, "html.parser")
                                keyfind3 = check3.find_all("input",{"name":"dwfrm_micommunicinfo_securekey"})
                                key3 = keyfind3[0]["value"]
                                
                                var3 = check3.find_all("form",{"id":"dwfrm_micommunicinfo"})
                                v3 = var3[0]["action"]
                                varend3 = v3.split("Register/")[1]
                                
                                #Appending the starting url to the variable we just parsed EX: (https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MiAccount-Register/ +C193986886)
                                url4 = url + varend3
                                
                                #Our payload for step 3
                                load3 = {
				                'dwfrm_micommunicinfo_agreeterms': 'true',
				                'dwfrm_micommunicinfo_step3': 'Register',
				                'dwfrm_micommunicinfo_securekey': key3
			                    } 
                                
                                #Post request for Step 3
                                post3 = session.post(url4,data=load3)     
                                
                                #sleep(1)
                             
                                #Condition to see if account was successfully created 
                                if post3.status_code == 200 and "MiAccount-Redirect?justRegistered=true&redirect=" in post3.text:
                                        print('[',datetime.datetime.utcnow(),']','Step 3 Passed!')
                                        print('[',datetime.datetime.utcnow(),']','Account Created!')
                                        print(accs+"\n")
                                        
                                        #Writes successfully created accounts to a .txt file
                                        f = open("adidasaccounts.txt","a")
                                        f.write("\n" + accs)
                                
   
        

    #sleep(randtime)

main()