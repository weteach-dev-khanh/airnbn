from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from .models import (
    AirbnbListing, PropertyType, Location,
    BlogPost, BlogCategory, BlogAuthor, Booking, CourseEnrollment
)

# Course data (static - no models needed)
COURSE_LISTINGS = [
    {
        'id': 1,
        'slug': 'complete-airbnb-hosting',
        'title': 'Khóa Học Toàn Diện về Kinh Doanh Airbnb',
        'instructor': 'Nguyễn Văn A',
        'price': '2,990,000',
        'duration': '8 weeks',
        'image': '/static/core/images/courses/image.jpg',
        'students': 1234,
    },
    {
        'id': 2,
        'slug': 'airbnb-photography',
        'title': 'Chụp Ảnh Chuyên Nghiệp cho Airbnb',
        'instructor': 'Nguyễn Việt Anh',
        'price': '1,490,000',
        'duration': '4 weeks',
        'image': '/static/core/images/courses/image1.jpg',
        'students': 856,
    },
    {
        'id': 3,
        'slug': 'airbnb-interior-design',
        'title': 'Thiết Kế Nội Thất cho Airbnb',
        'instructor': 'Lê Văn C',
        'price': '2,490,000',
        'duration': '6 weeks',
        'image': '/static/core/images/courses/image2.jpg',
        'students': 945,
    },
    {
        'id': 4,
        'slug': 'airbnb-business-management',
        'title': 'Quản Lý Kinh Doanh Airbnb Hiệu Quả',
        'instructor': 'Phạm Thị D',
        'price': '3,490,000',
        'duration': '10 weeks',
        'image': '/static/core/images/courses/image3.jpg',
        'students': 678,
    },
    {
        'id': 5,
        'slug': 'airbnb-marketing',
        'title': 'Marketing cho Airbnb',
        'instructor': 'Hoàng Văn E',
        'price': '1,990,000',
        'duration': '5 weeks',
        'image': '/static/core/images/courses/image4.jpg',
        'students': 1023,
    },
    {
        'id': 6,
        'slug': 'airbnb-customer-service',
        'title': 'Kỹ Năng Chăm Sóc Khách Hàng',
        'instructor': 'Vũ Thị F',
        'price': '1,490,000',
        'duration': '4 weeks',
        'image': '/static/core/images/courses/image5.jpg',
        'students': 567,
    },
]

COURSE_DETAILS = {
    'complete-airbnb-hosting': {
        'description': 'Khóa học toàn diện giúp bạn xây dựng và vận hành thành công doanh nghiệp Airbnb của mình. Từ việc setup căn hộ đến quản lý đặt phòng và tối ưu doanh thu.',
        'curriculum': [
            'Giới thiệu về Airbnb',
            'Chuẩn bị và setup căn hộ',
            'Chụp ảnh và viết mô tả listing',
            'Định giá và chiến lược kinh doanh',
            'Quản lý đặt phòng và giao tiếp với khách',
            'Tối ưu doanh thu và mở rộng kinh doanh',
        ],
        'features': [
            'Video bài giảng HD',
            'Tài liệu PDF chi tiết',
            'Group hỗ trợ riêng',
            'Chứng chỉ hoàn thành',
        ],
    },
    'airbnb-photography': {
        'description': 'Học cách chụp ảnh chuyên nghiệp cho listing Airbnb của bạn. Khóa học cung cấp kỹ thuật chụp ảnh, chỉnh sửa và tối ưu hình ảnh để thu hút khách hàng.',
        'curriculum': [
            'Cơ bản về nhiếp ảnh',
            'Thiết bị và setup',
            'Kỹ thuật chụp ảnh nội thất',
            'Chụp ảnh góc rộng',
            'Chỉnh sửa ảnh cơ bản',
            'Tối ưu hình ảnh cho Airbnb',
        ],
        'features': [
            'Video hướng dẫn chi tiết',
            'Thực hành với giảng viên',
            'Feedback 1-1',
            'Bộ preset chỉnh ảnh',
        ],
    },
    'airbnb-interior-design': {
        'description': 'Khám phá nghệ thuật thiết kế nội thất cho căn hộ Airbnb. Học cách tạo không gian đẹp, tiện nghi và ấn tượng với ngân sách tối ưu.',
        'curriculum': [
            'Nguyên lý thiết kế cơ bản',
            'Lựa chọn màu sắc và vật liệu',
            'Thiết kế phòng ngủ',
            'Thiết kế phòng khách',
            'Thiết kế phòng tắm',
            'Trang trí và phụ kiện',
        ],
        'features': [
            'Mẫu thiết kế có sẵn',
            'Tư vấn 1-1 với chuyên gia',
            'Danh sách nhà cung cấp',
            'Hướng dẫn shopping tour',
        ],
    },
    'airbnb-business-management': {
        'description': 'Học cách quản lý hiệu quả doanh nghiệp Airbnb của bạn. Từ vận hành hàng ngày đến chiến lược phát triển dài hạn.',
        'curriculum': [
            'Xây dựng mô hình kinh doanh',
            'Quản lý vận hành',
            'Quản lý tài chính',
            'Quản lý nhân sự',
            'Marketing và bán hàng',
            'Phát triển quy mô',
        ],
        'features': [
            'Template quản lý',
            'Phần mềm tracking',
            'Tư vấn kinh doanh',
            'Network doanh nghiệp',
        ],
    },
    'airbnb-marketing': {
        'description': 'Chiến lược marketing toàn diện cho Airbnb. Từ SEO đến social media và email marketing để tăng booking và doanh thu.',
        'curriculum': [
            'Xây dựng thương hiệu',
            'SEO cho Airbnb',
            'Social Media Marketing',
            'Email Marketing',
            'Content Marketing',
            'Quảng cáo online',
        ],
        'features': [
            'Công cụ marketing',
            'Template content',
            'Case study thực tế',
            'Group chia sẻ kinh nghiệm',
        ],
    },
    'airbnb-customer-service': {
        'description': 'Nâng cao kỹ năng chăm sóc khách hàng cho host Airbnb. Học cách xử lý tình huống và tạo trải nghiệm tuyệt vời cho khách.',
        'curriculum': [
            'Nguyên tắc giao tiếp',
            'Kỹ năng lắng nghe',
            'Xử lý khiếu nại',
            'Tạo trải nghiệm khách hàng',
            'Xây dựng loyalty',
            'Quản lý review',
        ],
        'features': [
            'Role-play thực tế',
            'Script mẫu',
            'Hướng dẫn xử lý tình huống',
            'Chứng chỉ nghiệp vụ',
        ],
    },
}

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
    context = {
        'courses': COURSE_LISTINGS
    }
    return render(request, 'core/courses.html', context)

def course_detail(request, slug):
    """Individual course detail page"""
    # Find course by slug
    course = None
    for c in COURSE_LISTINGS:
        if c['slug'] == slug:
            course = c
            break
    
    if not course:
        # Return 404 if course not found
        from django.http import Http404
        raise Http404("Course not found")
    
    # Get course details
    details = COURSE_DETAILS.get(slug, {})
    
    # Merge course data with details
    course_data = course.copy()
    course_data.update(details)
    
    context = {
        'course': course_data
    }
    return render(request, 'core/course_detail.html', context)

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


@csrf_exempt
@require_http_methods(["POST"])
def create_course_enrollment(request):
    """API endpoint to create a course enrollment"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['course_slug', 'course_title', 'course_price', 'fullname', 'email', 'phone']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'Trường {field} là bắt buộc'
                }, status=400)
        
        # Validate course exists in our static data
        course_exists = any(c['slug'] == data['course_slug'] for c in COURSE_LISTINGS)
        if not course_exists:
            return JsonResponse({
                'success': False,
                'error': 'Khóa học không tồn tại'
            }, status=400)
        
        # Create course enrollment
        enrollment = CourseEnrollment.objects.create(
            course_slug=data['course_slug'],
            course_title=data['course_title'],
            course_price=data['course_price'],
            fullname=data['fullname'],
            email=data['email'],
            phone=data['phone'],
            payment_status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'enrollment_id': enrollment.id,
            'message': 'Đăng ký thành công'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
