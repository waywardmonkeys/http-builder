# Copyright (c) 2012, Dylan Hackers.
# See License.txt for details.

import fcntl, os, subprocess, time
from textwrap import dedent

TIMEOUT = 10

LID_TEMPLATE = dedent("""\
  library: %(taskID)s
  executable: %(taskID)s
  files: library
         code
  """)

LIBRARY_TEMPLATE = dedent("""\
  module: dylan-user
  
  define library %(taskID)s
    use common-dylan;
    use io;
  end library;
  
  define module %(taskID)s
    use common-dylan;
    use format-out;
    use standard-io;
    use streams;
  end module;
  """)

DYLAN_TEMPLATE = dedent("""\
  module: %(taskID)s
  
  %(code)s
  """)

def writeToFile(fileName, data):
  f = open(fileName, 'w')
  f.write(data)
  f.close()

def makeNonBlocking(f):
  fd = f.fileno()
  fl = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

def safeRead(f):
  try:
    return f.read()
  except:
    return ''

class DylanBuilder(object):
  def __init__(self, taskID, code):
    self.directoryName = str(taskID)
    self.baseName = str(taskID)
    self.lidFileName = os.path.join(self.directoryName, self.baseName + '.lid')
    self.libraryFileName = os.path.join(self.directoryName, 'library.dylan')
    self.dylanFileName = os.path.join(self.directoryName, 'code.dylan')
    self.params = {
      'taskID': taskID,
      'code': code
    }

  def prepare(self):
    os.mkdir(self.directoryName)
    writeToFile(self.lidFileName, LID_TEMPLATE % self.params)
    writeToFile(self.libraryFileName, LIBRARY_TEMPLATE % self.params)
    writeToFile(self.dylanFileName, DYLAN_TEMPLATE % self.params)

  def compile(self):
    (ret, stdout, stderr) = self.runWithTimeout(TIMEOUT, ["/opt/opendylan-2011.1/bin/dylan-compiler", "-build", self.lidFileName])
    writeToFile(os.path.join(self.directoryName, 'compile-out.txt'), stdout)
    writeToFile(os.path.join(self.directoryName, 'compile-err.txt'), stderr)
    return (ret, stdout, stderr)

  def run(self):
    (ret, stdout, stderr) = self.runWithTimeout(TIMEOUT, [os.path.join("_build", "bin", self.baseName)])
    writeToFile(os.path.join(self.directoryName, 'run-out.txt'), stdout)
    writeToFile(os.path.join(self.directoryName, 'run-err.txt'), stderr)
    return (ret, stdout, stderr)

  def runWithTimeout(self, timeout, args):
    beginTime = time.time()
    elapsedTime = 0

    stdout = ''
    stderr = ''

    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    makeNonBlocking(p.stdout)
    makeNonBlocking(p.stderr)

    while p.poll() is None and elapsedTime < timeout:
      time.sleep(0.1)
      elapsedTime = time.time() - beginTime
      stdout += safeRead(p.stdout)
      stderr += safeRead(p.stderr)

    if elapsedTime >= timeout:
      p.kill()

    return (p.returncode, stdout, stderr)

