# output method name at load

import gdb

def break_handler(event):
  print ">>[rb_load_file] "+gdb.parse_and_eval("fname").string()
  gdb.execute('continue')

gdb.events.stop.connect(break_handler)
gdb.Breakpoint("rb_load_file")
gdb.execute("run")
