from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, UserProfileForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from bookings.models import Booking, Payment
from reviews.models import Review
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum
from hotels.models import Hotel
from django.utils.dateparse import parse_date
import csv

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotel_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'users/dashboard.html', {'bookings': bookings, 'reviews': reviews})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')
    total_bookings = Booking.objects.count()
    total_revenue = Payment.objects.filter(status='succeeded').aggregate(total=models.Sum('amount'))['total'] or 0
    total_users = User.objects.count()
    return render(request, 'users/admin_dashboard.html', {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'total_users': total_users,
    })

@login_required
def admin_analytics_data(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    # Filters
    start = request.GET.get('start')
    end = request.GET.get('end')
    hotel_id = request.GET.get('hotel')
    user_id = request.GET.get('user')
    bookings = Booking.objects.all()
    if start:
        bookings = bookings.filter(created_at__date__gte=parse_date(start))
    if end:
        bookings = bookings.filter(created_at__date__lte=parse_date(end))
    if hotel_id:
        bookings = bookings.filter(room__hotel_id=hotel_id)
    if user_id:
        bookings = bookings.filter(user_id=user_id)
    # Bookings per month
    bookings_by_month = (
        bookings.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    # Revenue per month
    revenue_by_month = (
        Payment.objects.filter(booking__in=bookings, status='succeeded')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    # Booking status breakdown
    status_breakdown = bookings.values('status').annotate(count=Count('id'))
    # For drill-down: bookings by hotel
    bookings_by_hotel = (
        bookings.values('room__hotel__name')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="analytics.csv"'
        writer = csv.writer(response)
        writer.writerow(['Month', 'Bookings', 'Revenue'])
        for b, r in zip(bookings_by_month, revenue_by_month):
            writer.writerow([b['month'], b['count'], r['total'] if 'total' in r else 0])
        return response
    return JsonResponse({
        'bookings_by_month': list(bookings_by_month),
        'revenue_by_month': list(revenue_by_month),
        'status_breakdown': list(status_breakdown),
        'bookings_by_hotel': list(bookings_by_hotel),
    })

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
