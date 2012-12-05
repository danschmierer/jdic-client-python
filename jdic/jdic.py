# -*- coding: utf-8 -*-
import argparse
import re
import urllib2

class SearchType:
    WORD_EN = 'word_en'
    WORD_JP = 'word_jp'
    KANJI_SINGLE = 'single_kanji'
    KANJI_BY_RADICAL = 'kanji_by_radical'

class Client(object):
    """
    Provides methods to access the jdic api
    
    Details: http://www.csse.monash.edu.au/~jwb/wwwjdicinf.html
    """
    
    def __init__(self, options=None):
        self._urllib = options['urllib'] if options and options['urllib'] else urllib2
    
    def get_word_en(self, word):
        """
        Gets the English/Japanese definition for a given word entered in English
        """
        request = HttpRequest(dict(urllib=self._urllib))
        options = dict(search_value=word, search_type=SearchType.WORD_EN)
        entries = request.get(options)
        
        return entries
    
    def get_word_jp(self, word):
        """
        Gets the English/Japanese definition for a given word entered in Japanese
        """
        request = HttpRequest(dict(urllib=self._urllib))
        options = dict(search_value=word, search_type=SearchType.WORD_JP)
        entries = request.get(options)
        
        return entries
    
    def get_kanji(self, kanji):
        """
        Gets the definition and readings for a given kanji character
        """
        request = HttpRequest(dict(urllib=self._urllib))
        options = dict(search_value=kanji, search_type=SearchType.KANJI_SINGLE)
        entries = request.get(options)
        
        return entries
    
    def get_kanji_by_radical(self, radical):
        """
        Gets the definitions and readings for all kanji containing a given kanji radical
        """
        request = HttpRequest(dict(urllib=self._urllib))
        options = dict(search_value=radical, search_type=SearchType.KANJI_BY_RADICAL)
        entries = request.get(options)
        
        return entries

class RequestHandler(object):
    """
    Base class for handling the response for a jdic http request
    """
    def parse_response(self, response):
        start = response.find('<pre>') + 5
        end = response.find('</pre>')
        
        #entry per line
        raw_entries = [line.strip() for line in response[start:end].split('\n') if line.strip()]
        entries = [self._parse_entry(entry) for entry in raw_entries]
        return entries
    
    def _parse_entry(self, entry):
        pass

class WordRequestHandler(RequestHandler):
    """ 
    Class for handling the response for word lookup requests
    """
    def _parse_entry(self, entry):
        entry = entry.strip()
        entry_parts_pattern = """
        ([^\s]*)        #group 1: all chars until the first space
        \s              #a space
        \[([^\]]*)]     #group 2: all chars between [ and ]
        \s              #a space
        /\(([^\)]*)\)   #group 3: all chars between /( and )
        \s              #a space
        ([^/]*)         #group 4: all chars until end / character
        """
        m = re.search(entry_parts_pattern, entry, re.VERBOSE)
        
        word = m.group(1)
        reading = m.group(2)
        
        #wordtype can contain multiple values separated by comma
        wordtype = m.group(3).split(',')
        definition = m.group(4)
        
        return dict(
            word=word,
            reading=reading,
            wordtype=wordtype,
            definition=definition
        )

class KanjiRequestHandler(RequestHandler):
    """
    Class for handling the response for kanji lookup requests (single kanji, kanji by radical)
    """
    def _parse_kanji(self, entry):
        #kanji character itself is at the start of the line.
        kanji_range = u"([\u4E00-\u9FBF]+)"
        kanji_pattern = re.compile(kanji_range, re.UNICODE)
        
        match = kanji_pattern.match(entry).group(1)
        return match
    
    def _parse_meanings(self, entry):
        #kanji meanings are contained inside brackets {}
        meaning = u"{([^}]*)}"
        meaning_pattern = re.compile(meaning, re.UNICODE)
        matches = meaning_pattern.findall(entry)
        return matches
    
    def _parse_on_yomi(self, entry):
        #chinese readings are written in katakana, match using katakana unicode range
        on_yomi = u"([\u30A0-\u30FF]+) "
        on_yomi_pattern = re.compile(on_yomi, re.UNICODE)
        matches = on_yomi_pattern.findall(entry)
        return matches
    
    def _parse_kun_yomi(self, entry):
        #japanese readings are written in hiragana, match using hiragana unicode range
        kun_yomi = u"((?:[\u3040-\u309F\-\.]+ )+)(?=T1)"
        kun_yomi_pattern = re.compile(kun_yomi, re.UNICODE)
        kun_yomi_section = kun_yomi_pattern.findall(entry)
        matches = kun_yomi_section[0].strip().split(' ') if len(kun_yomi_section) > 0 else None
        return matches
    
    def _parse_entry(self, entry):
        kanji = self._parse_kanji(entry)
        meanings = self._parse_meanings(entry)
        on_yomi = self._parse_on_yomi(entry)
        kun_yomi = self._parse_kun_yomi(entry)
        
        return dict(
            kanji=kanji, 
            meanings=meanings, 
            readings=dict(
                on=on_yomi,
                kun=kun_yomi,
                names=[]
            )
        )

class Request(object):
    """
    Base class that represents a request to jdic
    """
    def __init__(self):
        self._debug = 0
    
    def get(self, options):
        pass

class HttpRequest(Request):
    """
    Class that can be used to make http requests to the jdic api
    """
    
    def __init__(self, options=None):
        super(HttpRequest, self).__init__()
        self._urllib = options['urllib'] if options and options['urllib'] else urllib2
        self._base_url = options['base_url'] if options and 'base_url' in options else 'http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?'
    
    #query codes used by wwwjdic for particular dictionary queries
    #Details: http://www.csse.monash.edu.au/~jwb/wwwjdicinf.html#backdoor_tag
    query_codes = {
        SearchType.WORD_EN : '4ZUE',
        SearchType.WORD_JP : '4ZUJ',
        SearchType.KANJI_SINGLE : '1ZMJ',
        SearchType.KANJI_BY_RADICAL : '1ZFX'
    }
    
    #structure of request responses differ depending on the type of request (word lookup/kanji lookup)
    request_handlers = {
        SearchType.WORD_EN:WordRequestHandler,
        SearchType.WORD_JP:WordRequestHandler,
        SearchType.KANJI_SINGLE:KanjiRequestHandler,
        SearchType.KANJI_BY_RADICAL:KanjiRequestHandler
    }
    
    def set_base_url(self, base_url):
        self._base_url = base_url
    
    def set_urllib(self, urllib):
        self._urllib = urllib
    
    def build_url(self, options):
        """
        Returns a url to query jdic, using one of the available jdic query codes
        
        Details: http://www.csse.monash.edu.au/~jwb/wwwjdicinf.html#backdoor_tag
        """
        search_type = options['search_type']
        search_value = options['search_value']
        query_code = self.query_codes[search_type]
        
        return '{0}{1}{2}'.format(self._base_url, query_code, search_value)
    
    def get(self, options):
        search_type = options['search_type']
        request_handler = self.request_handlers[search_type]()
        url = self.build_url(options)
        
        opener = self._urllib.OpenerDirector()
        http_handler = self._urllib.HTTPHandler(debuglevel=self._debug)
        opener.add_handler(http_handler)
        
        #ensure response is utf-8 encoded
        response = opener.open(url).read().decode('utf-8')
        opener.close()
        
        entries = request_handler.parse_response(response)
        return entries

def main():
    """
    simple command line interface for the jdic client
    """
    parser = argparse.ArgumentParser()
    
    parser.add_argument("search_term", help="search jdic for given word or kanji")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-k", "--kanji", help="search for single kanji definition", action="store_true")
    group.add_argument("-r", "--radical", help="search for all kanji containing radical", action="store_true")
    group.add_argument("-j", "--jp", help="search for word using japanese", action="store_true")
    group.add_argument("-e", "--en", help="search for word using english", action="store_true")
    
    args = parser.parse_args()
    
    jdic_client = Client()
    
    if args.kanji:
        result = jdic_client.get_kanji(args.search_term)
    elif args.radical:
        result = jdic_client.get_kanji_by_radical(args.search_term)
    elif args.jp:
        result = jdic_client.get_word_jp(args.search_term)
    elif args.en:
        result = jdic_client.get_word_en(args.search_term)
    
    print result
    
if __name__ == "__main__":
    main()
