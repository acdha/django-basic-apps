from django.db import models
from django.db.models import permalink
from django.conf import settings

from tagging.fields import TagField
import tagging

LICENSES = (
    ('http://creativecommons.org/licenses/by/2.0/',         'CC Attribution'),
    ('http://creativecommons.org/licenses/by-nd/2.0/',      'CC Attribution-NoDerivs'),
    ('http://creativecommons.org/licenses/by-nc-nd/2.0/',   'CC Attribution-NonCommercial-NoDerivs'),
    ('http://creativecommons.org/licenses/by-nc/2.0/',      'CC Attribution-NonCommercial'),
    ('http://creativecommons.org/licenses/by-nc-sa/2.0/',   'CC Attribution-NonCommercial-ShareAlike'),
    ('http://creativecommons.org/licenses/by-sa/2.0/',      'CC Attribution-ShareAlike'),
)

class BaseMetadata(models.Model):
    """Common metadata for all media resources"""
    title       = models.CharField(max_length=255)
    slug        = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SetBase(BaseMetadata):
    """Common base class for containers"""

    class Meta:
        abstract = True

class MediaBase(BaseMetadata):
    """Common base class for media files"""

    credit     = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(max_length=255, unique=True, blank=True, null=True, help_text="For non-original images, refers to where we got it")
    license    = models.URLField(blank=True, choices=LICENSES)
    tags       = TagField()

    class Meta:
        abstract = True

class AudioSet(SetBase):
  """ AudioSet model """
  audios        = models.ManyToManyField('Audio', related_name='audio_sets')

  class Meta:
    db_table = 'media_audio_sets'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
    return ('audio_set_detail', None, { 'slug': self.slug })


class Audio(MediaBase):
  """ Audio model """
  still         = models.FileField(upload_to='audio_stills', blank=True, help_text='An image that will be used as a thumbnail.')
  audio         = models.FilePathField(path=settings.MEDIA_ROOT+'audios/', recursive=True)

  class Meta:
    db_table = 'media_audio'
    verbose_name_plural = 'audios'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
    return ('audio_detail', None, { 'slug': self.slug })


class PhotoSet(SetBase):
  """ PhotoSet model """
  cover_photo   = models.ForeignKey('Photo', blank=True, null=True)
  photos        = models.ManyToManyField('Photo', related_name='photo_sets')

  class Meta:
    db_table = 'media_photo_sets'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
    return ('photo_set_detail', None, { 'slug': self.slug })


class Photo(MediaBase):
  """ Photo model """
  photo         = models.FileField(upload_to="photos")
  _exif         = models.TextField(blank=True) # TODO: Replace this with JSONField
  def _set_exif(self, d):
      self._exif = simplejson.dumps(d)
  def _get_exif(self):
      if self._exif:
          return simplejson.loads(self._exif)
      else:
          return {}
  exif = property(_get_exif, _set_exif, "Photo EXIF data, as a dict.")

  class Meta:
    db_table = 'media_photos'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @property
  def url(self):
    return '%s%s' % (settings.MEDIA_URL, self.photo)

  @permalink
  def get_absolute_url(self):
    return ('photo_detail', None, { 'slug': self.slug })


class VideoSet(SetBase):
  """ VideoSet model """
  videos        = models.ManyToManyField('Video', related_name='video_sets')

  class Meta:
    db_table = 'media_video_sets'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
    return ('video_set_detail', None, { 'slug': self.slug })


class Video(MediaBase):
  """ Video model """
  still         = models.FileField(upload_to='video_stills', blank=True, help_text='An image that will be used as a thumbnail.')
  video         = models.FilePathField(path=settings.MEDIA_ROOT+'videos/', recursive=True)

  class Meta:
    db_table = 'media_videos'

  class Admin:
    pass

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
    return ('video_detail', None, { 'slug': self.slug })