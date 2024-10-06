.PHONY: venv setup install run migrate makemigrations shell test clean help all

# Python interpreter to use
PYTHON := python3

# Virtual environment directory
VENV := .venv

# Poetry executable
POETRY := poetry

# Activate virtual environment command
ifeq ($(OS),Windows_NT)
	VENV_ACTIVATE := $(VENV)/Scripts/activate.bat
else
	VENV_ACTIVATE := . $(VENV)/bin/activate
endif

# Django management command
MANAGE := $(POETRY) run python manage.py

# Default target
all: venv setup install migrate run

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)

# Set up the project environment
setup: venv
	@echo "Setting up the project environment..."
	@$(VENV_ACTIVATE) && $(PYTHON) -m pip install --upgrade pip setuptools wheel
	@$(VENV_ACTIVATE) && $(PYTHON) -m pip install poetry

# Install project dependencies
install: venv
	@echo "Installing project dependencies..."
	@$(VENV_ACTIVATE) && $(POETRY) install

# Run the Django development server
run: venv
	@echo "Running the Django development server..."
	@$(VENV_ACTIVATE) && $(MANAGE) runserver

# Run database migrations
migrate: venv
	@echo "Running database migrations..."
	@$(VENV_ACTIVATE) && $(MANAGE) migrate

# Create database migrations
makemigrations: venv
	@echo "Creating database migrations..."
	@$(VENV_ACTIVATE) && $(MANAGE) makemigrations

# Open Django shell
shell: venv
	@echo "Opening Django shell..."
	@$(VENV_ACTIVATE) && $(MANAGE) shell

# Run tests
test: venv
	@echo "Running tests..."
	@$(VENV_ACTIVATE) && $(MANAGE) test

# Clean up cached Python files and virtual environment
clean:
	@echo "Cleaning up cached Python files and virtual environment..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf $(VENV)

# Show help message
help:
	@echo "Available commands:"
	@echo "  make venv          - Create virtual environment"
	@echo "  make setup         - Set up the project environment"
	@echo "  make install       - Install project dependencies"
	@echo "  make run           - Run the Django development server"
	@echo "  make migrate       - Run database migrations"
	@echo "  make makemigrations - Create database migrations"
	@echo "  make shell         - Open Django shell"
	@echo "  make test          - Run tests"
	@echo "  make clean         - Clean up cached Python files and virtual environment"
	@echo "  make all           - Create venv, setup, install, migrate, and run the project"
	@echo "  make help          - Show this help message"