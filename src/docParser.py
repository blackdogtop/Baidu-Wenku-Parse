#!usr/bin/env python
# -*- coding:utf-8 -*-

import os
import requests
import re
from lxml import etree
import json


def getAddressList(url):
    """
    获取百度文库的json地址
    :param url:百度文库链接（仅doc格式的文件）
    :return addressList:json地址组成的list
    :return title:文库文件名
    """
    sourceHTML = requests.get(url).content
    addresses = re.findall(r'wkbjcloudbos\.bdimg\.com.*?json.*?Expire.*?\}', str(sourceHTML))
    title = etree.HTML(sourceHTML).xpath("//title/text()")[0].strip()
    addressList = []
    for address in addresses:
        address = "https://" + address.replace("\\\\", "")
        # address = "https://" + address.replace("\\\\\\\\\\\\/", "/")  # 同样正确
        address = address[:-2]
        addressList.append(address)
    return addressList, title


def getJsonContent(urlList, title, savePath = '../data/'):
    """
    获取json文件内容
    :param savePath:文件保存路径（默认为../data/）
    :return 保存文件的绝对路径
    """
    content, result = '', ''
    pageNum, i = len(urlList), 1
    print('共计{}页'.format(pageNum))
    for address in urlList:
        print("正在获取第{}页".format(i))
        i += 1
        content = requests.get(address).content.decode()
        content = re.match(r'.*?\((.*)\)$', content).group(1)
        allBodyInfo = json.loads(content)["body"]
        for bodyInfo in allBodyInfo:
            result = result + bodyInfo['c'].strip()

    if not os.path.exists(savePath):
        os.mkdir(savePath)
    fileName = title + '.txt'
    with open(savePath + fileName, 'w') as f:
        f.write(result)
    return os.path.abspath(savePath) + '/' +fileName


def main():
    baiduURL = input('请输入百度文库链接：')
    addressList, title = getAddressList(baiduURL)
    filePath = getJsonContent(addressList, title)
    print('获取成功，保存路径为{}'.format(filePath))


if __name__ == '__main__':
    main()