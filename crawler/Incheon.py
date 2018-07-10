from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import re
import os
import selenium

driver = webdriver.Chrome("D:/A/Python/chromedriver.exe")


def key_words_URL(keyword):
    # 페이지접속. 기간정해져있음! 현재3년으로 지정
    driver.get("http://www.incheonilbo.com/?mod=search&act=engine&cust_div_code=&searchContType=article&searchWord=수력"
               "&period=1y&fromDate=2015-06-01&toDate=2018-06-01&section_code%5B%5D=&sfield=&article_type=&searchWord2=수력")
    # 상세검색창
    driver.find_element_by_xpath('//*[@id="search_form"]/div[1]/div[1]/button[2]').click()
    # 제목만
    driver.find_element_by_xpath('//*[@id="syw_detail_layer"]/div[2]/dl[3]/dd/button[2]').click()
    # 검색어입력창
    a = driver.find_element_by_name("searchWord2")
    a.clear()
    # 검색어입력
    a.send_keys(keyword)
    # 검색버튼
    driver.find_element_by_xpath('//*[@id="syw_detail_layer"]/div[2]/p/button[1]/span').click()
    # 처음버튼
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[3]/a[1]').click()
    return driver.current_url


def get_text(URL):  # 기사본문붙이기
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml')
    contents = [str(soup.find('div', id= 'arl_view_content'))]
    # date = soup.find('span', 'arl_view_date').get_text()
    # date = re.sub('[ㄱ-ㅣ가-힣]+', '', date)
    # date = re.sub('\s', '', date)
    # date = [re.split("\s", date)[1]]  # split 하는 대상은 반드시 str
    # contents = date + contents
    return contents


def web_spider(key_words,output_file):
    print("%s crawling" % (key_words))
    article_len = 0
    URL = key_words_URL(key_words)
    # article_URL 기사링크를 계속 붙여넣은 리스트
    article_URL = []
    # 페이지별 총 해당 기사 긁어오기
    for i in range(1, 9999):
        # 페이지 url
        current_page_num = i
        position = URL.index('=')
        URL_with_page_num = URL[: position+1] + str(current_page_num) + URL[position+2 :]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml')
        # 페이지당 있는 기사 url
        for title in soup.find_all('li', 'li summary'):
            title_link = title.select('a')
            article_URL.append(title_link[0]['href'])
        if article_len != len(article_URL):
            article_len = len(article_URL)
        else:
            break
    news_text = open(output_file, 'w', encoding='utf8')  # 저장할 파일 열기
    # 긁어온 총 기사에 다시 들어가서 본문긁어오기
    for i in article_URL:
        news_text.write("%s\n" % get_text(i))  # \n 안붙이면 기사가 모두 하나의 리스트로 나온다.
    return output_file


clean_list = []
def cleaner(txt):
    def clean_text(txt):
        cleaned_text = re.sub('[a-zA-Z]', ' ', txt)  # 영어는 다 지움ㅎ 빈칸 ' ' 반드시 한칸 띄어져있어야함!
        cleaned_text = re.sub('\d{4,30}', ' ', cleaned_text)  # 숫자4자리부터 30자리 삭제
        cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#△▲▽▼▷▶◁◀※○●◎◇◆□■→$%&\\\=\(\'\"]', ' ', cleaned_text)
        cleaned_text = re.sub(' +', " ", cleaned_text)  # 빈칸 두개이상은 하나로.
        return cleaned_text  # type(cleaned_text) = str
    read_file = open(txt, 'r', encoding='utf8')
    write_file = open("cleaned_"+txt, 'w', encoding='utf8')
    text = read_file.read()
    text = clean_text(text)
    write_file.write(text)
    write_file.close()
    read_file.close()
    os.remove(txt)
    clean_list.append("cleaned_"+txt)


def split_news(news):
    os.makedirs(news+"_split")
    text = open(news, "r", encoding='utf8')
    num = 1
    for i in text:
        file_dir=os.path.join(news+"_split","%s_split"%news + str(num))
        write_file = open(file_dir, 'w', encoding='utf8')
        write_file.write(i)
        num += 1


def real_main():
    water_issues = ["수력", "하수", "용수", "하천", "댐", "강우", "저수", "호우", "빗물", "상수",
                    "조류", "녹조", "수질", "풍수", "누수", "유수", "강수", "정수", "취수",
                    "수돗물", "배수", "오염", "홍수", "가뭄"]
    file_list = []
    for file in water_issues:
        file_list.append(file+".txt")
    word_zip = list(zip(water_issues,file_list))
    for word, file in word_zip:
        try:
            web_spider(word, file)
        except selenium.common.exceptions.NoSuchElementException:
            continue
        cleaner(file)

    for word in clean_list:
        try:
            split_news(word)
        except FileExistsError:  # 검색어추가시 기존에 있는거 또 돌릴 필요없으니.
            continue
    print("Complete")


real_main()