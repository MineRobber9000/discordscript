#36393F
import json, argparse, io, re, time, random
import headless_chrome as hc
from PIL import Image

#BLANK_URL = "https://nkxanp.us.to/fakecord?message=eyJtZXNzYWdlIjp7ImhpZGVfYm90Ijp0cnVlfX0"
BLANK_URL = "https://nkxanp.us.to/fakecord?message=eyJtZXNzYWdlIjp7ImNvbnRlbnQiOiJ0aGlzIGlzIGEgdGVzdCBtZXNzYWdlIiwidXNlcm5hbWUiOiJCZXlvbmRJbmZpbml0eSIsImF2YXRhcl91cmwiOiJodHRwczovL2todXhrbS50aWxkZS50ZWFtL2Rpc2NvcmRfc2NyZWVuc2hvdHMvaW5maW5pdGUucG5nIiwiaGlkZV9ib3QiOnRydWV9fQ"

MESSAGE_XPATH = "//main/div[1]/div[1]"
BG_COLOR = (0x36,0x39,0x3F,0xFF)

MESSAGE_INPUT_XPATH = "//div/div[2]/textarea"
ID_REGEX = re.compile(r"message\-(\-?\d+)\-content")
NAME_INPUT_FS = "message-{id}-username"
AVA_INPUT_FS = "message-{id}-avatar"
ID = None

parser = argparse.ArgumentParser(description="Reads DiscordScript files")
parser.add_argument("script",type=argparse.FileType("r"),help="The JSON to read")
args = parser.parse_args()

script = json.load(args.script)
messages = script["messages"]
chars = script["characters"]

driver = hc.get_driver("window-size=1300x731","hide-scrollbars")
driver.get(BLANK_URL)

out = Image.new("RGBA",(1,18),BG_COLOR)

def add_image(rawpng):
	global out
	raw = Image.open(io.BytesIO(rawpng))
	padded = Image.new("RGBA",(raw.size[0],raw.size[1]+18),BG_COLOR)
	padded.paste(raw,(0,0))
	width_old, height_old = out.size
	width_new, height_new = padded.size
	width = max(width_old,width_new)
	height = (height_old+height_new)
	res = Image.new("RGBA",(width,height),BG_COLOR)
	res.paste(out,(0,0))
	res.paste(padded,(0,height_old))
	out = res

def set_inputs(content,name,avatar):
	global ID
	message_el = driver.find_element_by_xpath(MESSAGE_INPUT_XPATH)
	if ID is None:
		m = ID_REGEX.match(message_el.get_attribute("id"))
		if not m:
			print("Something has gone wrong, please try again.")
			raise SystemExit(-1)
		ID = m.group(1)
	name_el = driver.find_element_by_id(NAME_INPUT_FS.format(id=ID))
	ava_el = driver.find_element_by_id(AVA_INPUT_FS.format(id=ID))
	message_el.clear()
	message_el.send_keys(content)
	name_el.clear()
	name_el.send_keys(name)
	ava_el.clear()
	ava_el.send_keys(avatar)
	time.sleep(1) # ensure everything's loaded
	return

# setup
date = ""
if "time" in script:
	date=script["time"]
else:
	month=random.randint(1,12)
	day=random.randint(1,(31 if month in (1,3,5,7,8,10,12) else (28 if month==2 else 30)))
	date="{:02d}/{:02d}/22XX".format(month,day)
driver.execute_script("for(var n=window.setInterval(function(){},0);n--;)window.clearInterval(n)")
# now that we're pretty sure the intervals are dead, let's do some magic
driver.execute_script("""var style = document.createElement("style");
style.innerHTML = ".cvXgKb:before { content:none!important; }";
document.body.appendChild(style);
document.getElementsByClassName("cvXgKb")[0].innerText=arguments[0];""",date)

for message in messages:
	try:
		name, avatar = chars[message["speaker"]]
	except KeyError:
		print("Undefined speaker {}".format(message["speaker"]))
		raise SystemExit(-1)
	set_inputs(message["message"],name,avatar)
	add_image(driver.find_element_by_xpath(MESSAGE_XPATH).screenshot_as_png)

out.save("out.png")
