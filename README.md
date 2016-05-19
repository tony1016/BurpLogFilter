# BurpLogFilter
一个python3写的，用于过滤BurpSuite日志的小程序

A python3 program to filter BurpSuite log file.

# WHY？

为什么要写这个程序呢？强大的SqlMap支持使用BurpSuite的日志进行批量分析，但是BurpSuite的日志记录了所有走代理的流量，包括静态资源啊，重复的提交啊，这些都会影响SqlMap的分析效率。于是打算写一个小程序，可以做到：

- 可以按照域名过滤请求
- 可以自动过滤静态资源请求
- 可以自动按照模式过滤URL，即相同URL和参数的请求，只会留其一（参数值对于SqlMap没有什么作用）

Why I wrote this program?The powerful SqlMap accepts a BurpSuite log file to make batch anaylze,but the log of BurpSuite record everything,includes static resources,duplicated submits,which will reduce the efficiency of the analyze.So I wrote this utility to make:

- can filter with a hostname
- can filter static resources automatic
- can filter duplicated submits according to the url and params(the value of params is useless for SqlMap analyze)




# USAGE

### 1.勾选BurpSuite输出日志(check the logging option)

![burpsuite](https://github.com/tony1016/BurpLogFilter/raw/master/res/burpsuite.png)

### 2.使用burplogfilter.py过滤日志(use burplogfilter.py to filter log file)

```sh
Usage: python3 burplogfilter.py [options]

Options:
  -h                                  Show this showHelp
  -f filepath                         The BurpSuite log to analyze
  --host keyword, --host=keyword      Host name filter
  -v                                  Show debug message

Examples:
  python3 burplogfilter.py -f /tmp/burp.log --host='google.com' > burp-proxy.log
```

### 3.使用SqlMap批量分析日志(Use SqlMap to batch analyze log)

```sh
sqlmap -l burp-proxy.log --batch -smart
```

### 4.查看分析结果(Check result)

```sh
ls /usr/local/Cellar/sqlmap/0.9_1/libexec/output/
```

