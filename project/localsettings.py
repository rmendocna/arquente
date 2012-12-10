DEBUG=True
TEMPLATE_DIRS = (
    '/home/ricardo/projects/arquente/project/templates',
)

#LOCALES_PATH = (
#    '/home/ricardo/projects/arquente/locale/',
#)
#MEDIA_ROOT = '/home/ricardo/projects/arquente/sitemedia/'
#ADMIN_MEDIA_PREFIX = '/media/'
#MEDIA_URL = '/sitemedia/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'mptt',
    'reversion',
    'tagging',
    'tinymce',
    'filebrowser',
    'project.countries', 
    'project.production',  
    'project.photologue', 
    'project.content',    
)
