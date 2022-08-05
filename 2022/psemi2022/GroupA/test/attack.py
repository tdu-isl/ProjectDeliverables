from selenium import webdriver
import chromedriver_binary

import time


def main():
    try:
        # opt = webdriver.ChromeOptions()
        # opt.add_argument("--headless")
        # driver = webdriver.Chrome(options=opt)
        driver = webdriver.Chrome()
        driver.get("http://localhost:8080/login")

        # driver.find_element_by_id("recaptcha01").click()
        # print(driver.page_source)

        # t = driver.find_element_by_id("empty")
        # for _ in range(10 * 5):
        #     t.click()

        driver.find_element_by_id("email-form").send_keys("\r@selenium")
        driver.find_element_by_id("pw-form").send_keys("selenium")

        driver.execute_script("window.scroll(0, 5000);")
        iframe = driver.find_element_by_css_selector("#rc-test > div:nth-child(3) > div > div > div > iframe")
        driver.switch_to.frame(iframe)
        driver.find_element_by_css_selector("#recaptcha-anchor").click()

        time.sleep(1)
        driver.switch_to.default_content()
        driver.find_element_by_id("rc-submit").click()

    except Exception as e:
        time.sleep(60)
        print(e)
    finally:
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()
