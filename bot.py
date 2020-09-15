from selenium import webdriver
from datetime import timedelta, datetime
import time
import re
import random
random.seed()

from authorization import username, password
from link import link 



days = 20
publications = 10
like_time = 10 # время между каждым лайком 
all_likes = 270 #за сутки 
all_subscriptions = 300 #за сутки 
hour_like = 30 #максимальное число лайков за час
hour_sub = 30 #максимальное число подписок за час

#в этом часу уже есть 
likes = 0
subscriptions = 0

#Подписки 
all = 300

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1 
    except NoSuchElementException:
        existence = 0
    return existence


browser = webdriver.Chrome("C:\\Users\\User\\Desktop\\Instagrambot\\chromedriver.exe")

browser.get("https://www.instagram.com/")

#Вход в инстаграм
browser.get("https://www.instagram.com/accounts/login")
time.sleep(3)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div/div[1]/div/label/input").send_keys(
    username) #логин вашего инстаграм аккаунта который вы указали в autorization.py
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div/div[2]/div/label/input").send_keys(
    password) # Пароль вашего инстаграм аккаунта который вы указали в autorization.py
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div/div[3]").click() # Вход
time.sleep(5)
browser.implicitly_wait(5)
#Переход на нужную страницу, бот будет подписываться и ставить лайки подписчикам этой страницы
browser.get(link)# Укажите ссылку страницы в link.py
time.sleep(3)
browser.implicitly_wait(3)
browser.find_element_by_xpath("//section/main/div/header/section/ul/li[2]/a").click()
time.sleep(3)
#открытие списка подписчиков и scroll
element = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 6, element)
time.sleep(1.2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 4, element)
time.sleep(1.2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 3, element)
time.sleep(1.2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 2, element)
time.sleep(1.2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 1.4, element)
time.sleep(1.2)
#Вытаскивает ссылки на подписчиков
pers = []
t = 1
p = 0
num_scroll = 0

while len(pers) < all:
    num_scroll += 1
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)

    if num_scroll % 10 == 0:
        print("!")
       
        persons = browser.find_elements_by_xpath("//div[4]/div/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/span/a")
        for i in range(len(persons)):
            pers.append(str(persons[i].get_attribute('href')))
    time.sleep(t)


    if ( len(pers) > (2000 + 1000*p) ):
        print("\n Ожидание 10 минут")
        time.sleep(60*10)
        p += 1

f = open("personslist.txt", 'w')
for person in pers:
    f.write(person)
    f.write("\n")

f.close()
# Завершение сбора ссылок на подписчиков

# Фильтр собранных адресов 
f = open("personslist.txt", "r")
file_list = []
for line in f:
    file_list.append(line)
f.close()

filtered_list = []
i = 0 
j = 0 

for person in file_list:
    j += 1
    browser.get(person)
    time.sleep(1)

    # Если аккаунт закрытый
    element = "//section/main/div/div/article/div/div/h2"
    if xpath_existence(element) == 1:
        try:
            if browser.find_element_by_xpath(element).text == "This Account is Private" or "Это закрытый аккаунт":
                print(j, "Приватный аккаунт")
                continue
        except StaleElementReferenceException:
            print("Ошибка, код ошибки: 1")

    # Если в шапке аккаунта есть ссылка на сайт

    element = "//section/main/div/header/section/div[2]/a"
    if xpath_existence(element) == 1:
        print(j, "Есть ссылка на сайт")
        continue

    # Если у подписчика слишком мало публикаций(10)
    element = "//div[1]/section/main/div/header/section/ul/li[1]/span/span"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 4")
        continue
    status = browser.find_element_by_xpath(element).text
    status = re.sub(r'\s', '', status)
    if int(status) < publications:
        print(j, "У аккаунта слишком мало публикаций")
        continue

  
    # Добавление пользователей в отфильтрованный файл
    filtered_list.append(person)
    print(j, "Добавлен новый пользователь", person)
    i += 1
    

 
# Добавление в файл
f = open("filtered_persons_list.txt", "w")
for line in filtered_list:
    f.write(line)
f.close()
print("\nДобавлено", i, "пользователей")


#Считывание отфильтрованных пользователей
f = open("filtered_persons_list.txt", "r")
file_list = []
for line in f:
    file_list.append(line)
f.close()

#лист с моими подписчиками 
subscriptions_list = []
f1 = open("my_subscriptions.txt", "r")
for line in f1:
    subscriptions_list.append(line)
f1.close
j = 0 #номер вывода в терминале
n = 0 #пропущенноу число пользователей из за совпадений
next_person = 0 #если true - следующий пользователь по циклу
start_time = time.time()# время начала цикла

# Цикл
for person in file_list:
    #условия паузы цикла
    if likes >= all_likes:
        print("Предел числа лайков за сутки")
        break 
    if subscriptions >= all_subscriptions:
        print("Предел числа подписок за сутки")
        break 
    # максимальное число подписок в час
    if ((time.time() - start_time) <= 60*60) and (hour_sub <= subscriptions):
        print("Предел числа подписок в час")
        print("Подождите", int((60*60 - (time.time() - start_time))/60), "мин.")
        #удаление из отфильтрованных пользователей тех, на которых уже произвелась подписка
        f = open("filtered_list.txt", "w")
        for i in range(j, len(file_list)):
            f.write(file_list[i])
        f.close()

        time.slip(60*60 - (time.time() - start_time))
        start_time = time.time()
        subscriptions = 0
        likes = 0

     # максимальное число лайков в час
    if ((time.time() - start_time) <= 60*60) and (hour_like <= likes):
        print("Предел числа лайка в час")
        print("Подождите", int((60*60 - (time.time() - start_time))/60), "мин.")
        #удаление из отфильтрованных пользователей тех, на которых уже поставили лайк
        f = open("filtered_list.txt", "w")
        for i in range(j, len(file_list)):
            f.write(file_list[i])
        f.close()

        time.slip(60*60 - (time.time() - start_time))
        start_time = time.time()
        subscriptions = 0
        likes = 0


    # обнуление часа 
    if ( (time.time() - start_time) >= 60*60):
        start_time = time.time()
        subscriptions = 0 
        likes = 0

    #сравнение с массивом подписок 
    for line in subscriptions_list:
        next_person = 0
        if person == line:
            next_person = 1
            print(j + 1, "\t Подписка на этого человека уже есть")
            j += 1 
            n += 1 
    if next_person == 1:
        continue

    #вывод в терминал номера 
    j += 1 
    print("\n" + str(j - n) + ": ") 

    #открытие страницы пользователя

    browser.get(person)
    time.sleep(1.5)
    #1) открытие публикаций и лайки
    #   проверка есть ли уже подписка на этого пользователя
    element = "//section/main/div/header/section/div/div/div/div/div/span/span/button"
    if xpath_existence(element) == 1:
        try:
            follow_status = browser.find_element_by_xpath(element).text 
        except StaleElementReferenceException:
            print(j, "Ошибка, код ошибки: 1")
            continue
        if (follow_status == "following") or (follow_status == "Подписки"):
            print("вы уже подписаны на этого человека\n")
            continue
        #поиск публикаций и откртие случайных 
        element = "//a[contains(@href, '/p/')]"
        if xpath_existence(element) == 0:
            print(j, "Ошибка, код ошибки: 2")
            continue
        posts = browser.find_elements_by_xpath(element)
        i = 0
        for post in posts:
            posts[i] = post.get_attribute("href")
            i += 1 
        rand_post = random.randint(0,5) # случайный 1-6 пост
        for i in range(2):
            browser.get(posts[rand_post + i])
            time.sleep(0.5)
            browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()#like
            likes += 1
            print("+1 лайк")
            time.sleep(like_time)
            

            #2)подписка на пользователя 
        try:
            
            element = "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button"
            if xpath_existence(element) == 0:
                print(j, "Ошибка, код ошибки: 2")
            try:
                browser.find_element_by_xpath(element).click()
            except StaleElementReferenceException:
                print(j, "Ошибка, код ошибки 3")
                continue
        except ElementClickInterceptedException:
            print(j, "Ошибка, код ошибки: 4")
            continue

        subscriptions += 1
        print("+1 Подписка", person[0:len(person)-1])
        time.sleep(1)


    #запись новой подписки в файл подписок
    f = open("my_subscriptions.txt", "a")
    f.write(person)
    f.close()
browser.quit()

