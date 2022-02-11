from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dateutil.parser import parse
import json

RISK_FREE_RATE_URL = 'https://ng.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver


def get_latest_date_value(driver):
  driver.get(RISK_FREE_RATE_URL)
  
  latest_date = driver.find_element(By.XPATH, '/html/body/div[5]/section/div[9]/table[1]/tbody/tr[1]/td[1]').text
  latest_value = driver.find_element(By.XPATH, '/html/body/div[5]/section/div[9]/table[1]/tbody/tr[1]/td[2]').text
  return {
    'currentDate' : latest_date,
    'currentValue' : latest_value
  }

if __name__ == "__main__":
  print('Creating driver')
  driver = get_driver()

  print('Fetching RISK FREE RATE Page')
  latest_date_value = get_latest_date_value(driver)
  
  print(f'Found {len(latest_date_value)} data points')
  
  print('currentDate:', latest_date_value['currentDate'])
  print('currentValue:', latest_date_value['currentValue'])

  # Convert Date to YYYY-MM-DD format
  format_date = str(parse(latest_date_value['currentDate'])).split()[0]
  print(format_date)

  # Append date to JSON file.
  data = {
               "Date": format_date,
               "Price": latest_date_value['currentValue']
          }

  # with open('United States 10-Year Bond Yield Historical Data.json', 'ab+') as outfile:
    ## End of File - Working fine
    # outfile.seek(0,2)
    # outfile.seek(-1,2)  
    # outfile.truncate()
    # outfile.write(','.encode())
    # outfile.write(json.dumps(data).encode())
    # outfile.write(']'.encode())
    # outfile.close()


  with open('United States 10-Year Bond Yield Historical Data.json', 'r') as outfile:
    next(outfile)
    data_file = outfile.readlines()

  with open('United States 10-Year Bond Yield Historical Data.json', 'w+') as outfile:
    outfile.write("[")
    outfile.write("\n")
    outfile.write(json.dumps(data, indent=4))
    outfile.write(",")
    outfile.write("\n")
    
    for line in data_file:
      outfile.write(line)

    outfile.close()

  print('Finished.')
