from django.views import View
from django.shortcuts import render

from .logics import inconsistent_events


class ConsistencyTestView(View):
    template_name = "staff/consistency_test.html"
    result_template_name = "staff/consistency_test_result.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        week_no = int(request.POST["week-no"])
        data = str(request.POST["data"])
        e = inconsistent_events(int(week_no), str(data))
        return render(
            request,
            self.result_template_name,
            {"debug": request.POST, "inconsistent_events": e},
        )
