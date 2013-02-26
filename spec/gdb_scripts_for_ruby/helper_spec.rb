# -*- encoding: utf-8 -*-

require "spec_helper"

describe "helper.py" do
  describe '#get_class_name' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
obj = Object.new
klass = Class.new
pr = Proc.new { }
puts({}, "foo", obj, [], :foo, 1, nil, false, true, klass, pr)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  argc = gdb.parse_and_eval('argc')
  for i in range(argc):
    value = gdb.parse_and_eval("argv[%d]" % i)
    print get_class_name(value)
APPEND_STATEMENT

      results[0].should == "Hash"
      results[1].should == "String"
      results[2].should == "Object"
      results[3].should == "Array"
      results[4].should == "None"
      results[5].should == "None"
      results[6].should == "None"
      results[7].should == "None"
      results[8].should == "None"
      results[9].should =~ /^#<Class\b/
      results[10].should == "Proc"
      results.size.should == 11
    end
  end

  describe '#get_ruby_object_type' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
obj = Object.new
klass = Class.new
pr = Proc.new { }
puts({}, "foo", obj, [], :foo, 1, nil, false, true, klass, pr)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  argc = gdb.parse_and_eval('argc')
  for i in range(argc):
    value = gdb.parse_and_eval("argv[%d]" % i)
    print get_ruby_object_type(value)
APPEND_STATEMENT

      results[0].should == '11'
      results[1].should == '7'
      results[2].should == '2'
      results[3].should == '9'
      results[4].should == "None"
      results[5].should == "None"
      results[6].should == "None"
      results[7].should == "None"
      results[8].should == "None"
      results[9].should == '3'
      results[10].should == '34'
      results.size.should == 11
    end
  end

  describe '#inspect_value' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts('foo', :bar, 30, true, false, nil, [1, 2])
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  argc = gdb.parse_and_eval('argc')
  for i in range(argc):
    str = gdb.parse_and_eval("argv[%d]" % i)
    print inspect_value(str)
APPEND_STATEMENT

     results[0].should == "'foo'"
     results[1].should == ":bar"
     results[2].should == "30"
     results[3].should == "true"
     results[4].should == "false"
     results[5].should == "nil"
     results[6].should == "[1, 2]"
    end

    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts(135, nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  x = gdb.parse_and_eval("argv[0]")
  print inspect_value(x)
APPEND_STATEMENT

      results[0].should == "135"
    end
  end

  describe '#inspect_string' do
    it 'when ELTS_SHARED flag is false' do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
print('foo', nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  str = gdb.parse_and_eval("argv[0]")
  print inspect_string(str)
APPEND_STATEMENT

     results[0].should == "'foo'"
    end

    it 'when ELTS_SHARED flag is true' do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
9.times do |i|
  x = 'foo'
  p(x, nil)
end
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  str = gdb.parse_and_eval("argv[0]")
  print inspect_string(str)
APPEND_STATEMENT

     results[0].should == "'foo'"
    end
  end

  describe '#inspect_symbol' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts(:foo, nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  str = gdb.parse_and_eval("argv[0]")
  print inspect_symbol(str)
APPEND_STATEMENT

      results[0].should == ':foo'
    end
  end

  describe '#inspect_integer' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts(15, nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  num = gdb.parse_and_eval("argv[0]")
  print inspect_integer(num)
APPEND_STATEMENT

      results[0].should == '15'
    end
  end

  describe '#inspect_bool' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts(true, false, nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  argc = gdb.parse_and_eval('argc')
  for i in range(argc):
    str = gdb.parse_and_eval("argv[%d]" % i)
    print inspect_bool(str)
APPEND_STATEMENT

      results[0].should == 'true'
      results[1].should == 'false'
      results[2].should == 'nil'
    end
  end

  describe '#inspect_array' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts([:foo, 135, 'bar', nil, true, false], nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  x = gdb.parse_and_eval("argv[0]")
  print inspect_array(x)
APPEND_STATEMENT

      results[0].should == "[:foo, 135, 'bar', nil, true, false]"
    end

    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts([[12, 34], 56], nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  x = gdb.parse_and_eval("argv[0]")
  print inspect_array(x)
APPEND_STATEMENT

      results[0].should == "[[12, 34], 56]"
    end
  end

  describe '#have_valid_flags' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts(nil, 3, :foo, [], "foo", {},  nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  for i in range(6):
    x = gdb.parse_and_eval("argv[%d]" % i)
    print have_valid_flags(x)
APPEND_STATEMENT

      results[0].should == "False"
      results[1].should == "False"
      results[2].should == "False"
      results[3].should == "True"
      results[4].should == "True"
      results[5].should == "True"
    end
  end

  describe '#get_node_type' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py', :multiple => true)
if true
else
end
RB_SOURCE
break eval.c:2979
break eval.c:4183
BREAK_STATMENT
  node = gdb.parse_and_eval('node')
  print get_node_type(node)
APPEND_STATEMENT

      results.should be_include('NODE_NEWLINE')
      results.should be_include('NODE_TRUE')
      results.should be_include('NODE_IF')
    end

    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py', :multiple => true)
i = 0
while i < 3
  i += 1
  puts i
end
RB_SOURCE
break eval.c:2979
break eval.c:4183
BREAK_STATMENT
  node = gdb.parse_and_eval('node')
  print get_node_type(node)
APPEND_STATEMENT

      results.should be_include('NODE_NEWLINE')

      results.should be_include('NODE_WHILE')
      results.should be_include('NODE_BLOCK')

      results.should be_include('NODE_LIT')
      results.should be_include('NODE_LASGN')
      results.should be_include('NODE_LVAR')
      results.should be_include('NODE_CALL')
      results.should be_include('NODE_FCALL')
      results.length.should == 8
    end

    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py', :multiple => true)
class Foo
end
Foo.new
RB_SOURCE
break eval.c:2979
break eval.c:4183
BREAK_STATMENT
  node = gdb.parse_and_eval('node')
  print get_node_type(node)
APPEND_STATEMENT

      results.should be_include('NODE_NEWLINE')

      results.should be_include('NODE_CLASS')
      results.should be_include('NODE_BLOCK')

      results.should be_include('NODE_CONST')
      results.should be_include('NODE_CALL')
    end
  end

  describe '#enhance_method_missing' do
    specify do
      output = execute_plain(<<RB_SOURCE, <<BREAK_STATMENT, 'helper.py')
arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
arr3 = nil
p arr1.sort + arr2.sort + arr3.sort
RB_SOURCE
enhance_method_missing()
gdb.execute('run')
BREAK_STATMENT

      output.should =~ /type.*NODE_CALL/
    end
  end

  describe '#print_backtrace' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
def bar
  puts(1, 2)
end
def foo
  bar
end
foo
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  print_backtrace()
APPEND_STATEMENT

      results.should be_any{|line| line =~ /test_target\.rb:2:in `bar`$/}
      results.should be_any{|line| line =~ /test_target\.rb:5:in `foo`$/}
      results.should be_any{|line| line =~ /test_target.rb:7:$/}
    end
  end

  describe '#inspect_node' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py', :multiple => true)
puts(10)
RB_SOURCE
break eval.c:2979
break eval.c:4183
BREAK_STATMENT
  node = gdb.parse_and_eval('node')
  if get_node_type(node) == 'NODE_FCALL':
    pp = pprint.PrettyPrinter(2)
    pp.pprint(inspect_node(node))
APPEND_STATEMENT

      require "json"
      results = JSON.parse(results.join("\n").gsub(/u?'/){ '"' })
      results['u3']['node']['u1']['node']['u1']['value'].should == "10"
    end
  end

  describe '#get_node_by_xml' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py', :multiple => true)
if true
  puts(10)
else
  1 + 3
end
RB_SOURCE
break eval.c:2979
break eval.c:4183
BREAK_STATMENT
  node = gdb.parse_and_eval('node')
  if get_node_type(node) == 'NODE_FCALL':
    print get_node_by_xml(node)
APPEND_STATEMENT

      require "rexml/document"
      doc = REXML::Document.new results.join("\n")
      REXML::XPath.first(doc, "//type[text()='NODE_FCALL']").should be_true
      REXML::XPath.first(doc, "//type[text()='NODE_IF']").should be_false
      REXML::XPath.first(doc, "//type[text()='NODE_ARRAY']").should be_true
      REXML::XPath.first(doc, "//type[text()='NODE_LIT']").should be_true
      REXML::XPath.first(doc, "//node[@value='10']").should be_true
    end
  end

  describe '#observe_call' do
    specify do
      results = execute_plain(<<RB_SOURCE, <<BREAK_STATMENT, 'helper.py')
puts "123".to_i
{:x => 10, :y => 20}.merge({})
{:x => 10, :y => 20}.values_at(:x, :y)
{}.inspect
puts 123.to_s
RB_SOURCE
observe_call('Hash')
gdb.execute('run')
BREAK_STATMENT

      results = results.split(/\n/)
      results.find{|r| r =~ /to_i/}.should be_false
      results.find{|r| r =~ /merge/}.should be_true
      results.find{|r| r =~ /values_at.*:x.*:y/}.should be_true
      results.find{|r| r =~ /inspect\(\)/}.should be_true
      results.find{|r| r =~ /to_s/}.should be_false
    end
  end

  describe '#current_line' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
def bar
  puts(1, 2)
end
def foo
  bar
end
foo
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  print "current_line = %d;" % current_line()
APPEND_STATEMENT

      results.should be_include("current_line = 2;")
    end
  end

  describe '#current_fname' do
    specify do
      results = execute_with_break(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'helper.py')
puts(1, 2, 3)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  print "current_fname = %s;" % current_fname()
APPEND_STATEMENT

      results.should be_any{|line| line =~ /current_fname = .*test_target\.rb;/}
    end
  end

  def execute_with_break(src, break_statements, appending_src, python_fname, options={})
    break_statements = break_statements.split("\n").map do |break_stat|
      "gdb.execute('#{break_stat.strip}')"
    end.join("\n")

    breaked_python_src = <<-EOS
#{File.read("#{BASE_DIR}/scripts/#{python_fname}")}

def break_handler(event):
  print "APPENDING_SRC_RESULT_START"
#{appending_src}
  print "APPENDING_SRC_RESULT_END"
  gdb.execute('continue')

gdb.events.stop.connect(break_handler)
#{break_statements}
gdb.execute('run')
    EOS

    execute0(src, breaked_python_src, python_fname, options)
  end

  def execute_plain(src, break_statement, python_fname, options={})
    breaked_python_src = <<-EOS
#{File.read("#{BASE_DIR}/scripts/#{python_fname}")}

#{break_statement}
    EOS

    execute0(src, breaked_python_src, python_fname, options.merge(:all => true))
  end

  def execute0(src, breaked_python_src, python_fname, options={})
    target_fname = "#{BASE_DIR}/tmp/test_target.rb"
    python_script = "#{BASE_DIR}/tmp/test_target.py"
    open(target_fname, 'w'){|f| f.write src }
    open(python_script, 'w'){|f| f.write breaked_python_src }

    command = "gdb --ex 'source #{python_script}' --args ~/mybuild/usr/local/bin/ruby #{target_fname} 2>&1"

    test_output = []
    io = IO.popen(command, 'r')
    while line = io.gets
      test_output << line
      #puts line

      if line =~ /\[Inferior \d+ \(process \d+\) exit/
        break
      end
    end

    Process.kill('KILL', io.pid)
    io.close

    if options[:multiple]
      test_output.join.scan(/APPENDING_SRC_RESULT_START(.*?)APPENDING_SRC_RESULT_END/m).flatten.map(&:strip).sort.uniq
    elsif options[:all]
      test_output.join
    else
      (test_output.join[/APPENDING_SRC_RESULT_START(.*?)APPENDING_SRC_RESULT_END/m, 1] || '').strip.split(/\n/)
    end
  end
end
