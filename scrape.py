from selenium import webdriver
from datetime import datetime
from credentials import username, password
import requests, lxml.html

def getPercentageFromElement(li):
    if li.get('style') == 'display: none;':
        return 100
    
    return int(lxml.html.fromstring(li.getchildren()[0].get('data-content')).xpath('//div//div/text()')[0].split('%')[0])

def generateFilename():
    return "Level_" + str(getLevel()) + "_" + getTimeString() + ".txt"

def getTimeString():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def getLevel():
    return int(dashboard_html.xpath("//li[@class='dropdown levels']//a//span//text()")[0])

def getTotal(dashboard_html):
    total = 0
    for ele in dashboard_html.xpath("//span[contains(@class, 'total')]//text()"):
        total += int(ele) 
    return total

browser = webdriver.PhantomJS()
browser.get('https://www.wanikani.com/login')

usernameElement = browser.find_element_by_id("user_login")
passwordElement = browser.find_element_by_id("user_password")
submit = browser.find_element_by_css_selector('button')

usernameElement.send_keys(username)
passwordElement.send_keys(password)
submit.click()

innerHTML = browser.execute_script("return document.body.innerHTML")

dashboard_html = lxml.html.fromstring(innerHTML)
lis = dashboard_html.xpath("//div[@class='lattice-single-character']//ul//li")

sum = 0

output = ""

for li in lis:
    character = li.getchildren()[0]
    kanji = character.text
    percentage = getPercentageFromElement(li)

    sum += percentage

    output += str(kanji) + ': ' + str(percentage) + "\n"

output += "Overall: " + str(sum / getTotal(dashboard_html))

print(output)

f = open(generateFilename(), 'w')
f.write(output)
f.close()
