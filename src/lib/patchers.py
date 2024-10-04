from .response import Response 

from typing import Callable, List

import re
import random
from bs4 import BeautifulSoup

type Patcher = Callable[[Response, 'Request'], Response]

def find_substring_in_lines(s, substring):
    for line_index, line in enumerate(s.splitlines()):
        position = line.find(substring)
        if position != -1:
            return line_index

    return 0

def extract_words_from_line(line):
    clean_line = re.sub(r'<[^>]+>', '', line)
    words = clean_line.split()
    return words

def uwuify_text(text):
    replacements = [
        (r'r', 'w'),
        (r'l', 'w'),
        (r'R', 'W'),
        (r'L', 'W'),
        (r'no', 'nyo'),
        (r'No', 'Nyo'),
        (r'u', 'uwu'),
        (r'U', 'Uwu')
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    
    expressions = [" owo", " UwU", " rawr", " >w<"]
    sentences = text.split('. ')
    uwuified_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            uwuified_sentences.append(sentence + (random.choice(expressions) if random.randint(0, 5) > 4 else ''))
    
    return '. '.join(uwuified_sentences)

def apply_url_params(body, params: str):
    body = body.decode('utf-8')
    soup = BeautifulSoup(body, 'html.parser')

    for a_tag in soup.find_all('a', href=True):
        original_href = a_tag['href']
        if '?' in original_href:
            new_href = f"{original_href}&{params}"
        else:
            new_href = f"{original_href}?{params}"
        a_tag['href'] = new_href
        
    return str(soup)

def uwuify(body):
    body = body.decode('utf-8')
    soup = BeautifulSoup(body, 'html.parser')

    for text in soup.find_all(text=True):
        if text.parent.name not in ['script', 'style']:
            original_text = text.string
            words = extract_words_from_line(original_text)
            uwuified_words = [uwuify_text(word) for word in words]
            uwuified_text = ' '.join(uwuified_words)
            text.replace_with(uwuified_text)

    for a_tag in soup.find_all('a', href=True):
        original_href = a_tag['href']
        if '?' in original_href:
            new_href = f"{original_href}&uwu=true"
        else:
            new_href = f"{original_href}?uwu=true"
        a_tag['href'] = new_href


    return str(soup)

def is_subdict(sub_dict, main_dict):
    for key, value in sub_dict.items():
        if key not in main_dict or main_dict[key] != value:
            return False
    return True

patchers: List[Patcher] = [
    # lambda response, request: Response(
    #     response.code, 
    #     response.headers,
    #     "\n".join(line.replace('e', 'a') if index > find_substring_in_lines(response.body.decode('utf-8'), '</head>') else line for index, line in enumerate(response.body.decode('utf-8').splitlines())).encode('utf-8')
    # ) if 'text/html' in response.headers.values() else response
    lambda response, request: Response(
        response.code, 
        response.headers,
        uwuify(response.body).encode('utf-8')
    ) if 'text/html' in response.headers.values() and is_subdict({'uwu': 'true'}, request.path.params) else response,
        lambda response, request: Response(
        response.code, 
        response.headers,
        re.sub(r'sludge', lambda match: 'sludge' + ' (/&#x73;&#x6c;&#x28c;&#x64;&#x361;&#x292;/)' if random.randint(0, 5) < 1 else 'sludge', response.body.decode('utf-8')).encode('utf-8')
    ) if 'text/html' in response.headers.values() else response,
    lambda response, request: Response(
        response.code,
        response.headers, 
        apply_url_params(response.body.replace(b'<head>', b'<head><style>:root,body,body>main>section{animation:swing 180s infinite ease-in-out;transform-origin:center}@keyframes swing{0%{transform:rotate(0deg)}50%{transform:rotate(-1deg)}100%{transform:rotate(1deg)}}</style>'), 'swing=true').encode('utf-8')
    ) if 'text/html' in response.headers.values() and (random.randint(0, 100) < 1 or is_subdict({'swing': 'true'}, request.path.params)) else response,
    # spiin!
    lambda response, request: Response(
        response.code,
        response.headers, 
        apply_url_params(response.body.replace(b'<head>', b'<head><style>:root,body,body>main>section,body>main>section>flex-grid>flex-grid-item{animation:spiin 480s infinite ease-in-out;transform-origin:center}@keyframes spiin{0%{transform:rotate(0deg)}50%{transform:rotate(180)}100%{transform:rotate(360deg)}}</style>'), 'spin=true').encode('utf-8')
    ) if 'text/html' in response.headers.values() and (random.randint(0, 1000) < 1 or is_subdict({'spiin': 'true'}, request.path.params)) else response
]
