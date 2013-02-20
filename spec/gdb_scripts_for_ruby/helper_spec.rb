# -*- encoding: utf-8 -*-

require "spec_helper"

describe "helper.py" do
  describe '#get_class_name' do
    specify do
      results = execute(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'sample.py')
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
      results = execute(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'sample.py')
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

  describe '#print_value' do
    specify do
      results = execute(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'sample.py')
puts('foo', nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  str = gdb.parse_and_eval("argv[0]")
  print_value(str)
APPEND_STATEMENT

     results[0].should == "'foo'"
    end
  end

  describe '#print_string' do
    it 'when ELTS_SHARED flag is false' do
      results = execute(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'sample.py')
print('foo', nil)
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  str = gdb.parse_and_eval("argv[0]")
  print_string(str)
APPEND_STATEMENT

     results[0].should == "'foo'"
    end

    it 'when ELTS_SHARED flag is true' do
      results = execute(<<RB_SOURCE, <<BREAK_STATMENT, <<APPEND_STATEMENT, 'sample.py')
9.times do |i|
  x = 'foo'
  p(x, nil)
end
RB_SOURCE
break rb_call if argc > 1
BREAK_STATMENT
  str = gdb.parse_and_eval("argv[0]")
  print_string(str)
APPEND_STATEMENT

     results[0].should == "'foo'"
    end
  end

  def execute(src, break_statement, appending_src, python_fname)
    breaked_python_src = <<EOS
#{File.read("#{BASE_DIR}/python_scripts/#{python_fname}")}


def break_handler(event):
  print "APPENDING_SRC_RESULT_START"
#{appending_src}
  print "APPENDING_SRC_RESULT_END"
  gdb.execute('continue')

gdb.events.stop.connect(break_handler)
gdb.execute("#{break_statement.strip}")
gdb.execute('run')
EOS

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

    (test_output.join[/APPENDING_SRC_RESULT_START(.*?)APPENDING_SRC_RESULT_END/m, 1] || '').strip.split(/\n/)
  end
end
