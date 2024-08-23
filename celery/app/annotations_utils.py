from celery.app.annotations import _first_match, _first_match_any

__all__ = ('resolve_all')

def resolve_all(anno, task):
    """Resolve all pending annotations."""
    return (x for x in (_first_match(anno, task), _first_match_any(anno)) if x)
