# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

import anyjson, datetime, tornado, uuid
from opendylan.celery.tasks import dylan_builder

class DylanBuildHandler(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def post(self, **kwargs):
    taskID = 'build-' + str(uuid.uuid4())
    code = self.get_argument('code')
    task = dylan_builder.delay(taskID, code)
    def check_build_task():
      if task.ready():
        self.write(anyjson.serialize(task.result))
        self.set_header("Content-Type", "application/json")
        self.finish()
      else:
        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(0.00001), check_build_task)
    tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(0.00001), check_build_task)

