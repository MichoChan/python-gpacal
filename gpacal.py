#encoding=utf-8
import urllib2
import urllib
import cookielib
import re
def Brower(url,user,password,utype):
    #登陆页面，可以通过抓包工具分析获得，如fiddler，wireshark
    login_page = "http://jwgl.ahnu.edu.cn/login/check.shtml"
    try:
        #获得一个cookieJar实例
        cj = cookielib.CookieJar()
        #cookieJar作为参数，获得一个opener的实例
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
        opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0')]
        #生成Post数据，含有登陆用户名密码。
        data = urllib.urlencode({"user":user,"pass":password,"usertype":utype})
    
        headers = {'Referer':'http://jwgl.ahnu.edu.cn'}

        req = urllib2.Request(login_page,data)
        #以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
        opener.open(req)
        #以带cookie的方式访问页面
        #op=opener.open(url)
        #读取页面源码
        #data= op.read()
        req = urllib2.Request('http://jwgl.ahnu.edu.cn/query/cjquery',headers=headers)
        rlt=opener.open(req)
        return rlt.read()
    except Exception,e:
        print str(e)
        
if __name__ == '__main__':
    page = Brower("http://jwgl.ahnu.edu.cn","120705008","assign5926136","stu")
    rule = 'center">(.*?)</tr'
    ans = re.findall(rule,page,re.S)
    alls={}
    for subj in ans:
        rule = '>(.*?)</td'
        out = re.findall(rule,subj)
        alls[out[0]]=out[1:]
    su = 0.0
    cnt = 0.0
    key={
        '优秀':95,
        '良好':85,
        '中等':75,
        '及格':60,
        '不及格':45
        }
    for i in alls:
        try:
            su+=float(alls[i][3])*float(alls[i][-3])    
        except Exception,e:
            su+=float(alls[i][3])*key[alls[i][-3]]
        cnt+=float(alls[i][3])
        print alls[i][0].decode('utf-8'),'',alls[i][-3]
    print '\n平均学分绩点='.decode('utf-8'),'%.2lf' % (su/cnt)
