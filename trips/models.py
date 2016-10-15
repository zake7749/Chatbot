from django.db import models

class Post(models.Model):
	iden = models.CharField(max_length=100)
	content = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	
class Article(models.Model):
	content = models.TextField(u'Content')
	frontId = models.CharField(u'frontId', max_length=50, null=True, blank=True)

	def __unicode__(self):
		return self.frontId