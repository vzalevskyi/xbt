import os
import unittest
import sys
import new
from selenium import webdriver
from sauceclient import SauceClient

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

browsers = [{
    "platform": "Windows 7",
    "browserName": "internet explorer",
    "version": "11"
} ]

def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator

def log_to_file(data):
    if os.environ.has_key("LOG_OUTPUT"):
        with open("result_log.txt", "a") as f:
            f.write(data + "\n")

class TestFW(unittest.TestCase):

    # setUp runs before each test case
    def setUp(self):
        self.desired_capabilities['name'] = self.id()
        self.driver = webdriver.Remote(
           command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (username, access_key),
           desired_capabilities=self.desired_capabilities)
           
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.implicitly_wait(30)
        
    def waitNclick(self, x_path):
            self.wait.until(EC.visibility_of_element_located((By.XPATH, x_path)))
            self.driver.find_element_by_xpath(x_path).click()

    def waitNinput(self, x_path, txt):
            self.wait.until(EC.visibility_of_element_located((By.XPATH, x_path)))
            self.driver.find_element_by_xpath(x_path).send_keys(txt)
            
    def test_sauce(self):

        print "Starting test in ", self.driver.capabilities["browserName"], " ", self.driver.capabilities["version"]," on ", self.driver.capabilities["platform"]

        #going to the page
        self.driver.get(data.user_data["url"])

        #swithcing to the login frame and loging in
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["loginFrame"])))
        self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[@name='login']"))
        # self.driver.switch_to.frame(data.frames["loginFrame"])
        self.waitNinput(data.xpth["username"], data.user_data["username"])
        self.waitNinput(data.xpth["password"], data.user_data["password"])
        self.waitNclick(data.xpth["submit"])
        self.driver.switch_to.default_content()

        #opening the WF
        #time.sleep(2)
        self.waitNclick(data.xpth["wfLink"])

                   #app frame check
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["appFrame"])))
        self.driver.switch_to.frame(data.frames["appFrame"])

        #Inbox frame check
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["mailBoxFrame"])))
        self.driver.switch_to.frame(data.frames["mailBoxFrame"])
        arrows = self.driver.find_elements_by_xpath(data.xpth["nextStepsArrow"])
        print "There are ", len(arrows), " documents in the INBOX folder"

        # Sent folder
        self.driver.switch_to.default_content()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["appFrame"])))
        self.driver.switch_to.frame(data.frames["appFrame"])
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["navigationFrame"])))
        self.driver.switch_to.frame(data.frames["navigationFrame"])
        self.waitNclick(data.xpth["sentFolder"])
        #time.sleep(2)

        self.driver.switch_to.default_content()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["appFrame"])))
        self.driver.switch_to.frame(data.frames["appFrame"])
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["mailBoxFrame"])))
        self.driver.switch_to.frame(data.frames["mailBoxFrame"])
        arrows = self.driver.find_elements_by_xpath(data.xpth["nextStepsArrow"])
        print "There are ", len(arrows), " documents in the SENT folder"
        self.driver.switch_to.default_content()

        #Drafts folder
        self.driver.switch_to.default_content()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["appFrame"])))
        self.driver.switch_to.frame(data.frames["appFrame"])
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["navigationFrame"])))
        self.driver.switch_to.frame(data.frames["navigationFrame"])
        self.waitNclick(data.xpth["draftsFolder"])
        time.sleep(2)

        self.driver.switch_to.default_content()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["appFrame"])))
        self.driver.switch_to.frame(data.frames["appFrame"])
        self.wait.until(EC.visibility_of_element_located((By.XPATH, data.xpth["mailBoxFrame"])))
        self.driver.switch_to.frame(data.frames["mailBoxFrame"])
        arrows = self.driver.find_elements_by_xpath(data.xpth["nextStepsArrow"])
        print "There are ", len(arrows), " documents in the DRAFTS folder"
        self.driver.switch_to.default_content()


    def tearDown(self):
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
