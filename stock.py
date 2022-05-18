from bs4 import BeautifulSoup
import requests
import time
import smtplib
import os

email=os.environ.get('EMAIL_ADDRESS')
password=os.environ.get('PASSWORD')

print('Running')
def nifty50_stocks():
    links=list()
    count=0
    html_text1=requests.get('https://www.moneycontrol.com/stocks/marketstats/indcontrib.php?optex=NSE&opttopic=indcontrib&index=9').text
    soup=BeautifulSoup(html_text1,'lxml')
    index=soup.find_all('a',class_='bl_12')
    for i in index:
        count=count+1
        if count%2!=0:
            i1=i.text
            link=i['href']
            links.append(link)
    
    top50stocks=list()
    for index,parsedlink in enumerate(links):
        html_text=requests.get('https://www.moneycontrol.com'+parsedlink).text
        soup=BeautifulSoup(html_text,'lxml')
        var=soup.find('div',class_='inid_name')
        company_name=var.find('h1').text
        price=soup.find('div',class_='inprice1 nsecp').text
        open_price=float(soup.find('td',class_='nseopn bseopn').text.replace(',',''))
        close_price=float(soup.find('td',class_='nseprvclose bseprvclose').text.replace(',',''))
        high_price=float(soup.find('td',class_='nseHP bseHP').text.replace(',',''))
        low_price=float(soup.find('td',class_='nseLP bseLP').text.replace(',',''))
        top50=f'Company: {company_name} Last Price: {price} O: {open_price} C: {close_price} H: {high_price} L: {low_price} \n'
        top50stocks.append(top50)

        if -1<=open_price-low_price<=1 and -1<=close_price-high_price<=1:
            with smtplib.SMTP('smtp.gmail.com',587) as smtp:
                smtp.ehlo()
            #Encrypt the traffic
                smtp.starttls()
            #Re-identify as an encrypted connection
                smtp.ehlo()
            #Login into gmail account using environment variables    
                smtp.login(email,password)
                subject='BULLISH MARUBUZO'
                body=f'A bullish marubuzo is formed whenever the, Open = Low and High = Close. We observed a bullish marunuzo today in {company_name}'
                msg=f'Subject: {subject}\n\n{body}'
                smtp.sendmail(email,email,msg)
                
        elif -1<=open_price-high_price<=1 and -1<=close_price-low_price<=1:
            with smtplib.SMTP('smtp.gmail.com',587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(email,password)
                subject='BEARSIH MARUBUZO'
                body=f'A bearish marubuzo is formed whenever the, Open = High and Low = Close. We observed a bullish marunuzo today in {company_name}'
                msg=f'Subject: {subject}\n\n{body}'
                smtp.sendmail(email,email,msg)
    
    with open(f'{index}.txt','w') as f:
        for x in top50stocks:
            f.write(x)    


if __name__=='__main__':
    while True:
        nifty50_stocks()
        timetill=30
        time.sleep(timetill*60)