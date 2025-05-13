import requests
from bs4 import BeautifulSoup
import re
import base64
from urllib.parse import unquote
import urllib.parse
import sys
import html
import functools

# 接受输入
number = input("请输入要下载的集数：")
number_list = number.split(",")
# 设置保存地址
path = rf"E:\视频\python下载\海贼王{num}.mp4"

# 正则一：匹配player_aaaa：
pattern = re.compile(r"player_aaaa=\{.+}")
# 正则二：匹配url
pattern_1 = re.compile("\"url\":\".*?\"")
pattern_2 = re.compile("\"url_next\":\".*?\"")
# 正则匹配最终url
prog_first = re.compile(r"container.*\n.*\n.*theme:.*")
prog_second = re.compile(r"'http.*'")

# 一轮处理request+Beautifulsoup，查找scripts标签
def find_scrips(url, pattern):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    scripts = soup.find_all("script",type="text/javascript")[0].text
    scripts = re.search(pattern, scripts)
    return scripts

# @decorator
def re_url(pattern_1,pattern_2,scripts):
    url = re.search(pattern_1, scripts[0]).group()[7:-1]
    url_next = re.search(pattern_2, scripts[0]).group()[12:-1]
    return url, url_next

# base64解码函数
def decode_base64(url,url_next):
    decode_base64_url = base64.b64decode(url)
    decode_base64_url_next = base64.b64decode(url_next)
    return decode_base64_url, decode_base64_url_next

# 编写unescape解码函数
def unescape(string):
    string = urllib.parse.unquote(string)
    quoted = html.unescape(string).encode(sys.getfilesystemencoding()).decode('utf-8')
    # 转成中文
    return re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: chr(int(m.group(1), 16)), quoted)

# unescape解码函数
def unescape_str(decode_base64_url,decode_base64_url_next):
    decode_url_unescape = unescape(decode_base64_url)
    decode_url_next_unescape = unescape(decode_base64_url_next)
    return decode_url_unescape, decode_url_next_unescape

# 内层地址拼接函数
def url_fix(decode_url_unescape):
    second_url_font=r"https://www.aowu.tv/player/?url="
    second_url_back=r"&next=/play/ZuQCCS-1-1026.html"
    second_url = second_url_font + decode_url_unescape + second_url_back
    return second_url

# request请求得到url
def deal_request(second_url,headers):
    print("Beautifulsoup处理并读取视频链接")
    res = requests.get(second_url,headers=headers)
    return res

# Beautifulsoup解析函数
# @decorator
def BS_analysis(res):
    if res.status_code == 200:
        soup_another = BeautifulSoup(res.content,"html.parser")
        script = soup_another.find_all("script")[-1]
        script_string = script.string
        return script_string
    else:
        print(f"请求失败,status_code={res.status_code}")

# download函数
def download(num,response):
    with open(path, 'wb') as file:
        print(f"正在下载海贼王第{num}集")
        # 使用iter_content方法逐块读取响应内容
        for chunk in response.iter_content(chunk_size=8192):  # 设置块大小为8192字节
            if chunk:  # 检查块是否为空
                file.write(chunk)
                file.flush()  # 刷新缓冲区，确保数据写入磁盘

def main():
    # 调用find_scrips函数
    scripts = find_scrips(url=url1,pattern=pattern)
    # 调用re_url函数
    url, url_next = re_url(pattern_1,pattern_2,scripts)
    # 调用base64解码函数
    decode_base64_url, decode_base64_url_next = decode_base64(url,url_next)
    # unescape解码
    decode_url_unescape,decode_url_next_unescape = unescape_str(decode_base64_url,decode_base64_url_next)
    # 调用url_fix函数
    second_url = url_fix(decode_url_unescape)
    # 调用deal_request函数,对second_url发送请求
    res = deal_request(second_url,headers)
    return res

def tries():
    while True:
        try:
            # 调用BS_analysis函数,解析second_url
            script_string = BS_analysis(res = main())
            return script_string
        except IndexError:
            print("IndexError!!!\n再次重新尝试")

# 获取最终视频url
def re_download_url():
    print("正则定位url")
    url_re_first = re.search(prog_first,script_string).group()
    url_re_second = re.search(prog_second,script_string).group().replace("'", "")
    print(f"正则定位url完成,最终视频链接为\n{url_re_second}")
    return url_re_first, url_re_second

# 根据输入设置下载次数
for num in number_list:
    num = int(num)
    number = num - 3
    url1 = rf"https://www.aowu.tv/play/ZuQCCS-1-{number}.html"
    # 设置请求headers
    headers = {
        "user-agent": , "referer": rf"https://www.aowu.tv/play/ZuQCCS-1-{num}.html"
    }
    # 尝试执行
    script_string = tries()
    url_re_first, url_re_second = re_download_url()
    # 下载视频
    response = requests.get(url_re_second,stream=True)
    if response.status_code == 200:  # 检查请求是否成功
        download(num,response)  # 调用download函数
        print('文件下载成功！')
    else:
        print(f'文件下载失败，状态码：{response.status_code}')
        print(response.text)  # 输出响应内容以查看错误详情










