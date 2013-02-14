# rubyの意味でload時にファイル名表示
# 多分C拡張ライブラリは表示されない

define notice_load_file
  echo >>[rb_load_file]
  output fname
  echo \n
end

break rb_load_file
commands
  notice_load_file
  continue
  echo >>>>
end

continue
