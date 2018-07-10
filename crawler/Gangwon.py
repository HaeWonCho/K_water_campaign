'''
강원 도민 일보 웹 크롤링
주석은 코드 위에 표시
'''
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import re
import os
import selenium

driver = webdriver.Chrome("C:/Users/hw340/Anaconda2/Lib/site-packages/spyder/widgets/driver/chromedriver.exe")
#크롬 웹 드라이버("크롬 드라이버 경로")

def keywords_get_URL(keyword):
    '''
    상세검색 페이지에서 검색할 키워드, 검색 시작 날짜, 검색 종료 날짜를 입력 한 후 크롤링 시작페이지를 return
    :param keyword: 검색할 키워드
    :param from_dat: 검색 시작 날짜
    :param to_dat: 검색 종료 날짜
    :return: 키워드 입력 웹크롤링 시작 페이지 URL
    '''
    #  검색 시작 페이지 - 기존에 키워드를 임의로 입력 후 상세검색 버튼이 존재하는 페이지로 이동
    driver.get("http://www.kado.net/?mod=search&act=engine&cust_div_code=&searchContType=article&searchWord=%ED%99%8D%EC%88%98&fromDate=&toDate=&sfield=&article_type=&sort=date")
    # 상세검색버튼 클릭 (driver.find_elements와 element 조심)
    driver.find_element_by_xpath('//*[@id="search_form"]/div[1]/div[1]/button[2]').click()
    # 제목만 버튼 클릭 - 글 내용 포함 시 키워드와 상관없는 기사가 나옴
    driver.find_element_by_xpath('//*[@id="syw_detail_layer"]/div[2]/dl[3]/dd/button[2]').click()
    # 시작 날짜 입력
    from_date = driver.find_element_by_name('fromDate')
    from_date.send_keys('0020150601')
    # 종료 날짜 입력
    to_date = driver.find_element_by_name('toDate')
    to_date.send_keys('0020180601')

    # 검색어 입력창 element 찾기
    a = driver.find_element_by_id("syw_search_word2")
    # 입력창 clear
    a.clear()
    # 검색어입력
    a.send_keys(keyword)

    driver.find_element_by_xpath('//*[@id="syw_detail_layer"]/div[2]/p/button[1]/span').click()
    try:
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/div[3]/a').click()
    except selenium.common.exceptions.NoSuchElementException:
        pass
    try:
        driver.find_element_by_xpath('// *[ @ id = "content"] / div[2] / div[2] / div[3] / a[1]').click()
    except selenium.common.exceptions.NoSuchElementException:
        pass
    return driver.current_url  # 키워드 입력 웹크롤링 시작 페이지 URL


def get_news_text(URL):
    '''
    :param URL:
    :return:
    '''
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url,'lxml')
    contents = [str(soup.find('div', 'arl_view_content'))]
    # date = str(soup.find('div', 'View_Time'))
    # date = [re.split("\s", date)[2]]
    # try:
    #     date = soup.find('div', 'View_Time').get_text()
    #     date = [re.split("\s", date)[1]]
    # except AttributeError:
    #     date = []
    # contents = date + contents
    return contents


def web_spider(key_words,output_file):
    print("%s crawling" % (key_words))
    article_len = 0
    URL = keywords_get_URL(key_words) #키워드 입력 웹크롤링 시작 페이지 URL
    # article_URL 기사 URL 리스트
    article_URL = []
    #모든 페이지 URL 크롤링
    for i in range(1,9999):
        #URL에 page가 있는 경우의 페이지 URL 저장
        current_page_num = i
        position = URL.index('=')
        URL_with_page_num = URL[: position+1] + str(current_page_num) + URL[position+2 :]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml')
        #페이지당 있는 기사 url
        for title in soup.find_all("li","li ellipsis title"):
            title_link = title.select('a')
            article_URL.append(title_link[0]['href'])
        if article_len != len(article_URL):
            article_len = len(article_URL)
        else:
            break
    # 저장할 파일 열기
    news_text = open(output_file, 'w',encoding='utf8')
    #긁어온 총 기사에 다시 들어가서 본문긁어오기
    for i in article_URL:
        news_text.write("%s\n" % get_news_text(i))  #\n 안붙이면 기사가 모두 하나의 리스트로 나온다.
    return output_file


clean_list = []
def cleaner(txt):
    def clean_text(txt):
        cleaned_text = re.sub('[a-zA-Z]', ' ', txt)  # 영어는 다 지움ㅎ 빈칸 ' ' 반드시 한칸 띄어져있어야함!
        cleaned_text = re.sub('\d{4,30}', ' ', cleaned_text)  # 숫자4자리부터 30자리 삭제
        cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#△▲▽▼▷▶◁◀※○●◎◇◆□■→$%&\\\=\(\'\"]', ' ', cleaned_text)
        cleaned_text = re.sub(' +', " ", cleaned_text)  # 빈칸 두개이상은 하나로.
        return cleaned_text  # type(cleaned_text) = str
    read_file = open(txt, 'r',encoding='utf8')
    write_file = open("cleaned_"+txt, 'w',encoding='utf8')
    text = read_file.read()
    text = clean_text(text)
    write_file.write(text)
    write_file.close()
    read_file.close()
    os.remove(txt)
    clean_list.append("cleaned_"+txt)


def split_news(news):
    os.makedirs(news+"_split")
    text = open(news,"r",encoding='utf8')
    num = 1
    for i in text:
        file_dir=os.path.join(news+"_split","%s_split"%news + str(num))
        write_file = open(file_dir , 'w',encoding='utf8')
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
        # try:
        web_spider(word,file)
        # except selenium.common.exceptions.NoSuchElementException:
        #     continue
        cleaner(file)

    for word in clean_list:
        try:
            split_news(word)
        except FileExistsError:
            continue
    print("Complete")


real_main()