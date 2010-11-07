import sys

# From http://www.djangosnippets.org/snippets/420/  ---------------------------------------
# It shows the exception in the console. Useful if trying to debug an internal server error with Ajax queries.
# But crashes mod_wsgi since it uses print (hence the import stuff above)

class ConsoleExceptionMiddleware:
    def process_exception(self, request, exception):
        import traceback
        exc_info = sys.exc_info()
        print "######################## Exception #############################"
        print '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
        print "################################################################"
        return None