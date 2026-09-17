import os
import re

def test_required_files_exist():
    assert os.path.exists('agent/config.py')
    assert os.path.exists('requirements.txt')
    assert os.path.exists('.gitignore')
    assert os.path.exists('.env.example')
    assert os.path.exists('README.md')

def test_gitignore_contains_env():
    with open('.gitignore', 'r') as f:
        content = f.read()
    assert '.env' in content

def test_config_imports_without_error():
    # Attempting to import should run validate_config()
    import agent.config
    assert agent.config.COMPOSIO_API_KEY is not None

def test_requirements_pinned():
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                assert '==' in line or '>=' not in line, f"Requirement {line} is not properly pinned"

def test_readme_sections():
    with open('README.md', 'r') as f:
        content = f.read()
    assert 'Overview' in content
    assert 'Architecture' in content
    assert 'Setup' in content
