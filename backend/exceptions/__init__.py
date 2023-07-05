"""
Global FastAPI exception and warning classes.
"""


class ImproperlyConfigured(Exception):
    """FastAPI is somehow improperly configured"""
    pass


class SuspiciousOperation(Exception):
    """The user did something suspicious"""


class SuspiciousMultipartForm(SuspiciousOperation):
    """Suspect MIME request in multipart form data"""
    pass


class SuspiciousFileOperation(SuspiciousOperation):
    """A Suspicious filesystem operation was attempted"""
    pass


class VideoProcessingException(Exception):
    """Video processing exception"""
    pass


class FastAPIUnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, obj, *args):
        self.obj = obj
        super().__init__(*args)

    def __str__(self):
        return '%s. You passed in %r (%s)' % (
            super().__str__(),
            self.obj, type(self.obj)
        )
