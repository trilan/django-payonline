import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.importlib import import_module


def import_by_path(dotted_path, error_prefix=''):
    """
    Import a dotted module path and return the attribute/class designated
    by the last name in the path.
    Raise ImproperlyConfigured if something goes wrong.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
            error_prefix, dotted_path))
    try:
        module = import_module(module_path)
    except ImportError as e:
        msg = '%sError importing module %s: "%s"' % (
            error_prefix, module_path, e)
        six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                    sys.exc_info()[2])
    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured(
            '%sModule "%s" does not define a "%s" attribute/class' % (
                error_prefix, module_path, class_name)
        )
    return attr


def get_backends_dict(settings_attr):
    backends = []
    for backend_path in getattr(settings, settings_attr, ()):
        backend = import_by_path(backend_path)
        backends.append(backend)
    return backends


def get_success_backends():
    backends_list = get_backends_dict('PAYONLINE_SUCCESS_BACKENDS')
    return backends_list


def get_fail_backends():
    backends_list = get_backends_dict('PAYONLINE_FAIL_BACKENDS')
    return backends_list
