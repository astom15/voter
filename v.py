from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import config as cfg
import time
import random as r
from selenium.common.exceptions import TimeoutException

class Votebot:
    def __init__(self):
        # option to not load images
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images':2}
        chromeOptions.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(cfg.info['cdPath'], options=chromeOptions)

    def get_page(self):
        # open the page
        return self.driver.get(cfg.info['webPage'])

    def wait(self, button, timeout=10):
        # wait for elements to load before clicking
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH, button)))

    # def vote(self, player, v):
    #     # we need to hover over the player button for the vote to become clickable
    #     button = self.driver.find_element_by_xpath(v)
    #     hover = ActionChains(self.driver). \
    #     move_to_element(player).move_to_element(button)
    #     hover.click().perform()

    def submit(self, s):
        # submit button
        self.driver.find_element_by_xpath(s).click()

    def vote_again(self, link_text):
        self.driver.find_element_by_link_text(link_text).click()


def main():
        v = Votebot()
        v.get_page()
        while True:
            v.wait(cfg.info['wrButton']).click()
            v.wait(cfg.info['player']).click()
            # v.vote(player, cfg.info['vote'])
            v.submit(cfg.info['submit'])
            try:
                v.wait(cfg.info['pop_up']).click()
            except TimeoutException:
                v.vote_again(cfg.info['refresh'])
                time.sleep(r.uniform(1,3))
                print('Vote Submitted!')
                continue
            v.vote_again(cfg.info['refresh'])
            print('Vote Submitted!')
            time.sleep(r.uniform(1,3))

if __name__ == '__main__':
    main()
