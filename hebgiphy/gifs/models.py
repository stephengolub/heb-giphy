from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.db import models


class Gif(models.Model):
    """A Gif Model

    Attributes:
        giphy_id (models.CharField): The ID String from GIPHY
        giphy_slug (modela.CharField): The slug String from GIPHY
        giphy_url (models.URLField): The url String to this Gif on GIPHY
        giphy_direct_url (models.URLField): The direct url for the full-size version of the Gif.
        giphy_embed_url (models.URLField): The embed_url for Giphy.
        tags (models.ManyToManyField(Tag)): Tag Objects that a user can catalog images they've favorited.
        favorited_by (models.ManyToManyField(User)): Users that have favorited this Gif.
    """
    giphy_id = models.CharField(max_length=255, unique=True)
    giphy_slug = models.CharField(max_length=255)
    giphy_url = models.URLField()
    giphy_direct_url = models.URLField()
    giphy_embed_url = models.URLField()
    tags = models.ManyToManyField('Tag')
    favorited_by = models.ManyToManyField(get_user_model())

    @staticmethod
    def get_img_url(giphy_obj, img_type):
        """Parse the giphy object for the specified url type.

        Arguments:
            giphy_obj (dict|object): The object from GIPHY
            img_type (str): The type of url to look for.

        Returns:
            str: The url for the particular gif
        """
        if not isinstance(giphy_obj, dict):
            giphy_obj = giphy_obj.to_dict()
        return giphy_obj.get('images', {}).get(img_type, {}).get('url')

    @classmethod
    def get_dict_from_giphy(cls, giphy_obj):
        """Create a dict from the GIPHY object.

        Arguments:
            giphy_obj (dict|object): The object from GIPHY

        Returns:
            dict: An internal use dictionary that can be used to create this model.
        """
        if not isinstance(giphy_obj, dict):
            giphy_obj = giphy_obj.to_dict()
        return {
            'giphy_direct_url': cls.get_img_url(giphy_obj, 'original'),
            'giphy_id': giphy_obj['id'],
            'giphy_slug': giphy_obj['slug'],
            'giphy_url': giphy_obj['url'],
            'giphy_embed_url': giphy_obj['embed_url'],
            'giphy_tags': giphy_obj['tags'] or [],
        }

    @classmethod
    def from_giphy_response(cls, giphy_obj):
        """Build a Gif model from a GIPHY object.

        Arguments:
            giphy_obj (dict|object): The object from GIPHY

        Returns:
            Gif: An instance of this model.
        """
        giphy_dict = cls.get_dict_from_giphy(giphy_obj)
        tags = giphy_dict.pop('giphy_tags', [])
        try:
            model = cls.objects.get(giphy_id=giphy_dict['giphy_id'])
        except cls.DoesNotExist:
            model = cls(**giphy_dict)
        finally:
            model.save()
            tag_source, tag_source_created = TagSource.objects.get_or_create(name='GIPHY')
            tags = [Tag(name=t, source=tag_source) for t in tags]
            for t in tags:
                t.save()
            model.tags.set(tags)
        return model

    def as_dict(self):
        """Fetch this model as a dictionary"""
        model_dict = model_to_dict(self, fields=[
            'giphy_id',
            'giphy_slug',
            'giphy_url',
            'giphy_direct_url',
            'giphy_embed_url'
        ])
        model_dict['giphy_tags'] = [model_to_dict(t) for t in self.tags.all()]
        model_dict['favorited_by'] = [model_to_dict(u) for u in self.favorited_by.all()]
        return model_dict

    def __str__(self):
        return f'Gif: {self.giphy_slug}'


class Tag(models.Model):
    """A Tag Model.

    Tags are unique on `source` and `name`.

    Attributes:
        name (models.CharField): The name of the tag.
        source (models.ForeignKey(TagSource)): The source of the tag. Generally `'GIPHY'` or `'user'`
    """
    name = models.CharField(max_length=50)
    source = models.ForeignKey('TagSource', on_delete=models.CASCADE)

    def as_dict(self):
        """Fetch this model as a dictionary"""
        return model_to_dict(self)

    class Meta:
        unique_together = ('name', 'source',)

    def __str__(self):
        return f'Tag: {self.name} ({self.source})'


class TagSource(models.Model):
    """A TagSource Model.

    Attributes:
        name (models.CharField): The name of the source.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'TagSource: {self.name}'
