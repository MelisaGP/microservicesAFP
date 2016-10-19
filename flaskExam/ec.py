from subprocess import Popen, PIPE

def create_file(filename, content):
  result1 = Popen(["touch",'/home/filesystem_user/'+filename], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  log = open('/home/filesystem_user/'+filename, 'w')
  log.write(content)
  log.flush()
  return True

def get_all_files():
  result1 = Popen(["ls","/home/filesystem_user","-p"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  result2 = Popen(["grep", "-v", "/"], stdin=result1.stdout, stdout=PIPE, stderr=PIPE)
  return result2.communicate()[0].split('\n')

def get_recent_files():
  result1 = Popen(["ls","/home/filesystem_user","-Art"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  result2 = Popen(["tail", "-n", "2"], stdin=result1.stdout, stdout=PIPE, stderr=PIPE)
  return result2.communicate()[0].split('\n')

def remove_one_file(file):
  process = Popen(["rm", "/home/filesystem_user/"+file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  process.wait()
  return True
