import gdb
import pprint

#=========================== helper module
available_children = [
  ('NODE_METHOD', []),
  ('NODE_FBODY', []),
  ('NODE_CFUNC', []),
  ('NODE_SCOPE', [['u3', 'node'], ['u2', 'value'], ['u1', 'tbl']]),
  ('NODE_BLOCK', [['u1', 'node'], ['u3', 'node']]),
  ('NODE_IF', [['u1', 'node'], ['u2', 'node'], ['u3', 'node']]),
  ('NODE_CASE', [['u1', 'node'], ['u2', 'node'], ['u3', 'node']]),
  ('NODE_WHEN', [['u1', 'node'], ['u2', 'node'], ['u3', 'node']]),
  ('NODE_OPT_N', [['u2', 'node']]),
  ('NODE_WHILE', [['u1', 'node'], ['u2', 'node'], ['u3', 'state']]),
  ('NODE_UNTIL', [['u1', 'node'], ['u2', 'node'], ['u3', 'state']]),
  ('NODE_ITER', [['u1', 'node'], ['u2', 'node'], ['u3', 'node']]),
  ('NODE_FOR', [['u1', 'node'], ['u2', 'node'], ['u3', 'node']]),
  ('NODE_BREAK', [['u1', 'node']]),
  ('NODE_NEXT', [['u1', 'node']]),
  ('NODE_REDO', []),
  ('NODE_RETRY', []),
  ('NODE_BEGIN', [['u2', 'node']]),
  ('NODE_RESCUE', [['u1', 'node'], ['u2', 'node'], ['u3', 'node']]),
  ('NODE_RESBODY', []),
  ('NODE_ENSURE', [['u1', 'node'], ['u3', 'node']]),
  ('NODE_AND', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_OR', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_NOT', [['u2', 'node']]),
  ('NODE_MASGN', [['u2', 'node']]),
  ('NODE_LASGN', [['u2', 'node'], ['u3', 'cnt']]),
  ('NODE_DASGN', [['u2', 'node'], ['u1', 'id']]),
  ('NODE_DASGN_CURR', [['u2', 'node'], ['u1', 'id']]),
  ('NODE_GASGN', [['u2', 'node'], ['u3', 'entry']]),
  ('NODE_IASGN', [['u2', 'node'], ['u1', 'id']]),
  ('NODE_CDECL', [['u2', 'node'], ['u3', 'node']]),
  ('NODE_CVASGN', [['u2', 'node'], ['u1', 'id']]),
  ('NODE_CVDECL', [['u2', 'node'], ['u1', 'id']]),
  ('NODE_OP_ASGN1', [['u1', 'node'], ['u3', 'node'], ['u2', 'id']]),
  ('NODE_OP_ASGN2', [['u1', 'node'], ['u2', 'node'], ['u3', 'node'], ['u3', 'id'], ['u2', 'id']]),
  ('NODE_OP_ASGN_AND', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_OP_ASGN_OR', [['u1', 'node'], ['u2', 'node'], ['u3', 'id']]),
  ('NODE_CALL', [['u1', 'node'], ['u3', 'node'], ['u2', 'id']]),
  ('NODE_FCALL', [['u3', 'node'], ['u2', 'id']]),
  ('NODE_VCALL', [['u2', 'id']]),
  ('NODE_SUPER', [['u3', 'node']]),
  ('NODE_ZSUPER', [['u3', 'node']]),
  ('NODE_ARRAY', [['u1', 'node'], ['u3', 'node'], ['u2', 'argc']]),
  ('NODE_ZARRAY', []),
  ('NODE_HASH', [['u1', 'node']]),
  ('NODE_RETURN', [['u1', 'node']]),
  ('NODE_YIELD', [['u1', 'node'], ['u3', 'state']]),
  ('NODE_LVAR', [['u3', 'cnt']]),
  ('NODE_DVAR', [['u1', 'id']]),
  ('NODE_GVAR', [['u3', 'entry']]),
  ('NODE_IVAR', [['u1', 'id']]),
  ('NODE_CONST', [['u1', 'id']]),
  ('NODE_CVAR', [['u1', 'id']]),
  ('NODE_NTH_REF', [['u2', 'argc']]),
  ('NODE_BACK_REF', [['u2', 'argc']]),
  ('NODE_MATCH', [['u1', 'value']]),
  ('NODE_MATCH2', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_MATCH3', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_LIT', [['u1', 'value']]),
  ('NODE_STR', [['u1', 'value']]),
  ('NODE_DSTR', []),
  ('NODE_XSTR', [['u1', 'value']]),
  ('NODE_DXSTR', []),
  ('NODE_EVSTR', [['u2', 'node']]),
  ('NODE_DREGX', []),
  ('NODE_DREGX_ONCE', []),
  ('NODE_ARGS', []),
  ('NODE_ARGSCAT', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_ARGSPUSH', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_SPLAT', [['u1', 'node']]),
  ('NODE_TO_ARY', [['u1', 'node']]),
  ('NODE_SVALUE', [['u1', 'node']]),
  ('NODE_BLOCK_ARG', [['u3', 'cnt']]),
  ('NODE_BLOCK_PASS', []),
  ('NODE_DEFN', [['u3', 'node'], ['u3', 'cnt'], ['u2', 'id']]),
  ('NODE_DEFS', [['u1', 'node'], ['u3', 'node'], ['u1', 'id']]),
  ('NODE_ALIAS', []),
  ('NODE_VALIAS', []),
  ('NODE_UNDEF', []),
  ('NODE_CLASS', [['u1', 'node'], ['u3', 'node'], ['u2', 'id']]),
  ('NODE_MODULE', [['u1', 'node']]),
  ('NODE_SCLASS', [['u1', 'node']]),
  ('NODE_COLON2', [['u1', 'node'], ['u2', 'id']]),
  ('NODE_COLON3', [['u2', 'id']]),
  ('NODE_CREF', []),
  ('NODE_DOT2', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_DOT3', [['u1', 'node'], ['u2', 'node']]),
  ('NODE_FLIP2', [['u1', 'node'], ['u2', 'node'], ['u3', 'cnt']]),
  ('NODE_FLIP3', [['u1', 'node'], ['u2', 'node'], ['u3', 'cnt']]),
  ('NODE_ATTRSET', []),
  ('NODE_SELF', []),
  ('NODE_NIL', []),
  ('NODE_TRUE', []),
  ('NODE_FALSE', []),
  ('NODE_DEFINED', [['u1', 'node']]),
  ('NODE_NEWLINE', [['u3', 'node']]),
  ('NODE_POSTEXE', []),
  ('NODE_ALLOCA', []),
  ('NODE_DMETHOD', []),
  ('NODE_BMETHOD', []),
  ('NODE_MEMO', []),
  ('NODE_IFUNC', []),
  ('NODE_DSYM', [['u1', 'value'], ['u2', 'id']]),
  ('NODE_ATTRASGN', [['u1', 'node'], ['u3', 'node'], ['u2', 'id']]),
  ('NODE_LAST', []),
]

def get_node_type(node):
  if node:
    return map((lambda e: e[0]), available_children)[get_node_type_integer(node)]
  else:
    return 'None'

def get_node_type_integer(node):
  if node:
    return (int(node['flags']) >> 11) & 0xFF
  else:
    return None

def find(elem, whole):
  arr = filter((lambda t: t[0] == elem), whole)
  if arr:
    return arr[0][1]
  else:
    return []

def inspect_node(node):
  node_type = get_node_type(node)
  result = {'type': node_type, 'u1': {},  'u2': {}, 'u3': {}}
  for key, category in find(node_type, available_children):
    try:
      if category == 'value': r = inspect_value(node[key][category])
      elif category == 'node': r = inspect_node(node[key][category])
      elif category == 'id': r = id2name(node[key][category])
      elif category == 'argc': r = str(node[key][category])
      elif category == 'entry': r = "(entry)"
      elif category == 'cnt':
        if node_type == 'NODE_LVAR' or node_type == 'NODE_LASGN' or node_type == 'NODE_BLOCK_ARG':
          r = gdb.parse_and_eval("rb_id2name(ruby_scope.local_tbl[%d])" % node[key][category]).string()
        else:
          r = str(node[key][category])
      elif category == 'tbl': r = "(tbl)"
      elif category == 'cfunc': r = "(cfunc)"
      elif category == 'state': r = str(node[key][category])
      else: r = '(None)'
    except gdb.MemoryError, gdb.error:
      r = '(EREOR)'
    result[key][category] = r
  return result

def get_class_name(value):
  if have_valid_flags(value):
    basic = cast(value, 'struct RBasic', True)
    if (basic['flags'] & 0x3F == t_node):
      return '(NODE)'
    else:
      return cast(gdb.parse_and_eval("rb_class_path(%d)" % basic['klass']), 'struct RString', True)['ptr'].string()

def get_ruby_object_type(value):
  if have_valid_flags(value):
    return cast(value, 'struct RBasic', True)['flags'] & 0x3f

def have_valid_klass(value):
  return get_ruby_object_type(value)

t_none = 0x00
t_nil = 0x01
t_object = 0x02
t_class = 0x03
t_iclass = 0x04
t_module = 0x05
t_float = 0x06
t_string = 0x07
t_regexp = 0x08
t_array = 0x09
t_fixnum = 0x0a
t_hash = 0x0b
t_struct = 0x0c
t_bignum = 0x0d
t_file = 0x0e
t_true = 0x20
t_false = 0x21
t_data = 0x22
t_match = 0x23
t_symbol = 0x24
t_node = 0x3f

types_with_klass = [t_none, t_nil, t_object, t_class, t_iclass, t_module,
    t_float, t_string, t_regexp, t_array, t_fixnum, t_hash, t_struct,
    t_bignum, t_file, t_true, t_false, t_data, t_match, t_symbol]

def is_integer(value):
  return ((value % 2) == 1)

def is_symbol(value):
  return ((value & 0xFF) == 0x0E)

def is_true(value):
  return (value == 2)

def is_false(value):
  return (value == 0)

def is_nil(value):
  return (value == 4)

def is_bool(value):
  return (is_true(value) or is_false(value) or is_nil(value))

def have_valid_flags(value):
  value = int(cast(value, 'int'))
  return not (is_bool(value) or is_symbol(value) or is_integer(value))

def inspect_value(value):
  if have_valid_klass(value):
    klass = get_class_name(value)
    if klass == 'String':
      return inspect_string(value)
    elif klass == 'Array':
      return inspect_array(value)
    else:
      return "(NA klass: %s)" % klass
  else:
    if is_integer(value):
      return inspect_integer(value)
    elif is_symbol(value):
      return inspect_symbol(value)
    elif is_bool(value):
      return inspect_bool(value)
    else:
      return "(NA not klass)"

def inspect_string(value):
  flags = cast(value, 'struct RBasic', True)['flags']
  elts_shared_flag = (flags >> 13) & 0x01
  if(elts_shared_flag == 1):
    return inspect_string(cast(value, 'struct RString', True)['aux']['shared'])
  else:
    return "'%s'" % cast(value, 'struct RString', True)['ptr'].string()

def inspect_symbol(value):
  return ":%s" % callc('rb_id2name', (value >> 8)).string()

def inspect_integer(value):
  return str(value >> 1)

def inspect_bool(value):
  if is_true(value):
    return 'true'
  elif is_false(value):
    return 'false'
  elif is_nil(value):
    return 'nil'
  else:
    return '(NA)'

def inspect_array(value):
  arr = cast(value, 'struct RArray', True)
  length = int(arr['len'])
  return '[' + ', '.join(map((lambda i: inspect_value(arr['ptr'][i])), range(length))) + ']'

def enhance_method_missing():
  def break_handler(event):
    pp = pprint.PrettyPrinter(2)
    while (gdb.selected_frame().name() != 'rb_eval'):
      gdb.execute('up')
    node = gdb.parse_and_eval('node')
    pp.pprint(inspect_node(node))
    gdb.execute('continue')
  gdb.events.stop.connect(break_handler)
  gdb.execute('break rb_method_missing')

def observe_call(klass_name):
  def handler(event):
    recv = gdb.parse_and_eval('recv')
    mid  = gdb.parse_and_eval('mid')
    argc = gdb.parse_and_eval('argc')
    argv = gdb.parse_and_eval('argv')
    if get_class_name(recv) == klass_name:
      args = map((lambda i: inspect_value(argv[i])), range(int(argc)))
      print "%s#%s(%s)" % (inspect_value(recv), id2name(mid), ', '.join(args))
    gdb.execute('continue')
  gdb.events.stop.connect(handler)
  gdb.execute('break rb_call')

# == more abstract
def callc(method_name, args):
  cmd = "%(method_name)s(%(args)s)" % {'method_name': method_name, 'args': str(args)}
  return gdb.parse_and_eval(cmd)

def cast(value, typ, pointer=False):
  if pointer:
    return value.cast(gdb.lookup_type(typ).pointer())
  else:
    return value.cast(gdb.lookup_type(typ))

def parse(gdb_string):
  return gdb.parse_and_eval(gdb_string)

def id2name(id_):
  return gdb.parse_and_eval("rb_id2name(%s)" % str(id_)).string()
