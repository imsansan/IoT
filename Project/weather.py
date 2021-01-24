import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header

def get_content(url):
    
    # pretend to be a browser
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    }
    response = requests.get(url, headers= header)  
    #print(response.content.decode('utf-8'))

    # save to local file
    file_obj = open('weather.html', 'w')  # write a html file, named weather
    file_obj.write(response.content.decode('utf-8'))  # write content
    file_obj.close()  # close file
    
    
def get_weather():
    # read from weather.html
    file_obj = open('weather.html', 'r')  
    html = file_obj.read()  # take all content out
    file_obj.close()  # close html

    soup = BeautifulSoup(html, 'lxml')  # initialize BeautifulSoup
    #print(soup)

    all_div = soup.find('main', id = 'MainContent')

    date = all_div.find('div', class_ = 'CurrentConditions--timestamp--1SWy5').string
    temperature = all_div.find('span', class_ = 'CurrentConditions--tempValue--3KcTQ').get_text()
    phrase = all_div.find('div', class_ = 'CurrentConditions--phraseValue--2xXSr').string
    alertText = all_div.find('h2', class_ = 'AlertHeadline--alertText--aPVO9').get_text()

    detail = all_div.find_all('div', class_ = 'WeatherDetailsListItem--wxData--23DP5')

    high_low = detail[0].get_text()
    wind = detail[1].get_text()
    humidity = detail[2].get_text()
    dew_point = detail[3].get_text()
    pressure = detail[4].get_text()
    uv_index = detail[5].get_text()
    visibility = detail[6].get_text()
    moon_phase = detail[7].get_text()
    
    return (" Temperature: {}\n Phrase: {}\n Wind: {}\n Humidity: {}\n Pressure: {}\n UV Index: {}\n Visibility: {}\n Moon Phase: {}\n Alert: {}\n".format(high_low
    , phrase, wind, humidity, pressure, uv_index, visibility, moon_phase, alertText) )
    #print(all_div)
    #print(date, temperature, phrase, alertText)
    #print(high_low)
    
def send_email(text):
        '''
        sender = input('From: ')
        password = input('password: ')
        smtp_server = input('SMTP_Server: ')
        '''

        #
        sender = '499302455@qq.com'
        sent_host = 'smtp.qq.com'
        sent_user = '499302455@qq.com'
        sent_pass = 'lasuiojarhxfbihc'

        #
        receivers = ['asun5@stevens.edu']

        message = MIMEText("Weather today in Hoboken :\n{}\n".format(text),'plain','utf-8')

        #
        message['From'] = Header('Raspberry Pi','utf-8')
        message['To'] = Header('An Sun','utf-8')
        Subject = "Weather Today in Hoboken"
        message['Subject'] = Header(Subject,'utf-8')   #标题
        try:
            server = smtplib.SMTP_SSL(sent_host, 465)
            print("SMTP complete")

            #server.set_debuglevel(1)
            server.login(sent_user,sent_pass)
            print("login complete")

            server.sendmail(sender,receivers[0],message.as_string())
            print("Success")
            server.quit()

        except smtplib.SMTPException:
            print("Error")



if __name__ == '__main__':
    url = "https://weather.com/weather/today/l/cbb66885b9ded7ed9ce0621f07906cb5d22359040dedaf14fb96ce5ef6a90466"
    get_content(url) #get all content from website and save to local
    result = get_weather() # data wash and return weather data
    print(result)
    send_email(result)# send email