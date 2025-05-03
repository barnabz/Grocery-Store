import os
import sys

def is_venv_active():
    return sys.prefix != sys.base_prefix

print("Current sys.executable:", sys.executable)
print("Is virtual environment active?", is_venv_active())
print("sys.prefix:", sys.prefix)
print("sys.path:")
for path in sys.path:
    print(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lapaulla_store.settings')

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
