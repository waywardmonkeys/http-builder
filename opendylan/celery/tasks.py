# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

from builder import DylanBuilder
from celery.task import task

@task
def dylan_builder(taskID, code):
  r = {}
  b = DylanBuilder(taskID, code)
  b.prepare()
  (timedOut, ret, out, err, conditions) = b.compile()
  r['compile-timedout'] = timedOut
  r['compile-exitcode'] = ret
  r['compile-out'] = out
  r['compile-err'] = err
  r['compile-warnings'] = conditions
  (timedOut, ret, out, err) = b.run()
  r['run-timedout'] = timedOut
  r['run-exitcode'] = ret
  r['run-out'] = out
  r['run-err'] = err
  return r

