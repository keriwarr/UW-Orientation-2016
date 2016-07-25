import os

from django.db import models

from collections import OrderedDict


SPONSOR_TIERS = (
    ('ST', 'Single Tie'),
    ('DT', 'Double Tie'),
    ('SST', 'Silver Tie'),
    ('GT', 'Golden Tie'),
    ('PT', 'Platinum Tie'),
    ('DDT', 'Diamond Tie'),
)


class Sponsor(models.Model):
    """
    Represents an orientation sponsor.
    """
    LOGO_IMAGE_PATH = os.path.join('sponsors', 'logos')

    name = models.CharField(max_length=80, blank=False)
    tier = models.CharField(max_length=3, choices=SPONSOR_TIERS, default='ST')
    logo = models.ImageField(upload_to=LOGO_IMAGE_PATH, blank=False)
    link = models.URLField(blank=True)

    def sponsor_tier_as_int(self):
        tier_dict = OrderedDict(SPONSOR_TIERS)
        tier_names = tier_dict.keys()
        return tier_names.index(self.tier)

    def get_tier_name(self):
        tier_dict = OrderedDict(SPONSOR_TIERS)
        return tier_dict.get(self.tier)

    def __str__(self):
        return '%s <%s>' % (self.name, self.get_tier_name())

    @classmethod
    def tier_objects(self, increasing=False):
        tiers = list(short_name for short_name, _ in SPONSOR_TIERS)
        objects = []
        for tier in tiers:
            objects.append(Sponsor.objects.filter(tier=tier))
        return objects if increasing else reversed(objects)
