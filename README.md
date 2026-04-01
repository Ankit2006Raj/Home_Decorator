# Home Decorator - AI-Powered Interior Design Tool

A modern, feature-rich web application for creating stunning 2D floor plans and 3D visualizations of interior spaces with AI-powered furniture recommendations.

## 🎨 Features

### Core Features
- 🏠 Create designs for any room type (bedroom, kitchen, living room, office)
- 📐 2D Floor plan editor with grid-based alignment
- 🎯 Drag & drop furniture with snap-to-grid
- 🔄 Resize, rotate, and move objects
- ↩️ Undo/Redo functionality
- 🎨 Wall, floor, and ceiling color customization
- 💾 Save, load, and export designs

### AI Features (with Gemini API)
- 🤖 Smart furniture recommendations based on room type and budget
- 🎨 AI-generated color palette suggestions
- 💡 Smart layout optimization suggestions

### Additional Features
- 3D room visualization with Three.js
- 📊 Budget estimator
- 📦 Extensive furniture catalog
- 🛒 Price and material information
- 📱 Responsive design for mobile/tablet
- 🌙 Light/Dark mode support
- 👨‍💼 Admin panel for furniture management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- A Gemini API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone/Download the project**
```bash
cd home-decorator
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

5. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📖 Usage

### Creating Your First Design

1. **Go to the Editor**
   - Click "Start Design" on the home page
   - Enter room details (name, type, dimensions)

2. **Add Furniture**
   - Drag furniture from the left sidebar
   - Drop on the canvas to place items
   - Adjust position and rotation as needed

3. **Customize Colors**
   - Use the color picker in the toolbar
   - Choose wall, floor, and ceiling colors
   - Apply themes for quick styling

4. **Get AI Recommendations**
   - Click "AI Assist" button
   - Set your budget and style preference
   - Get furniture suggestions powered by Gemini AI

5. **View in 3D**
   - Click "3D View" to see your design in 3D
   - Rotate, zoom, and explore the space

6. **Export Your Design**
   - Save to database or export as JSON

## 🏗️ Project Structure

```
home-decorator/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── backend/
│   ├── models/            # Database models
│   │   ├── database.py
│   │   ├── user.py
│   │   ├── room.py
│   │   ├── furniture.py
│   │   ├── design.py
│   │   └── theme.py
│   ├── routes/            # API endpoints
│   │   ├── user_routes.py
│   │   ├── furniture_routes.py
│   │   ├── design_routes.py
│   │   └── ai_routes.py
│   └── services/          # Business logic
│       ├── gemini_service.py
│       ├── furniture_service.py
│       └── design_service.py
└── frontend/
    ├── index.html         # Home page
    ├── editor.html        # Room editor
    ├── 3d-view.html       # 3D viewer
    ├── admin.html         # Admin panel
    ├── css/
    │   ├── style.css      # Global styles
    │   ├── editor.css     # Editor styles
    │   └── admin.css      # Admin styles
    ├── js/
    │   ├── main.js        # Main page script
    │   ├── editor.js      # Editor functionality
    │   ├── admin.js       # Admin panel script
    │   └── three-viewer.js # 3D visualization
    ├── images/            # Image assets
    └── assets/            # Other assets
```

## 🔌 API Endpoints

### Users
- `GET /api/users` - Get or create default user
- `GET /api/users/<id>` - Get user by ID
- `POST /api/users/create` - Create new user

### Furniture
- `GET /api/furniture/all` - Get all furniture items
- `GET /api/furniture/room/<type>` - Get furniture by room type
- `GET /api/furniture/category/<category>` - Get furniture by category
- `GET /api/furniture/search?q=<query>` - Search furniture
- `POST /api/furniture/add` - Add custom furniture

### Designs
- `POST /api/designs/create` - Create new design
- `GET /api/designs/<id>` - Get design by ID
- `GET /api/designs/user/<user_id>` - Get user's designs
- `POST /api/designs/<id>/add-item` - Add furniture to design
- `POST /api/designs/item/<id>/update` - Update item position
- `POST /api/designs/item/<id>/remove` - Remove item from design
- `POST /api/designs/<id>/update-colors` - Update room colors
- `POST /api/designs/<id>/delete` - Delete design

### AI Features
- `POST /api/ai/recommendations` - Get furniture recommendations
- `POST /api/ai/color-palette` - Get color suggestions
- `POST /api/ai/layout-suggestions` - Get layout recommendations

## 🎯 Configuration

### Environment Variables
```env
# API Configuration
GEMINI_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///home_decorator.db

# Security
SECRET_KEY=your-secret-key-here
```

## 🤖 AI Features Setup

To use AI-powered recommendations:

1. **Get Gemini API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key

2. **Add to .env file**
   ```env
   GEMINI_API_KEY=your_copied_api_key
   ```

3. **Features Enabled:**
   - Furniture recommendations
   - Color palette suggestions
   - Layout optimization

## 📊 Database

The application uses SQLite by default. Database is automatically created on first run with all necessary tables:
- users
- rooms
- furniture
- designs
- design_items
- themes

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py or run on different port
python app.py --port 5001
```

### Database Errors
```bash
# Delete the database and let it recreate
rm home_decorator.db
python app.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🌐 Accessing the Application

Once running, access these pages:
- **Home**: http://localhost:5000/
- **Room Editor**: http://localhost:5000/editor
- **3D Viewer**: http://localhost:5000/3d-view
- **Admin Panel**: http://localhost:5000/admin

## 🎨 Customization

### Adding New Furniture
1. Use the admin panel or API
2. Provide furniture details (name, dimensions, price, category)
3. Furniture automatically available in editor

### Modifying Colors
Edit the CSS variables in `frontend/css/style.css`:
```css
:root {
    --primary: #3B82F6;
    --secondary: #A78BFA;
    --success: #10B981;
    --danger: #EF4444;
    --warning: #F59E0B;
}
```

### Adding New Room Types
Edit `backend/models/design.py` and update furniture categories to include new room types.

## 📝 License

This project is free to use and modify.

## 🤝 Support

For issues or questions, check the documentation or modify as needed for your use case.

## 🚀 Deployment

### Production Setup

1. **Install production server** (gunicorn)
```bash
pip install gunicorn
```

2. **Set environment variables**
```bash
export FLASK_ENV=production
export SECRET_KEY=your_production_secret_key
```

3. **Run with gunicorn**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

4. **Use with Nginx or Apache** for reverse proxy

### Cloud Deployment

**Heroku, AWS, Google Cloud, or any Python-supporting platform:**
1. Commit code to Git
2. Set environment variables in platform settings
3. Deploy using platform CLI or Git push
4. Database will be created automatically

## 🎉 Features Roadmap

- [ ] AR furniture placement
- [ ] Social sharing platform
- [ ] Community design library
- [ ] Collaboration features
- [ ] Offline mode
- [ ] Mobile app
- [ ] Advanced physics simulation
- [ ] Material library expansion

---

## 📞 Contact & Author

**Ankit Raj**

- 🔗 GitHub: [github.com/Ankit2006Raj](https://github.com/Ankit2006Raj)
- 💼 LinkedIn: [linkedin.com/in/ankit-raj-226a36309](https://www.linkedin.com/in/ankit-raj-226a36309)
- 📧 Email: [ankit9905163014@gmail.com](mailto:ankit9905163014@gmail.com)

---

**Made with ❤️ for beautiful homes**
# Home_Decorator
