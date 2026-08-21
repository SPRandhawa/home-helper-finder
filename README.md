# 🏠 Home Helper Finder

> A secure platform designed to connect customers with home helpers through verified profiles, location-based services, service requests, and smart assistance.

## 📌 About the Project

**Home Helper Finder** is a college project developed to provide a platform where customers can find suitable home helpers such as maids and other domestic service providers.

The system is designed with a focus on:

* 👤 Customer and Helper accounts
* 🔐 Secure authentication
* 🪪 Manual Aadhaar-based verification
* 📍 Location and map integration
* 📏 Distance, route and estimated travel information
* 📩 Customer-helper request system
* ✅ Accept/Reject workflow
* 🔔 Email/SMS notifications
* ⭐ Reviews and ratings
* 🤖 Expandable chatbot assistant
* 📱 Responsive design for different devices
* 🌐 Online and limited offline/PWA functionality
* 👑 Administrative management

---

## ✨ Main Features

### 👤 Customer

Customers can:

* Create an account
* Log in securely
* Complete their profile
* Search for helpers
* Filter helpers according to available criteria
* View helper profiles
* View location information
* Send service requests
* Receive request acceptance/rejection notifications
* View reviews and ratings
* Access helper details after a successful connection

### 👩‍🔧 Helper

Helpers can:

* Register on the platform
* Provide personal and professional information
* Upload a recent profile photograph
* Upload an Aadhaar photograph for verification
* Specify skills and working hours
* Wait for administrative verification
* Receive customer requests
* Accept or reject requests
* Receive appropriate notifications
* Manage permitted profile information

### 🪪 Verification

Helper accounts are subject to **manual administrative verification**.

The verification workflow is:

```text
Helper Registration
        ↓
Aadhaar + Profile Submission
        ↓
Waiting for Approval
        ↓
Admin Review
        ↓
Approved / Rejected
        ↓
Notification
```

Only approved helpers are made available for customer discovery.

> This project does not claim to provide official UIDAI Aadhaar authentication. Aadhaar documents are handled as part of the project's administrative verification workflow.

---

## 🗺️ Location & Maps

The project is designed to integrate map functionality for:

* Helper location
* Customer location
* Distance calculation
* Route information
* Estimated travel time

Location data may use geographical coordinates (latitude and longitude) together with the addresses supplied by users.

---

## 🤖 Chatbot

The project contains a small expandable chatbot assistant.

The initial chatbot is designed to answer predefined questions.

If a question is not currently available:

```text
User asks question
        ↓
System checks stored questions
        ↓
Answer found?
   ↙          ↘
 YES          NO
 ↓             ↓
Answer       Save question
              ↓
          Admin reviews
              ↓
         Admin adds answer
              ↓
      Future users receive answer
```

This architecture allows the chatbot to be expanded in the future.

---

## 📩 Contact System

The Contact page allows visitors to submit:

* Name
* Email address
* Query/message

Submitted queries are stored for administrative review.

The administrator can respond to the submitted email address using the project's configured official/company email identity rather than exposing a personal email address.

---

## 🔄 Request System

The customer-helper interaction follows a request-based workflow.

```text
Customer
   ↓
Select Helper
   ↓
Send Request
   ↓
Helper Receives Request
   ↓
Accept / Reject
   ↓
Customer Receives Notification
```

If the helper accepts:

> The customer is informed that the request has been accepted.

If the helper rejects:

> The customer is informed that the helper declined the request and can choose another helper.

---

## 🔐 Privacy & Contact Protection

The application is designed to avoid unnecessarily exposing personal phone numbers.

Instead of directly displaying phone numbers, the system can provide controlled communication functionality through the application's interface.

---

## 📱 Responsive & Offline Support

The application is intended to work across:

* Desktop computers
* Laptops
* Tablets
* Mobile devices

The project also aims to provide limited offline functionality through Progressive Web App (PWA) technologies where appropriate.

---

## 🛠️ Technology Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Backend         | Python / Django           |
| Frontend        | HTML / CSS / JavaScript   |
| Database        | SQLite during development |
| Maps            | Google Maps Platform      |
| Authentication  | Django Authentication     |
| Email           | SMTP / Email Service      |
| Offline Support | PWA technologies          |
| Version Control | Git / GitHub              |

---

## 📂 Project Structure

The final structure may include modules similar to:

```text
home-helper-finder/
│
├── manage.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
├── helpers/
├── customers/
├── requests/
├── chatbot/
├── contact/
├── maps/
├── templates/
├── static/
└── media/
```

The exact structure may change during development.

---

# 👥 Project Team

This project is being developed as a **two-person college project**.

**Developers:**

* SP Randhawa
* Satinder Kaur

---

# 📜 Copyright & Ownership

**Copyright © 2026 SP Randhawa and Project Partner. All Rights Reserved.**

This repository and its contents are proprietary project work.

The source code, documentation, designs, database structures, original graphics, chatbot logic, workflows, and other original materials contained in this repository may not be:

* Copied
* Reproduced
* Modified
* Republished
* Redistributed
* Rebranded
* Commercially used
* Submitted as another person's academic project
* Used as the basis of another project

without **prior written permission from the project owners**.

---

# 🚫 Usage Restrictions

No permission is granted to use this project or its source code for:

1. Academic submissions by other students.
2. Commercial products or services.
3. Personal projects that reproduce substantial portions of this project.
4. Redistribution or publication of the source code.
5. Creation of derivative projects based substantially on this work.
6. Removal or alteration of copyright notices.
7. Claiming this work as someone else's work.

Viewing the repository does **not** grant permission to copy or reuse the project.

---

# 📄 License

This project is **NOT open source**.

Unless explicit written permission is provided by the project owners, **all rights are reserved**.

The absence of a separate open-source license does not grant permission to copy, modify, distribute, or reuse this work.

See [`LICENSE`](LICENSE) for the complete proprietary license terms.

---

# ⚠️ Third-Party Services

This project may use third-party services and technologies such as Google Maps Platform and email service providers.

Those services are governed by their respective terms, licenses, and policies.

This copyright notice applies to the **original project code, documentation, designs, and materials created by the project team**, not to third-party software or services.

---

# 📚 Educational Purpose

This project is developed as part of an academic/educational project.

The application is intended as a demonstration of software development, database management, authentication, verification workflows, location-based functionality, and web application design.

---

# 🔮 Future Improvements

Possible future enhancements include:

* AI-powered chatbot
* Real-time messaging
* Advanced helper recommendation
* Online payments
* Improved location tracking
* Mobile application
* Advanced identity verification
* Multilingual support
* Emergency/help features
* Advanced notification system

---

# ⚖️ Disclaimer

The platform is designed to facilitate connections between customers and helpers.

The project itself does not guarantee the conduct, qualifications, availability, or quality of services provided by individual helpers.

Users should independently verify information and exercise appropriate caution before engaging in real-world services.

---

## 🔒 Proprietary Project

**© 2026 SP Randhawa & Project Partner — All Rights Reserved.**

**Unauthorized copying, reproduction, redistribution, or use is prohibited.**
