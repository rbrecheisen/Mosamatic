import os
import sys
import socket
import time
import subprocess
import webbrowser

from django.core.management import execute_from_command_line


# def wait_for_server(host, port, timeout=30):
#     start = time.time()
#     while time.time() - start < timeout:
#         try:
#             with socket.create_connection((host, port), timeout=1):
#                 return True
#         except OSError:
#             time.sleep(1)
#     return False


def run_server():
    appPath = os.path.join(os.path.abspath(__file__))
    appPath = os.path.dirname(appPath)
    appPath = os.path.join(appPath, 'backend')
    
    sys.path.append(appPath)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', '1')
    
    os.chdir(appPath)

    execute_from_command_line(['manage.py', 'makemigrations', 'app'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'create_admin_user'])
    execute_from_command_line(['manage.py', 'clear_logs'])
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

    # process = subprocess.Popen(
    #     [sys.executable, 'manage.py', 'runserver', 'localhost:8000'], 
    #     cwd=appPath, 
    #     stdout=subprocess.PIPE, 
    #     stderr=subprocess.PIPE
    # )
    # try:
    #     if wait_for_server('127.0.0.1', 8000):
    #         webbrowser.open('http://localhost:8000')
    #     else:
    #         print('Waiting for server timed out...')
    #     process.wait()
    # except KeyboardInterrupt:
    #     process.terminate()
    #     process.wait()


def main():
    run_server()