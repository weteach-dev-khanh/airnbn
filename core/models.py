from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

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
    image = models.ImageField(upload_to='blog/posts/', help_text="Main featured image for the blog post")
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.published and not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now()
        super().save(*args, **kwargs)


class BlogPostSection(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text="Section title")
    image = models.ImageField(upload_to='blog/sections/', blank=True, null=True, help_text="Optional section image")
    content = models.TextField(help_text="Section content/paragraph")
    order = models.PositiveIntegerField(default=0, help_text="Order of this section in the blog post")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Blog Post Section"
        verbose_name_plural = "Blog Post Sections"
    
    def __str__(self):
        return f"{self.blog_post.title} - {self.title}"



# Course Models
class CourseInstructor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='course/instructors/', blank=True, null=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Course Instructor"
        verbose_name_plural = "Course Instructors"


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    instructor = models.ForeignKey(CourseInstructor, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=0, help_text="Price in VND")
    duration = models.CharField(max_length=50, help_text="e.g., '8 weeks', '4 weeks'")
    image = models.ImageField(upload_to='courses/')
    students_count = models.PositiveIntegerField(default=0, help_text="Number of enrolled students")
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    active = models.BooleanField(default=True)
    enrolled_users = models.ManyToManyField(User, related_name='enrolled_courses', blank=True, help_text="Users enrolled in this course")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:course_detail', kwargs={'slug': self.slug})
    
    def get_price_display(self):
        return f"{self.price:,.0f}"
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']


class CourseCurriculumItem(models.Model):
    course = models.ForeignKey(Course, related_name='curriculum_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    youtube_link = models.URLField(blank=True, null=True, help_text="YouTube video link for this curriculum item")
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    class Meta:
        verbose_name = "Course Curriculum Item"
        verbose_name_plural = "Course Curriculum Items"
        ordering = ['order']


class CourseFeature(models.Model):
    course = models.ForeignKey(Course, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    class Meta:
        verbose_name = "Course Feature"
        verbose_name_plural = "Course Features"
        ordering = ['order']


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


class CourseEnrollment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('cancelled', 'Đã hủy'),
    ]
    
    # Course information (using slug to identify course from static data)
    course_slug = models.CharField(max_length=100)
    course_title = models.CharField(max_length=200)
    course_price = models.CharField(max_length=50)  # Store as string like "2,990,000"
    
    # Student information
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Payment status
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.fullname} - {self.course_title}"
    
    class Meta:
        verbose_name = "Course Enrollment"
        verbose_name_plural = "Course Enrollments"
        ordering = ['-created_at']
