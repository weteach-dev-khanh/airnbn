from django.contrib import admin
from .models import (
    PropertyType, Location, AirbnbListing, 
    ListingImage, Amenity, ListingAmenity,
    BlogPost, BlogCategory, BlogAuthor, BlogPostSection,
    Booking, CourseEnrollment,
    Course, CourseInstructor, CourseCurriculumItem, CourseFeature
)

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_vietnamese']
    search_fields = ['name', 'name_vietnamese']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_vietnamese']
    search_fields = ['name', 'name_vietnamese']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main', 'order']

class ListingAmenityInline(admin.TabularInline):
    model = ListingAmenity
    extra = 1

@admin.register(AirbnbListing)
class AirbnbListingAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'location', 'property_type', 'price', 
        'rating', 'featured', 'active', 'created_at'
    ]
    list_filter = [
        'property_type', 'location', 'featured', 'active', 'created_at'
    ]
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'location', 'property_type', 'description')
        }),
        ('Pricing & Reviews', {
            'fields': ('price', 'rating', 'reviews_count')
        }),
        ('Host Information', {
            'fields': ('host_name', 'host_image', 'host_response_time')
        }),
        ('Booking Information', {
            'fields': ('airbnb_link', 'phone', 'facebook_url')
        }),
        ('Settings', {
            'fields': ('featured', 'active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ListingImageInline, ListingAmenityInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'location', 'property_type'
        ).prefetch_related('images', 'amenities')

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'alt_text', 'is_main', 'order']
    list_filter = ['is_main', 'listing']
    search_fields = ['listing__title', 'alt_text']


# Blog Admin
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name_vietnamese', 'name', 'slug']
    search_fields = ['name', 'name_vietnamese']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    fields = ['name', 'bio', 'avatar', 'email', 'website']


class BlogPostSectionInline(admin.TabularInline):
    model = BlogPostSection
    extra = 1
    fields = ['title', 'image', 'content', 'order']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'featured', 'published', 'published_date']
    list_filter = ['category', 'author', 'featured', 'published', 'created_at']
    search_fields = ['title', 'excerpt', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'image')
        }),
        ('Classification', {
            'fields': ('category', 'author', 'tags')
        }),
        ('Settings', {
            'fields': ('featured', 'read_time', 'published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [BlogPostSectionInline]
    
    def save_model(self, request, obj, form, change):
        if obj.published and not obj.published_date:
            from django.utils import timezone
            obj.published_date = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(BlogPostSection)
class BlogPostSectionAdmin(admin.ModelAdmin):
    list_display = ['blog_post', 'title', 'order', 'created_at']
    list_filter = ['blog_post', 'created_at']
    search_fields = ['blog_post__title', 'title', 'content']
    ordering = ['blog_post', 'order']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('blog_post')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'listing', 'checkin_date', 'checkout_date', 'guests', 'total_price', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'checkin_date', 'created_at']
    search_fields = ['fullname', 'email', 'phone', 'listing__title']
    readonly_fields = ['created_at', 'updated_at', 'nights']
    fieldsets = (
        ('Guest Information', {
            'fields': ('fullname', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('listing', 'checkin_date', 'checkout_date', 'nights', 'guests', 'total_price', 'message')
        }),
        ('Payment & Status', {
            'fields': ('payment_status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('listing')


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'fullname', 'course_title', 'email', 'phone', 
        'course_price', 'payment_status', 'created_at'
    ]
    list_filter = ['payment_status', 'course_slug', 'created_at']
    search_fields = ['fullname', 'email', 'phone', 'course_title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course_slug', 'course_title', 'course_price')
        }),
        ('Student Information', {
            'fields': ('fullname', 'email', 'phone')
        }),
        ('Payment & Status', {
            'fields': ('payment_status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request)


# Course Admin
@admin.register(CourseInstructor)
class CourseInstructorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    fields = ['name', 'bio', 'avatar', 'email', 'website']


class CourseCurriculumItemInline(admin.TabularInline):
    model = CourseCurriculumItem
    extra = 1
    fields = ['title', 'youtube_link', 'order']


class CourseFeatureInline(admin.TabularInline):
    model = CourseFeature
    extra = 1
    fields = ['title', 'order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'instructor', 'price', 'duration', 
        'students_count', 'enrolled_count', 'featured', 'active', 'created_at'
    ]
    list_filter = [
        'instructor', 'featured', 'active', 'created_at'
    ]
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['enrolled_users']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'instructor')
        }),
        ('Course Details', {
            'fields': ('price', 'duration', 'image', 'students_count')
        }),
        ('Enrollment', {
            'fields': ('enrolled_users',)
        }),
        ('Settings', {
            'fields': ('featured', 'active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [CourseCurriculumItemInline, CourseFeatureInline]
    
    def enrolled_count(self, obj):
        return obj.enrolled_users.count()
    enrolled_count.short_description = 'Enrolled Users'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('instructor').prefetch_related('enrolled_users')


@admin.register(CourseCurriculumItem)
class CourseCurriculumItemAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'youtube_link', 'order']
    list_filter = ['course']
    search_fields = ['course__title', 'title']
    ordering = ['course', 'order']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course')


@admin.register(CourseFeature)
class CourseFeatureAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'order']
    list_filter = ['course']
    search_fields = ['course__title', 'title']
    ordering = ['course', 'order']