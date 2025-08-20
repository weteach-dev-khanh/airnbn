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

# Supabase Database Configuration (Extract these from your Supabase connection string)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-supabase-password
POSTGRES_DATABASE=postgres
POSTGRES_HOST=db.[YOUR-PROJECT-REF].supabase.co
POSTGRES_PORT=5432

# Optional: Keep these for reference but the above manual config is more reliable
POSTGRES_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
POSTGRES_PRISMA_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres?pgbouncer=true&connect_timeout=15
POSTGRES_URL_NON_POOLING=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

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
2. Make sure `vercel.json` and `requirements.txt` are in the root directory
3. The `build_files.sh` is not needed - Vercel will handle the build automatically

### 2. Setup Supabase Database

1. Go to your Supabase project dashboard
2. Navigate to Settings > Database
3. In the "Connection string" section, you'll find the connection details
4. Extract the individual components:
   - From `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`
   - `POSTGRES_USER`: postgres
   - `POSTGRES_PASSWORD`: [YOUR-PASSWORD] 
   - `POSTGRES_HOST`: db.[YOUR-PROJECT-REF].supabase.co
   - `POSTGRES_PORT`: 5432
   - `POSTGRES_DATABASE`: postgres
5. Add these individual values to your Vercel environment variables

**Important**: Use the individual database components rather than the full connection string to avoid parsing issues.

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

### 5. Post-Deployment Steps

After the first deployment:

1. Go to your Vercel project dashboard
2. Navigate to the Functions tab to see if the deployment was successful
3. If you need to run migrations manually, you can use the Vercel CLI:
   ```bash
   npm i -g vercel
   vercel login
   vercel link
   vercel env pull .env.production
   vercel dev
   ```

### 6. Create Superuser (Optional)

To create an admin user, you'll need to do this through a management command or directly in your Supabase database.

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

1. **Build Failures**: 
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility (Python 3.9)
   - Verify all environment variables are set

2. **Database Connection**: 
   - Verify Supabase connection strings
   - Check that the database is accessible from Vercel's servers
   - Ensure password and host are correct

3. **Static Files**: 
   - Vercel handles static files automatically with WhiteNoise
   - Make sure `STATIC_ROOT` path is correct

4. **Media Files**: 
   - Check Vercel Blob Storage token and URL
   - Verify the custom storage backend is working

5. **Migrations**:
   - Run migrations manually using Vercel CLI if needed:
     ```bash
     vercel env pull .env.production
     python manage.py migrate
     ```

### Running Migrations

If you need to run migrations after deployment:

1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Link your project: `vercel link`
4. Pull environment variables: `vercel env pull .env.production`
5. Run migrations: `python manage.py migrate`

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
