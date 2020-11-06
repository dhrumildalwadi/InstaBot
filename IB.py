from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import random
import getpass

class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def closeBrowser(self):
        self.driver.close()

    def login(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("/html/body/span/section/main/article/div[2]/div[2]/p/a")
        login_button.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(5)
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")


    def action(self, comment, number):
        driver = self.driver
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        counter = 0
        for i in range(1, 2):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                for href in hrefs_in_view:
                    if( href not in pic_hrefs):
                        if (counter == number):
                            break
                        pic_hrefs.append(href)
                        counter +=1

            except Exception:
                continue

        # Liking photos
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)


            #follow request

            try:
                time.sleep(3)
                follow_button = lambda: driver.find_element_by_class_name('oW_lN.sqdOP.yWX7d.y3zKF')
                follow_button().click()
                time.sleep(2)
            except Exception as e:
                time.sleep(2)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2, 4))
                like_button = lambda: driver.find_element_by_class_name('glyphsSpriteHeart__outline__24__grey_9.u-__7').click()
                like_button().click()
                time.sleep(2)
            except Exception as e:
                time.sleep(2)

           #Comment

            self.write_comment(random.choice(comment))


    def write_comment(self, comment_text):
        try:
            comment_button = lambda: self.driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[2]/section[1]/span[2]/button/span")
            comment_button().click()
        except NoSuchElementException:
            pass

        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath("/html/body/span/section/main/div/div/article/div[2]/section[3]/div/form/textarea")
            comment_box_elem().send_keys('')
            comment_box_elem().clear()
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1, 7) / 30))
            comment_box_elem().send_keys(Keys.RETURN)
            time.sleep(3)

            return comment_box_elem

        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False

if __name__ == "__main__":

    flag = ""
    username = input("Username: ")
    password = getpass.getpass(prompt='Password: ')
    tag = input("Hashtag: ")
    comment = []
    number_of_comments = input("Number of comments which will be posted randomly: ")
    for x in range(0 , int(number_of_comments)):
        print(str(x+1) + "st Comment: ")
        text = input()
        comment.append(text)
    number = input("No. of posts: ")

    ig = InstagramBot(username, password)
    ig.login(tag)

    try:
        ig.action(comment, int(number))
        time.sleep(2)
        ig.closeBrowser()
    except Exception as e:
        print(e)
        ig.closeBrowser()