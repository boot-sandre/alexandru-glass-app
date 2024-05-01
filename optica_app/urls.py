# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright © Simon ANDRÉ <simon@emencia.com>
# project: AlexandruOpticaApp
# github: https://github.com/boot-sandre/alexandru-optica-app/
from django.urls import path

from optica_app.views import home, view_index, order_view, identity_form_view, tunnel_form_view

app_name = 'optica_app'

urlpatterns = [
    path("", view_index, name="index"),
    path("home/", home, name="home"),
    path('order/', order_view, name='order'),
    path('identity/', identity_form_view, name='identity'),
    path('tunnel/', tunnel_form_view, name='tunnel'),
]
