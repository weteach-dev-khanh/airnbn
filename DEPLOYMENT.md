# AirBnB Django Project - Vercel Deployment Guide

This Django project is configured for deployment on Vercel with Supabase PostgreSQL database and Vercel Blob Storage for media files.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
3. **GitHub Repository**: Your code should be in a GitHub repository

## Environment Variables Setup

### Required Environment Variables for Vercel

Set these environment variables in your Vercel project dashboard:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app

# Supabase Database Configuration
POSTGRES_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
POSTGRES_PRISMA_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres?pgbouncer=true&connect_timeout=15
POSTGRES_URL_NON_POOLING=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-supabase-password
POSTGRES_DATABASE=postgres
POSTGRES_HOST=db.[YOUR-PROJECT-REF].supabase.co

# Supabase Configuration
SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
NEXT_PUBLIC_SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
SUPABASE_JWT_SECRET=your-jwt-secret
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Vercel Blob Storage
VERCEL_BLOB_BASE_URL=https://yryhdmorv8znchlu.public.blob.vercel-storage.com
BLOB_READ_WRITE_TOKEN=your-blob-token
```

## Deployment Steps

### 1. Prepare Your Repository

1. Ensure all files are committed to your GitHub repository
2. Make sure `vercel.json`, `build_files.sh`, and `requirements.txt` are in the root directory

### 2. Setup Supabase Database

1. Go to your Supabase project dashboard
2. Navigate to Settings > Database
3. Copy the connection strings and add them to your Vercel environment variables

### 3. Setup Vercel Blob Storage

1. In your Vercel dashboard, go to Storage
2. Create a new Blob Storage
3. Copy the token and URL, add them to your environment variables

### 4. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and click "New Project"
2. Import your GitHub repository
3. Vercel will automatically detect this as a Python project
4. Add all the environment variables listed above
5. Click "Deploy"

### 5. Run Database Migrations

After the first deployment, you need to run migrations. You can do this by:

1. Using Vercel CLI:
   ```bash
   vercel --prod
   vercel exec -- python manage.py migrate
   ```

2. Or by triggering a redeploy after setting up the database

### 6. Create Superuser (Optional)

To create an admin user:

```bash
vercel exec -- python manage.py createsuperuser
```

## File Structure

```
airnbn/
├── airnbn_project/
│   ├── settings.py          # Updated with production settings
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── storage_backends.py  # Custom Vercel Blob Storage backend
│   └── ... (other app files)
├── static/                  # Static files directory
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── build_files.sh          # Vercel build script
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── vercel.json             # Vercel configuration
```

## Custom Storage Backend

The project includes a custom storage backend (`core/storage_backends.py`) for Vercel Blob Storage that handles:

- File uploads to Vercel Blob Storage
- File retrieval with public URLs
- File deletion
- Integration with Django's file storage system

## Static Files

Static files are handled by WhiteNoise middleware and collected during the build process.

## Database Migrations

Migrations are automatically run during the Vercel build process via the `build_files.sh` script.

## Troubleshooting

### Common Issues

1. **Build Failures**: Check that all dependencies are in `requirements.txt`
2. **Database Connection**: Verify Supabase connection strings
3. **Static Files**: Ensure `STATIC_ROOT` path is correct
4. **Media Files**: Check Vercel Blob Storage token and URL

### Logs

View deployment logs in the Vercel dashboard under the "Functions" tab.

## Security Notes

- Never commit `.env` files or secrets to version control
- Use strong, unique passwords for your database
- Regularly rotate your API keys and tokens
- Enable HTTPS-only in production (handled automatically by Vercel)

## Support

For issues with:
- **Vercel**: Check [Vercel Documentation](https://vercel.com/docs)
- **Supabase**: Check [Supabase Documentation](https://supabase.com/docs)
- **Django**: Check [Django Documentation](https://docs.djangoproject.com/)
