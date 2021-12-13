from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse

from fetcher.models import PointRecord

def main(request):
    point_records = PointRecord.objects.order_by('timestamp')
    return render(request, 'fetcher/main.html', {'records': point_records})

def add(request):
    if request.method == "POST":
        post = request.POST
        pr = PointRecord(payer=post.get('payer'), points=int(post.get('points')), timestamp=timezone.now())
        pr.save()
        point_records = PointRecord.objects.order_by('timestamp')
        return HttpResponseRedirect(reverse('fetcher:main'))
    return HttpResponse("This is the Record Adder")

def spend(request):
    if request.method == "POST":
        point_records = PointRecord.objects.order_by('timestamp')
        charge = int(request.POST.get('points'))
        points = PointRecord.objects.aggregate(Sum('points'))
        total_balance = points.get('points__sum')
        if charge > total_balance:
            return render(request, 'main.html', {'records': point_records, 'spend_error_message':'Insufficent points to spend'})
        for record in point_records:
            points = record.points
            if points >= charge:
                points = points - charge
                record.points = points
                record.save()
                break
            charge = charge - points
            record.delete()
        return HttpResponseRedirect(reverse('fetcher:main'))
    return HttpResponse("This is the Point Spender")

def balance(request):
    points_balance = PointRecord.objects.values('payer').annotate(points=Sum('points'))
    return HttpResponse(points_balance)

