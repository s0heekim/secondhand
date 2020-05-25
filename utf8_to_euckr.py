from urllib import parse

def utf8_to_euckr(word):
    word_unicode = word.encode('euc-kr')
    word_euckr = parse.quote(word_unicode)
    return word_euckr


# 사용 예
keyword = utf8_to_euckr(keyword)
