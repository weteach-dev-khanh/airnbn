from django.contrib import admin
from .models import (
    PropertyType, Location, AirbnbListing, 
    ListingImage, Amenity, ListingAmenity,
    BlogPost, BlogCategory, BlogAuthor,
    Booking
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

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'featured', 'published', 'published_date']
    list_filter = ['category', 'author', 'featured', 'published', 'created_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content_file', 'image')
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
    
    def save_model(self, request, obj, form, change):
        if obj.published and not obj.published_date:
            from django.utils import timezone
            obj.published_date = timezone.now()
        super().save_model(request, obj, form, change)


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
