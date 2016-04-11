import environment
import os
import unittest
import sys
import new
from selenium import webdriver
from sauceclient import SauceClient
from selenium.webdriver.support.ui import WebDriverWait

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

browsers = os.environ['SAUCE_ONDEMAND_BROWSERS']
# environment.browsers
# browsers = [{
#     "platform": "Windows 7",
#     "browserName": "internet explorer",
#     "version": "11"
# } ]


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

@on_platforms(browsers)
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

        self.driver.get("https://google.com")


    def tearDown(self):
        self.driver.quit()
        session_id = self.driver.session_id
        job_name = self.id()
        sauce_client = SauceClient(username, access_key)
        status = (sys.exc_info() == (None, None, None))
        sauce_client.jobs.update_job(session_id, passed=status)
        output = "SauceOnDemandSessionID=%s job-name=%s" % (session_id, job_name)
        log_to_file(output)

if __name__ == "__main__":
    unittest.main()
