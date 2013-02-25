Gdb Script for Ruby
===================
Python-gdb methods for debugging ruby.
 
Install
-------
You need the following.
 * python-enabled gdb ( If you use MAC, then the gdb might be needed codesign ).
 * debug-builded ruby ( 1.8.7 is checked only ).
 * git clone https://github.com/mathfur/gdb_scripts_for_ruby.git

If you want to debug foo.rb, then
```shell
gdb --ex 'source scripts/helper.py' --args ruby foo.rb
```

If you want to add more information to method missing, then
```
gdb) python enhance_method_missing()
gdb) run
```

License
-------
Copyright &copy; 2012 mathfur
Licensed under the [Apache License,  Version 2.0][Apache]
Distributed under the [MIT License][mit].
Dual licensed under the [MIT license][MIT] and [GPL license][GPL].
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php

[GPL]: http://www.gnu.org/licenses/gpl.html
