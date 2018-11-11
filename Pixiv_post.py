"""
  作者：wanderees
  时间： 2018-7-27
  注：pixiv本站已被dns污染，需要改dns才能进行爬取。
"""
#coding=utf-8
import re
import requests
import vthread       #第三方线程池库，很方便，一个装饰器即可将你的函数变成多线程。
import time
from urllib import error
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#推荐页面url
url ='https://www.pixiv.net/rpc/recommender.php?type=illust&sample_illusts=auto&num_recommendations=1000&page=discovery&mode=all&tt=46bb49d20b7a81509aa5260989dfea3'

new_url = []
pic_url = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='     #每张图片前面的URL，后面加上图片id就是图片链接
s = requests.session()
headers = {
    'referer':'https://www.pixiv.net/discovery',
     'accept-encoding':'gzip, deflate, sdch, br',
    'accept-language':'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'
    }
cookies = {'PHPSESSID':'15966867_5cf9fb611398316b4cb7fece8d46c690',           #使用cookie登录
           '__utmz':'235335808.1535097332.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
           '__utmv':'235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=15966867=1^9=p_ab_id=1=1^10=p_ab_id_2=2=1^11=lang=zh=1',
            'a_type':'0',
            'auto_view_enabled':'1',
            'b_type':'1',
            'c_type':'30',
            'device_token':'7ef06393712a9b009c645d486c2c0a40',
            'login_bc':'1',
            'module_orders_mypage':'%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22showcase%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D',
            'p_ab_id':'1',
            'p_ab_id_2':'2',
           'privacy_policy_agreement':'1',
           'tag_view_ranking':'RTJMXD26Ak~Lt-oEicbBr~Oa9b6mEc1T~jH0uD88V6F~uusOs0ipBx~nQRrj5c6w_~1Xn1rApx2-~OT4SuGenFI~kP7msdIeEU~_pwIgrV8TB~wKl4cqK7Gl~LpjxMAWKke~RybylJRnhJ~TF0WQsVOcg~jOtGu8sIKu~w6DOLSTOSN~ETjPkL0e6r~tlI9YiBhjp~jhuUT0OJva~THI8rtfzKo~uW5495Nhg-~qtVr8SCFs5~3z9G1yhJBC~ykDUPR1jwm~Qdur7OglM-~Cr3jSW1VoH~i83OPEGrYw~BU9SQkS-zU~cJxW0nBuQ8~zIv0cf5VVk~wX6S8wLDeM~w_BFuPBIv3~cpt_Nk5mjc~gnTtYdDB_b~wh7sZziAaL~azESOjmQSV~3mLXnunyNA~8G7nApQlqf~0xsDLqCEW6~yTFlPOVybE~DuCdp8i1kQ~metPG27dgT~pzzjRSV6ZO~SvhFpM2bDA~3W4zqr4Xlx~_RfiUqtsxe~RKWhQt3bKa~vFwTRLUjL6~CrFcrMFJzz~LJo91uBPz4~-sp-9oh8uv~xPzNjdEfl2~mFuvKdN_Mu~K8esoIs2eW~RKAHEY3QDd~bXMh6mBhl8~a-yCMcqYxL~RFVdOq-YjA~pYlUxeIoeg~ZXFMxANDG_~LMpjieSVIv~2pZ4K1syEF~0G1fdsiW-i~1yIPTg75Rl~kGYw4gQ11Z~WQMRPz3l59~HBYFbIUAS8~GmdMh9y_Yz~WCITjcQNG4~VyMzgidqJ2~PwDMGzD6xn~tLrODMBPQT~nt6svoJL0B~9FdW67Hfv1~KvAGITxIxH~J1WMmtbpqz~j6Q3-ZKpTm~twv3UAr3z5~t2ErccCFR9~_hSAdpN9rx~F5CBR92p_Q~XW47HdFpTH~dOXilJsBsW~wqBB0CzEFh~1B_9zw2sZ7~KXfT8YWwR1~5_ms-N3Fk0~eE5ORV6KVQ~BLw7uT0VZ9~QjJSYNhDSl~YRDwjaiLZn~gVfGX_rH_Y~KN7uxuR89w~m3EJRa33xU~7PMB_obiO7~JdVOJVi8v3~Xka00AX0jf~dx7ljrJnxj~7NdSnX3_JU~HY55MqmzzQ',
            'login_ever':'yes',
            'first_visit_datetime_pc':'2018-08-24+16%3A54%3A23',
           'is_sensei_service_user':'1',
           'ki_t':'1534818314144%3B1534818314144%3B1534838613809%3B1%3B8',
            'pixivPreviewerSetting':'%7B%22enablePreview%22%3A%22true%22%2C%22previewQuality%22%3A%220%22%2C%22hideLoading%22%3A%22false%22%2C%22enableSort%22%3A%22true%22%2C%22pageCount%22%3A%223%22%2C%22favFilter%22%3A%223%22%2C%22linkBlank%22%3A%22true%22%2C%22hideFavorite%22%3A%22false%22%7D',
            'yuid':'NTCYWXM30'
            }
req = s.get(url, headers=headers, cookies=cookies, verify=False)
req.encoding = 'utf-8'    #设置编码utf-8
kk = re.findall(r'"(\d+)"',req.text,re.S)


def Get_url(id):        #获得推荐页图片的id
    old_url_list = []
    url_list = []
    url_pic = []
    new_url_pic = []
    x = 0
    for i in id:
        c_id = ''.join(map(str, i))
        main_url ='https://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s' % c_id
        url_list.append(main_url)
    cookies = {'PHPSESSID': '15966867_3d50bbd004b2aaeb640ce4ed36439e7a',
               'a_type': '0',
               'auto_view_enabled': '1',
               'b_type': '1',
               'c_type': '30',
               'device_token': 'cf23aa23b914d2a69a68451a94d0d272',
               'login_bc': '1',
               'module_orders_mypage': '%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22showcase%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D',
               'p_ab_id': '6',
               'p_ab_id_2': '3',
               'privacy_policy_agreement': '1',
               'tag_view_ranking': 'RTJMXD26Ak~Lt-oEicbBr~Oa9b6mEc1T~jH0uD88V6F~nQRrj5c6w_~uusOs0ipBx~1Xn1rApx2-~kP7msdIeEU~OT4SuGenFI~_pwIgrV8TB~wKl4cqK7Gl~LpjxMAWKke~RybylJRnhJ~tlI9YiBhjp~w6DOLSTOSN~ykDUPR1jwm~Cr3jSW1VoH~i83OPEGrYw~3z9G1yhJBC~qtVr8SCFs5~cJxW0nBuQ8~cpt_Nk5mjc~ETjPkL0e6r~metPG27dgT~DuCdp8i1kQ~azESOjmQSV~8G7nApQlqf~jhuUT0OJva~SvhFpM2bDA~3mLXnunyNA~3W4zqr4Xlx~_RfiUqtsxe~mFuvKdN_Mu~BU9SQkS-zU~LJo91uBPz4~RKAHEY3QDd~kGYw4gQ11Z~HBYFbIUAS8~RKWhQt3bKa~LMpjieSVIv~0G1fdsiW-i~1yIPTg75Rl~vFwTRLUjL6~WQMRPz3l59~pzzjRSV6ZO~uW5495Nhg-~GmdMh9y_Yz~WCITjcQNG4~VyMzgidqJ2~PwDMGzD6xn~-sp-9oh8uv~tLrODMBPQT~ZXFMxANDG_~7NdSnX3_JU~BLw7uT0VZ9~QjJSYNhDSl~YRDwjaiLZn~gVfGX_rH_Y~KN7uxuR89w~yTFlPOVybE~JdVOJVi8v3~Xka00AX0jf~pYlUxeIoeg~ay54Q_G6oX~gnTtYdDB_b~HY55MqmzzQ~9FdW67Hfv1~F5CBR92p_Q~K8esoIs2eW~MHugbgF9Xo~Spazle1KS8~0YMUbkKItS~KvAGITxIxH~2pZ4K1syEF~NBK37t_oSE~-EhCw9iKLt~igqBHMFFDi~V-nCbOENj2~e2yEFDVXjZ~65aiw_5Y72~lmb_eef2XG~sOBG5_rfE2~1B_9zw2sZ7~Sjwi7bh6-s~TXH0zUwQ7-~dOXilJsBsW~IyRhOdNpxG~wqBB0CzEFh~-7rTBf0PIy~SoxapNkN85~_O4JCuyrb7~G_f4j5NH8i~nnNDehe5s6~qZlv43XP1O~KHhKRc2P1_~e71s5Iv-7x~7koc5h60k7~kqu7T68WD3~JU32ZIyOoM~MO67n2Zm2e',
               'login_ever': 'yes',
               'first_visit_datetime_pc': '2018-07-26+18%3A11%3A16',
               'is_sensei_service_user': '1',
               'ki_t': '1534818314144%3B1534818314144%3B1534838613809%3B1%3B8',
               'pixivPreviewerSetting': '%7B%22enablePreview%22%3A%22true%22%2C%22previewQuality%22%3A%220%22%2C%22hideLoading%22%3A%22false%22%2C%22enableSort%22%3A%22true%22%2C%22pageCount%22%3A%223%22%2C%22favFilter%22%3A%223%22%2C%22linkBlank%22%3A%22true%22%2C%22hideFavorite%22%3A%22false%22%7D',
               'yuid': 'JGWYJ3Q57'
               }
    s = requests.session()
    for i in url_list:
        print(i)
        x += 1
        headers = {
            'referer': i,
            'accept-encoding': 'gzip, deflate, sdch, br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'
        }
        try:
            request = s.get(i,headers = headers,cookies = cookies,verify=False,timeout=10)
            Down_url = re.findall('"original":"(.+?)"},"tags"',request.text,re.S)
            old_url_list.append(Down_url)
        except:
            print('error')
        print(x)
    for i in old_url_list:
        xx = str(i).replace("\\", "").replace('\'','')      #对获得的链接进行替换，换成可用的链接。
        url_pic.append(xx)
    for i in url_pic:
        new_url_pic.append(str(i).replace('[', '').replace(']', ''))
    print(new_url_pic)
    return new_url_pic        #返回推荐页面的图片url列表


@vthread.pool(5)         #使用第三方库进行多线程下载，这里是5个线程进行下载。
def Download_img(url):       #下载函数，设置了40秒超时。
    x = 0
    id = re.findall(r'\d+/(\d+)_p0.\w+', str(url))
    new = ''.join(map(str, id))
    referer = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + '%s' % new         #P站的图片必须加上referer才能访问，否则会被服务器拒绝访问。
    headers = {
            'referer':referer,
             'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'
    }
    print(url)
    try:
        s = requests.get(url,headers=headers,timeout=40)      
        img = s.content
        with open(r'D:\VPN\%s.jpg' % new,'wb') as f:
            f.write(img)
    except error.HTTPError as e:
        print('下载失败:')
        print(e.code)
    print('id:%s done' % new)
    time.sleep(5)             #延时5秒进行下载，防止被BAN。

down_url = Get_url(kk)
for i in down_url:
    id = re.findall(r'\d+/(\d+)_p0.\w+', str(i))
    new = ''.join(map(str, id))
    if os.access(r'D:\VPN\%s.jpg' % new, os.F_OK):        #由于每次运行的推荐图片都有不同和相同的，这里把已经下载的图片过滤，优化下载。
        print('The %s.img already exists' % new)
        pass
    else:
        Download_img(i)

