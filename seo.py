#coding:utf-8
import prettytable as pt
import progressbar
import argparse
import requests
import re

def main():
    # 指定-r参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest='read', help='select domains file')
    args = parser.parse_args()
    
    # 参数为空 输出--help命令
    if args.read == None:
        parser.print_help()
    
    # 从文件中读取每行的域名
    try:
        f = open(args.read,"r")
        lines = ''.join(f.readlines()).split("\n")
        tb = pt.PrettyTable(["域名","百度权重","百度收录","站点标题","域名年龄"])
        p = progressbar.ProgressBar()
        for domain in p(lines):
            url = 'http://seo.chinaz.com/{domain}'.format(domain=domain)
            headers = {
                'Host': 'seo.chinaz.com',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = 'm=&host={domain}'.format(domain=domain)
            try:
                response = requests.post(url=url,headers=headers,data=data,timeout=10)
                html = response.text

                # 百度权重正则
                baidu_pattern = re.compile(r'baiduapp/(.*?).gif')
                baidu = baidu_pattern.findall(html)[0]
                
                # 收录数量正则
                count_pattern = re.compile(r'"Ma01LiRow w12-1 ">(.*?)</div>')
                count = count_pattern.findall(html)[4]

                # 站点标题正则
                domain_name = re.compile(r'class="ball">(.*?)</div>')
                name = domain_name.findall(html)[0]
                
                # 域名年龄正则
                domain_year = re.compile(r'wd={domain}" target="_blank">(.*?)</a>'.format(domain=domain))
                year = domain_year.findall(html)[1]

                tb.add_row([domain,baidu,count,name,year])

            except Exception as e:
                tb.add_row([domain,'访问超时','访问超时','访问超时','访问超时'])
        print(tb)

    except Exception as e:
        print(e) 
if __name__ == '__main__':
    main()