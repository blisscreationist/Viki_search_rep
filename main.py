from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def init_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def get_page_title(browser):
    return browser.find_element(By.ID, "firstHeading").text

def get_page_paragraphs(browser):
    content = browser.find_element(By.ID, "mw-content-text")
    paragraphs = content.find_elements(By.TAG_NAME, "p")
    return [p.text for p in paragraphs if p.text]

def get_page_links(browser):
    content = browser.find_element(By.ID, "mw-content-text")
    links = content.find_elements(By.TAG_NAME, "a")
    return {link.text: link.get_attribute("href") for link in links if link.get_attribute("href") and link.text}

def navigate_page(browser):
    while True:
        print(f"\nВы находитесь на странице: {get_page_title(browser)}")
        print("Выберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")
        choice = input("Ваш выбор: ")

        if choice == '1':
            paragraphs = get_page_paragraphs(browser)
            for i, paragraph in enumerate(paragraphs):
                print(f"Параграф {i + 1}:\n{paragraph}\n")
        elif choice == '2':
            links = get_page_links(browser)
            if not links:
                print("Связанные страницы не найдены.")
                continue
            print("Связанные страницы:")
            for title, url in links.items():
                print(f"- {title}")

            new_query = input("Введите название страницы для перехода: ")
            if new_query in links:
                browser.get(links[new_query])
                time.sleep(2)
            else:
                print("Страница не найдена. Попробуйте другой запрос.")
        elif choice == '3':
            print("Выход из программы.")
            return False
        else:
            print("Неверный выбор. Попробуйте снова.")

def main():
    browser = init_browser()
    try:
        while True:
            query = input("Введите запрос для поиска на Википедии: ")
            search_url = f"https://ru.wikipedia.org/wiki/{query}"
            browser.get(search_url)
            time.sleep(2)

            if "search" in browser.current_url:
                print("Страница не найдена. Попробуйте другой запрос.")
                continue

            if not navigate_page(browser):
                break

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()