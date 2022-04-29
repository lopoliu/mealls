import time
from rest_framework.throttling import BaseThrottle

VISIT_RECORD = {}


class CodeThrottling(BaseThrottle):

    def __init__(self):
        self.ident = None
        self.history = []
        self.INTERVAL = 60

    def get_ident(self, request):
        request_ident = request.GET["email"]
        self.ident = request_ident

    def allow_request(self, request, view):
        self.get_ident(request)
        # 首次访问
        if self.ident not in VISIT_RECORD:
            self.history.append(time.time())
            VISIT_RECORD[self.ident] = self.history
            return True

        self.history = VISIT_RECORD[self.ident]
        if time.time() - self.history[-1] > self.INTERVAL:
            self.history.append(time.time())
            if len(self.history) > 3:
                self.history.pop(1)
            VISIT_RECORD[self.ident] = self.history
            return True

    def wait(self):
        return self.history[-1] + self.INTERVAL - time.time()
