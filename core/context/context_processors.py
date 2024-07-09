from django.urls import reverse
from django.conf import settings


def is_active(request, view_names):
    result = ''
    parts = request.path.split("/")
    if parts[2] != '':
        result = parts[2]
    else:
        result = 'dashboard'
    return any(result == view_name for view_name in view_names)


def has_permission(user, view_names):
    if settings.LOCAL:
        return True
    else:
        return any(user.has_permission(view_name) for view_name in view_names)


def generate_drawer(request, user):
    drawer = [
        {
            'section': 'Productos',
            'childs': [
                {
                    "name": "Dashboard",
                    "href": reverse('dashboard:index'),
                    "href_native": ['dashboard:index'],
                    "icon": "fas fa-tachometer-alt",
                    "active": is_active(request, ['dashboard'])
                },
                {
                    "name": "Facturas",
                    "icon": "fas fa-file-invoice",
                    "href": reverse('dashboard:invoices'),
                    "href_native": ['dashboard:invoices'],
                    "active": is_active(request, ['invoices']),
                }
            ]
        },
        {
            'section': 'Configuración',
            'childs': [
                {
                    "name": "Puntos",
                    "icon": "fas fa-coins",
                    "href": reverse('dashboard:points'),
                    "href_native": ['dashboard:points'],
                    "active": is_active(request, ['points']),
                },
                {
                    "name": "Productos",
                    "icon": "far fa-clock",
                    "href": reverse('dashboard:products'),
                    "href_native": ['dashboard:products'],
                    "active": is_active(request, ['products']),
                },
                {
                    "name": "Stock",
                    "href": reverse('dashboard:stocks'),
                    "href_native": ['dashboard:stocks'],
                    "icon": "fas fa-chart-bar",
                    "active": is_active(request, ['stocks'])
                },
                {
                    "name": "Accesos",
                    "icon": "fas fa-sign-in-alt",
                    "href_native": ['dashboard:users',
                                    'dashboard:roles'],
                    "active": is_active(request, ['users',
                                                  'roles']),
                    "children": [
                        {
                            "name": "Roles",
                            "href": reverse('dashboard:roles'),
                            "href_native": ['dashboard:roles'],
                            "icon": "fas fa-user-cog",
                            "active": is_active(request, ['roles'])
                        },
                        {
                            "name": "Usuarios",
                            "href": reverse('dashboard:users'),
                            "href_native": ['dashboard:users'],
                            "icon": "fas fa-users",
                            "active": is_active(request, ['users']),
                        },

                    ]
                }
            ]
        }
    ]

    filtered_drawer = []
    flag = True
    for section in drawer:
        section_children = []
        for index, item in enumerate(section['childs']):
            if index == 0 and flag:
                section_children.append(item)
                flag = False
                continue
            if 'children' in item:
                children = []
                for child in item['children']:
                    if has_permission(user, child['href_native']):
                        children.append(child)
                if children:
                    item['children'] = children
                    section_children.append(item)
            else:
                if has_permission(user, item['href_native']):
                    section_children.append(item)
        if section_children:
            section['childs'] = section_children
            filtered_drawer.append(section)

    return filtered_drawer


def drawer(request):
    user = request.user
    if user.is_authenticated:
        filtered_drawer = generate_drawer(request, user)
        return {'drawer': filtered_drawer}
    else:
        return {}
