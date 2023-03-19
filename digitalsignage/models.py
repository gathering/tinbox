from django.db import models
from django.utils import timezone
from datetime import timedelta

def one_month_from_today():
    return timezone.now() + timedelta(days=30)

class Slideshow(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_master = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Screen(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    slideshow = models.ForeignKey(Slideshow, on_delete=models.SET_NULL, null=True, blank=True, related_name="slideshow")
    master = models.ForeignKey(Slideshow, on_delete=models.SET_NULL, null=True, blank=True, related_name="master")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SlideTemplates(models.Model):
    name = models.CharField(max_length=200)
    template = models.TextField()
    fields = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def usage(self):
        return len(Slide.objects.filter(template=self.id))

class Slide(models.Model):
    title = models.CharField(max_length=200, blank=True)
    template = models.ForeignKey(SlideTemplates, on_delete=models.CASCADE)
    slideshow = models.ForeignKey(Slideshow, on_delete=models.CASCADE, null=True, related_name="slide_slideshow")
    data = models.TextField(blank=True)
    duration = models.IntegerField(default=5)
    active = models.BooleanField(default=True)
    active_until = models.DateTimeField(default=one_month_from_today, blank=True, null=True)
    weight = models.IntegerField(default=10)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        if not self.active:
            return False
        elif self.active_until < timezone.now():
            return False
        return True
    
    @property
    def has_expired(self):
        if self.active_until < timezone.now():
            return True
        return False 