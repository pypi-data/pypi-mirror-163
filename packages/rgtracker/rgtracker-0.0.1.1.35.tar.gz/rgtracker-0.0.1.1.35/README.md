# Build Python project
change version in pyproject.toml
delete /dist files
python3 -m build

# Upload Python package
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*

# Update Local Python Package
pip install rgtracker==0.0.1.1.35

# Run RedisGears Jobs
python src/jobs/produce.py 
python src/jobs/axiom.py 
gears-cli run --host localhost --port 6379 src/jobs/sandbox.py
gears-cli run --host localhost --port 6379 src/jobs/sandbox_website.py
gears-cli run --host localhost --port 6379 src/jobs/sandbox_section.py
gears-cli run --host localhost --port 6379 src/jobs/sandbox_page.py
gears-cli run --host localhost --port 6379 src/jobs/bigbang.py REQUIREMENTS rgtracker==0.0.1.1.35
gears-cli run --host localhost --port 6379 src/jobs/megastar.py REQUIREMENTS rgtracker==0.0.1.1.35 pandas
gears-cli run --host localhost --port 6379 src/jobs/megastorm.py REQUIREMENTS rgtracker==0.0.1.1.35 pandas
