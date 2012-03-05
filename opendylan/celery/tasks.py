# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

from builder import DylanBuilder
from celery.task import task

@task
def dylan_builder(taskID, code):
  b = DylanBuilder(taskID, code)
  b.prepare()
  b.compile()
  b.run()
  return {}

