run-dev:
	PROFILE=dev 
	uv run -m aerosync.aerosync

build:
	pyinstaller --onefile aerosync/aerosync.py

sqllite:
	sqlite3 ~/.aerosync/aerosync.db
