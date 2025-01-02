from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
import csv

def main():
    try:
        # UC webdriver
        # NOTES FOR NON CANADIAN (en) USERS
        # /ca/en is probably just their language localization 
        # but make sure it is with your own localalized link
        driver = uc.Chrome()
        
        # driver.get("https://www.nespresso.com/ca/en/order/capsules/original")
        driver.get("https://www.nespresso.com/ca/en/order/capsules/vertuo")

        time.sleep(5)
        # Get the page source after JavaScript has rendered
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')

        # GET name of pods
        pods_name = soup.findAll('span', class_='_name_80ips_101')
        pods_name_filtered = [pod.text.strip() for pod in pods_name]

        # GET product image link of pods
        pods_img = soup.findAll('img', class_='_image_vei9w_87')
        pods_img_filtered = [f"https://www.nespresso.com{img.get('src')}" for img in pods_img]

        # GET product link of pods
        pods_link = soup.findAll('a', class_='_name_80ips_101')
        pods_link_filtered = [f"https://www.nespresso.com{link.get('href')}" for link in pods_link]

        # combine products details together
        all_pods = [list(pods) for pods in zip(pods_name_filtered, pods_img_filtered, pods_link_filtered)]

        # write to csv file
        with open('output.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for pod in all_pods:
              writer.writerow(pod)
        
        print("see output.csv")
   
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

    return 0


if __name__ == "__main__":
  main()