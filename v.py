from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg
import time
import random as r
from selenium.common.exceptions import TimeoutException
import asyncio

class Votebot:
    def __init__(self):
        # option to not load images
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images':2}
        chromeOptions.add_experimental_option("prefs", prefs)
        self.signedIn = False
        self.voteNumber = 1
        self.driver = webdriver.Chrome(cfg.info['cdPath'], options=chromeOptions)

    async def sign_in(self, u, uB, p, pB, timeout=10):
        try: 
            user = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, uB)))
            user.click()
            user.send_keys(u)
        except TimeoutException: 
            self.driver.close()
        await self.password(p, pB)
        
    
    async def password(self, p, pB):
        pw = self.driver.find_element_by_xpath(pB)
        pw.click()
        pw.send_keys(p)
        element = self.driver.find_element_by_xpath(cfg.info['signInConfirm'])
        ActionChains(self.driver).move_to_element(element).click().perform()
        self.signedIn = True

    def get_page(self):
        # open the page
        return self.driver.get(cfg.info['webPage'])

    def wait(self, button, timeout=10):
        # wait for elements to load before clicking
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, button)))

    def submit(self, s):
        # submit button
        self.driver.find_element_by_xpath(s).click()


def main():
        v = Votebot()
        v.get_page()
        if not v.signedIn: 
            loop = asyncio.get_event_loop()
            v.wait(cfg.info['signIn']).click()
            userSignIn = loop.create_task(v.sign_in(cfg.info['user'], cfg.info['userInputBox'], cfg.info['pw'], cfg.info['pwInputBox']))
            loop.run_until_complete(userSignIn)
        while True:
            v.wait(cfg.info['defense']).click()
            v.wait(cfg.info['cbButton']).click()
            v.wait(cfg.info['player']).click()
            v.submit(cfg.info['vote'])
            try:
                v.wait(cfg.info['submit']).click()
            except TimeoutException:
                v.submit(cfg.info['refresh'])
                time.sleep(r.uniform(1,3))
                print('Vote {} Submitted!'.format(v.voteNumber))
                v.voteNumber += 1
                continue
            v.wait(cfg.info['refresh']).click()
            print('Vote {} Submitted!'.format(v.voteNumber))
            v.voteNumber += 1
            time.sleep(r.uniform(1,3))

if __name__ == '__main__':
    main()
