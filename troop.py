from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import shutil
import xlwt
import time

#choose the source folder of the script and the destination folder of the excel file
src = 'C:/Users/rodry/OneDrive/Documentos/Projetos Python/troopscraper/TW_scraper_git/troops.xls'
dst = './data/troops_count.xls'

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Troop Counter", cell_overwrite_ok=False) 
style = xlwt.easyxf('font: bold 1, color blue;')
bold = xlwt.easyxf('font: bold 1')

# ask for tribal wars credentials
user = input ("Enter user :") 
userpass = input("Enter password : ")  

#get chromedriver and go to tribalwars
driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
#hide browser
driver.set_window_position(-10000,0)
driver.get('https://enc4.tribalwars.net/game.php?village=1980&screen=ally&mode=members_troops')

element = driver.find_element_by_tag_name('h2')

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

#playersID array
arr = [848937173 , 848941819, 848941982, 848945478, 848932450,848942150,848941598,848941934,848941896,848943143,10081546,11586147]
arr_nomes = ['caracortada', 'Claudiac8', 'F.T.Freitas', 'Forcedarmy', 'Guts', 'Jarbas', 'julzz', 'LaTila', 'Lord Shadow', 'Meiguinho', 'rodrygors', 'wendig0xd']
#types of units
tropas = ['lanças','espadas','vikings','espias','cl','cp','arietes','catas','nobres','comandos','a chegar']
r = 0
c = 0
x = 0
troops_final=[0] * 11
info = sheet.write(r,c,'Tropas da Tribo',style)
r = 7
#for each player check the troops
for i in range(len(arr)):
    troops=[0] * 11
    c = 2
    driver.get('https://enc4.tribalwars.net/game.php?screen=ally&mode=members_troops&player_id=%s&village=3680' % (arr[i]))
    troops_table = driver.find_elements_by_css_selector('.w100 td')
    info = sheet.write(r-1, 0, arr_nomes[i], bold)
    x = r
    for row in troops_table:
        if r - x == 12: 
            c += 1
            r = x
        if 0 < r - x < 13:
            troops[(r-x)-1] += int(row.text)
        if r-x != 0: info = sheet.write(r,c, row.text)
        else: info = sheet.write(r,c, row.text, bold)
        r += 1
    
    r = x
    info = sheet.write(r,1,'Total', bold)
    for k in range (len(troops)):
        r += 1
        info = sheet.write(r,1,troops[k])
        info = sheet.write(r, 0, tropas[k])
    kk = 0
    for k in troops:
        troops_final[kk] += k
        kk += 1
    troops.clear()
    r = x + 15
info = sheet.write(2,0,'Total', bold)
info = sheet.write(3,0,'de tropas', bold)
c = 1
for t_total in troops_final:
    info = sheet.write(2,c,tropas[c-1],bold)
    info = sheet.write(3,c,t_total)
    c += 1
workbook.save("troops.xls")
shutil.move(src, dst)
driver.quit()