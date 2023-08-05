# Build Python project
change version in pyproject.toml
delete /dist files
python3 -m build

# Upload Python package
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*

# Update Local Python Package
pip install rgtracker==0.0.1.1.39

# Run RedisGears Jobs
python src/jobs/produce.py 
python src/jobs/create_requirements.py 

gears-cli run --host localhost --port 6379 src/jobs/bigbang.py REQUIREMENTS rgtracker==0.0.1.1.39 pandas

gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/rotate_pg_website.py REQUIREMENTS rgtracker==0.0.1.1.39 pandas
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/rotate_pg_section.py REQUIREMENTS rgtracker==0.0.1.1.39 pandas
gears-cli run --host localhost --port 6379 src/jobs/rotate_pageviews/rotate_pg_page.py REQUIREMENTS rgtracker==0.0.1.1.39 pandas

gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/rotate_ud_website.py REQUIREMENTS rgtracker==0.0.1.1.39 pandas
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/rotate_ud_section.py REQUIREMENTS rgtracker==0.0.1.1.39 pandas
gears-cli run --host localhost --port 6379 src/jobs/rotate_unique_devices/rotate_ud_page.py REQUIREMENTS rgtracker==0.0.1.1.39 pandas