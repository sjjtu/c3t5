from selenium import webdriver
import csv

path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
browser = webdriver.Firefox(firefox_binary="/usr/bin/firefox")
url = "https://wasserportal.berlin.de/station.php?anzeige=i&sstation=5865900"
browser.get(url)
l = []
btn = browser.find_element_by_xpath("//a[@title='Nächste Messstelle']")
btn.click()
while url != browser.current_url:
    nr = browser.find_element_by_xpath("//table/tbody/tr[1]/td[2]").text
    name = browser.find_element_by_xpath("//table/tbody/tr[2]/td[2]").text
    rechtswert = browser.find_element_by_xpath("//table/tbody/tr[last()-1]/td[2]").text
    hochwert = browser.find_element_by_xpath("//table/tbody/tr[last()]/td[2]").text


    measure_types = browser.find_elements_by_xpath("//ul[@class='nav level-1']")
    s_measure_types = []
    for c in measure_types:
        for el in c.text.split():
            if el not in ["Informationen", "Kennwerte", "Lagekarte"]:
                s_measure_types.append(el)

    l.append([nr, name, rechtswert, hochwert, ",".join(s_measure_types)])

    btn = browser.find_element_by_xpath("//a[@title='Nächste Messstelle']")
    btn.click()

print(l)
with open("station.csv", "w", newline="") as file:
    wr = csv.writer(file)
    wr.writerows(l)