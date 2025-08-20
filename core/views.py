from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from .models import (
    AirbnbListing, PropertyType, Location,
    BlogPost, BlogCategory, BlogAuthor, Booking
)

def home(request):
    """Home page view"""
    # Get featured listings for homepage
    featured_listings = AirbnbListing.objects.filter(
        featured=True, active=True
    ).select_related('location', 'property_type').prefetch_related('images')[:3]
    
    context = {
        'featured_listings': featured_listings
    }
    return render(request, 'core/home.html', context)

def airbnb(request):
    """Airbnb listings page"""
    listings = AirbnbListing.objects.filter(active=True).select_related(
        'location', 'property_type'
    ).prefetch_related('images')
    
    # Get filter options
    property_types = PropertyType.objects.all()
    locations = Location.objects.all()
    
    # Apply filters
    property_type_filter = request.GET.get('property_type')
    location_filter = request.GET.get('location')
    search_query = request.GET.get('search')
    
    if property_type_filter and property_type_filter != 'all':
        listings = listings.filter(property_type__id=property_type_filter)
    
    if location_filter and location_filter != 'all':
        listings = listings.filter(location__id=location_filter)
    
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__name__icontains=search_query) |
            Q(location__name_vietnamese__icontains=search_query)
        )
    
    context = {
        'listings': listings,
        'property_types': property_types,
        'locations': locations,
        'current_property_type': property_type_filter,
        'current_location': location_filter,
        'search_query': search_query,
    }
    return render(request, 'core/airbnb.html', context)

def airbnb_detail(request, slug):
    """Individual Airbnb property detail page"""
    listing = get_object_or_404(
        AirbnbListing.objects.select_related('location', 'property_type').prefetch_related(
            'images', 'amenities__amenity'
        ),
        slug=slug,
        active=True
    )
    
    context = {
        'listing': listing
    }
    return render(request, 'core/airbnb_detail.html', context)

def courses(request):
    """Courses page"""
    return render(request, 'core/courses.html')

def blog(request):
    """Blog page"""
    # Get published posts
    posts = BlogPost.objects.filter(published=True).select_related(
        'category', 'author'
    ).order_by('-published_date')
    
    # Separate featured and recent posts
    featured_posts = posts.filter(featured=True)[:6]
    recent_posts = posts.filter(featured=False)[:9]
    
    # Get categories for filter (if needed later)
    categories = BlogCategory.objects.all()
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
    }
    return render(request, 'core/blog.html', context)

def blog_detail(request, slug):
    """Individual blog post detail page"""
    post = get_object_or_404(
        BlogPost.objects.select_related('category', 'author'),
        slug=slug,
        published=True
    )
    
    # Get related posts (same category, excluding current post)
    related_posts = BlogPost.objects.filter(
        category=post.category,
        published=True
    ).exclude(id=post.id).select_related('category', 'author')[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'core/blog_detail.html', context)

def careers(request):
    """Careers page"""
    return render(request, 'core/careers.html')

def contact(request):
    """Contact page"""
    return render(request, 'core/contact.html')


@csrf_exempt
@require_http_methods(["POST"])
def create_booking(request):
    """API endpoint to create a booking"""
    try:
        data = json.loads(request.body)
        
        # Get the listing
        listing = get_object_or_404(AirbnbListing, id=data['listing_id'])
        
        # Parse dates
        checkin_date = datetime.strptime(data['checkin_date'], '%Y-%m-%d').date()
        checkout_date = datetime.strptime(data['checkout_date'], '%Y-%m-%d').date()
        
        # Calculate nights
        nights = (checkout_date - checkin_date).days
        
        # Calculate total price
        total_price = listing.price * nights
        
        # Create booking
        booking = Booking.objects.create(
            listing=listing,
            fullname=data['fullname'],
            email=data['email'],
            phone=data['phone'],
            guests=data['guests'],
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            nights=nights,
            total_price=total_price,
            message=data.get('message', ''),
            payment_status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'booking_id': booking.id,
            'total_price': float(total_price),
            'nights': nights,
            'duration_display': booking.get_duration_display()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
