from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os

def validate_markdown_file(value):
    """Validate that the uploaded file is a markdown file"""
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.md', '.markdown']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only markdown files (.md, .markdown) are allowed.')

class PropertyType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    name_vietnamese = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Property Type"
        verbose_name_plural = "Property Types"

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_vietnamese = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

class AirbnbListing(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Price in VND per night")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    reviews_count = models.PositiveIntegerField(default=0)
    description = models.TextField()
    
    # Host information
    host_name = models.CharField(max_length=100, default="Viet Anh")
    host_image = models.ImageField(upload_to='hosts/', blank=True, null=True)
    host_response_time = models.CharField(max_length=50, default="within an hour")
    
    # Booking information
    airbnb_link = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, default="+84 123 456 789")
    facebook_url = models.URLField(blank=True, null=True)
    
    # Meta
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:airbnb_detail', kwargs={'slug': self.slug})
    
    def get_main_image(self):
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image
        return self.images.first()
    
    def get_price_display(self):
        return f"{self.price:,.0f}"
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Airbnb Listing"
        verbose_name_plural = "Airbnb Listings"
        ordering = ['-created_at']

class ListingImage(models.Model):
    listing = models.ForeignKey(AirbnbListing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listings/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.is_main:
            # Ensure only one main image per listing
            ListingImage.objects.filter(listing=self.listing, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.listing.title} - Image {self.order}"
    
    class Meta:
        verbose_name = "Listing Image"
        verbose_name_plural = "Listing Images"
        ordering = ['order']

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text="Lucide icon name")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

class ListingAmenity(models.Model):
    listing = models.ForeignKey(AirbnbListing, related_name='amenities', on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.listing.title} - {self.amenity.name}"
    
    class Meta:
        unique_together = ['listing', 'amenity']
        verbose_name = "Listing Amenity"
        verbose_name_plural = "Listing Amenities"


# Blog Models
class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_vietnamese = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name_vietnamese


class BlogAuthor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='blog/authors/', blank=True, null=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(help_text="Short description of the post")
    content_file = models.FileField(
        upload_to='blog/content/', 
        validators=[validate_markdown_file],
        help_text="Upload markdown file (.md or .markdown)"
    )
    image = models.ImageField(upload_to='blog/posts/')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(BlogAuthor, on_delete=models.CASCADE, related_name='posts')
    tags = models.CharField(max_length=500, help_text="Comma-separated tags")
    featured = models.BooleanField(default=False, help_text="Show in featured posts section")
    read_time = models.CharField(max_length=20, default="5 phút đọc")
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('core:blog_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_content(self):
        """Load markdown content from uploaded file"""
        if not self.content_file:
            return ""
        
        try:
            # Use the file path directly with proper encoding
            with open(self.content_file.path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return f"Markdown file not found."
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            try:
                with open(self.content_file.path, 'r', encoding='utf-8-sig') as file:
                    return file.read()
            except UnicodeDecodeError:
                try:
                    with open(self.content_file.path, 'r', encoding='latin-1') as file:
                        return file.read()
                except:
                    return "Could not decode file. Please ensure the file is saved in UTF-8 encoding."
        except Exception as e:
            return f"Error loading content: {str(e)}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.published and not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now()
        super().save(*args, **kwargs)



# Booking Models
class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Booking details
    listing = models.ForeignKey(AirbnbListing, on_delete=models.CASCADE, related_name='bookings')
    
    # Guest information
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    guests = models.PositiveIntegerField()
    
    # Stay details
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    nights = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=0)
    
    # Optional message
    message = models.TextField(blank=True)
    
    # Payment and status
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.fullname} - {self.listing.title} ({self.checkin_date} to {self.checkout_date})"
    
    def get_duration_display(self):
        return f"{self.nights + 1} ngày {self.nights} đêm"
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']
