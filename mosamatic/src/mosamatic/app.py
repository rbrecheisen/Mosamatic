import os
import sys
import signal
import subprocess

from django.core.management import execute_from_command_line


def run_setup_tasks():
    app_path = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(app_path, 'backend')
    sys.path.append(app_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', '1')
    os.chdir(app_path)
    execute_from_command_line(['manage.py', 'makemigrations', 'app'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'create_admin_user'])
    execute_from_command_line(['manage.py', 'clear_logs'])


def run_waitress():
    proc = subprocess.Popen(['waitress-serve', '--listen=0.0.0.0:8000', 'backend.wsgi:application'])
    try:
        proc.wait()
    except KeyboardInterrupt:
        print('\nCaught CTRL + C, stopping server...')
        proc.send_signal(signal.SIGTERM)
        proc.wait()
    except subprocess.CalledProcessError as e:
        print(f'Waitress failed to start: {e}')
    finally:
        sys.exit(1)


def main():
    run_setup_tasks()
    run_waitress()


if __name__ == '__main__':
    main()

# import os
# import sys
# from django.core.management import execute_from_command_line
# def run_server():
#     appPath = os.path.join(os.path.abspath(__file__))
#     appPath = os.path.dirname(appPath)
#     appPath = os.path.join(appPath, 'backend')   
#     sys.path.append(appPath)  
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
#     os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', '1')    
#     os.chdir(appPath)
#     execute_from_command_line(['manage.py', 'makemigrations', 'app'])
#     execute_from_command_line(['manage.py', 'migrate'])
#     execute_from_command_line(['manage.py', 'create_admin_user'])
#     execute_from_command_line(['manage.py', 'clear_logs'])
#     execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
# def main():
#     run_server()