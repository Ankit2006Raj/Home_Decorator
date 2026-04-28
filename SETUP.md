# Installation & Setup Guide

## System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

## Quick Setup

### 1. Clone/Download the Project
```bash
cd home-decorator
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy the example file
cp .env.example .env

# Edit .env file and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run the Application
```bash
python app.py
```

The application will start at `http://localhost:8000`

## Environment Variables

### Required Variables
- `GEMINI_API_KEY`: Your Google Gemini API key for AI features
- `DATABASE_URL`: PostgreSQL or SQLite database connection string
- `FLASK_ENV`: Set to 'development' or 'production'
- `SECRET_KEY`: Flask secret key for session management

## Troubleshooting

### CSS Not Loading
**Problem**: CSS files not appearing styled
**Solution**:
1. Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
2. Hard refresh (Ctrl+F5 or Cmd+Shift+R)
3. Check browser console for 404 errors
4. Ensure CSS files exist in `frontend/css/`
5. Restart the Flask server

### Port Already in Use
```bash
# Use a different port
python app.py
# Or modify PORT environment variable
PORT=5001 python app.py
```

### Database Errors
```bash
# Reset database
rm home_decorator.db

# Recreate on next run
python app.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Static Files Not Loading
- Ensure `frontend/` folder structure is correct
- Check that CSS/JS/images folders exist
- Look for 404 errors in browser console
- Verify static folder paths in app.py

## Browser Console Errors

Common issues:
1. **Failed to load resource**: Check static file paths
2. **CORS error**: Verify CORS configuration in app.py
3. **JSON parse error**: Check API endpoints return valid JSON
4. **Undefined variable**: Check script loading order in HTML

## Development Tips

### Debug Mode
Flask debug mode is enabled by default in development:
```bash
FLASK_ENV=development python app.py
```

### Database Inspection
```bash
python
>>> from backend.models import db, User, Furniture
>>> from app import create_app
>>> app = create_app()
>>> with app.app_context():
>>>     users = User.query.all()
>>>     print(users)
```

### API Testing
Use Thunder Client, Postman, or curl:
```bash
curl http://localhost:8000/api/users
curl -X POST http://localhost:8000/api/designs/create \
  -H "Content-Type: application/json" \
  -d '{"name":"test_design"}'
```

## Deployment

### Production Setup with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

### Environment Variables for Production
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-random-key
export GEMINI_API_KEY=your-api-key
export PORT=8000
```

### Using with Nginx
See deployment section in main README.md

## File Structure
```
home-decorator/
├── app.py                 # Flask application entry point
├── wsgi.py               # Production WSGI entry point
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create from .env.example)
├── .gitignore           # Git ignore rules
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   └── services/        # Business logic
└── frontend/
    ├── index.html       # Home page
    ├── editor.html      # Room editor
    ├── 3d-view.html     # 3D viewer
    ├── admin.html       # Admin panel
    ├── css/             # Stylesheets
    ├── js/              # JavaScript files
    ├── images/          # Images
    └── assets/          # Other assets
```

## Support
If you encounter issues:
1. Check this guide
2. Look at browser console errors
3. Check Flask server logs
4. Verify all files are in correct locations
5. Ensure dependencies are installed
# Note
