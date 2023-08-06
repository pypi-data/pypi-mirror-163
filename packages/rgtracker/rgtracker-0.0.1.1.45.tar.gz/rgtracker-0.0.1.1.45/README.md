# Build Python project
change version in pyproject.toml
delete /dist files
python3 -m build

# Upload Python package
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*

# Update Local Python Package
pip install rgtracker==0.0.1.1.45

# Run RedisGears Jobs
python src/jobs/produce.py
python src/jobs/create_requirements.py

gears-cli run --host localhost --port 6379 src/jobs/bigbang.py REQUIREMENTS rgtracker==0.0.1.1.45 pandas

gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/rotate_pg_website.py REQUIREMENTS rgtracker==0.0.1.1.45 pandas
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/rotate_pg_section.py REQUIREMENTS rgtracker==0.0.1.1.45 pandas
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/rotate_pg_page.py REQUIREMENTS rgtracker==0.0.1.1.45 pandas

gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/rotate_ud_website.py REQUIREMENTS rgtracker==0.0.1.1.45 pandas
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/rotate_ud_section.py REQUIREMENTS rgtracker==0.0.1.1.45 pandas
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/rotate_ud_page.py REQUIREMENTS rgtracker==0.0.1.1.45 pandas

# Notes
https://stackoverflow.com/questions/22875651/how-to-apply-hyperloglog-to-a-timeseries-stream
https://redis.com/blog/7-redis-worst-practices/
https://redis.com/blog/streaming-analytics-with-probabilistic-data-structures/