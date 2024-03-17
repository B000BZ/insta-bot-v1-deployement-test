from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
from pandas_parsing import *
import pyperclip

# Selenium Wire configuration to use a proxy
proxy_username = 'aarrahmaniea'
proxy_password = '96ZDdBBc2R'
seleniumwire_options = {
    'proxy': {
        'https': f'https://{proxy_username}:{proxy_password}@166.1.15.0:49155',
        'verify_ssl': False,
    },
}


class ScrapData:

    def __init__(self):
        self.username = ""
        self.postLink = ""
        self.postDate = time.time()
        self.likesCount = 0
        self.commentsCount = 0
        self.tags = []
        self.descriptionText = ""

    def __str__(self):
        return f"username: {self.username}, postLink: {self.postLink}, postDate: {self.postDate}, likesCount: {self.likesCount}, commentsCount: {self.commentsCount}, descriptionText: {self.descriptionText}, tags: {self.tags}"


class InstaBot:
    def __init__(self):
        self.posts = []
        self.dates = []
        self.likes = []
        self.comments = []
        self.list_of_people = []
        self.username = ""
        self.password = ""
        self.message = ""
        self.browser = webdriver.Chrome(
            seleniumwire_options=seleniumwire_options
        )

    def login(self):
        browser = self.browser
        browser.get('https://instagram.com/')

        try:
            username_input = WebDriverWait(browser, 1000).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input"))
            )
            username_input.send_keys(self.username)

            password_input = WebDriverWait(browser, 1000).until(
                EC.visibility_of_element_located((By.XPATH,
                                                  "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input"))
            )
            password_input.send_keys(self.password)

            password_input.submit()
        except TimeoutException:
            print("Login timed out")
            # Handle the timeout appropriately

    def dm(self, people_array=None, hashtag="albania"):
        if people_array is None:
            self.user_scraper(hashtag)
        else:
            self.list_of_people = people_array

        self.browser.get("https://www.instagram.com/direct/inbox/")
        time.sleep(3)
        search_input_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div/div[2]/input"
        add_user_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[3]/div/label/div/input"

        for name in self.list_of_people:
            msgclick = self.browser.find_element(By.XPATH,
                                                 "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div")
            msgclick.click()
            time.sleep(6)
            search = self.browser.find_element(By.XPATH, search_input_xpath)
            search.send_keys(name)
            # we need to wait
            try:
                time.sleep(2)
                add = self.browser.find_element(By.XPATH, add_user_xpath)
                add.click()
            except NoSuchElementException:
                time.sleep(4)
                add = self.browser.find_element(By.XPATH, add_user_xpath)
                add.click()

            time.sleep(3)
            chat = self.browser.find_element(By.XPATH,
                                             "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[4]/div")
            chat.click()
            time.sleep(3)
            text = self.browser.find_element(By.XPATH,
                                             "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/p")
            text.send_keys(self.message)
            text.send_keys("\ue007")
            time.sleep(5)

    def scrape_posts_by_hashtag(self, hashtag):

        self.browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(10)
        most_recent = self.browser.find_element(By.XPATH,
                                                "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div")

        anchors = most_recent.find_elements(By.TAG_NAME, 'a')
        posts = []
        for anchor in anchors:
            posts.append(anchor.get_attribute('href'))
        likesCount = most_recent.find_elements(By.XPATH,
                                               "/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a/span/span")
        commentsCount = most_recent.find_elements(By.XPATH, "")
        date = most_recent.find_elements(By.XPATH,
                                         "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[2]/div/a/span/time")

        for anchor in anchors:
            self.posts.append(anchor.get_attribute("href"))
            self.dates.append(date.get_attribute("datetime"))
            self.likes.append(likesCount)
            self.comments.append(commentsCount)
            print(posts)

            return self

    def user_scraper(self, hashtag):
        posts = self.scrape_posts_by_hashtag(hashtag).posts
        dates = self.dates
        likes = self.likes
        comments = self.comments
        links = []
        i = 0
        for post in posts:
            # if statement to filter user scraping !!!!
            self.browser.get(post)
            i += 1
            wait = WebDriverWait(self.browser, 1000)

            users_table = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]")))
            users = users_table.find_elements(By.TAG_NAME, 'a')
            for user in users:
                href = user.get_attribute("href")
                print(href)
                new_var = href.split("/")[-2].replace(".", " ")
                if new_var.isnumeric():
                    continue
                links.append(new_var)
                print(new_var)
            if i == 1:
                break
        time.sleep(5)
        self.list_of_people = list(set(links))

    def notification_handler(self):
        notnow = WebDriverWait(self.browser, 1000).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div["
                                           "2]/section/main/div/div/div/div/div")))
        notnow.click()
        wait = WebDriverWait(self.browser, 1000)
        notif = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")))
        notif.click()

    def comment(self, post_array=None, hashtag="albania"):
        number_of_comments = 0
        if post_array is None:
            post_array = self.scrape_posts_by_hashtag(hashtag)
        for post in post_array:
            number_of_comments += 1
            self.browser.get(post)
            time.sleep(3)
            try:
                comment_input = self.browser.find_element(By.XPATH,
                                                          "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div")
                comment_input.click()
                comment_textArea = self.browser.find_element(By.XPATH,
                                                             "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[4]/section/div/form/div/textarea")
                pyperclip.copy(self.message)
                act = ActionChains(self.browser)
                act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
                comment_textArea.send_keys("\ue007")
                time.sleep(5)
                print(number_of_comments)
            except NoSuchElementException:
                continue
        return number_of_comments

    def input_credentials(self):
        self.username = input("Enter your insta username: ")
        self.password = input("Enter your insta password: ")
        self.message = input("Enter your message or comment: ")
        self.login()
        self.notification_handler()
        return self

    def set_credentials(self, username, password, message):
        self.username = username
        self.password = password
        self.message = message
        self.login()
        self.notification_handler()
        return self

    def scraper_2(self, hashtag, prefLikeCount, prefCommentCount, datetime):
        sd1 = []
        self.browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(10)
        most_recent = self.browser.find_element(By.XPATH,
                                                "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div")
        posts = []
        anchors = most_recent.find_elements(By.TAG_NAME, 'a')
        for anchor in anchors:
            posts.append(anchor.get_attribute("href"))
        # if logged in then posts = self.scrape_posts_by_hashtag(hashtag).posts
        for post in posts:
            sc1 = ScrapData()
            self.browser.get(post)  # kanye test
            try:
                time.sleep(20)

                sc1.postDate = self.browser.find_element(By.TAG_NAME, 'time').get_attribute('datetime')  # Get post date
                print("postdate = ", sc1.postDate)
                likes_element = self.browser.find_element(By.XPATH,
                                                          "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/section/div/div/span/a/span/span")
                sc1.likesCount = int(likes_element.text.replace(",", ""))
                print("likescount = ", sc1.likesCount)
                commentSection = self.browser.find_element(By.XPATH,
                                                          "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[2]")
                users = commentSection.find_elements(By.TAG_NAME, "a")
                comments = []
                for user in users:
                    href = user.get_attribute("href")
                    new_var = href.split("/")[-2].replace(".", " ")
                    if new_var.isnumeric():
                        continue
                    comments.append(new_var)

                sc1.commentsCount = len(set(comments))
                print("commentsCounts= ", sc1.commentsCount)
                description_box = self.browser.find_element(By.XPATH,
                                                            "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/span")
                sc1.descriptionText = description_box.text
                anchor_tags = description_box.find_elements(By.TAG_NAME, "a")
                tags = []
                for anchor in anchor_tags:
                    tags.append(anchor.text)
                sc1.tags = tags
                print(sc1.tags)
                sc1.username = self.browser.find_element(By.XPATH,
                                                         "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/span/div/div/span[1]/div/a/div/div/span").text
                print(sc1.username)

            except NoSuchElementException:
                print("No such element found")
                continue

            if sc1.postDate != datetime and sc1.likesCount >= prefLikeCount and sc1.commentsCount >= prefCommentCount and (
                    "keywords" in sc1.descriptionText) and sc1.descriptionText != "":
                sd1.append(sc1)
                print(sc1)

        print(len(sd1))


test_bot = InstaBot()
test_bot.set_credentials("salma_lab0", "Lobabies2023", "")
test_bot.scraper_2("albania", 99, 20, 0)
# number of posts left 2044 /C391RBcxr7C/
