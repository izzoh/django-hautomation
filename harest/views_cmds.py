from hacore.models import Protocol, Device
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from auth import access_required
from django.core.urlresolvers import reverse
import simplejson
#
# Home automation commands
#
#   switch command
#      accepted values on|off


@csrf_exempt
@access_required
def pl_switch(request, protocol, did):

    if request.method != "PUT":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only PUT HTTP verb accepted for pl_switch command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )

    qd = QueryDict(request.body, request.encoding)
    if "value" not in qd:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Switch command needs a value to be set", ]}),
            content_type="application/json",
            )
    value = qd["value"].lower()

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, protocol=protocol, did=did)

    # ginsfsm ***********************************
    from ginsfsm.globals import global_get_gobj
    driver = global_get_gobj("driver_X10", "X10")
    driver.post_event(
        driver,
        "EV_COMMAND",
        data=simplejson.dumps({
            "cmd": "pl_switch",
            "did": device.did,
            "value": value,
        }))

    # ginsfsm ***********************************
    """
    exec "from %s.cmds import pl_switch" % protocol.module

    try:
        ret = pl_switch(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": [str(ex), ]}),
            content_type="application/json",
            )
    """
    #TODO changes in device must be made from EV_DEVICE_UPDATE
    device.status = 0 if value == "off" else 100
    device.save()
    response = redirect(reverse('device_by_id', kwargs={"protocol": device.protocol, "did": device.did}))
    response.content_type = "application/json"
    return response


@csrf_exempt
@access_required
def pl_dim(request, protocol, did):

    if request.method != "POST":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only POST(no idempotent) HTTP verb accepted for pl_dim command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )

    if "value" not in request.POST:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Dim command needs a value to be set", ]}),
            content_type="application/json", )
    value = request.POST["value"]

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, did=did, device_type="dimmer")

    exec "from %s.cmds import pl_dim" % protocol.module
    try:
        ret = pl_dim(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": [str(ex), ]}),
            content_type="application/json",
            )

    try:
        ds = int(device.status) - int(value)
    except TypeError:
        ds = int(value)

    if ds < 0:
        ds = 0
    device.status = ds
    device.save()
    response = redirect(reverse('device_by_id', kwargs={"protocol": device.protocol, "did": device.did}))
    response.content_type = "application/json"
    return response


@csrf_exempt
@access_required
def pl_bri(request, protocol, did):

    if request.method != "POST":
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Only POST(no idempotent) HTTP verb accepted for pl_bri command!!, arrived: %s" % request.method, ]}),
            content_type="application/json",
            )
    if "value" not in request.POST:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": ["Bri command needs a value to be set", ]}),
            content_type="application/json",
            )
    value = request.POST["value"]

    protocol = get_object_or_404(Protocol, name=protocol)

    device = get_object_or_404(Device, did=did, device_type="dimmer")

    exec "from %s.cmds import pl_bri" % protocol.module
    try:
        ret = pl_bri(device.did, value)
    except ValueError, ex:
        return HttpResponseBadRequest(
            content=simplejson.dumps({"errors": [str(ex), ]}),
            content_type="application/json",
            )
    try:
        ds = int(device.status) + int(value)
    except TypeError:
        ds = int(value)

    if ds > 100:
        ds = 100
    device.status = ds
    device.save()
    response = redirect(reverse('device_by_id', kwargs={"protocol": device.protocol, "did": device.did}))
    response.content_type = "application/json"
    return response
