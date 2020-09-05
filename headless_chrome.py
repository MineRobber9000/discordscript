from selenium import webdriver

def _options_factory():
	"""Produces a selenium.webdriver.ChromeOptions object. Used to force "headless" on invocation. You shouldn't call this function."""
	ret = webdriver.ChromeOptions()
	ret.add_argument("headless")
	return ret

def get_driver(*varargs,args=[]):
	"""Creates headless selenium.webdriver.Chrome object. Supply command-line options in args or varargs."""
	args.extend(varargs)
	args = list(set(args))
	opt = _options_factory()
	for arg in args:
		if arg=="headless": continue # already headless
		opt.add_argument(arg)
	return webdriver.Chrome(chrome_options=opt)

# import other useful things
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions

# BeautifulSoup support
from bs4 import BeautifulSoup

def soupify(driver):
	return BeautifulSoup(driver.page_source,"html.parser")
