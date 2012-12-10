from models import Photo
from django.http import HttpResponseRedirect

def photo(request, id=None):
  img = Photo.objects.get(id=id)
  response = HttpResponseRedirect(img.get_admin_thumbnail_url())
  return response