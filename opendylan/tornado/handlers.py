# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

import datetime, tornado, uuid
from opendylan.celery.tasks import dylan_builder

class DylanBuildHandler(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self, **kwargs):
    taskID = 'build-' + str(uuid.uuid4())
    code = False # self.get_argument('code')
    if not code:
      code = 'format-out("Hello world!");'
    task = dylan_builder.delay(taskID, code)
    def check_build_task():
      if task.ready():
        self.write({'success':True} )
        self.set_header("Content-Type", "application/json")
        self.finish()
      else:
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(0.00001), check_build_task)
    tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(0.00001), check_build_task)

