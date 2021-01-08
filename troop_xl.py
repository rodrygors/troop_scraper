from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import shutil
import xlwt
import time

class Player:
    id = 0
    name = ''
    p_troops=[0] * 11

    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __str__(self): return ('Nome: ' +self.name+ '\nID: ' +self.id)

#choose the source folder of the script and the destination folder of the excel file
src = 'C:/Users/rodry/OneDrive/Documentos/Projetos Python/troopscraper/TW_scraper_git/troops.xls'
dst = './data/troop_base.xls'

#excel stuff
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Troop Counter", cell_overwrite_ok=False) 
style = xlwt.easyxf('font: bold 1, color blue;')
bold = xlwt.easyxf('font: bold 1')

# ask for tribal wars credentials and other necessary info
user = input ("Enter user :") 
userpass = input("Enter password : ")  
tribe_id = input("Enter your tribe ID : ")

#get chromedriver and go to tribalwars
driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
extra_driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

#hide browser
#driver.set_window_position(-10000,0)

#find login elements
driver.get('https://enc4.tribalwars.net')
username = driver.find_element_by_id("user")
password = driver.find_element_by_id("password")

#fill login
username.send_keys(user)
password.send_keys(userpass)
driver.find_element_by_class_name('btn-login').click()

#check the title of the website
actualtitle = driver.title
print(actualtitle)

#wait for button to load in the html
time.sleep(2)
driver.find_element_by_xpath('//a[2]/span').click()

#Get tribe member's names and ids
driver.get('https://enc4.tribalwars.net/game.php?screen=ally&mode=members')
arr_players = []
n_membros = int(driver.find_element_by_xpath('//form[@id=\'form_rights\']/table/tbody/tr[last()-1]/td[2]').text)
print(n_membros)
for i in range(n_membros):
    member_name = driver.find_element_by_xpath('//form[@id=\'form_rights\']/table/tbody/tr[%s]/td/a' % (i+2)).text
    print(member_name)

    member_link = str(driver.find_element_by_xpath('//a[contains(text(),\'%s\')]' % member_name).get_attribute('href'))
    
    member_id = member_link.split('id=')
    
    try:
        p = Player(member_id[1], member_name)
    except:
        extra_driver.get('https://www.twstats.com/enc4/index.php?page=tribe&mode=members&id=%s'% tribe_id)
        member_link = str(extra_driver.find_element_by_xpath('//a[contains(text(),\'%s\')]' % member_name).get_attribute('href'))
        member_id = member_link.split('id=')
        print(member_id)
        p = Player(member_id[1], member_name)
        extra_driver.quit()
    print(p)
    arr_players.append(p)

#types of units
troops_names = ['lanças','espadas','vikings','espias','cl','cp','arietes','catas','nobres','comandos','a chegar']

#loops to read and print every village's units
r = 2
c = 0
x = 0

for i in range(len(arr_players)):
    r += 1
    c = 1
    driver.get('https://enc4.tribalwars.net/game.php?screen=ally&mode=members_troops&player_id=%s' % (arr_players[i].id))
    troops_table = driver.find_elements_by_css_selector('.w100 td')
    info = sheet.write(r, 0, arr_players[i].name)
    for row in troops_table:
        if c % 13 == 0:
            r += 1
            sheet.write(r, 0, arr_players[i].name)
            c = 1
        sheet.write(r,c, row.text)
        c += 1

workbook.save("troops.xls")
shutil.move(src, dst)
driver.quit()