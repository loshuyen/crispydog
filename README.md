# CrispyDog
### A platform for trading digital goods online

Website URL: https://crispydog.xyz

# Contents
* [Core Features](#Core-Features)
* [Tech Stack](#Tech-Stack)
* [System Architecture](#System-Architecture)
* [RESTful APIs](#RESTful-APIs)
* [Database ERD](#Database-ERD)
* [Implements](#Implements)
* [Contact](#Contact)

# Core Features
### User Flow
<img width="673" alt="image" src="https://github.com/user-attachments/assets/9e4f3912-6ba0-4c49-a586-40a553967c93">

### Real-time Notification System
Notify users while they should be responding to trading actions

### Demo Videos
[直購商品](https://youtu.be/f_hwcqRy090)

[似顏繪](https://youtu.be/qnAeB0XSzE0)

# Tech Stack
### Backend
* Python (FastAPI)
* WebSocket
* MySQL
* OAuth 2.0
* Third-party payment service (Credit card, LINE Pay)
* JWT
* Docker
* Nginx

### Cloud Service (AWS)
* EC2
* RDS
* S3
* CloudFront

### Frontend
* HTML
* CSS
* JavaScript

# System Architecture
<img width="672" alt="image" src="https://github.com/user-attachments/assets/68fa575e-ab01-4e13-92de-b33053c62960">

# RESTful APIs
[API Document](https://crispydog.xyz/docs)

# Database ERD
### Database: MySQL
<img width="673" alt="image" src="https://github.com/user-attachments/assets/624175bf-6439-4c58-82ad-a26f81de26f0">

# Implements
### Transaction and Row Lock Mechanisms in Savings Data Manipulation
* Utilize rollback logic for integrity in updating multiple savings data
* Utilize row lock of savings data when updating to prevent dirty read by other transactions
<img width="673" alt="image" src="https://github.com/user-attachments/assets/02441bae-09a7-4499-82ee-420a4f67c43c">


### Google OAuth 2.0 Integration
* Generate JWT with user information from google
* Deliver JWT to the frontend through the query parameter in the redirection url
<img width="673" alt="image" src="https://github.com/user-attachments/assets/5cfe5523-4542-4940-8c12-c3e0a768ba45">

### Download Endpoint Generation and Download Process for 直購商品
* Create an unique download endpoint for the buyer
* Prevent from accessing files by unauthorized users
<img width="673" alt="image" src="https://github.com/user-attachments/assets/e778add7-4f4e-4937-bc41-db060563e2a2">

### WebSocket for real-time notifications
* Users will be notified when corresponding action happens
<img width="673" alt="image" src="https://github.com/user-attachments/assets/c4ebea9b-e1a0-4e2c-8c94-a49a156dfcf3">

# Contact
Author: 羅書硯 Shu-Yen Lo

Email: sycw723@gmail.com

