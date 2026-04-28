# Home Decorator - AI-Powered Interior Design Tool

A modern, feature-rich web application for creating stunning 2D floor plans and 3D visualizations of interior spaces with AI-powered furniture recommendations.

## ✨ Key Features
- **2D Floor Planning**: Intuitive drag-and-drop interface for creating room layouts
- **AI Recommendations**: Powered by Google Gemini for smart furniture suggestions
- **3D Visualization**: Immersive 3D view of your designs using Three.js
- **Theme Support**: Pre-built themes for quick styling
- **Budget-Aware**: Get recommendations within your budget constraints
- **Real-time Updates**: Live preview of design changes as you work




### Creating Your First Design

     

   
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

### AI Features
- `POST /api/ai/recommendations` - Get furniture recommendations
- `POST /api/ai/color-palette` - Get color suggestions

## 🎯 Configuration

### Environment Variables

# API Configuration
GEMINI_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///home_decorator.db

```

## 🤖 AI Features Setup

To use AI-powered recommendations:

2. **Add to .env file**
   ```env
   GEMINI_API_KEY=your_copied_api_key


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

---

## 🌟 Footer

<div align="center">

### 📞 Connect with the Creator

**Ankit Raj**

<p>
  <a href="https://github.com/Ankit2006Raj" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
  <a href="https://www.linkedin.com/in/ankit-raj-226a36309" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
  </a>
  <a href="mailto:ankit9905163014@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/>
  </a>
</p>

| Platform | Link |
|----------|------|
| 🔗 **GitHub** | [github.com/Ankit2006Raj](https://github.com/Ankit2006Raj) |
| 💼 **LinkedIn** | [linkedin.com/in/ankit-raj-226a36309](https://www.linkedin.com/in/ankit-raj-226a36309) |
| 📧 **Email** | [ankit9905163014@gmail.com](mailto:ankit9905163014@gmail.com) |

---

### Made with ❤️ by [Ankit Raj](https://github.com/Ankit2006Raj)

**Building beautiful homes, one design at a time** 🏠✨

<p align="center">
  <strong>33 Contributions</strong> | <em>Last Updated: April 19, 2026</em>
</p>

<p align="center">
  <i>© 2026 Home Decorator. All rights reserved.</i>
</p>

</div>
# Contribution 1
