from selenium import webdriver
import csv

path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
browser = webdriver.Chrome()
url = "https://wasserportal.berlin.de/station.php?anzeige=i&sstation=5865900"
browser.get(url)
l = []
next_url = ""
print("sadas")
while next_url != url:
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
    browser.implicitly_wait(2)
    next_url = browser.current_url

print(l)
with open("station.csv", "w", newline="") as file:
    wr = csv.writer(file)
    wr.writerows(l)