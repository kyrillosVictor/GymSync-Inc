# GymSync

![Gym Management System Logo](project_logo.jpg)

A web-based application built using Django and PostgreSQL to manage gym memberships, classes, trainers, and other related operations. This project aims to simplify the administration and operational tasks of gym management by providing an easy-to-use interface for gym owners and staff.

## Features

- **Membership Management**: Track and manage gym memberships, including membership types, renewal dates, and member details.
- **Class Scheduling**: Manage class schedules, including assigning trainers and managing participant lists.
- **Trainer Management**: Keep records of trainers, their expertise, and the classes they lead.
- **Attendance Tracking**: Monitor member attendance for classes and overall gym visits.
- **Payment Management**: Track payments for memberships and other gym services.
- **Admin Interface**: Use Django’s built-in admin interface for easy management of the system’s data.

## Technologies Used

- **Frontend**: Bootstrap 5 for a responsive and modern UI.
- **Backend**: Django 3 for building the web application.
- **Database**: PostgreSQL for storing all data securely.
- **Authentication**: Django’s built-in authentication system to manage user roles and permissions.

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Virtualenv (optional but recommended)

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Black-Dragon-Kalameet/Gymsystem.git
   cd Gymsystem
   ```

2. **Create a Virtual Environment and Activate It**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Configure the Database**
   - Update the `DATABASES` setting in `settings.py` with your PostgreSQL database credentials.

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open your browser and go to `http://127.0.0.1:8000/` to view the application.
   - Admin interface: `http://127.0.0.1:8000/admin/`

## Usage

- **Admin Interface**: After logging in as the superuser, you can manage members, trainers, classes, and other data through Django’s admin interface.
- **User Interface**: Members can view their membership details, class schedules, and make payments online.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/mit) for more details.
