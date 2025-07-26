# 🏨 Hotel Booking System

![Hotel Booking Animation](https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif)

A modern, feature-rich hotel booking platform built with Django. This project includes user authentication, hotel and room management, booking and payment integration, reviews, image galleries, dashboards, wishlist, advanced search, Google Maps, and more—all with a beautiful, responsive UI.

---

## ✨ Features

- **User Authentication**: Register, login, password reset, social login, and two-factor authentication.
- **Hotel & Room Management**: CRUD for hotels and rooms, image galleries, amenities, and Google Maps integration.
- **Booking System**: Real-time room availability, booking calendar, and wishlist/favorites.
- **Payments**: Stripe integration for secure payments.
- **Dashboards**: User and admin dashboards with analytics, real-time charts, and CSV export.
- **Reviews & Ratings**: Users can review and rate hotels and rooms.
- **Advanced Search & Filters**: Search by price, rating, amenities, and location.
- **Pagination**: For hotel and room listings.
- **Responsive Design**: Mobile-friendly, modern UI with Bootstrap 5 and custom CSS.
- **Animations**: Smooth transitions and interactive elements for a delightful user experience.

---

## 🚀 Demo

![Hotel Booking Demo](https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif)

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/hotelbooking.git
   cd hotelbooking
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:**
   - Visit [http://localhost:8000/](http://localhost:8000/)

---

## 📸 Screenshots

| Home Page | Hotel Detail | Booking Calendar | Dashboard |
|-----------|--------------|------------------|-----------|
| ![](static/img/screenshot_home.png) | ![](static/img/screenshot_detail.png) | ![](static/img/screenshot_calendar.png) | ![](static/img/screenshot_dashboard.png) |

---

## 📚 Tech Stack

- **Backend:** Django, SQLite (default, can use PostgreSQL/MySQL)
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript, Chart.js
- **Payments:** Stripe
- **Maps:** Google Maps API
- **Authentication:** Django Allauth, 2FA

---

## 💡 Advanced Features

- Real-time analytics and charts (Chart.js)
- Wishlist/favorites for hotels and rooms
- Booking calendar with availability
- Social login (Google, Facebook)
- Two-factor authentication
- Email notifications
- Google Maps for hotel locations
- Pagination and advanced search

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE)

---

## 🙏 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Stripe](https://stripe.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/)
- [Google Maps Platform](https://cloud.google.com/maps-platform)

---

## ⚡ FastAPI Real-Time Booking API

This project includes a FastAPI-based real-time hotel room booking API for integration and automation.

### Start the FastAPI Server

1. **Install FastAPI and Uvicorn:**
   ```bash
   pip install fastapi uvicorn
   ```
2. **Run the FastAPI server:**
   ```bash
   python -m uvicorn hotelbooking.fastapi_app:app --reload
   ```
   - If you see `'uvicorn' is not recognized as a command`, always use the `python -m uvicorn ...` form on Windows.

3. **Access the API docs:**
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

### Booking Endpoint

- **POST** `/api/book-room/`
- **Request Body (JSON):**
  ```json
  {
    "user_id": 1,
    "room_id": 2,
    "check_in": "2024-06-01",
    "check_out": "2024-06-05"
  }
  ```
- **Response:**
  - `{"booking_id": 123, "message": "Room booked successfully."}`
  - Returns error if room is unavailable or user/room not found.

---

> Made with ❤️ for the hotel industry!
