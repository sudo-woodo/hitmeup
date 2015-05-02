from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=256)
    out_friends = models.ManyToManyField('self', through='Friendship', symmetrical=False,
                                              related_name='in_friends')

    def __unicode__(self):
        return self.name

class Friendship(models.Model):
    from_friend = models.ForeignKey(UserProfile, related_name='out_friendships')
    to_friend = models.ForeignKey(UserProfile, related_name='in_friendships')
    level = models.IntegerField(default=0)

    class Meta:
        unique_together = ('from_friend', 'to_friend')

    def __unicode__(self):
        return '%s --(%s)--> %s' % (self.from_friend, self.level, self.to_friend)

