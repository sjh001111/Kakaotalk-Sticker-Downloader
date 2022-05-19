def webp2gif(eid, idx):
    import os
    from time import sleep
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()})
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

    if os.path.isfile("ezgif.com-gif-maker.gif"):
        os.remove("ezgif.com-gif-maker.gif")
    
    driver.get("https://ezgif.com/maker")
    driver.find_element_by_css_selector("input[type='file']").send_keys(os.path.join(os.getcwd(),"test.webp"))
    driver.find_element_by_css_selector("input[type='submit']").click()
    driver.find_element_by_name("nostack").click()
    driver.find_element_by_name("make-a-gif").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'output')))
    sleep(1)
    driver.find_elements_by_class_name("save")[1].click()
    while not os.path.isfile("ezgif.com-gif-maker.gif"):
        sleep(1)
    os.rename("ezgif.com-gif-maker.gif", os.path.join(str(eid), str(idx) + ".gif"))

webp2gif(123, 1)
