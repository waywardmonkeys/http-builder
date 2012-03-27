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
    use system;
    use collections;
  end library;
  
  define module %(taskID)s
    use common-dylan,
      exclude: { format-to-string };
    use transcendentals;
    use simple-random;
    use machine-words;
  
    use date;
  
    use streams;
    use standard-io;
    use print;
    use format;
    use format-out;
  
    use bit-vector;
    use bit-set;
    use byte-vector;
    use collectors;
    use set;
    use table-extensions;
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
    (timeout, ret, stdout, stderr) = self.runWithTimeout(TIMEOUT, ["/opt/opendylan-2011.1/bin/dylan-compiler", "-build", self.lidFileName])
    conditionLog = os.path.join('_build', 'build', self.baseName, self.baseName + '.log')
    writeToFile(os.path.join(self.directoryName, 'compile-out.txt'), stdout)
    writeToFile(os.path.join(self.directoryName, 'compile-err.txt'), stderr)
    conditions = parse_build_log(conditionLog)
    return (timeout, ret, stdout, stderr, conditions)

  def run(self):
    (timeout, ret, stdout, stderr) = self.runWithTimeout(TIMEOUT, [os.path.join("_build", "bin", self.baseName)])
    writeToFile(os.path.join(self.directoryName, 'run-out.txt'), stdout)
    writeToFile(os.path.join(self.directoryName, 'run-err.txt'), stderr)
    return (timeout, ret, stdout, stderr)

  def runWithTimeout(self, timeout, args):
    beginTime = time.time()
    elapsedTime = 0
    timedOut = False

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
      timedOut = True

    return (timedOut, p.returncode, stdout, stderr)

def parse_build_log(filename):
  STARTING = 0
  DESCRIPTION = 1
  CODE = 2
  conditions = []
  current_condition = {'description': ''}
  state = STARTING
  try:
    f = open(filename, 'r')
  except:
    return []
  for line in f:
    line = line.strip('\n')
    if line.startswith('//'):
      continue
    if line == '':
      if state == DESCRIPTION:
        current_condition['code'] = []
        state = CODE
      elif state == CODE:
        conditions.append(current_condition)
        current_condition = {'description': ''}
        state = DESCRIPTION
      else:
        state = DESCRIPTION
    elif state == DESCRIPTION:
      current_condition['description'] += line
    elif state == CODE:
      current_condition['code'].append(line)
  return conditions

