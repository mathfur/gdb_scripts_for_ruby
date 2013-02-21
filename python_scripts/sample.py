import gdb

#=========================== helper module
node_types = [
  ('NODE_METHOD', []),
  ('NODE_FBODY', [1]),
  ('NODE_CFUNC', [1, 2, 3]),
  ('NODE_SCOPE', [1, 2, 3]),
  ('NODE_BLOCK', [1, 2, 3]),
  ('NODE_IF', [1, 2, 3]),
  ('NODE_CASE', [1, 2, 3]),
  ('NODE_WHEN', [1, 2, 3]),
  ('NODE_OPT_N', [2]),
  ('NODE_WHILE', [1, 2, 3]),
  ('NODE_UNTIL', [1, 2, 3]),
  ('NODE_ITER', [1, 2, 3]),
  ('NODE_FOR', [1, 2, 3]),
  ('NODE_BREAK', [1, 2, 3]),
  ('NODE_NEXT', [1, 2, 3]),
  ('NODE_REDO', [1]),
  ('NODE_RETRY', [1, 2, 3]),
  ('NODE_BEGIN', [2]),
  ('NODE_RESCUE', [1, 2, 3]),
  ('NODE_RESBODY', [1, 2, 3]),
  ('NODE_ENSURE', [1, 2, 3]),
  ('NODE_AND', [1, 2, 3]),
  ('NODE_OR', [1, 2, 3]),
  ('NODE_NOT', [1, 2, 3]),
  ('NODE_MASGN', [1, 2, 3]),
  ('NODE_LASGN', [2]),
  ('NODE_DASGN', [1, 2, 3]),
  ('NODE_DASGN_CURR', [1, 2, 3]),
  ('NODE_GASGN', [1, 2, 3]),
  ('NODE_IASGN', [1, 2, 3]),
  ('NODE_CDECL', [1]),
  ('NODE_CVASGN', [1, 2, 3]),
  ('NODE_CVDECL', [1, 2, 3]),
  ('NODE_OP_ASGN1', [1, 2, 3]),
  ('NODE_OP_ASGN2', [1, 2, 3]),
  ('NODE_OP_ASGN_AND', [1, 2, 3]),
  ('NODE_OP_ASGN_OR', []),
  ('NODE_CALL', [1]),
  ('NODE_FCALL', [3]),
  ('NODE_VCALL', [2]),
  ('NODE_SUPER', [1, 2, 3]),
  ('NODE_ZSUPER', [1, 2, 3]),
  ('NODE_ARRAY', [1]),
  ('NODE_ZARRAY', []),
  ('NODE_HASH', [1, 2, 3]),
  ('NODE_RETURN', [1, 2, 3]),
  ('NODE_YIELD', [1]),
  ('NODE_LVAR', [3]),
  ('NODE_DVAR', []),
  ('NODE_GVAR', [3]),
  ('NODE_IVAR', []),
  ('NODE_CONST', []),
  ('NODE_CVAR', []),
  ('NODE_NTH_REF', [1, 2, 3]),
  ('NODE_BACK_REF', [1, 2, 3]),
  ('NODE_MATCH', [1]),
  ('NODE_MATCH2', []),
  ('NODE_MATCH3', [1, 2, 3]),
  ('NODE_LIT', []),
  ('NODE_STR', [1]),
  ('NODE_DSTR', [1, 2, 3]),
  ('NODE_XSTR', [1, 2, 3]),
  ('NODE_DXSTR', [1, 2, 3]),
  ('NODE_EVSTR', [1, 2, 3]),
  ('NODE_DREGX', [1, 2, 3]),
  ('NODE_DREGX_ONCE', [1, 2, 3]),
  ('NODE_ARGS', [1, 2, 3]),
  ('NODE_ARGSCAT', [1, 2, 3]),
  ('NODE_ARGSPUSH', [1, 2, 3]),
  ('NODE_SPLAT', [1, 2, 3]),
  ('NODE_TO_ARY', [1, 2, 3]),
  ('NODE_SVALUE', [1, 2, 3]),
  ('NODE_BLOCK_ARG', [1, 2, 3]),
  ('NODE_BLOCK_PASS', [1, 2, 3]),
  ('NODE_DEFN', [1, 2, 3]),
  ('NODE_DEFS', [1, 2, 3]),
  ('NODE_ALIAS', [1, 2, 3]),
  ('NODE_VALIAS', [1, 2, 3]),
  ('NODE_UNDEF', [1, 2, 3]),
  ('NODE_CLASS', [1, 2, 3]),
  ('NODE_MODULE', [1, 2, 3]),
  ('NODE_SCLASS', [1, 2, 3]),
  ('NODE_COLON2', [1, 2, 3]),
  ('NODE_COLON3', [1, 2, 3]),
  ('NODE_CREF', [1, 2, 3]),
  ('NODE_DOT2', [1, 2, 3]),
  ('NODE_DOT3', [1, 2, 3]),
  ('NODE_FLIP2', [1, 2, 3]),
  ('NODE_FLIP3', [2]),
  ('NODE_ATTRSET', [1, 2, 3]),
  ('NODE_SELF', [1, 2, 3]),
  ('NODE_NIL', [1, 2, 3]),
  ('NODE_TRUE', [1, 2, 3]),
  ('NODE_FALSE', [1, 2, 3]),
  ('NODE_DEFINED', [1, 2, 3]),
  ('NODE_NEWLINE', [3]),
  ('NODE_POSTEXE', [1, 2, 3]),
  ('NODE_ALLOCA', [1, 2, 3]),
  ('NODE_DMETHOD', [1, 2, 3]),
  ('NODE_BMETHOD', [2]),
  ('NODE_MEMO', [1, 2, 3]),
  ('NODE_IFUNC', [1, 2, 3]),
  ('NODE_DSYM', [1, 2, 3]),
  ('NODE_ATTRASGN', [1, 2, 3]),
  ('NODE_LAST', [1, 2, 3])
]

def get_node_type(node):
  return map((lambda e: e[0]), node_types)[get_node_type_integer(node)]

def get_node_type_integer(node):
  return (int(node['flags']) >> 11) & 0xFF

# under construction
# call by:
#  node = gdb.parse_and_eval('n')
#  print_node(node, 0)
def print_node(node, indent):
  node_type = get_node_type(node)
  print ' '*indent + ">>>%(node)d: %(name)s" % {'node': (int(node['flags']) >> 11) & 0xFF, 'name': node_type}
  #print ' '*indent + node_type
  for i in filter((lambda e: e[0] == node_type), node_types)[0][1]:
    print ' '*indent + ">>>>> %d" % i
    child = node['u%d' % i]['node']
    print_node(child, indent+1)

def get_class_name(value):
  if have_valid_flags(value):
    basic = value.cast(gdb.lookup_type('struct RBasic').pointer())
    return gdb.parse_and_eval("rb_class_path(%d)" % basic['klass']).cast(gdb.lookup_type('struct RString').pointer())['ptr'].string()

def get_ruby_object_type(value):
  if have_valid_flags(value):
    return value.cast(gdb.lookup_type('struct RBasic').pointer())['flags'] & 0x3f

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
  return not (is_bool(value) or is_symbol(value) or is_integer(value))

def inspect_value(value):
  if have_valid_klass(value):
    klass = get_class_name(value)
    if klass == 'String':
      return inspect_string(value)
    else:
      return "(NA klass)"
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
  flags = value.cast(gdb.lookup_type('struct RBasic').pointer())['flags']
  elts_shared_flag = (flags >> 13) & 0x01
  if(elts_shared_flag == 1):
    return inspect_string(value.cast(gdb.lookup_type('struct RString').pointer())['aux']['shared'])
  else:
    return "'%s'" % value.cast(gdb.lookup_type('struct RString').pointer())['ptr'].string()

def inspect_symbol(value):
  return ":%s" % callc('rb_id2name', (value >> 8)).string()

def inspect_integer(value):
  return (value >> 1)

def inspect_bool(value):
  if is_true(value):
    return 'true'
  elif is_false(value):
    return 'false'
  elif is_nil(value):
    return 'nil'
  else:
    return '(NA)'

# == more abstract
def callc(method_name, args):
  cmd = "%(method_name)s(%(args)s)" % {'method_name': method_name, 'args': str(args)}
  return gdb.parse_and_eval(cmd)
