from django.shortcuts import render

# Create your views here.


def test_view(request):
    if request.method == "GET":
        return render(request, 'Portfolio_Management_System/tso_archive.html')
