from selenium import webdriver
import time

chrome_driver_path = "C:/development/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")


five_min = time.time() + 60*1   # 1 minutes from now
buy_timeout = time.time() + 5 # 5 seconds

# Get cookie to click
cookie = driver.find_element_by_css_selector("div #cookie")

# Get upgrade item ids.
items = driver.find_elements_by_css_selector("#store div")
item_ids = [item.get_attribute("id") for item in items]


while True:
	cookie.click()

	if time.time() > buy_timeout:
		
		# Get all inventory by store id and <b> tag
		all_prices = driver.find_elements_by_css_selector("#store b")
		

		# Convert <b> text into an integer price and append to item_prices
		item_prices = []
		for price in all_prices:
			element_text = price.text
			if element_text != "":
				cost = int(element_text.split("-")[1].strip().replace(",",""))
				item_prices.append(cost)


		# Create dictionary of store items and prices
		cookie_upgrades = {}
		for x in range(len(item_prices)):
			cookie_upgrades[item_prices[x]] = item_ids[x]


		# Get current cookie count
		money_element = driver.find_element_by_css_selector("#money").text
		if "," in money_element:
			money_element = money_element.replace(",","")
		cookie_count = int(money_element)

		# Find upgrades that we can currently afford
		affordable_upgrades = {}
		for cost, id in cookie_upgrades.items():
		    if cookie_count > cost:
		    	affordable_upgrades[cost] = id
		


		# Purchase the most expensive affordable upgrade
		highest_affortable_upgrade = max(affordable_upgrades)
		print(f"{affordable_upgrades[highest_affortable_upgrade]} : {highest_affortable_upgrade}")

		to_purchase_id = affordable_upgrades[highest_affortable_upgrade] # Will return the name string of highest upgrade
		driver.find_element_by_id(to_purchase_id).click() # Got to webpage and click the item

		#Add another 5 seconds until the next check
		buy_timeout = time.time() + 15


	#After 5 minutes stop the bot and check the cookies per second count.
	if time.time() > five_min:
	    cookie_per_s = driver.find_element_by_id("cps").text
	    print(f'Your rate is: {cookie_per_s} cookies/second')
	    five_min = time.time() + 60*5




