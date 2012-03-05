# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

from builder import DylanBuilder
from celery.task import task

@task
def dylan_builder(taskID, code):
  r = {}
  b = DylanBuilder(taskID, code)
  b.prepare()
  (ret, out, err) = b.compile()
  r['compile-exitcode'] = ret
  r['compile-out'] = out
  r['compile-err'] = err
  (ret, out, err) = b.run()
  r['run-exitcode'] = ret
  r['run-out'] = out
  r['run-err'] = err
  return r

