define output_info_of_no_method_error
  # output method name
  echo >>[method_missing]
  output rb_id2name(id)
  echo \n
end

break method_missing
commands
  output_info_of_no_method_error
  continue
end

run
