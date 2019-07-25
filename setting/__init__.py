#coding=utf-8
import sys
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from . import settings
sys.path.append(settings.BASE_PATH)

from index import index_app
from users import user_app
from payment import payment_app


# appindex匹配路由时不需要前缀，appuser匹配路由时要加上/user前缀
application = DispatcherMiddleware(index_app, {
    '/user': user_app,
    '/payment': payment_app,
})
# 得到的这个application对象没有run方法
# 所以要用run_simple

class FlaskServer():
    def run(self,host='localhost',port=5000,debug=False):
        self.host=host
        self.port=port
        self.debug=debug
        run_simple( self.host,
                    self.port,
                    application,
                    use_debugger=self.debug,
                    use_reloader=True
                )