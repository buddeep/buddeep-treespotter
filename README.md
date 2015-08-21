# TreeSpotter

Spots street trees!

As requested by this poster on the C line of the NYC subway:

![we-demand-a-treecount](https://cloud.githubusercontent.com/assets/1735/9038769/e3cd927c-39c4-11e5-8cf7-21cbed6df11f.jpg)

[treescount.nycgovparks.org](https://treescount.nycgovparks.org/)

## Development

Please fork the repo and submit pull requests as needed.

The `data` directory holds scripts for pulling down datasets. The directory also
stores the actual datasets when fetched, but note that these should not be
committed into the repo. Use `.gitignore` files to avoid such issues.

The `models` directory holds Caffe model descriptions. It may also store trained
weights which should not be committed into the repo. Again, use `.gitignore`
files to avoid issues.

The `tools` directory contains subproject code in its subdirectories. Any new
code should exist in a subdirectory of the `tools` directory.

Please follow these coding style guides where relevant:

* [Python](http://google.github.io/styleguide/pyguide.html)
* [C++](http://google.github.io/styleguide/cppguide.html)
* [Shell](http://google.github.io/styleguide/shell.xml)
* [JavaScript](https://github.com/airbnb/javascript)
