from django.shortcuts import render
from django.views import View


class RankingView(View):
    def get(self, request):
        return render(request, "ranking/get.html", {})
