from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from curses import use_default_colors
from email.policy import default
import os
import re
import glob
import subprocess
from enum import Enum
from fbp.parser import *
from threading import Thread

def cwd(s):
  print(s)
  return os.system(s)

class BuilderContext:
  class OverwriteProtector(Enum):
    FolderCopy = 0
    NameMangle = 1

  def __init__(self):
    self.target = ''
    self.script_path = ''
    self.script = ''

    # flags
    self.fastmode = False
    self.use_glob = False
    self.no_overwrite = BuilderContext.OverwriteProtector.FolderCopy

    # source file flags
    self.src_flags = defaultdict(str)

    # directories
    self.include  = [ ]
    self.source   = [ ]
    self.object_outdir  = 'build'
    self.object_subdir  = [ ]

    # compilers
    self.compilers = { }

    # files
    self.src_files = [ ]
    self.obj_files = [ ]

    self.extensions = defaultdict(list)

class Builder:
  class InvalidArgument(Exception):
    pass

  class ElementNotFound(Exception):
    def __init__(self, name):
      self.name = name

  def __init__(self):
    self.target = ''
    self.script = ''
    self.script_path = ''
    self.context = 0
    self.ndlist = [ ]
    self.argv = [ ]
    self.updated = False
    self.errflag = False

    self.f_clean = False
    self.f_debug = False
    self.f_re = False

  # ==== Parse arguments passed to application ====
  def parse_argv(self, argv) -> bool:
    i = 1

    try:
      while i < len(argv):
        arg = argv[i]

        if arg.startswith('-'):
          arg = arg[1:]

          if arg == 'fast':
            self.context.fastmode = True
            i += 1
          elif arg == 'clean':
            self.f_clean = True
            i += 1
          elif arg == 'debug':
            self.f_debug = True
            i += 1
          elif arg == 're':
            self.f_re = True
            i += 1
          elif arg == 'C':
            os.chdir(d := argv[i + 1])
            print(f'entered in directory "{d}"')
            i += 2
          else:
            raise Builder.InvalidArgument()
        elif self.context == 0:
          self.target = arg
          self.script_path = arg + '.buildpy'

          with open(self.script_path, mode='r') as fs:
            self.script = ''.join(fs.readlines())

          self.script = self.script.strip()

          i += 1
        else:
          print('script file already specified')
          raise Builder.InvalidArgument()
    except:
      return False

    return True
  
  def get_elem(self, sym) -> str:
    li = sym.split('.')
    ret = -1

    for nd in self.ndlist:
      if nd.name == li[0]:
        ret = nd
        break

    if ret == -1:
      return 0

    for sym in li[1:]:
      found = False

      for nd in ret.value:
        if nd.name == sym:
          ret = nd
          found = True
          break

      if not found:
        return 0

    return ret

  def detect_lang(self, file):
    ext = file[file.rfind('.') + 1:]

    for key in self.context.extensions.keys():
      if ext in self.context.extensions[key]:
        return key

    return 0

  def mangle(self, path: str) -> str:
    return path[path.find('/') + 1:].replace('/', '@')

  def init_context(self) -> BuilderContext:
    ret = BuilderContext()

    ret.include = self.get_elem('folders.include').value
    ret.source = self.get_elem('folders.source').value

    # === builder flags ===
    if (e := self.get_elem('build.fast')) != 0:
      ret.fastmode = e.value == 'true'

    if (e := self.get_elem('build.use_glob')) != 0:
      ret.use_glob = e.value == 'true'

    # ===== Extensions =====
    for item in self.get_elem('build.extensions').value:
      ret.extensions[item.name].extend(item.value)

    # ===== Flags =====
    for item in self.get_elem('build.flags').value:
      ret.src_flags[item.name] = ' '.join(item.value)

    # ===== Compilers =====
    for clist in self.get_elem('build.compiler').value:
      ret.compilers[clist.name] = clist.value[0]

    # ===== Source files =====
    for fol in ret.source:
      for extkey in ret.extensions.keys():
        for ext in ret.extensions[extkey]:
          if ret.use_glob:
            ret.src_files.extend(glob.glob(f'{fol}/**/*.{ext}', recursive=True))
          else:
            ret.src_files.extend(glob.glob(f'{fol}/*.{ext}'))

    # ===== builder flag: no_overwrite =====
    if (e := self.get_elem('build.no_overwrite')) != 0:
      if e.value == 'copy_folder':
        ret.no_overwrite = BuilderContext.OverwriteProtector.FolderCopy

        for src in ret.src_files:
          if not (objdir := src[src.find('/') + 1 : src.rfind('/')]) in ret.object_subdir:
            ret.object_subdir.append(objdir)
      elif e.value == 'mangle':
        ret.no_overwrite = BuilderContext.OverwriteProtector.NameMangle

    return ret

  def to_output_path(self, file):
    if self.context.no_overwrite == BuilderContext.OverwriteProtector.FolderCopy:
      return self.context.object_outdir + file[file.find('/') : file.rfind('.')] + '.o'
    else:
      return self.context.object_outdir + '/' + file[file.find('/') + 1: file.rfind('.')].replace('/', '@') + '.o'

  def compile(self, file):
    lang = self.detect_lang(file)

    com = self.context.compilers[lang]
    destpath = self.to_output_path(file)
    dep_path = destpath[:-1] + 'd'

    flags = self.context.src_flags[lang]
    incl_flag = ' '.join(['-I' + x for x in self.context.include])

    cmdline = f'{com} -MP -MMD -MF {dep_path} {flags} {incl_flag} {file} -c -o {destpath}'
    need2do = False

    if (need2do := os.path.exists(destpath)):
      chklist = []

      if os.path.exists(dep_path):
        need2do = False

        with open(dep_path, encoding='utf-8') as fs:
          tmp = ''

          for i, l in enumerate(fs.readlines()):
            line = l.strip()

            if '\\' in line:
              line = line[:-1]

            if line == '':
              break
            elif i == 0:
              tmp += line[line.find(':') + 2:]
            else:
              tmp += line

          chklist.extend(re.split(' +', tmp))

        for chk in chklist:
          if os.path.getmtime(chk) > os.path.getmtime(destpath):
            need2do = True
            break
    else:
      need2do = True

    if need2do:
      self.updated = True
      print(file)
      return os.system(cmdline)

    return 0

  def link(self):
    line = f'{self.context.compilers["cpp"]} ' \
      f'{" ".join(self.context.obj_files)} ' \
      f'{" ".join(self.get_elem("build.flags.link").value) if not self.f_debug else ""} -pthread -o {self.target}'

    print('linking...')
    return os.system(line)

  def execute(self) -> int:
    self.context = self.init_context()

    self.context.obj_files = [self.to_output_path(x) for x in self.context.src_files]

    if self.f_clean or self.f_re:
      cwd(f'rm -rf {self.context.object_outdir} {self.target}')

      if self.f_clean:
        print('cleaned.')
        return 0

    # == create objects folder ==
    os.system(f'mkdir -p {self.context.object_outdir}')

    for sub in self.context.object_subdir:
      os.system(f'mkdir -p {self.context.object_outdir}/{sub}')

    # == Compile ==
    def comp(x):
      if self.errflag == True:
        return

      res = self.compile(x)

      if res != 0:
        self.errflag = True
    # ====

    if self.context.fastmode:
      with ThreadPoolExecutor() as executor:
        executor.map(comp, self.context.src_files)
    else:
      for src in self.context.src_files:
        comp(src)

    if self.errflag:
      print('failed to compile')
      return 1

    # == Link ==
    if self.updated:
      self.link()
    else:
      print('already up to date.')
    
    return 0

  def run(self, argv) -> int:
    try:
      self.argv = argv

      if not self.parse_argv(argv):
        print('invalid argument')
        return 1

      if self.script_path == '':
        print('no build-script file')
        return 1

      prs = Parser(self.script)

      self.ndlist = prs.parse()

      if self.f_debug:
        def repl(nd, s1, s2):
          if nd.kind == Node.Kind.Let:
            nd.value = [s2 if s1 in x else x for x in nd.value]
          elif nd.kind == Node.Kind.Properties:
            nd.value = [repl(x, s1, s2) for x in nd.value]

          return nd

        self.ndlist = [repl(nd, '-O', '-O0 -g') for nd in self.ndlist]

      return self.execute()
    except Parser.ParseError as e:
      print('parse error!')
    except Builder.ElementNotFound as e:
      print(f'element {e.name} is not defined!')

    return 1