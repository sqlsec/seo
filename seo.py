import re
import os
import time
import argparse
import requests
from multiprocessing import Pool


def args():
    """
    命令行参数以及说明
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--read', dest='read', help='input domains file path')
    parse_args = parser.parse_args()

    # 参数为空 输出--help命令
    if parse_args.read is None:
        parser.print_help()
        os._exit(0)
    
    return parse_args.read


def seo(domain_url):
    """
    利用爱站接口查询权重信息
    """
    url = f'http://seo.chinaz.com/?host={domain_url}'
    headers = {
        'Host': 'seo.chinaz.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    r = requests.get(url=url, headers=headers, timeout=6)
    html = r.text

    # 百度权重正则
    baidu_pattern = re.compile(r'baiduapp/(.*?).gif')
    baidu = baidu_pattern.findall(html)[0]

    # 站点标题正则
    site_name_rules = re.compile(r'class="ball">(.*?)</div>')
    site_name = site_name_rules.findall(html)[0]

    print(str(domain_url).ljust(30), '\t', baidu, '\t', site_name)


def main():
    start = time.time()
    file_path = args()
    try:
        #  读取文件所有行
        with open(file_path, "r") as f:
            lines = ''.join(f.readlines()).split("\n")

        print('域名'.ljust(30), '权重\t 站点标题')
        #  设置一个容量为8的进程池
        pool_number = 10
        pool = Pool(pool_number)

        for line in lines:
            if 'http://' in line:
                line = line[7:]
            elif 'https://' in line:
                line = line[8:]
            if line:
                pool.apply_async(seo, (line,))

        pool.close()
        pool.join()

        end = time.time()
        print(f'\n耗时: {end - start:.4f} 秒')
    except Exception as e:
        print('文件读取异常，请检查文件路径是否正确！')
        print(e)


if __name__ == '__main__':
    main()
