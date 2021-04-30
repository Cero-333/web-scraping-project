from selenium import webdriver
import csv
import time
import pandas as pd

# just to create the csv without index easily.
df = pd.DataFrame(columns=["NEW", "COST", "BD", "BA", "AREA", "ADR", "STATE", "NAME", "URL"])
df.to_csv("houses.csv", index=False)

chrome_driver_path = "C:/NewDevelopment/chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)

page = f"https://www.trulia.com/OH/Maineville/"
driver.get(page)

information = {}
key = 1

time.sleep(1)
window_before = driver.current_window_handle

results = driver.find_elements_by_css_selector(".Grid__CellBox-sc-144isrp-0")
for li in results:
    text = li.text
    li.click()
    time.sleep(1)
    # getting the new url.
    new_tab = driver.window_handles
    driver.switch_to.window(new_tab[-1])
    url = driver.current_url
    text += f"\n{url}"
    # creating a house dictionary.
    text_list = text.split("\n")
    try:
        house_dict = {
            "COST": text_list[-8],
            "bd": text_list[-7],
            "ba": text_list[-6],
            "sqft": text_list[-5],
            "adr": text_list[-4],
            "state": text_list[-3],
            "name": text_list[-2],
            "url": text_list[-1]
        }
    except IndexError:
        pass
    else:
        if text_list[0] == "NEW":
            house_dict["NEW"] = "Yes"
        else:
            house_dict["NEW"] = "No"
        information[key] = house_dict
        key += 1
        if len(information) > 9:
            break

    # switching back to main page.
    driver.switch_to.window(window_before)

print(information)

with open("houses.csv", mode="a", newline="") as file:
    writer = csv.writer(file)
    for house in information:
        info = [information[house]["NEW"], information[house]["COST"], information[house]["bd"],
                information[house]["ba"], information[house]["sqft"], information[house]["adr"],
                information[house]["state"], information[house]["name"], information[house]["url"]]
        writer.writerow(info)
