from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from hotels.models import Hotel

@login_required
def add_review(request, hotel_id=None):
    hotel = get_object_or_404(Hotel, pk=hotel_id) if hotel_id else None
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            if hotel:
                review.hotel = hotel
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('hotel_detail', pk=hotel.id if hotel else 1)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'hotel': hotel})
