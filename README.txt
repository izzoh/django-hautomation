=====
Django Home Automation
=====

Django Home Automation is a Django app which provides a REST API meant to
control home automation devices. It also provides a modular framework for 
developing home automation drivers to enable more protocolos to be drived by the app.

The application by it self wont be enable to manage any home automation protocol
You need to install any protocol app to do this. For example you can use django-hax10 to
manage X10 devices.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "hacore" and "harest" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'hacore',
	  'harest',
      )

2. Include the polls URLconf in your project urls.py like this::

	    url(r'rest/', include('harest.urls'))

3. Run `python manage.py syncdb` to create the homeautomation models.

