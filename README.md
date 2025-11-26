# Car Rental System

[![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-javascript.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

## 📰 Project Summary

This project involves designing and deploying a full-stack online car rental system to digitally transform a 40-year-old company, enabling seamless vehicle booking, payment, and customer feedback.

## Table of Contents

- [Project Description](#-project-description)
- [Installation](#-installation-steps)
- [Tech Stack](#-tech-stack)
- [Visuals](#%EF%B8%8F-visuals)
- [Known Issues](#-known-issues)
- [License](#-license)
- [Team](#-team)


## 🔖 Project Description
This project involves the end-to-end development of a digital platform for Manta, a car rental company with a 40-year history, under new ownership. The core mandate is to design and implement a robust, scalable, and user-friendly system that supports the complete online rental lifecycle. The solution will allow customers to search for vehicles, make bookings, and process payments seamlessly, while providing the business with valuable feedback through an integrated rating system.

## 🔌 Installation Steps

### Frontend
1. **Install Dependencies**
    Install [node.js](https://nodejs.org/en/download)
    Check if installed in terminal:
    ```bash
    node -v
    npm -v
    ```

2. **Install serve globally**
    From the frontend folder, run:
   ```bash
   sudo npm install -g serve
   ```

3. **Run the Server**
    From the root, run:
   ```bash
   serve .
   ```

4. **Open in Browser**
    Go to:
    ```bash
    http://localhost:3000
    ```

5. **Stop the Server**
    Press Ctrl + C in the terminal to stop the server.

### Backend Server (Flask API)
Assuming at root codebase
1. Create a Python virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install backend dependencies:

```bash
pip install -r backend/Server/requirements.txt
```

3. Run the Flask server (from project root):

```bash
python3 backend/Server/server.py
```

4. Example API calls:

```bash
# health check
curl http://127.0.0.1:5000/api/health

# list vehicles
curl http://127.0.0.1:5000/api/vehicles

```

## 💻 Tech Stack

### Programming Languages
JS, HTML, CSS, Python

### Libraries and Frameworks


## 🎞️ Visuals


## 💡 Known Issues


## 📝 License
This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## 👥 Team
Feel free to contact us for further inquiries or feedback.

#### Enrique Albavera
- Email: [ealsamano.gmail.com](mailto:ealsamano@gmail.com)
- LinkedIn: [Enrique-Albavera](https://www.linkedin.com/in/enrique-albavera-405218387/)

#### Britaney Do
- Email: [britaney.do@gmail.com](mailto:britaney.do@gmail.com)
- LinkedIn: [britaney-do](https://linkedin.com/in/britaney-do-6866a9230/)

#### David Le
- Email: [davidle173@gmail.com](mailto:davidle173@gmail.com)
- LinkedIn: [David-Le](https://www.linkedin.com/in/david-le-b313912a7/)

#### Mahmoud Nanah

#### Nguyen Nguyen
- Email: [nguyennguyen.apr@gmail.com](nguyennguyen.apr@gmail.com)

#### Conner O'donnell
- Email: [connerodonnell21@gmail.com](mailto:connerodonnell21@gmail.com)
