from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from math import floor
from time import sleep
import discord
from secrets import username, password

allow_role_id = 0 # set this to only have a specific role allowed to use the bot

class GeoGuessrBot():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path='./drivers/chromedriver', options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        self.driver.get("https://www.geoguessr.com/")

        login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/div/header/div[2]/div/div[2]/a')))
        login_btn.click()

        email_field = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/form/div/div[1]/div[2]/input')))
        email_field.send_keys(username)

        password_field = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/form/div/div[2]/div[2]/input')
        password_field.send_keys(password)

        enter_btn = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/form/div/section/section[2]/div/div/button')
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
        no_default = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div/label/span[1]')))
        try:
            slider = self.driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[2]')
        except:
            no_default.click()

        slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div/div[2]/article/div[3]/div/div/div[2]/div[2]')))
        amount = floor(options['time']/10)
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
        amount = floor(options['time']/10)
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
        self.driver.get(options['map'])

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

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))

    async def on_message(self, message):
        if(allow_role_id != 0):
            kunku = message.guild.get_role(allow_role_id)
            if(kunku not in message.author.roles):
                await message.channel.send("OOT LIIAN NOBO! " + message.author.mention)
                return

        option = self.parse_options(message.content)

        if(message.content.lower().startswith("!geo")):
            if(option['map'] != ""):
                link = web.get_map(option)
            else:
                link = web.get_link(option)
            await message.channel.send(link)
            return

    def parse_options(self, message):
        a = 0
        amount = message.count("=")
        optlist = message.split()[1:]
        if(len(optlist) > 0):
            if(not "=" in optlist[0]):
                mode = optlist[0]
                a = 1
        mode = "country-streak"
        rules = ""
        time = 0
        gmap = ""
        for i in optlist[a:]:
            if(i.startswith("mode")):
                mode = i[i.find("=")+1:]
            elif(i.startswith("rules")):
                rules = i[i.find("=")+1:]
            elif(i.startswith("time")):
                time = int(i[i.find("=")+1:])
            elif(i.startswith("map")):
                gmap = i[i.find("=")+1:]

        opts = {
            'mode': mode,
            'rules': rules,
            'time': time,
            'map': gmap,
        }
        return opts

web = GeoGuessrBot()
web.login()
client = MyClient()
client.run("YourTokenHere")
