# rubyにアタッチして関数呼び出しごとにログを出力する

set $node_if = 5
set $node_call = 37
set $node_fcall = 38

set $rb_eval_again = 2979
set $rb_eval_finish = 4183
set $rb_eval_node_call__call_rb_eval = 3516
set $rb_eval_node_fcall2__call_rb_eval = 3531

def get_current_line
  set $current_line = ((ruby_current_node.flags >> 19) & 0x1FFF)
end

define output_method_name
  # 呼び出された関数名を出力
  output rb_id2name(mid)
  echo \n

  continue
end

break rb_call
commands
  output_method_name
end

continue
