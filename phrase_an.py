import os


water_issues = ["수력", "하수", "용수", "하천", "댐", "강우",
                "저수", "호우", "빗물", "상수","조류","녹조",
                "수질", "풍수", "누수", "유수", "강수","정수",
                "취수", "수돗물", "수자원", "배수", "오염", "홍수",
                "가뭄"]

region = ["서울","부산","기장","대구","달성","인천","강화","옹진","광주","대전",
 "울산","울주","세종","수원","성남","안양","안산","용인","광명","평택",
 "과천","오산","시흥","군포","의왕","하남","이천","안성","김포","화성",
 "경기도_광주","여주","부천","양평","고양","의정부","동두천","구리","남양주",
 "파주","양주","포천","연천","가평","춘천","원주","강릉","동해","태백",
 "속초","삼척","홍천","횡성","영월","평창","정선","철원","화천","양구",
 "인제","고성","양양","청주","충주","제천","보은","옥천","영동","진천",
 "괴산","음성","단양","증평","천안","공주","보령","아산","서산","논산",
 "계룡","당진","금산","부여","서천","청양","홍성","예산","태안",'전주',
 '군산','익산','정읍','남원','김제','완주','진안','무주','장수','임실',
 '순창','고창','부안','목포','여수','순천','나주','광양','담양','곡성',
 '구례','고흥','보성','화순','장흥','강진','해남','영암','무안','함평',
 '영광','장성','완도','진도','신안','창원','진주','통영','사천','김해',
 '밀양','거제','양산','의령','함안','창녕','고성','남해','하동','산청',
 '함양','거창','합천','포항','경주','김천','안동','구미','영주','영천',
 '상주','문경','경산','군위','의성','청송','영양','영덕','청도','고령',
 '성주','칠곡','예천','봉화','울진','울릉','제주']
# doc = open(os.path.join("cleaned_가뭄.txt_split","cleaned_가뭄.txt_split5")).read()
# phrase = concordance(u'가뭄',doc, show = True)


def concordance(phrase, text, show=False):
    terms = text.split()
    indexes = [i for i, term in enumerate(terms) if phrase in term]
    list = []
    if show:
        for i in indexes:
            list.extend(terms[max(0, i - 3):i + 3])
    if list == False:
        return None
    else:
        return list



def phrase2(region, water_issues):
    file = open(os.path.join("region", "%s.txt"%region),encoding='utf8').read()
    '''
    file = os.path.join("local_phrase","%s.txt"%region))
    doc = open(file).read()에서 계속 cp949에러 발생, utf-8로 변경해도 에러
    한 줄로 고치니까 에러 발생 x
    '''
    write_file = os.path.join("local_phrase", "%s_phrase.txt" % region)
    write_file = open(write_file, "w",encoding='utf8')
    phrase1 = concordance(u'%s' % water_issues, file, show=True)
    if len(phrase1) == 0:
        pass
    else:
        write_file.write(str(phrase1)) #phrase1을 str로 고치니까 에러가 뜸


os.makedirs("local_phrase")
for i in region:
    for j in water_issues:
        phrase2(i,j)