from django import template
from ..models import Menu, MenuItem
from django.urls import resolve

register = template.Library()

@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_url = resolve(context.request.path_info).url_name
    try:
        menu = Menu.objects.prefetch_related('items').get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_tree': [], 'current_url': current_url}

    items = menu.items.all()

    def build_tree(parent=None):
        tree = []
        for item in items.filter(parent=parent):
            tree.append({
                'item': item,
                'children': build_tree(item)
            })
        return tree

    menu_tree = build_tree()

    return {
        'menu_tree': menu_tree,
        'current_url': current_url,
    }
