# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string

from random import randrange

register = template.Library()


@register.simple_tag
def random_image():
    cats = ['abstract', 'nightlife', 'nature', 'transport', 'animals',
        'city', 'fashion', 'sports', 'business', 'food', 'people', 'technics']
    random_cat = cats[randrange(len(cats))]
    return "http://lorempixel.com/800/400/%s/%s" % \
        (random_cat, randrange(1, 11))


@register.simple_tag
def random_text():
    texts = [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu tortor eget nunc condimentum venenatis sit amet et mi. Nulla tincidunt imperdiet ipsum ultricies placerat. Nunc eget elit et libero dictum pellentesque a quis mi. Suspendisse elit turpis, lobortis eu lacinia ac, pharetra et mauris. Phasellus adipiscing pharetra lorem ac adipiscing. Quisque arcu massa, venenatis eu euismod ut, ultricies eu nunc. Integer ullamcorper urna in mi elementum commodo. Aenean et magna orci, in tincidunt tellus. Ut suscipit arcu in augue viverra mollis. Integer sem mauris, imperdiet eget accumsan et, dapibus non turpis. Fusce consectetur sem eget eros bibendum id suscipit enim vulputate.',
        'Sed euismod urna id sapien scelerisque sed elementum metus volutpat. Suspendisse ultrices imperdiet est vitae bibendum. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sem leo, sagittis id ullamcorper at, tincidunt in dolor. Nullam erat purus, venenatis tristique lobortis quis, sollicitudin vitae urna. Donec ultrices sodales tristique. Maecenas sollicitudin vestibulum sem, a pharetra tortor pellentesque quis. Fusce semper magna convallis mauris semper vehicula. Integer convallis accumsan nisl vitae mollis. Mauris laoreet tempor nunc luctus tincidunt. Vestibulum vel tellus sem, non aliquam ligula. Morbi suscipit ultrices varius.',
        'Suspendisse eget arcu nec justo consequat ultrices. Aenean posuere faucibus libero vel lacinia. Etiam quis neque sit amet nunc rutrum interdum id quis nisl. Nam elementum lobortis nisl non imperdiet. Nullam sapien diam, volutpat a volutpat ac, elementum vitae felis. Praesent aliquet semper tortor eu varius. In hac habitasse platea dictumst. Nullam purus odio, ultrices non adipiscing ac, euismod rutrum quam. Morbi dui enim, dictum in sodales sed, pellentesque id turpis. Mauris leo orci, egestas eu tincidunt ut, fringilla vitae odio. Sed neque velit, elementum et luctus fringilla, tempus gravida enim. Pellentesque lobortis, purus at luctus blandit, diam risus congue elit.',
        'Pellentesque eu diam vel enim vulputate consectetur eget nec eros. Suspendisse suscipit, mi at posuere commodo, ligula ante interdum sapien, vitae blandit magna risus faucibus erat. Quisque vestibulum tortor vitae felis facilisis imperdiet. Etiam mattis, nisi eget pharetra auctor, nibh massa rutrum orci, nec tincidunt eros libero ac mi. Maecenas ut mattis ante. Morbi tempus ipsum consequat quam posuere ultrices. Curabitur metus nisi, condimentum at placerat et, sodales dignissim massa. Donec sed nisi nisl, ac varius urna. Quisque tempus bibendum arcu at dictum. Maecenas euismod lobortis sem, sed ullamcorper quam elementum gravida. Cras venenatis est ut lacus convallis rhoncus.'
    ]
    return texts[randrange(len(texts))]


@register.simple_tag
def random_logo(user):
    template_list = ['_zagrad.html', 'za_grad.html', 'zagrad_.html']
    template = template_list[randrange(len(template_list))]
    template_options = {
        '_zagrad.html': [user.get_profile().name if user.is_authenticated() else 'Ti'],
        'za_grad.html': ['bolji', 'zabavniji', 'održivi'],
        'zagrad_.html': ['crtica', 'patlidžana']
    }
    template_option = template_options[template]
    underline = template_option[randrange(len(template_option))]
    return render_to_string('big_logo/%s' % template, {'underline': underline})
