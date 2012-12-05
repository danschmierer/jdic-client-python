# -*- coding: utf-8 -*-
import unittest
import jdic

import sys
sys.path.append('../')

class ApiTests(unittest.TestCase):
    def setUp(self):
        self._urllib = MockUrllib()
        self._client = jdic.Client(dict(urllib=self._urllib))
        self._url = 'http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?'
    
    def _add_handler(self, url, callback):
        self._urllib.AddHandler(url, callback)
    
    def _get_word_entry(self):
        #test data. keep whitespace as is
        return u"""<HTML>
<HEAD><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><TITLE>WWWJDIC: Word Display</TITLE>
</HEAD><BODY>
<p>
<pre>

向上 [こうじょう] /(n) improvement/

</pre>
</BODY>
</HTML>"""
    
    def _get_empty_response(self):
        #test data. keep whitespace as is
        return u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><TITLE>WWWJDIC: Kanji Display</TITLE>
</HEAD><BODY>
<br>
<pre>
</pre>
<p>
</BODY>
</HTML>"""
    
    def _get_single_kanji_entry(self):
        #test data. keep whitespace as is
        return u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><TITLE>WWWJDIC: Kanji Display</TITLE>
</HEAD><BODY>
<pre>
付 4955 U4ed8 B9 G4 S5 F322 J2 N363 V124 H31 DK19 L1000 K251 O126 DO259 MN373 MP1.0601 E574 IN192 DS502 DF302 DH602 DT454 DJ365 DB2.15 DG62 DM1009 P1-2-3 I2a3.6 Q2420.0 DR2148 Yfu4 Wbu フ つ.ける -つ.ける -づ.ける つ.け つ.け- -つ.け -づ.け -づけ つ.く -づ.く つ.き -つ.き -つき -づ.き -づき T1 つけ {adhere} {attach} {refer to} {append} 
</pre>
<p>
</BODY>
</HTML>"""
    
    def _get_multiple_kanji_entries(self):
        #test data. keep whitespace as is
        return u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><TITLE>WWWJDIC: Multirad Kanji Display</TITLE>
</HEAD><BODY>
<font size="-3">&nbsp;</font><br>
Target Radicals: 一 (5) <br>
<pre>
一 306C U4e00 B1 G1 S1 XJ05021 F2 J4 N1 V1 H3341 DK2105 L1 K4 O3 DO1 MN1 MP1.0001 E1 IN2 DS1 DF1 DH1 DT1 DC1 DJ1 DB1.A DG1 DM1 P4-1-4 I0a1.1 Q1000.0 DR3072 Yyi1 Wil イチ イツ ひと- ひと.つ T1 かず い いっ いる かつ かづ てん はじめ ひ ひとつ まこと {one} {one radical (no.1)} 
丁 437A U4e01 B1 G3 S2 F1312 J1 N2 V2 H3348 DK2106 L91 K794 O8 DO166 MN2 MP1.0072 E346 IN184 DS473 DF1024 DH367 DT241 DJ550 DG3 DM92 P4-2-1 I0a2.4 Q1020.0 DR3153 Yding1 Yzheng1 Wjeong チョウ テイ チン トウ チ ひのと {street} {ward} {town} {counter for guns, tools, leaves or cakes of something} {even number} {4th calendar sign} 
乃 4735 U4e43 B4 G9 S2 F1978 J1 N145 V42 H2927 DK1858 L686 K1960 O27 DO1962 MN113 MP1.0339 IN2003 DM693 P3-1-1 I0a2.10 Q1722.7 DR3545 ZPP4-2-1 ZSP3-2-1 ZBP4-3-1 Ynai3 Wnae ナイ ダイ ノ アイ の すなわ.ち なんじ T1 おさむ お のり {from} {possessive particle} {whereupon} {accordingly} 
了 4E3B U4e86 B6 G8 S2 F792 J2 N268 V67 H3350 DK2107 L97 K919 O9 DO1018 MN226 MP1.0409 E1905 IN941 DF293 DT1008 DJ818 DG273 DM98 P4-2-1 I2c0.3 Q1720.7 DR3553 ZSP4-1-1 Yliao3 Yle5 Wryo リョウ T1 さとる {complete} {finish} 
下 323C U4e0b B1 G1 S3 XJ13023 F97 J4 N9 V9 H3378 DK2115 L50 K72 O46 DO30 MN14 MP1.0220 E7 IN31 DS21 DF6 DH24 DT13 DC75 DJ32 DB2.1 DG4 DM50 P4-3-1 I2m1.2 Q1023.0 DR3154 Yxia4 Wha カ ゲ した しも もと さ.げる さ.がる くだ.る くだ.り くだ.す -くだ.す くだ.さる お.ろす お.りる T1 さか しと {below} {down} {descend} {give} {low} {inferior} 
</pre>
<p>
</BODY>
</HTML>"""

    def test_get_word_jp(self):
        search_term = 'koujou'
        query_prefix = '4ZUJ'
        url = self._url + query_prefix + search_term
        self._add_handler(url, self._get_word_entry)
        
        entries = self._client.get_word_jp(search_term)
        self.assertEqual(len(entries), 1)
        
        entry = entries[0]
        self.assertEqual(entry['word'], u'向上')
        self.assertEqual(entry['definition'], 'improvement')
    
    def test_get_kanji(self):
        search_term = '付'
        query_prefix = '1ZMJ'
        url = self._url + query_prefix + search_term
        self._add_handler(url, self._get_single_kanji_entry)
        
        entries = self._client.get_kanji(search_term)
        self.assertEqual(len(entries), 1)
        
    def test_get_kanji_empty(self):
        search_term = 'a'
        query_prefix = '1ZMJ'
        url = self._url + query_prefix + search_term
        self._add_handler(url, self._get_empty_response)
        
        entries = self._client.get_kanji(search_term)
        self.assertEqual(len(entries), 0)
       
    def test_get_kanji_by_radical(self):
        search_term = '一'
        query_prefix = '1ZFX'
        url = self._url + query_prefix + search_term
        self._add_handler(url, self._get_multiple_kanji_entries)
        
        entries = self._client.get_kanji_by_radical(search_term)
        self.assertEqual(len(entries), 5)
        
    def test_get_kanji_by_radical_empty(self):
        search_term = '一'
        query_prefix = '1ZFX'
        url = self._url + query_prefix + search_term
        self._add_handler(url, self._get_empty_response)
        
        entries = self._client.get_kanji_by_radical(search_term)
        self.assertEqual(len(entries), 0)

class KanjiRequestHandlerTests(unittest.TestCase):
    def setUp(self):
        self._handler = jdic.KanjiRequestHandler()
    
    def _get_kanji_entries(self):
        #test data. keep whitespace as is
        return u"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
<HEAD><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><TITLE>WWWJDIC: Multirad Kanji Display</TITLE>
</HEAD><BODY>
<font size="-3">&nbsp;</font><br>
Target Radicals: 一 (5) <br>
<pre>
一 306C U4e00 B1 G1 S1 XJ05021 F2 J4 N1 V1 H3341 DK2105 L1 K4 O3 DO1 MN1 MP1.0001 E1 IN2 DS1 DF1 DH1 DT1 DC1 DJ1 DB1.A DG1 DM1 P4-1-4 I0a1.1 Q1000.0 DR3072 Yyi1 Wil イチ イツ ひと- ひと.つ T1 かず い いっ いる かつ かづ てん はじめ ひ ひとつ まこと {one} {one radical (no.1)} 
丁 437A U4e01 B1 G3 S2 F1312 J1 N2 V2 H3348 DK2106 L91 K794 O8 DO166 MN2 MP1.0072 E346 IN184 DS473 DF1024 DH367 DT241 DJ550 DG3 DM92 P4-2-1 I0a2.4 Q1020.0 DR3153 Yding1 Yzheng1 Wjeong チョウ テイ チン トウ チ ひのと {street} {ward} {town} {counter for guns, tools, leaves or cakes of something} {even number} {4th calendar sign} 
乃 4735 U4e43 B4 G9 S2 F1978 J1 N145 V42 H2927 DK1858 L686 K1960 O27 DO1962 MN113 MP1.0339 IN2003 DM693 P3-1-1 I0a2.10 Q1722.7 DR3545 ZPP4-2-1 ZSP3-2-1 ZBP4-3-1 Ynai3 Wnae ナイ ダイ ノ アイ の すなわ.ち なんじ T1 おさむ お のり {from} {possessive particle} {whereupon} {accordingly} 
了 4E3B U4e86 B6 G8 S2 F792 J2 N268 V67 H3350 DK2107 L97 K919 O9 DO1018 MN226 MP1.0409 E1905 IN941 DF293 DT1008 DJ818 DG273 DM98 P4-2-1 I2c0.3 Q1720.7 DR3553 ZSP4-1-1 Yliao3 Yle5 Wryo リョウ T1 さとる {complete} {finish} 
下 323C U4e0b B1 G1 S3 XJ13023 F97 J4 N9 V9 H3378 DK2115 L50 K72 O46 DO30 MN14 MP1.0220 E7 IN31 DS21 DF6 DH24 DT13 DC75 DJ32 DB2.1 DG4 DM50 P4-3-1 I2m1.2 Q1023.0 DR3154 Yxia4 Wha カ ゲ した しも もと さ.げる さ.がる くだ.る くだ.り くだ.す -くだ.す くだ.さる お.ろす お.りる T1 さか しと {below} {down} {descend} {give} {low} {inferior} 
</pre>
<p>
</BODY>
</HTML>"""
    
    def test_parse_response_entries(self):
        entries = self._handler.parse_response(self._get_kanji_entries())
        self.assertEqual(len(entries), 5)
    
    def test_parse_response_meanings(self):
        entries = self._handler.parse_response(self._get_kanji_entries())
        entry = entries[0]
        meanings = entry['meanings']
        
        self.assertEqual(len(meanings), 2)
        self.assertEqual(meanings[0], "one")
        self.assertEqual(meanings[1], "one radical (no.1)")
        
    def test_parse_response_on_yomi_readings(self):
        entries = self._handler.parse_response(self._get_kanji_entries())
        entry = entries[0]
        
        self.assertEqual(len(entry['readings']['on']), 2)
        self.assertEqual(entry['readings']['on'][0], u'イチ')
        self.assertEqual(entry['readings']['on'][1], u'イツ')
        
    def test_parse_response_kun_yomi_readings(self): 
        entries = self._handler.parse_response(self._get_kanji_entries())
        entry = entries[0]
        
        self.assertEqual(len(entry['readings']['kun']), 2)
        self.assertEqual(entry['readings']['kun'][0], u'ひと-')
        self.assertEqual(entry['readings']['kun'][1], u'ひと.つ')

class WordRequestTests(unittest.TestCase):
    def setUp(self):
        self._handler = jdic.WordRequestHandler()

    def _get_word_entry(self):
        #test data. keep whitespace as is
        return u"""<HTML>
<HEAD><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><TITLE>WWWJDIC: Word Display</TITLE>
</HEAD><BODY>
<p>
<pre>

向上 [こうじょう] /(n) improvement/

</pre>
</BODY>
</HTML>"""
    
    def _get_word_entries(self):
        #test data. keep whitespace as is
        return u"""<HTML>
<HEAD><META http-equiv="Content-Type" content="text/html; charset=UTF-8"><TITLE>WWWJDIC: Word Display</TITLE>
</HEAD><BODY>
<p>
<pre>

控除 [こうじょ] /(n) exemption/

工場 [こうじょう] /(n) factory/

向上 [こうじょう] /(n) improvement/

</pre>
</BODY>
</HTML>"""
    
    def test_parse_entry_jp(self):
        entries = self._handler.parse_response(self._get_word_entry())
        
        entry = entries[0]
        self.assertEqual(entry['word'], u'向上')
        self.assertEqual(entry['definition'], 'improvement')

    def test_parse_response(self):
        entries = self._handler.parse_response(self._get_word_entries())
        
        entry = entries[1]
        self.assertEqual(entry['word'], u'工場')
        self.assertEqual(entry['definition'], u'factory')
        
        entry = entries[2]
        self.assertEqual(entry['word'], u'向上')
        self.assertEqual(entry['definition'], u'improvement')


class HttpRequestTests(unittest.TestCase):
    def setUp(self):
        self._request = jdic.HttpRequest()
    
    def test_build_url_word_jp_romaji(self):
        word = u'koujou'
        query_prefix = '4ZUJ'
        query_string = self._request.build_url(dict(search_value=word, search_type=jdic.SearchType.WORD_JP))
        self.assertEqual(query_string, self._request._base_url + query_prefix + word)
        
    def test_build_url_word_jp_katakana(self):
        word = u'バナナ'
        query_prefix = u'4ZUJ'
        query_string = self._request.build_url(dict(search_value=word, search_type=jdic.SearchType.WORD_JP))
        self.assertEqual(query_string, self._request._base_url + query_prefix + word)
        
    def test_build_url_word_jp_mixed(self):
        word = u'食べる'
        query_prefix = u'4ZUJ'
        query_string = self._request.build_url(dict(search_value=word, search_type=jdic.SearchType.WORD_JP))
        self.assertEqual(query_string, self._request._base_url + query_prefix + word)
        
    def test_build_url_word_jp_hiragana(self):
        word = u'こうじょう'
        query_prefix = u'4ZUJ'
        query_string = self._request.build_url(dict(search_value=word, search_type=jdic.SearchType.WORD_JP))
        self.assertEqual(query_string, self._request._base_url + query_prefix + word)
        
    def test_build_url_word_jp_kanji(self):
        word = u'工場'
        query_prefix = u'4ZUJ'
        query_string = self._request.build_url(dict(search_value=word, search_type=jdic.SearchType.WORD_JP))
        self.assertEqual(query_string, self._request._base_url + query_prefix + word)
    
    def test_build_url_word_en(self):
        word = u'factory'
        query_prefix = u'4ZUJ'
        query_string = self._request.build_url(dict(search_value=word, search_type=jdic.SearchType.WORD_JP))
        self.assertEqual(query_string, self._request._base_url + query_prefix + word)
        
    def test_build_url_single_kanji(self):
        word = u'付'
        query_prefix = u'1ZMJ'
        query_string = self._request.build_url(dict(search_value=word, search_type=jdic.SearchType.KANJI_SINGLE))
        self.assertEqual(query_string, self._request._base_url + query_prefix + word)
    
    def test_build_url_kanji_by_radical(self):
        word = u'一'
        query_prefix = u'1ZFX'
        query_string = self._request.build_url(dict(search_value=word, search_type=jdic.SearchType.KANJI_BY_RADICAL))
        self.assertEqual(query_string, self._request._base_url + query_prefix + word)

class MockUrllib(object):
    """
    Mock for urllib, creates a MockOpener
    """
    def __init__(self):
        self._handlers = {}

    def AddHandler(self, url, callback):
        self._handlers[url] = callback

    def HTTPHandler(self, *args, **kwargs):
        return None

    def OpenerDirector(self):
        return self.build_opener()

    def build_opener(self, *handlers):
        return MockOpener(self._handlers)

class MockOpener(object):
    """
    Mock for Opener. Provides a mechanism for registering a test callback function for an individual test url
    """
    def __init__(self, handlers):
        self._handlers = handlers
        self._opened = False

    def open(self, url, data=None):
        if url in self._handlers:
            self._opened = True
            response = MockFileLike(self._handlers[url]())
            return response
        else:
            raise Exception('Unexpected url: %s, checked: %s' % (url, self._handlers))

    def add_handler(self, *args, **kwargs):
        pass

    def close(self):
        self._opened = False
        
class MockFileLike(object):
    """
    Mock for FileLike. Request handler uses read() in jdic api, so we need to mock this in testing.
    """
    def __init__(self, data):
        self.data = data
    
    def read(self):
        return self.data

if __name__ == "__main__":
    unittest.main()
