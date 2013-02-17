# output current backtrace

import gdb

def line_num(node):
  return ((node['flags'] >> 19) & 0xFFF)

def print_ruby_frame(origin_frame):
  if origin_frame['prev'] != 0 and origin_frame['prev']['last_func'] != 0:
    caller_info = {
        'fname': origin_frame['node']['nd_file'].string(),
        'method_name': gdb.parse_and_eval("rb_id2name(%d)" % origin_frame['prev']['last_func']).string(),
        'num': line_num(origin_frame['node'])
    }
    print "%(fname)s:%(num)d:in `%(method_name)s`" % caller_info
    print_ruby_frame(origin_frame['prev'])

def break_handler(event):
  print_ruby_frame(gdb.parse_and_eval("ruby_frame"))

gdb.events.stop.connect(break_handler)
break_point = gdb.Breakpoint('rb_eval')
break_point.condition = "((n.flags >> 19) & 0xFFF) == 12"
gdb.execute("run")
