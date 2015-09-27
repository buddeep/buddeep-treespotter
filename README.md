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


## Data Setup

Please request the URLs to our cached maps. Then paste them into the following config files:

    echo "PRIVATELY_SHARED_URL/2012.tar.gz" > data/config/2012_MAP_URL.txt
    echo "PRIVATELY_SHARED_URL/2014.tar.gz" > data/config/2014_MAP_URL.txt

Now let's fetch all raw data:

    cd data

    # Fetch NYC street tree census
    make fetch_trees

    # Fetch NYC satellite maps
    make fetch_cached_maps

    # Fetch NYC street data
    make fetch_streets

    cd ..

Now let's munge the data for training:

    # Install Python script dependencies
    # (alternatively use virtualenv if you don't want system level install)
    sudo pip install -r tools/street_finder/requirements.txt
    sudo pip install -r tools/cut_training_images/requirements.txt

    ## You may need add this to your env on OSX:
    # export DYLD_FALLBACK_LIBRARY_PATH=$DYLD_FALLBACK_LIBRARY_PATH:$(HOME)/lib:/usr/local/lib:/lib:/usr/lib

    # Create a CSV of streets from the source KML
    python tools/street_finder --streets_dir data/streets

    # Slice up positive and negative examples to train and test on
    python tools/cut_training_images --trees_dir data/trees --map_dir data/maps/2014 --streets_dir data/streets --slices_dir data/slices/2014_64px --slice_size=64

    # Create training list of images for caffe
    ./data/scripts/create_image_data_list.sh data/slices/2014_64px 0.7 > data/slices/2014_64px/train.txt
    ./data/scripts/shuffle_lines.sh data/slices/2014_64px/train.txt > data/slices/2014_64px/train_shuffled.txt

    # Create testing list of images for caffe
    ./data/scripts/create_image_data_list.sh data/slices/2014_64px -0.7 > data/slices/2014_64px/test.txt
    ./data/scripts/shuffle_lines.sh data/slices/2014_64px/test.txt > data/slices/2014_64px/test_shuffled.txt


## Training the Naive Model

A naive three-layer model is included as `naive_64px`

To train this model:

    ./models/scripts/train.sh naive_64px

After training, you can test it against the test data:

    ./models/scripts/test.sh naive_64px


## Training a Custom Model

If you don't want to start from scratch, simply copy the naive model:

    cp -rf models/naive_64px models/my_net

Now edit:

  * the `name` value in `models/my_net/train_test.prototxt`
  * the `name` value in `models/my_net/deploy.prototxt`
  * the `net` and `snapshot_prefix` paths in `models/my_net/solver.prototxt`

You can now tweak the architecture of the network in `models/my_net/train_test.prototxt` and solver hyperparamters in `models/my_net/solver.prototxt`.

To train your network:

    ./models/scripts/train.sh my_net

To test your network:
    ./models/scripts/test.sh my_net
