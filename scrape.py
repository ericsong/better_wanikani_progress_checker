from selenium import webdriver
from datetime import datetime
from credentials import username, password
import requests, lxml.html

def getPercentageFromElement(a):
    return int(lxml.html.fromstring(a.get('data-content')).xpath('//div//div/text()')[0].split('%')[0])

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
characters = dashboard_html.xpath("//div[@class='lattice-single-character']//ul//li//a")

sum = 0

output = ""

for character in characters:
    kanji = character.text
    percentage = getPercentageFromElement(character)

    sum += percentage

    output += str(kanji) + ': ' + str(percentage) + "\n"

output += "Overall: " + str(sum / getTotal(dashboard_html))

f = open(generateFilename(), 'w')
f.write(output)
f.close()
