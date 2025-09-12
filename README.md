# Online Shopping Mall

An e-commerce web application for electronics & consumer goods built using **Django**, **Bootstrap**, and **SQLite**.  
This system enables customers to register, browse, search, and purchase products, while vendors can manage products, orders, and recommendations.  

---

## 📌 Project Information
- **Course**: COMP321 – Information System Implementation  
- **Academic Year**: 2023/24 (2nd Semester)  
- **Group**: 12  
- **Supervisor**: Andrew Sio  
- **Assessor**: Philip Lei  
- **Submission Date**: Apr 17, 2024  

**👨‍💻 Group Members**
- Wai Kei Lap (P2104180)  
- Leong Chin Hou (P2104621)  
- Mak Cheok In (P2104308)  
- Lee Ling Yu (P2104521)  

---

## 🚀 Features

### Customer
- Register, login, and manage account  
- Browse product catalog with search & filters  
- Product detail view with multiple photos  
- Shopping cart management (add, update, remove items)  
- Checkout & order creation  
- Order history with status tracking (pending, shipped, cancelled, on hold)  
- Internationalization (English/Chinese switch)  
- Personalized product recommendations (by brand, technology, top-selling, new items)  

### Vendor/Admin
- Add, edit, remove products  
- Upload & manage multiple product images  
- View and process customer orders  
- Manage order statuses  
- Admin dashboard with product & order management tools  

---

## 🏗️ System Architecture
- **Frontend**: HTML, CSS, JavaScript, Bootstrap  
- **Backend**: Python (Django framework)  
- **Database**: SQLite  
- **Version Control**: GitHub  

**Three-tier architecture**  
1. **Presentation Layer** – User interface (browser-based)  
2. **Application Layer** – Business logic (Django server-side)  
3. **Data Layer** – SQLite database for persistence  

---

## 📊 Data Model
- **Customer** – ID, name, email, password, shipping address  
- **Product** – ID, name, price, brand, technology, description, cover image, active status  
- **Order** – ID, customer, date, shipping/cancel status, items  
- **OrderItem** – Links products and orders with quantity & pricing  
- **Image** – Belongs to a product, with multiple images  

(Relationships normalized to reduce redundancy — handled via entity associations.)  

---

## 🧪 Software Quality
- Requirement-based testing for all critical features (e.g., login, register, checkout, order cancellation)  
- Data validation and error-checking on inputs  
- Secure password storage & encrypted transmission  
- Controlled access rights (separating customer vs vendor login)  

---

## 📋 Project Management
- **Team Charter**: Defined roles, weekly meetings, and consensus-based decision-making  
- **Time Management**: Activity list, Precedence Diagram (PDM), Gantt chart scheduling  
- **Risk Management**:  
  - *Data breach*: security audits & encryption  
  - *Technical failures*: backups, updates, contingency plans  
  - *Scope creep*: clear requirements & change management  

### Job Distribution
- **Wai Kei Lap (55%)** – Scheduling, data modelling, coding, testing, major writing (Ch. 3, 4, 6)  
- **Leong Chin Hou (15%)** – Report writing (Ch. 2, 5)  
- **Mak Cheok In (15%)** – Report writing (Ch. 1, 7), data modelling  
- **Lee Ling Yu (15%)** – Coding (Block A), testing, proofreading  

---

## 📈 Project Outcomes
- Functional online shopping mall prototype  
- Secure user & vendor workflows  
- Accessibility (multilingual support)  
- Personalized recommendation system  
- Demonstrates system design, implementation & software quality assurance  

---

## 🔮 Limitations & Future Work
- Need dedicated team to update product info regularly  
- Introduce automated data update mechanisms  
- Expand feature set via **open-source contributions** to enhance innovation and developer collaboration  

---

## 📚 References
- [Django](https://www.djangoproject.com/)  
- [Bootstrap](https://getbootstrap.com/)  
- [SQLite](https://www.sqlite.org/)  
- Additional references: research articles on requirements analysis, software quality, and open-source collaboration (see report)  