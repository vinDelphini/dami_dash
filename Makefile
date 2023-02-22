export DJANGO_SETTINGS_MODULE=dami.settings

clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete

# pip-sync ensures that the virtual environment contains exactly 
# the packages specified in the requirements.txt file, with the correct versions.
install_requirements:
	@echo 'Installing requirements...'
	pip-sync requirements.txt


run-local:
	@echo 'Running local development'
	python3 manage.py runserver &

run-tests:
	@echo 'Checking for migrations'
	python3 manage.py makemigrations --dry-run --check
	pytest

check-servers:
	@echo 'checking all running servers'
	ps -ef | grep runserver

kill-servers:
	@echo 'killing all running servers'
	sudo pkill -f runserver
	ps -ef | grep runserver
