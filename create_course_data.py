from core.models import CourseCategory, Course

# Create Course Categories
categories_data = [
    {
        'name': 'airbnb-hosting',
        'name_vietnamese': 'Kinh doanh Airbnb',
        'slug': 'airbnb-hosting',
        'description': 'Học cách kinh doanh Airbnb từ cơ bản đến nâng cao',
        'icon': 'home'
    },
    {
        'name': 'marketing',
        'name_vietnamese': 'Marketing & Quảng cáo',
        'slug': 'marketing',
        'description': 'Chiến lược marketing hiệu quả cho Airbnb',
        'icon': 'megaphone'
    },
    {
        'name': 'photography',
        'name_vietnamese': 'Chụp ảnh chuyên nghiệp',
        'slug': 'photography',
        'description': 'Kỹ thuật chụp ảnh thu hút khách hàng',
        'icon': 'camera'
    },
    {
        'name': 'customer-service',
        'name_vietnamese': 'Dịch vụ khách hàng',
        'slug': 'customer-service',
        'description': 'Nâng cao chất lượng dịch vụ khách hàng',
        'icon': 'heart'
    }
]

for cat_data in categories_data:
    category, created = CourseCategory.objects.get_or_create(
        slug=cat_data['slug'],
        defaults=cat_data
    )
    if created:
        print(f"Created category: {category.name_vietnamese}")

# Create Sample Courses
courses_data = [
    {
        'title': 'Khóa học Kinh doanh Airbnb từ A-Z',
        'slug': 'kinh-doanh-airbnb-tu-a-z',
        'description': '''Khóa học toàn diện về kinh doanh Airbnb, từ việc tìm kiếm và thiết lập căn hộ đến quản lý khách hàng và tối ưu hóa doanh thu. 

Bạn sẽ học được:
- Cách chọn địa điểm và loại hình bất động sản phù hợp
- Thiết lập và trang trí căn hộ thu hút khách
- Tạo listing hiệu quả trên Airbnb
- Chiến lược định giá và quản lý lịch đặt phòng
- Xử lý khách hàng và các tình huống phát sinh
- Tối ưu hóa doanh thu và mở rộng quy mô kinh doanh''',
        'short_description': 'Học cách kinh doanh Airbnb thành công từ việc thiết lập đến tối ưu hóa doanh thu với hướng dẫn chi tiết từ chuyên gia.',
        'category_slug': 'airbnb-hosting',
        'instructor': 'Nguyễn Việt Anh',
        'duration': '8 tuần',
        'difficulty': 'beginner',
        'price': 2500000,
        'original_price': 3500000,
        'students_enrolled': 1250,
        'rating': 4.9,
        'total_lessons': 45,
        'what_you_learn': 'Thiết lập căn hộ Airbnb từ đầu, Tạo listing thu hút khách hàng, Chiến lược định giá tối ưu, Quản lý khách hàng chuyên nghiệp, Tối ưu hóa doanh thu, Mở rộng quy mô kinh doanh',
        'requirements': 'Máy tính có kết nối internet, Tiếng Anh cơ bản (để hiểu Airbnb platform), Sẵn sàng đầu tư thời gian học và thực hành',
        'featured': True
    },
    {
        'title': 'Chụp ảnh Airbnb chuyên nghiệp',
        'slug': 'chup-anh-airbnb-chuyen-nghiep',
        'description': '''Học cách chụp ảnh căn hộ Airbnb thu hút và chuyên nghiệp để tăng tỷ lệ booking.

Khóa học bao gồm:
- Nguyên tắc cơ bản về nhiếp ảnh bất động sản
- Cách sử dụng ánh sáng tự nhiên và đèn LED
- Góc chụp và composition tạo ấn tượng
- Chỉnh sửa ảnh cơ bản với Lightroom và Photoshop
- Tạo virtual tour 360 độ
- Xu hướng nhiếp ảnh Airbnb mới nhất''',
        'short_description': 'Nắm vững kỹ thuật chụp ảnh bất động sản chuyên nghiệp để listing Airbnb của bạn nổi bật và thu hút khách hàng.',
        'category_slug': 'photography',
        'instructor': 'Nguyễn Việt Anh',
        'duration': '4 tuần',
        'difficulty': 'intermediate',
        'price': 1500000,
        'original_price': 2000000,
        'students_enrolled': 650,
        'rating': 4.8,
        'total_lessons': 25,
        'what_you_learn': 'Kỹ thuật nhiếp ảnh bất động sản, Sử dụng ánh sáng hiệu quả, Composition và góc chụp đẹp, Chỉnh sửa ảnh chuyên nghiệp, Tạo virtual tour, Xu hướng nhiếp ảnh hiện đại',
        'requirements': 'Máy ảnh DSLR hoặc smartphone có camera tốt, Phần mềm chỉnh sửa ảnh cơ bản, Sẵn sàng thực hành thường xuyên',
        'featured': True
    },
    {
        'title': 'Marketing Airbnb hiệu quả',
        'slug': 'marketing-airbnb-hieu-qua',
        'description': '''Tìm hiểu các chiến lược marketing hiện đại để tăng độ nhận diện và booking cho listing Airbnb.

Nội dung khóa học:
- SEO cho Airbnb listing
- Social media marketing
- Content marketing và storytelling
- Quảng cáo trả tiền (Google Ads, Facebook Ads)
- Email marketing và automation
- Xây dựng thương hiệu cá nhân
- Phân tích dữ liệu và tối ưu hóa''',
        'short_description': 'Nắm vững các chiến lược marketing số để tăng visibility và booking rate cho listing Airbnb của bạn.',
        'category_slug': 'marketing',
        'instructor': 'Nguyễn Việt Anh',
        'duration': '6 tuần',
        'difficulty': 'intermediate',
        'price': 1800000,
        'original_price': 2500000,
        'students_enrolled': 890,
        'rating': 4.7,
        'total_lessons': 32,
        'what_you_learn': 'SEO cho Airbnb, Social media marketing, Content marketing, Quảng cáo trả tiền, Email marketing, Xây dựng thương hiệu, Analytics và optimization',
        'requirements': 'Hiểu biết cơ bản về digital marketing, Có listing Airbnb để thực hành, Sẵn sàng đầu tư vào quảng cáo',
        'featured': False
    },
    {
        'title': 'Dịch vụ khách hàng xuất sắc',
        'slug': 'dich-vu-khach-hang-xuat-sac',
        'description': '''Nâng cao kỹ năng giao tiếp và dịch vụ khách hàng để tạo trải nghiệm tuyệt vời cho guests.

Những gì bạn sẽ học:
- Nguyên tắc dịch vụ khách hàng xuất sắc
- Giao tiếp hiệu quả với guests quốc tế
- Xử lý phàn nàn và tình huống khó khăn
- Tạo welcome package ấn tượng
- Automation trong customer service
- Xây dựng mối quan hệ dài hạn với khách''',
        'short_description': 'Phát triển kỹ năng dịch vụ khách hàng chuyên nghiệp để tạo trải nghiệm đáng nhớ và nhận review 5 sao.',
        'category_slug': 'customer-service',
        'instructor': 'Nguyễn Việt Anh',
        'duration': '3 tuần',
        'difficulty': 'beginner',
        'price': 900000,
        'original_price': 1200000,
        'students_enrolled': 1100,
        'rating': 4.9,
        'total_lessons': 18,
        'what_you_learn': 'Nguyên tắc dịch vụ khách hàng, Giao tiếp đa văn hóa, Xử lý phàn nàn, Tạo welcome experience, Automation tools, Xây dựng loyalty',
        'requirements': 'Kỹ năng giao tiếp cơ bản, Tiếng Anh giao tiếp, Sẵn sàng thực hành với khách thật',
        'featured': False
    }
]

for course_data in courses_data:
    category = CourseCategory.objects.get(slug=course_data['category_slug'])
    course_data['category'] = category
    del course_data['category_slug']
    
    course, created = Course.objects.get_or_create(
        slug=course_data['slug'],
        defaults=course_data
    )
    if created:
        print(f"Created course: {course.title}")

print("Sample course data created successfully!")
