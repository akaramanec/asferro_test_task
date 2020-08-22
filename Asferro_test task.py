# coding=utf-8
"""
Тестовое задание для Караманеца Александра Константиновича
на должность AQA Engineer

Залдание:
1. Залогиниться в почту (любую).
2. Отправить самому себе на эту же почту 15 писем, в которых сообщение -
рандомная строка, содержащая 10 символов (буквы и цифры), тема - рандомная
строка, содержащая 10 символов (буквы и цифры).
3. Проверить что все 15 писем доставлены.
4. Собрать текст сообщений с главной страницы почтового ящика, сохранить их в
дикт, где ключ - тема письма, значение - текст сообщения.
5. Полученную информацию отправить себе же в одном сообщении в таком виде:
"Received mail on theme {тема письма} with message: {текст письма}. It
contains {кол-во букв в письме} letters and {кол-во цифр в письме} numbers".
Важно - значение должно вычисляться исходя из данных в дикте, не браться из
памяти. В таком формате должны быть перечислены все полученные сообщения.
6. Удалить все полученные письма, кроме последнего.

Для запуска необходимы:
Python 2.7       - https://www.python.org/download/releases/2.7/
Selenium server  - https://selenium-python.readthedocs.io/installation.html
Chrome WebDriver - https://chromedriver.chromium.org/downloads
"""
# imports
import time
import local_settings as settings
from selenium.common.exceptions import StaleElementReferenceException
from random_string import get_random_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# variables
repeats = 15  # number of emails to sent
subject = {}
body = {}
mails_data = {}
sends_mails_data = {}
mails_count_before = 0


# functions
def driver_init():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options, executable_path='chromedriver.exe')


def login():
    browser.find_element_by_id('id-input-login').send_keys(settings.EMAIL_USER)
    browser.find_element_by_id('id-input-password').send_keys(settings.EMAIL_PASSWORD)


def close_old_tab(current_handle):
    all_handles = browser.window_handles
    browser.close()
    for handle in all_handles:
        if handle != current_handle:
            browser.switch_to.window(handle)


def mail_generate(mail):
    browser.find_element_by_xpath('//button[@class="default compose"]').click()
    browser.find_element_by_name('toFieldInput').send_keys(settings.EMAIL_USER + '@ukr.net')
    subject[mail] = get_random_string(10)
    browser.find_element_by_name('subject').send_keys(subject[mail])
    body[mail] = get_random_string(10)
    browser.switch_to.frame(browser.find_elements_by_tag_name("iframe")[1])
    browser.find_element_by_id('tinymce').send_keys(body[mail])
    browser.switch_to.default_content()
    browser.find_element_by_xpath('//button[@class="default send"]').click()
    browser.find_element_by_link_text(u'письмо')


def get_separate_subject_and_body_from_link(mails):
    for mail in mails:
        mail_subject, mail_body = mail.text.strip().split('  ')
        mails_data[mail_subject] = mail_body
    return mails_data


def delete_all_mails():
    """ check is mails in mailbox """
    try:
        browser.find_element_by_css_selector('table.noselect').find_elements_by_css_selector('td.msglist__row-subject')
    except StaleElementReferenceException:
        return

    """ delete all mails """
    browser.find_element_by_id('0').click()
    browser.find_element_by_xpath('//*[@class="msglist__checkbox"]//label').click()
    browser.find_element_by_link_text(u'Удалить').click()


def count_numbers_and_latters(mails_body):
    numbers_count = 0
    list_of_body = list(mails_body)
    for symb in list_of_body:
        if symb.isdigit():
            numbers_count += 1
    letters_count = len(mails_body) - numbers_count
    return numbers_count, letters_count


""" script body """
""" start driver """
browser = driver_init()
browser.implicitly_wait(5)

""" enter on mail server"""
browser.get('https://www.ukr.net/')
current_handle = browser.current_window_handle

""" open user email compose on ukr.net """
browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
login()
browser.find_element_by_xpath('//button[@class="form__submit"]').click()
time.sleep(1)
browser.find_element_by_xpath('//a[text()="Вхідні"]').click()
close_old_tab(current_handle)

""" delete all mails from mailbox """
delete_all_mails()

""" save count of mails before test """
try:
    mails_count_before += len(
        browser.find_element_by_css_selector('table.noselect').find_elements_by_css_selector('td.msglist__row-subject'))
except StaleElementReferenceException:
    pass

"""generation of 15 letters with specified conditions (10 characters in the subject line and 10 characters in the 
body) """
for mail in range(1, repeats + 1):
    mail_generate(mail)
subject = {value: key for key, value in subject.items()}
for key, value in subject.items():
    sends_mails_data[key] = body[value]

""" check that all emails are sent """
if len(sends_mails_data) != repeats:
    print("Count of sends mails [%s] not equal to count of mails [%s] need to sent" % (len(sends_mails_data), repeats))
    browser.quit()

""" go to the inbox """
browser.find_element_by_xpath('//button[text()="Вернуться во входящие"]').click()

""" save data of sent mails and check that all sent emails are received """
mails = browser.find_element_by_css_selector('table.noselect').find_elements_by_css_selector('td.msglist__row-subject')
mails_count_after = mails_count_before + repeats
if mails_count_after != len(mails):
    print("Sum of sends mails [%s] and mails that were in the box [%s] not equal to count of mails [%s] in the "
          "inbox!" % (repeats, mails_count_before, len(mails)))
    browser.quit()
else:
    print("Sum of sends mails [%s] and mails that were in the box [%s] is equal to count of mails [%s] in the "
          "inbox!" % (repeats, mails_count_before, len(mails)))
mails_data = get_separate_subject_and_body_from_link(mails)
if not sends_mails_data == mails_data:
    print('Not all of the sent mails are received')
    print(sends_mails_data, mails_data)
    browser.quit()

""" create and sent result mail """
browser.find_element_by_xpath('//button[@class="default compose"]').click()
browser.find_element_by_name('toFieldInput').send_keys(settings.EMAIL_USER + '@ukr.net')
browser.find_element_by_name('subject').send_keys('result mail')

""" generate body of result mail """
result_body = ''
for subj, mails_body in sends_mails_data.items():
    numbers, letters = count_numbers_and_latters(mails_body)
    result_body += "Received mail on theme %s with message: %s. It contains %s " \
                   "letters and %s numbers \n" % (str(subj), str(mails_body), letters, numbers)
browser.switch_to.frame(browser.find_elements_by_tag_name("iframe")[1])
browser.find_element_by_id('tinymce').send_keys(result_body)
browser.switch_to.default_content()
browser.find_element_by_xpath('//button[@class="default send"]').click()
browser.find_element_by_link_text(u'письмо')

""" delete all sent mails except result mail """
browser.find_element_by_id('0').click()
need_to_delete = browser.find_elements_by_css_selector('.checkbox.noselect')
for item in range(1, len(need_to_delete)):
    need_to_delete[item].click()
browser.find_element_by_link_text(u'Удалить').click()

""" close driver """
browser.quit()
