from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.template import Template, Context
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import json, os

from .models import *

def index(request):
    if not request.user.is_authenticated:
        if os.environ.get("OAUTH_ENABLED", True):
            return render(request, 'login.html')
        else:
            return redirect("/accounts/login")

    slideshows = Slideshow.objects.all()
    screens = Screen.objects.all()
    slide_templates = SlideTemplates.objects.all()
    slides = Slide.objects.all()

    context = {"slides": len(slides), "slide_templates": len(slide_templates), "screens": len(screens), "slideshows": len(slideshows)}
    return render(request, 'index.html', context)

@login_required
def list_assets(request):
    assets = Asset.objects.all()
    context = {"assets": assets}
    return render(request, 'assets.html', context)

@login_required
def view_asset(request, id):
    asset = Asset.objects.get(id=id)
    if request.method == "POST":
        asset.name = request.POST['name']
        asset.save()
    context = {"asset": asset}
    return render(request, 'asset.html', context)


@login_required
def delete_asset(request, id):
    asset = Asset.objects.get(id=id)
    asset.delete()
    return redirect(reverse('list_assets'))


@login_required
def new_asset(request):
    if request.method == "POST":
        asset = Asset(name=request.POST['name'], image=request.FILES['image'])
        asset.save()
        return redirect(reverse('list_assets'))
    return render(request, 'new_asset.html')

@login_required
def list_screens(request):
    screens = Screen.objects.all()
    context = {"screens": screens}
    return render(request, 'screens.html', context)

@login_required
def list_slide_templates(request):
    slide_templates = SlideTemplates.objects.all()
    context = {"slide_templates": slide_templates}
    return render(request, 'slide_templates.html', context)

@login_required
def list_slideshows(request):
    slideshows = Slideshow.objects.all()
    context = {"slideshows": slideshows}
    return render(request, 'slideshows.html', context)

@login_required
def edit_slideshow(request, id):
    slideshow = Slideshow.objects.get(id=id)
    slides = Slide.objects.filter(slideshow=id).order_by('-weight')
    main_screens = Screen.objects.filter(slideshow=id)
    master_screens = Screen.objects.filter(master=id)
    screens = main_screens | master_screens
    templates = SlideTemplates.objects.all()
    edit_access = request.user.has_perm('digitalsignage.change_slideshow', slideshow)
    context = {"slideshow": slideshow, "slides": slides, "templates": templates, "screens": screens, "edit_access": edit_access}
    return render(request, 'slideshow.html', context)

@login_required
def edit_slide(request, id):
    slideshow = Slideshow.objects.get(slide_slideshow__id=id)
    slide = Slide.objects.get(id=id)
    template_fields = json.loads(slide.template.fields)

    if not request.user.has_perm('digitalsignage.change_slideshow', slideshow):
        return render(request, '403.html')

    if request.method == "POST":
        data = request.POST
        slide_data = {}
        
        if 'settings-active' in data and data['settings-active'] == "on":
            slide.active = True
        else:
            slide.active = False

        slide.weight = data['settings-weight']
        slide.title = data['settings-title']
        slide.duration = data['settings-duration']
        if data['settings-active_until'] != "":
            slide.active_until = data['settings-active_until']

        for field in template_fields['fields']:
            if field['name'] in data:
                slide_data[field['name']] = data[field['name']]

        slide.data = json.dumps(slide_data)
        slide.save()
        slide = Slide.objects.get(id=id)

    slide_data = json.loads(slide.data)
    print(slide_data)
    for field in template_fields['fields']:
        if field['name'] in slide_data:
            field['data'] = slide_data[field['name']]
        else:
            field['data'] = ""



    context = {"slideshow": slideshow, "slide": slide, "template_fields": template_fields }
    return render(request, 'slide.html', context)

@login_required
def new_slide(request, slideshow_id, template_id):
    slideshow = Slideshow.objects.get(id=slideshow_id)
    template = SlideTemplates.objects.get(id=template_id)
    template_fields = json.loads(template.fields)

    if not request.user.has_perm('digitalsignage.change_slideshow', slideshow):
        return render(request, '403.html')

    if request.method == "POST":
        data = request.POST
        slide_data = {}
        slide = Slide()
        
        slide.title = data['settings-title']

        if 'settings-active' in data and data['settings-active'] == "on":
            slide.active = True
        else:
            slide.active = False

        if data['settings-duration'].isnumeric():
            slide.duration = data['settings-duration']

        if data['settings-weight'].isnumeric():
            slide.weight = data['settings-weight'] 

        for field in template_fields['fields']:
            if field['name'] in data:
                slide_data[field['name']] = data[field['name']]
        slide.template = template
        slide.slideshow = slideshow
        if data['settings-active_until'] != "":
            slide.active_until = data['settings-active_until']
        slide.data = json.dumps(slide_data)
        slide.save()
        return redirect("/slide/" + str(slide.id))

    for field in template_fields['fields']:
        field['data'] = ""

    context = {"slideshow": slideshow, "template": template, "template_fields": template_fields }
    return render(request, 'new_slide.html', context)

@login_required
def delete_slide(request, id):
    slide = Slide.objects.get(id=id)
    slideshow_id = slide.slideshow.id
    slide.delete()
    return redirect("/slideshow/" + str(slideshow_id))

def view_screen(request, id):
    screen = Screen.objects.get(id=id)
    context = {"screen": screen}
    return render(request, 'slideshow/screen.html', context)

@xframe_options_exempt
def view_slide(request, id):
    slide = Slide.objects.get(id=id)
    t = Template(slide.template.template)
    slide_data = json.loads(slide.data)
    c = Context(slide_data)
    slide_template = t.render(c)
    if "preview" in request.GET:
        preview = bool(request.GET['preview'])
    else:
        preview = False
    context = {"slide": slide, "slide_template": slide_template, "preview": preview}
    return render(request, 'slideshow/slide.html', context)

def api_get_screen(request, id):
    screen = Screen.objects.get(id=id)
    main_slides = Slide.objects.filter(slideshow_id=screen.slideshow, active=True, active_until__gte=timezone.now()).order_by('-weight').values()
    if screen.master is not None:
        master_slides = Slide.objects.filter(slideshow_id=screen.master, active=True, active_until__gte=timezone.now()).order_by('-weight').values()
        slides = list(master_slides) + list(main_slides)
    else:
        slides = list(main_slides)

    screen_dict = model_to_dict(screen)
    slides_dict = slides

    data = {"screen": screen_dict, "slides": slides_dict}
    return JsonResponse(data)

