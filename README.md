# EntDataCrawl
## 完成的工作：
1. 尝试极验验证码破解（主要python库Selenium,BeautifulSoup,urllib,PIL）
2. 解析抓取的企业信用的数据，保存为json格式数据，由于抓取的网站采用ajax异步加载，所以要具体分析每个部分信息的url，发起请求获取
3. 用Flask框架，将前面的工作全部写成api调用，用到sqlite3数据库，所以将封装了部分数据库操作，数据库用于保存获取到的临时url，获取到的url有访问的时间限制，api的访问顺序需要从头开始（这部分写的太弱了，逻辑混乱，可以改进的地方很多。。。）
