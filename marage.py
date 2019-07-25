#coding=utf-8

import sys

from setting import FlaskServer

server = FlaskServer()

def main():
    bandaddr={}
    debug=True
    if sys.argv[1:]:
        try:
            bandaddr=dict(zip(['host','port'],sys.argv[1].split(':')))
        except:
            raise ValueError('命令行输入的参数不正确')
    if sys.argv.pop=='False':
        debug=False
    host=bandaddr.get('host','127.0.0.1')
    port=bandaddr.get('port',8888)
    server.run(host,port,debug)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('系统退出')
