#!/usr/bin/env python


class CodequiryAPIException(Exception):
    """
    As a result of an API error response.
    """

    def message(self):
        return self.__dict__.get('message', None) or getattr(self, 'args')[0]
