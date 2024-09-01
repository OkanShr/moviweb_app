# MovieWeb App

MovieWeb App is a web application for managing movies and their reviews. Built using Flask and styled with Tailwind CSS, this app allows users to view movie details, add, edit, and delete reviews, and manage a list of movies.

## Features

- **View Movies**: Browse a list of movies with details including name, director, and IMDB rating.
- **Manage Reviews**: Add, edit, and delete reviews for each movie.
- **User Management**: Each user can manage their own movie list and reviews.

## Installation

### Prerequisites

- Python 3.x
- Flask
- Tailwind CSS

### Setting Up the Project

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/movieweb-app.git
   cd movieweb-app

2. Create a virtual environment 
   ```bash
   python -m venv venv

3. Activate venv
   ```bash
   venv\Scripts\activate

4. Install Dependencies
   ```bash
   pip install -r requirements.txt

5. Install Tailwind CSS
   ```bash
   npm install -D tailwindcss
   npx tailwindcss init
Then, create a tailwind.config.js
file with default settings, and configure 
your build process to 
include Tailwind CSS.

6. Run The application
   ```bash 
   python3 app.py


### Usage
Home Page: Navigate to the home page to view a list of movies.
Movie Details: Click on a movie to see its details and reviews.
Manage Reviews: Add, edit, or delete reviews for movies you have permission to modify.
User Management: View and manage the list of movies associated with your user account.
### File Structure
app.py: Main Flask application file.
templates/: Directory containing HTML templates.
static/: Directory for static files (CSS, JS, images).
requirements.txt: List of Python dependencies.
README.md: Project documentation.
### Customization
To customize the styling or add new features:

1. Tailwind CSS: Modify styles in the base.html file and add custom Tailwind CSS configurations if needed.

2. Flask Routes: Update routes and logic in app.py to handle new features or change existing functionality.