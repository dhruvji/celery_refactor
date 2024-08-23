"""Task Annotations.

Annotations is a nice term for monkey-patching task classes
in the configuration.

This prepares and performs the annotations in the
:setting:`task_annotations` setting.
"""
from celery.utils.functional import firstmethod, mlazy
from celery.utils.imports import instantiate

__all__ = ('MapAnnotation', 'prepare')

_first_match = firstmethod('annotate')
_first_match_any = firstmethod('annotate_any')

class MapAnnotation(dict):
    """Annotation map: task_name => attributes."""

    def annotate_any(self):
        try:
            return dict(self['*'])
        except KeyError:
            pass

    def annotate(self, task):
        try:
            return dict(self[task.name])
        except KeyError:
            pass


def prepare(annotations):
    """Expand the :setting:`task_annotations` setting."""
    def expand_annotation(annotation):
        if isinstance(annotation, dict):
            return MapAnnotation(annotation)
        elif isinstance(annotation, str):
            return mlazy(instantiate, annotation)
        return annotation

    if annotations is None:
        return ()
    elif not isinstance(annotations, (list, tuple)):
        annotations = (annotations,)
    return [expand_annotation(anno) for anno in annotations]
