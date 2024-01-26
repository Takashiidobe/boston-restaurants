all: boston_restaurants_sorted_by_rating.csv _template.html
	mkdir -p site && pandoc boston_restaurants_sorted_by_rating.csv -o site/index.html --template=_template.html
sort: boston_restaurants_sorted_by_rating.csv
	head -1 boston_restaurants_sorted_by_rating.csv > output.csv
	tail -n+2 boston_restaurants_sorted_by_rating.csv | sort --field-separator=',' -k 1,1 >> output.csv
	mv output.csv boston_restaurants_sorted_by_rating.csv
