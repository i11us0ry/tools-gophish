# 0x01 环境
python3

# 0x02 配置
打开脚本填写API KEY和gophish地址即可

# 0x02 Options:
  -h, --help                 show this help message and exit
  
  --createSP                 create Sending Profiles
  
  --createG                  create groups
  
  --createC                  create campaigns
  
  --deleteSP=DELETESP        delete Sending Profiles
  
  --deleteG=DELETEG          delete groups
  
  --deleteC=DELETEC          delete campaigns
  
  --getSP=GETSP              get Sending Profiles
  
  --getG=GETG                get groups
  
  --getC=GETC                get campaigns
  
  --complete=COMPLETE        complete campaigns
  
  --saveResults=SAVERESULTS  save Results
  
  --dir=DIR                  指定目录
  
  --ifile=IFILE              指定文件
  
  --ofile=OFILE              输出文件
  
  --helps                    参考语法
  

# 0x03 参考语句
01、创建发件邮箱（指定目录）:python3 Gofish.py --createSP --dir C:\\Users\\gophish\\smtp

02、创建发件邮箱（指定文件）:python3 Gofish.py --createSP --ifile C:\\Users\\gophish\\smtp\\1.csv

03、删除发件邮箱（所有邮箱）:python3 Gofish.py --deleteSP 0

04、删除发件邮箱（指定ID值）:python3 Gofish.py --deleteSP 81-85,87,88-90

05、获取发件邮箱（所有邮箱）:python3 Gofish.py --getSP 0

06、获取发件邮箱（指定ID值）:python3 Gofish.py --getSP 81-85,87,88-90

07、创建发件目标（指定目录）:python3 Gofish.py --createG --dir C:\\Users\\gophish\\groups

08、获取发件目标（所有目标）:python3 Gofish.py --getG 0

09、获取发件目标（指定ID值）:python3 Gofish.py --getG 20-25,27,28-30

10、删除发件目标（所有目标）:python3 Gofish.py --deleteG 0

11、获取发件目标（指定ID值）:python3 Gofish.py --deleteG 20-25,27,28-30

12、创建钓鱼任务（指定文件）:python3 Gofish.py --createC --ifile C:\\Users\\gophish\\campaigns\\1.csv

13、获取钓鱼任务（所有任务）:python3 Gofish.py --getC 0

14、获取钓鱼任务（指定ID值）:python3 Gofish.py --getC 45-47,50

15、删除钓鱼任务（所有任务）:python3 Gofish.py --deleteC 0

16、删除钓鱼任务（指定ID值）:python3 Gofish.py --deleteC 45-49,50

17、完成钓鱼任务（所有任务）:python3 Gofish.py --complete 0

18、获取钓鱼任务（指定ID值）:python3 Gofish.py --complete 51-53

19、导出钓鱼任务（所有任务）:python3 Gofish.py --saveResults 0 --ofile allResults

20、导出钓鱼任务（中招用户）:python3 Gofish.py --saveResults 1 --ofile submitDat
