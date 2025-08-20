# Database Administration Tools

This project now includes two web-based database administration tools to watch and manage your PostgreSQL database.

## 🔗 PostgreSQL Connection Strings

### For Applications:
- **Docker Internal:** `postgresql://airbnb_user:airbnb_pass@db:5432/airbnb_db`
- **Local External:** `postgresql://airbnb_user:airbnb_pass@localhost:5432/airbnb_db`
- **Django Format:** `DATABASE_URL=postgresql://airbnb_user:airbnb_pass@db:5432/airbnb_db`

### Connection Details:
- **Host:** `db` (Docker) / `localhost` (local)
- **Port:** `5432`
- **Database:** `airbnb_db`
- **Username:** `airbnb_user`
- **Password:** `airbnb_pass`

## 🔧 Available Tools

### 1. Adminer (Lightweight)
- **URL:** http://localhost:8081
- **Description:** Simple, lightweight database management tool
- **Login Details:**
  - **System:** PostgreSQL
  - **Server:** db
  - **Username:** airbnb_user
  - **Password:** airbnb_pass
  - **Database:** airbnb_db

### 2. pgAdmin (Full-featured)
- **URL:** http://localhost:8080
- **Description:** Comprehensive PostgreSQL administration platform
- **Login Details:**
  - **Email:** admin@airbnb.com
  - **Password:** admin123

#### To connect pgAdmin to your database:
1. Login to pgAdmin with the credentials above
2. Right-click "Servers" in the left panel
3. Select "Create" > "Server"
4. In the "General" tab, give it a name: "Airbnb Database"
5. In the "Connection" tab, enter:
   - **Host name/address:** db
   - **Port:** 5432
   - **Maintenance database:** airbnb_db
   - **Username:** airbnb_user
   - **Password:** airbnb_pass
6. Click "Save"

## 🚀 Features You Can Use

### With Both Tools:
- **View Tables:** Browse all your Django models' data
- **Run Queries:** Execute custom SQL queries
- **Monitor Performance:** Check database statistics
- **Backup/Restore:** Export and import data
- **User Management:** Manage database users and permissions

### Specific to Each Tool:

#### Adminer:
- Quick and simple interface
- No setup required
- Direct access to database
- Great for quick data viewing and editing

#### pgAdmin:
- Advanced query editor with syntax highlighting
- Visual explain plans
- Database monitoring and statistics
- Schema visualization
- More comprehensive administration features

## 📊 Your Django Tables

You can now view and monitor these Django tables:
- `auth_user` - User accounts
- `core_listing` - Airbnb property listings
- `core_blogpost` - Blog posts
- `core_blogauthor` - Blog authors
- `core_blogcategory` - Blog categories
- `django_migrations` - Django migration history
- And all other Django system tables

## 💡 Useful SQL Queries

```sql
-- View all users
SELECT * FROM auth_user;

-- View all listings
SELECT * FROM core_listing;

-- Count listings by location
SELECT location, COUNT(*) FROM core_listing GROUP BY location;

-- View recent blog posts
SELECT title, created_at FROM core_blogpost ORDER BY created_at DESC LIMIT 5;
```

## 🔒 Security Note

These tools are configured for development. For production:
- Change all default passwords
- Restrict network access
- Enable SSL/TLS
- Use environment variables for credentials
