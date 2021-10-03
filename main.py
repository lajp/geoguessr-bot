from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from math import floor
from time import sleep
from secrets import username, password
from maps import explore_maps
import discord, sys, json

allow_role_id = 0 # set this to only have a specific role allowed to use the bot
your_id = 0 # set to have the stop command work

default_opts = {
    'mode': "country-streak",
    'rules': "",
    'time': 0,
    'lobby': "",
    'map': "",
    'count': 1,
}

help_message = """
**GEOGUESSR-BOT**: [USAGE]
`!geo`
`!geo [rules=rules] [time=time] [count=count]`
`!geo [mode] [rules=rules] [time=time] [count=count]`
`!geo [mode]`
`!geo [map=map] [rules=rules] [time=time] [count=count]`
`!geo [lobby=lobby] [mode=mode] [rules=rules]`
`!geo [help]`

**MODE:** [cs|country-streak|brc|brd]
**RULES:** rules=[nm|nz|nmz|nmpz] OR rules=[nopower|5050|spy]
**MAP:** map=[link-to-map]
**LOBBY:** lobby=[link-to-lobby]
**TIME:** time=[0-500]
**COUNT:** count=[1-10]"""

class GeoGuessrBot():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path='./drivers/chromedriver', options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.busy = False
        with open('stats.json', 'w+') as json_file:
            try:
                data = json.load(json_file)
                self.count = data['count']
            except:
                self.count = 0

    def login(self):
        self.driver.get("https://www.geoguessr.com/signin")

        email_field = self.wait.until(EC.element_to_be_clickable((By.NAME, 'email')))
        email_field.send_keys(username)

        password_field = self.driver.find_element_by_name('password')
        password_field.send_keys(password)

        enter_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div[2]/main/div/div/form/div/div[3]/div/button')
        enter_btn.click()

        sleep(2)

    def get_link(self, options):
        self.driver.get("https://www.geoguessr.com/" + options['mode'])

        challenge_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[2]/div/div[2]/label/div[1]')))
        challenge_btn.click()

        self.set_options(options)

        invite_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[4]/button')))
        invite_btn.click()

        start_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/button')))
        start_btn.click()

        self.wait.until(lambda driver: self.driver.current_url != "https://www.geoguessr.com/" + options['mode'])

        link = self.driver.current_url
        self.driver.get("https://www.geoguessr.com/")
        return link

    def set_options(self, options):
        no_default = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div/label')))
        try:
            slider = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[2]')
        except:
            no_default.click()

        slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[2]')))
        amount = floor(int(options['time'])/10)
        slider.click()
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(slider, 12+amount*5,0)
        actions.click()
        actions.perform()

        if(options['rules'] == ""):
            no_rules = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[1]')
            no_rules.click()
        elif(options['rules'].lower() == "nm"):
            nm_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[2]')
            nm_btn.click()
        elif(options['rules'].lower() == "nz"):
            nz_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[3]')
            nz_btn.click()
        elif(options['rules'].lower() == "nmz"):
            nmz_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[4]')
            nmz_btn.click()
        elif(options['rules'].lower() == "nmpz"):
            nmpz_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[5]')
            nmpz_btn.click()
        return

    def set_map_options(self, options):
        no_default = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[3]/div/div/div/label/span[2]')))
        try:
            slider = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[2]/div[2]')
        except:
            no_default.click()

        slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[2]')))
        amount = floor(int(options['time'])/10)
        slider.click()
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(slider, 12+amount*5,0)
        actions.click()
        actions.perform()

        if(options['rules'] == ""):
            no_rules = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[1]')
            no_rules.click()
        elif(options['rules'].lower() == "nm"):
            nm_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[2]')
            nm_btn.click()
        elif(options['rules'].lower() == "nz"):
            nz_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[3]')
            nz_btn.click()
        elif(options['rules'].lower() == "nmz"):
            nmz_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[4]')
            nmz_btn.click()
        elif(options['rules'].lower() == "nmpz"):
            nmpz_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[3]/div/div/div[2]/div[3]/div/div[2]/div/label[5]')
            nmpz_btn.click()
        return

    def get_map(self, options):
        if(not options['map'].startswith("https://")):
            options['map'] = "https://www.geoguessr.com/maps/" + options['map']

        self.driver.get(options['map'])

        maplink = options['map']
        maphash = maplink[maplink.rfind("/")+1:]
        if(len(maphash) != 24):
            if(maphash in explore_maps):
                try: # every explore-mode map
                    play_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div[1]/div[4]/button')))
                except: # world and famous-places (maybe more)
                    play_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div[1]/div[3]/button')))
            else:
                try:
                    play_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div[1]/div[3]/button')))
                except:
                    play_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div[1]/div[4]/button')))
        else: # Every map that has a 24-digit hexadecimal id
            play_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div[1]/div[3]/button')))

        play_btn.click()

        challenge_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[2]/div/div[2]/label/div[1]')))
        challenge_btn.click()

        self.set_map_options(options)

        invite_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[4]/button')))
        invite_btn.click()

        start_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/article/div[2]/button')))
        start_btn.click()

        self.wait.until(lambda driver: self.driver.current_url != options['map']+"/play")

        link = self.driver.current_url
        self.driver.get("https://www.geoguessr.com/")
        return link

    def create_battle_royale(self, options):
        self.driver.get("https://www.geoguessr.com/play-with-friends")

        if(options["mode"] == "brd"):
            lobby_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/main/div[1]/div/div/div[2]/div/div[2]/div')))
        else:
            lobby_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/main/div[1]/div/div/div[2]/div/div[1]/div')))

        lobby_btn.click()

        self.wait.until(lambda driver: self.driver.current_url != "https://www.geoguessr.com/play-with-friends")

        link = self.driver.current_url
        self.driver.get("https://www.geoguessr.com/")
        return link

    def start_battle_royale(self, options):
        self.driver.get(options['lobby'])
        if(options['rules'] != ""):
            if options['rules'] == "nopower":
                fiftyfifty_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div/div/div/div[3]/div[2]/div[2]/div/div[1]/div[2]/div[1]/button')))
                fiftyfifty_btn.click()
                spy_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div/div/div/div[3]/div[2]/div[2]/div/div[1]/div[2]/div[2]/button')))
                spy_btn.click()
            elif options['rules'] == "5050":
                spy_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div/div/div/div[3]/div[2]/div[2]/div/div[1]/div[2]/div[2]/button')))
                spy_btn.click()
            elif options['rules'] == "spy":
                fiftyfifty_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div/div/div/div[3]/div[2]/div[2]/div/div[1]/div[2]/div[1]/button')))
                fiftyfifty_btn.click()

        start_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div/div/div/div[3]/div[2]/div[1]/button')))
        start_btn.click()
        self.driver.get("https://www.geoguessr.com/")
        return


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))

    async def on_message(self, message):
        if(message.content.lower().startswith("!fix")):
            web.busy = False
            return
        if(message.content.lower().startswith("!geo")):
            if(not type(message.channel) is discord.DMChannel):
                if(allow_role_id != 0):
                    kunku = message.guild.get_role(allow_role_id)
                    if(kunku not in message.author.roles):
                        return await message.channel.send("OOT LIIAN NOBO! " + message.author.mention)

            option = self.parse_options(message.content)
            if(web.busy):
                return await message.channel.send("Bot is busy! Please try again in a second...")
            if(int(option['count']) == 0):
                option['count'] = 1
            elif(int(option['count']) > 10):
                return await message.channel.send("https://media1.tenor.com/images/dc29e366458426e5c12ed5b481f713b2/tenor.gif?itemid=16851937")
            web.busy = True
            await message.channel.trigger_typing()
            i = 0
            while(i < int(option['count'])):
                if(option['map'] != ""):
                    link = web.get_map(option)
                elif(option['mode'] == "help"):
                    await self.send_help(message)
                    web.busy = False
                    return
                elif(option['lobby'] != ""):
                    web.start_battle_royale(option)
                    web.busy = False
                    return
                elif(option['mode'].startswith("br")):
                    link = web.create_battle_royale(option)
                else:
                    link = web.get_link(option)
                await message.channel.send(link)
                web.count+=1
                i+=1
            web.busy = False
            self.print_log(message)
            # Update the status message
            return await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=str(str(web.count) + " succesfully sent challenges!")))

        elif(message.content.lower().startswith("!stop")):
            if(message.author.id == your_id):
                return await self.stop_and_save()

    async def send_help(self, message):
        return await message.channel.send(help_message)

    async def stop_and_save(self):
        data = {}
        data['count'] = web.count
        with open('stats.json', 'w') as outfile:
            json.dump(data, outfile)
        web.driver.quit()
        await self.close()
        sys.exit()

    def parse_options(self, message):
        a = 0
        opts = default_opts.copy()
        optlist = message.split()[1:]
        if(len(optlist) > 0):
            if(not "=" in optlist[0]):
                opts['mode'] = optlist[0]
                a = 1
        for i in optlist[a:]:
            opts[i[:i.find("=")]] = i[i.find("=")+1:]
        return opts

    def print_log(self, message):
        print("`{0}` recieved by: {1}".format(message.content, message.author))

web = GeoGuessrBot()
print("Geoguessr initialized")
web.login()
print("Geoguessr login")
client = MyClient()
client.run("YourTokenHere")
