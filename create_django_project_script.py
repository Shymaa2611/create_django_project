import os
import subprocess
virtual_environment=input("Enter The Name of Virtual Environment ? ")
project=input("Enter The Name Of Project ? ")
app=input("Enter The Name Of App ? ")
result = subprocess.run(['python', '-m', 'venv', virtual_environment], shell=True, stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))
result = subprocess.run([f'{virtual_environment}\\Scripts\\activate'], shell=True, stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))

result = subprocess.run(['pip', 'install', 'django'], shell=True, stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))
os.chdir(virtual_environment)
result = subprocess.run(['django-admin', 'startproject',project], shell=True, stdout=subprocess.PIPE)
print(result.stdout.decode('utf-8'))
print(os.getcwd())
print(os.listdir())
os.chdir(project)
result = subprocess.run(['python', 'manage.py', 'migrate'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode==0:
    print("Successfully migration")
else:
    print("somthing is wrong")
    print(result.stdout.decode('utf-8'))
result = subprocess.run(['python', 'manage.py', 'startapp',app], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode == 0:
    print(f'Successfully created app!')
else:
    print('Failed to create app')
    print(result.stderr.decode('utf-8'))
#====================== Add new app in installed app ==================#
settings_path = os.path.join(os.getcwd(),project, 'settings.py')
with open(settings_path, 'r') as f:
    contents = f.readlines()
installed_apps_line = None
for i, line in enumerate(contents):
    if 'INSTALLED_APPS' in line:
        installed_apps_line = i
        break
if installed_apps_line is not None:
    line = contents[installed_apps_line]
    indent = line.split('INSTALLED_APPS', maxsplit=1)[0]
    new_line = f"{indent}    '{app}',\n"
    contents.insert(installed_apps_line + 1, new_line)
with open(settings_path, 'w') as f:
    contents = ''.join(contents)
    f.write(contents)
print(f'Successfully added app')
#============ create urls.py file in App ======================== #
app_directory = os.path.join(os.getcwd(), app)
urls_file_path = os.path.join(app_directory, 'urls.py')
urls_file_contents = f"""from django.urls import path

from . import views

urlpatterns = [
   # path('', views.index, name='index'),
]
"""

with open(urls_file_path, 'w') as f:
    f.write(urls_file_contents)

print(f'Successfully created urls.py file for app {app}!')
#======================= include app urls in urls.py in project =================#
urls_path = os.path.join(os.getcwd(), project, 'urls.py')
urls_file_contents = f"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('{app}.urls')) 
]
# Media setting #
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""

with open(urls_path, 'w') as f:
    f.write(urls_file_contents)
#================================= Add import os ====================#
with open(settings_path, 'r') as f:
    contents = f.read()
new_contents = 'import os\n' + contents
with open(settings_path, 'w') as f:
    f.write(new_contents)
#============================== Add Template Settings =============================#
with open(settings_path, 'r') as f:
    contents = f.readlines()

templates_start = None
templates_end = None

for i, line in enumerate(contents):
    if 'TEMPLATES' in line.strip():
        templates_start = i
    if templates_start is not None and line.strip() == '],':
        templates_end = i + 1
        break

if templates_start is not None and templates_end is not None:
    del contents[templates_start:templates_end+1]

last_line = len(contents) - 1
new_templates ='''TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR,"templates")],
        'APP_DIRS':True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
'''
with open(settings_path, 'a') as f:
    f.writelines(new_templates)

print("Successfully removed the old TEMPLATES setting and added the new one.")
#===================================== add Static settings =============================#
new_lines = [
    '\n',
    '# Static files\n',
    'STATIC_ROOT = os.path.join(BASE_DIR, "static")\n',
    'STATIC_URL = "/static/"\n',
    'STATICFILES_DIRS = [\n',
    f'    os.path.join(BASE_DIR, "project", "static"),\n',
    ']\n',
    '\n',
]

with open(settings_path, 'a') as f:
    f.writelines(new_lines)

print("Successfully added static files settings to settings.py")
#==================== Add Media Settings ============================================#
new_lines = '''
    # Media files\n
MEDIA_ROOT=os.path.join(BASE_DIR,"media")
MEDIA_URL = "media/"
    \n
'''

with open(settings_path, 'a') as f:
    f.writelines(new_lines)

print("Successfully added media files settings to settings.py")
subprocess.call(['python', 'manage.py', 'collectstatic'])
subprocess.call(['pip', 'install', 'pillow'])
#===================================== add Static Folder =============================#
os.chdir(project)
if not os.path.exists("static"):
    os.makedirs("static")
    print("Folder templates created successfully.")
else:
    print("Folder templates already exists.")

#============================== create templates folder =============================#
os.chdir("..")
os.chdir(app)
if not os.path.exists("templates"):
    os.makedirs("templates")
    print("Folder templates created successfully.")
else:
    print("Folder templates already exists.")


    
