define output_method_name
  output rb_id2name(mid)
  echo ,
  output/t recv
  echo ,
  output/t klass
  echo ,
  output argc
  echo \n

  continue
end

break rb_call
commands
  output_method_name
end

continue
