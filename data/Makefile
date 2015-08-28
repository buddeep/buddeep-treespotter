all: fetch_trees fetch_cached_maps fetch_streets

fetch_cached_maps:
	./scripts/fetch_all_cached_maps.sh

fetch_trees:
	./scripts/fetch_trees.sh

fetch_streets:
	./scripts/fetch_streets.sh
	
clean:
	rm -rf trees maps streets
