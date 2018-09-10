# _*_coding:utf-8_*_
import re
import requests
import hashlib
import time
import os
import io
import sys

def read_data(filename):
    filedir = 'D:\\download\\www.lee-mac.com\\'
    #filedir ='D:/roehead/软件/LISP/lee-mac-18/www.lee-mac.com/'
    filepath = filedir+filename
    file_contents = '000'
    if os.path.exists(filepath) == True:
        file_handle = open(filepath,mode='r',encoding='utf-8',errors='ignore')
        #file_contents = file_handle.readlines()
        file_contents = file_handle.read()
        #for student in students:
        #    student = student.strip('\n')
        #    list = student.split(' ')
        #    list.pop()
        #    student_list.append(list)
        #file_handle.close()
    return file_contents

def get_index(url):
    #获取网页源码
    respose = requests.get(url)
    if respose.status_code==200:
        return respose.text

def parse_index(res):
    #print(res)
    urls = re.findall(r'</td><td><a href="(.*?)"', res,re.S)  #(.)字符配匹配年有字符，包括换行符
    #print(urls)
    return urls

def get_detail(urls):
    for url in urls:
        if not url.startswith('http'):
            print(url, end=' ')
            url = "http://www.lee-mac.com/%s" % url
        result = requests.get(url)
        if result.status_code==200 :
            lisp_url_m = re.search(r'<td><a href="(lisp/.*?)"',result.text,re.S)
            if lisp_url_m:
                lisp_url=lisp_url_m.group(1)
                #print(lisp_url,end=' ')
                save(lisp_url)
            gif_url_iter = re.finditer(r'<p><img src="(lisp/gifs.*?)"', result.text, re.S)
            if gif_url_iter:
                for gif_url_m in gif_url_iter:
                  gif_url=gif_url_m.group(1)
                  print(gif_url,end=' ')
                  #save(gif_url)
        print(' ')


def save(url):
    respose = requests.get("http://www.lee-mac.com/%s" % url)
    if respose.status_code==200:
        #m=hashlib.md5()
        #m.updata(url.encode('utf-8'))
        #m.updata(str(time.time()).encode('utf-8'))
        #filename=r'%s.lsp'% m.hexdigest()
        filedir = "D:\\roehead\软件\LISP\lee-mac-18"
        filename =re.search(r'.*?/(?!gif)(.*)',url).group(1)
        filepath=filedir + r'\%s'%filename
        print(filepath,end = ' ')
        with open(filepath, 'wb') as f:
            f.write(respose.content)

def parse_code(res):
    #print(res)
    code_list =[]
    codeiter = re.findall(r'<div class="code">.*?<pre>(.*?)</pre>.*?</div>', res,re.S)
    for codeblock in codeiter:
        #print(codeblock)
        print("*********************")
        lines = re.finditer(r'(\s*<span.*?>.*</span>)(?=\n)', codeblock +'<span></span>\n', re.S)
        for line in lines:
            words = re.finditer(r'(\s*)<span.*?>(.*?)</span>(.*?)(?=<)', line.group(1),re.S)
            for word in words:
              #print(word.group(1)+ word.group(2)+ word.group(3),end="")
              code_list.append(word.group(1)+ word.group(2)+ word.group(3))
          #print()
        print()
        code_list.append('\n')
    return code_list

def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
    #res1 = get_index('http://www.lee-mac.com/programs.html' )
    #res2 = parse_index(res1)
    #get_detail(res2)
    res1 = read_data('programs.html')
    #print(res1)
    programs = parse_index(res1)
    #print(res2)
    for program in programs:
        print(program)
        #if program not in ('totallengthandarea.html','fractals.html','iteratedfunctionsystems.html','koch.html','layerstatus.html','getsyntaxsub.html','gettruecontent.html','listdifference.html','listintersection.html','listsymdifference.html','listunion.html'):
        code_lines = read_data(program)
        #print(res)
        codes = parse_code(code_lines)
        if codes:
            fp = open('D:\\download\\www.lee-mac.com\\lispcode\\' + program.replace('.html','')+'.txt','w')
            for line in codes:
                #line = line.encode('utf-8')
                fp.write(line)
                #fp.write('\n'.encode('utf-8'))
            fp.close()


if __name__ == '__main__':
    main()