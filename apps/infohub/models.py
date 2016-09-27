from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User

########## Info ##########

class InfoSourceMgr(models.Manager):
    # Adds a new source the user wants to use.
    def add(self, data, user_id):
        #TODO: Add check if source already exists.
        MAX_NUM_SNIPPETS = 5
        source = InfoSource.objects.create(
            source_type = data['source_type'],
            location = data['location'],
            active = True, # Default to True until we allow user to pause
            max_snippets = MAX_NUM_SNIPPETS,
            highlight_text = data['highlight_text'],
            user = User.objects.get(id = user_id)
        )

        Audit.objects.audit(user_id, "Added source")
        return source

    # Updates settings for an existing information source.
    def update(self, data, user_id):
        #TODO: Don't fail if source doesn't exist.
        source = InfoSource.objects.get(id = data['source_id'])
        source.source_type = data['source_type']
        source.location = data['location']
        source.active = True # Always set to True until we allow user to pause
        #source.max_snippets = data['max_snippets'] # Not yet implemented
        source.highlight_text = data['highlight_text']
        source.save()

        Audit.objects.audit(user_id, "Updated source")
        return source

    # Removes an information source.
    # NOTE: This could instead be implemented with just setting a Deleted bit to 1.
    def remove(self, data, user_id):
        #TODO: Fail silently if source doesn't exist.
        InfoSource.objects.get(id = data['source_id']).delete()

        Audit.objects.audit(user_id, "Removed source")
        return

    def getActive(self, user_id):
        return InfoSource.objects.filter(user_id = user_id).filter(active = True)

# Handles manipulating information sources that are aggregated into the UI.
class InfoSource(models.Model):
    source_type = models.CharField(max_length=100) # Scrape or call API
    location = models.CharField(max_length=500) # The location of the info (URL or API name)
    active = models.BooleanField(default=True) # Whether this source is active
    max_snippets = models.PositiveSmallIntegerField()
    highlight_text = models.CharField(max_length=50) # Keyword/text to be highlighted on result page.
    user = models.ForeignKey(User, related_name='sources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = InfoSourceMgr()

########## Audit ##########

# Handles auditing of user/site activity.
class AuditMgr(models.Manager):
    def audit(self, user_id, action):
        Audit.objects.create(
            action = action,
            user = User.objects.get(id = user_id)
        )

    def getAll(self, max_rows):
        return Audit.objects.all().order_by('-created_at')[:max_rows]

class Audit(models.Model):
    action = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='audits')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AuditMgr()
