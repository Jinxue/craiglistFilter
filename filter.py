import re
import time
import urllib2
from BeautifulSoup import BeautifulSoup
from sets import Set

# For sending Email
import smtplib
from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
#from email import Encoders

mail_user = "zhangjinxue1984@hotmail.com"
mail_pwd = "Myzhang123"
mail_SMTP_server = "smtp.live.com"
mail_SMTP_port = 587

#def mail(to, subject, text, attach):
def mail(to, subject, text):
    msg = MIMEMultipart()

    msg['From'] = mail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    #part = MIMEBase('application', 'octet-stream')
    #part.set_payload(open(attach, 'rb').read())
    #Encoders.encode_base64(part)
    #part.add_header('Content-Disposition',
    #        'attachment; filename="%s"' % os.path.basename(attach))
    #msg.attach(part)
    
    mailServer = smtplib.SMTP(mail_SMTP_server, mail_SMTP_port)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(mail_user, mail_pwd)
    mailServer.sendmail(mail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

results = re.compile('<p.+<div>', re.DOTALL)

#results = re.compile('<p>.+<div>sort by')
delay = 100
errorcount = 0

def urlAccess(url):
    dat = None
    ua = "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.4) Gecko/20091007 Firefox/3.5.4"
    head = {'User-agent': ua}
    
    errorcount = 0
    msg = ''

    #Get page
    req = urllib2.Request(url, dat, head)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError:
        if errorcount < 1:
            errorcount = 1
            print "Request failed, retrying in " + str(delay) + " seconds"
            time.sleep(int(delay))
            response = urllib2.urlopen(req)
    except urllib2.URLError:
        if errorcount < 1:
            errorcount = 1
            print "Request failed, retrying in " + str(delay) + " seconds"
            time.sleep(int(delay))
            response = urllib2.urlopen(req)
    except:
        print "Request failed, retrying in " + str(delay) + " seconds"
        time.sleep(int(delay))
        response = urllib2.urlopen(req)
    
    try:
        msg = response.read()
        errorcount = 0
    except:
        errorcount = 1
        print "Read URL failed!"
        msg = 'error'
        pass
    return msg

model_check_re = re.compile("civic|accord|acura|corolla|camry|lexus|sentra|sonata|altima|infiniti|mazda ?6|elantra|impala|malibu|focus|fusion|lancer|galant|jetta|passat")
#model_check_re = re.compile("civic|corolla")
#fake_check_re = re.compile("honda&")
def model_check(desp):
    """ We need to get rid of the fake keywords"""
    if re.search("honda", desp) and re.search("toyota", desp) and re.search("nissan", desp):
        return False
     
    res = re.search(model_check_re, desp)
    if res:
        return True
    else:
        return False
    
clean_re = re.compile("clean|excellent|clear|perfect|great")
def clean_check(desp):
    #y = re.compile("clean|excellent|fax|clear|perfect|great")
    res = re.search(clean_re, desp)
    
    #if "clean" in desp or "excellent" in desp or "fax" in desp or "clear" in desp or "perfect" in desp:
    if res:
        return True
    else:
        return False
    
maintain_re = re.compile("maint|record|condition|female|lady|girl")
def maintain_check(desp):
    #y = re.compile("maint|record")
    res = re.search(maintain_re, desp)

    #if "maint" in desp or "record" in desp:
    if res:
        return True
    else:
        return False

owner_re = re.compile("own|original")
def owner_check(desp):
    #y = re.compile("owner|original")
    res = re.search(owner_re, desp)

    #if "owner" in desp or "original" in desp:
    if res:
        return True
    else:
        return False

call_re = re.compile("call|4\.?8\.?[0o]|6\.?[0o]\.?2|6\.?2\.?3")
def call_check(desp):
    #y = re.compile("call|4\.?8\.?[0o]|6\.?[0o]\.?2|6\.?2\.?3")
    res = re.search(call_re, desp)

    #if "call" in desp or "480" in desp or "602" in desp or "623" in desp or  \
    #    "6o2" in desp or "48o" in desp or "6.0.2" in desp:
    if res:
        return True
    else:
        return False

regular_re = re.compile("(regular|clean|clear) (az|arizona )?title|(car)?fax")      
restore_re = re.compile("restore|salvage")
""" we need to handle the case like: "clear title - not salvage title"""""
def clean_title_check(desp):
    #y = re.compile("regular|clean (az )?title")
    res = re.search(regular_re, desp)
    #y1 = re.compile("restore|salvage|manual")
    res1 = re.search(restore_re, desp)
    if res:
        return True
    #elif "restore" in desp or "salvage" in desp or "manual" in desp:
    elif res1:
        return False
    else:
        return True

auto_re = re.compile("automatic|automanual")      
manual_re = re.compile("manual|speed")
""" we need to handle the case like: "automatic - not manual"""""
def auto_check(desp):
    #y = re.compile("regular|clean (az )?title")
    res = re.search(auto_re, desp)
    #y1 = re.compile("restore|salvage|manual")
    res1 = re.search(manual_re, desp)
    if res:
        return True
    #elif "restore" in desp or "salvage" in desp or "manual" in desp:
    elif res1:
        return False
    else:
        return True
    
rich_re = re.compile("chandler|scottsdale")
def rich_check(title):
    #y = re.compile("chandler|scottsdale")
    res = re.search(rich_re, title)

    #if "chandler" in title or "scottsdale" in title:
    if res:
        return True
    else:
        return False

non_sedan_re = re.compile("coupe|truck|convert(ible|\.)|tracker|van|cab|jeep|runner|4x4|pickup")
def sedan_check(desp):
    #y = re.compile("coupe|truck|convertible|tracker|van")
    res = re.search(non_sedan_re, desp)

    #if "coupe" in desp or "truck" in desp or "convertible" in desp or "tracker" in desp or "van" in desp:
    if res:
        return False
    else:
        return True
    
year_re = re.compile("200[7-9]|201[0-2]")
def year_check(desp):
    res = re.search(year_re, desp)
    
    if res:
        return True;
    else:
        return False

vin_re = re.compile("vin")
def vin_check(desp):
    res = re.search(vin_re, desp)
    
    if res:
        return True;
    else:
        return False

def find_end(desp):
    endI = 100000;
    end1 = desp.find('<script') 
    if  end1 > 0:
        endI = min(endI, end1) 
    end1 = desp.find('<a') 
    if  end1 > 0:
        endI = min(endI, end1)
    end1 = desp.find('<center') 
    if  end1 > 0:
        endI = min(endI, end1)
    end1 = desp.find('<img') 
    if  end1 > 0:
        endI = min(endI, end1)
    end1 = desp.find('<!--') 
    if  end1 > 0:
        endI = min(endI, end1)
    return endI
                
def search_city_min_max_clean():
    #t = datetime.datetime.now()
    #tyme = time.mktime(t.timetuple())
    
    #url = "http://" + city + ".craigslist.org/search/" + section + "?query=" + query  + "&srchType=" + srchType + "&maxAsk=" + maxAsk + "&minAsk=" + minAsk 
    #url = "http://" + city + ".craigslist.org/search/" + section + "?maxAsk=" + maxAsk + "&minAsk=" + minAsk 
    url = "http://" + city + ".craigslist.org/search/" + section + "?maxAsk=" + maxAsk + "&minAsk=" + minAsk 
    #Setup headers to spoof Mozilla
    msg = urlAccess(url)
    if errorcount == 1:
        return 0
    #print msg;

    soup = BeautifulSoup(msg)
    total = 0
    goodNews = 0
    content = '\r\n'
    # Obtain the messages in the first page
    for tag in soup.findAll('a', href=True):
        #print tag['href']
        href = tag['href']
        # Find a new one
        if href.endswith("html") and href not in WholeList:
            #print tag['href']
            total += 1
            WholeList.add(href)
            #href = "http://phoenix.craigslist.org/nph/cto/3602714024.html"
            post = urlAccess(href)
            #post = urlAccess("http://phoenix.craigslist.org/nph/cto/3533733353.html")
            # First, parse the webpage to extract the clean <section id="userbody">
            soup = BeautifulSoup(post)
            #print soup
            #soup.replace('<br />', '\r\n')
            try:
                title = soup.find("h2", {"class" : "postingtitle"}).getText().lower()
            except:
                continue # The post has been deleted
            #print title
            
            #desp = soup.find(id = "userbody")
            # Craiglist has changed this domain to a new name.
            desp = soup.find(id = "postingbody")
            desp = str(desp)
            #print desp
            endI = find_end(desp)
            #desp = soup.find(id = "userbody").getText()
            #endI = desp.find('<!--')
            
            desp = desp[:endI].lower()
            #print desp
            
            desp = desp.replace('<br />', '\r\n')
            desp = desp.replace('<section id=\"postingbody\">', '')
            desp = desp.replace('</section>', '')
            #print desp
            
            titles = title[:title.find('(')]
            
            # just check the model we are interested
            if model_check(desp) == False and model_check(titles) == False:
                continue 
            
            # I like the car after 2000
            if year_check(desp) == False and year_check(titles) == False:
                continue
            
            if auto_check(desp) == False:
                continue

            if sedan_check(desp) == False and sedan_check(titles) == False:
                continue

            # Ignore the restored title.
            if clean_title_check(desp) == False:
                continue
            
            # Second, we find the good words
            # If there is no phone number, it should be a nice car;
            # If it only has one owner, it also should be a nice car.
             
            if (call_check(desp) == False and clean_check(desp) == True) or \
            (clean_check(desp) == True and maintain_check(desp) == True) or \
            (clean_check(desp) == True and owner_check(desp) == True) or \
            (clean_check(desp) == True and vin_check(desp) == True) or \
            (maintain_check(desp) == True and owner_check(desp) == True) or \
            (clean_check(desp) == True and rich_check(title) == True) :
            #if desp.find('clean'):
                try:
                    content += title;
                    content += '\r\n'
                    content += desp;
                    content += '\r\n'
                    content += href;
                    content += '\r\n---------------------------------------------------------------\r\n'
                    goodNews += 1
                
                    print desp
                except:
                    pass

    if goodNews > 0:
        print 'send Email.'
        subj = str(goodNews) +  ' ' + subject
        print content               
        #mail(to, subj,content)

    return total      
            
        
city = "phoenix"
section = "cto"
query="clean"
srchType = "A"
minAsk = "8000"
maxAsk = "11000"

WholeList = Set([])

#Mail setting
to = 'zhangjinxue@gmail.com'
#to = "jxcking@gmail.com"
subject = 'New Craiglist messages with clean, maitained and less-owner cars'
#content = 'test'

#mail(to, subject, content)
while 1:
    t_start = time.time()
    print "\nBegin crawl"
    tot = search_city_min_max_clean();
    used = time.time() - t_start
    print 'Check ' + str(tot) + ' new messages. Use ' + str(used) + ' seconds.'
    time.sleep(60)
