# eCertificate Platform

**GAMKERS**

A production-focused Flask application for creating, managing, generating, publishing and distributing digital PDF eCertificates in bulk from Excel, XLS and CSV recipient lists.

## Overview

The eCertificate Platform is designed for colleges, institutions, organizations and event teams that need to generate large numbers of personalized certificates without manually creating each certificate.

Upload a recipient file, define the certificate title and description, preview the detected records, and generate an individual PDF certificate for every valid recipient. Each certificate receives a unique certificate number and a secure public URL that can be shared without requiring the recipient to sign in.

## Key Features

### Certificate Generation

- Bulk certificate generation from `.xlsx`, `.xls` and `.csv`
- Automatic detection of recipient columns
- Supports common column aliases for:
  - Recipient name
  - College / institution name
- Preview of the first 3 records before generation
- Displays total and valid record counts before processing
- Individual PDF generation for every recipient
- Unique certificate number for every generated certificate
- Secure random public token for every certificate
- Unique PDF filename for generated files
- Certificate descriptions support template variables:
  - `{name}`
  - `{college_name}`
  - `{certificate_number}`
  - `{date}`
- Batch-level generation status:
  - `pending`
  - `processing`
  - `completed`
  - `completed_with_errors`
  - `failed`
- Tracks generated and failed certificate counts

### Public Certificates

Every successfully generated certificate can be accessed through a public, no-login URL.

Recipients can:

- Open the certificate verification/view page
- View certificate information
- Download the generated PDF
- Access the PDF directly through its public link

This makes certificates easy to distribute through WhatsApp, email, websites, QR codes or other channels.

### Export

Generated batch data can be exported as:

- Excel (`.xlsx`)
- CSV (`.csv`)

Exports include:

- Recipient name
- College name
- Certificate number
- Certificate status
- Public certificate link

### Authentication & Security

- Sign in
- Public sign up
- Sign out
- Forgot password
- Single-use password reset tokens
- Password reset token expiry
- Password hashing through Werkzeug
- Flask-WTF CSRF protection
- Login-protected application areas
- Role-based authorization
- Request rate limiting
- Secure session cookie configuration
- Upload size limits
- Allowed file-extension validation

Password reset currently generates the reset link in the application log. An outbound email provider can be integrated later.

### User Roles

The application supports three roles:

| Role | Access |
| --- | --- |
| Admin | Full application administration, user management and certificate access |
| Manager | Certificate workflows and college management |
| Staff | Certificate generation and their permitted certificate workflows |

Public registration creates `staff` accounts. The first administrator should be created using the Flask CLI command.

### College Management

Authorized users can:

- View colleges
- Search colleges
- Add colleges
- Activate/deactivate colleges
- Delete colleges
- Associate generated certificates with colleges
- View college-related certificate statistics

When a certificate is generated, the application automatically matches the recipient's college with an existing college record or creates the college record when necessary.

### Dashboard

The authenticated dashboard provides application-level certificate analytics, including:

- Total certificates
- College count
- Certificate generation activity
- College-wise certificate statistics
- Recent certificate/batch information

### Profile Management

Authenticated users can:

- View and update profile information
- Change password
- Delete their account

## Technology Stack

### Backend

- Python `>=3.12`
- Flask `3.1.2`
- Flask-Login `0.6.3`
- Flask-WTF `1.2.2`
- Flask-Limiter `3.12`
- PyMySQL `1.1.2`
- python-dotenv `1.1.1`

### Data & Files

- pandas `2.3.2`
- openpyxl `3.1.5`
- xlrd `2.0.1`
- ReportLab `4.4.3`

### Production

- Gunicorn `23.0.0`
- MySQL / MariaDB
- Tailwind CSS `v4`
- Node.js / npm for CSS compilation

The application uses **PyMySQL directly** for database access. It does not require a SQLAlchemy database URL.

## Project Structure

```text
eCertificate-Python/
├── app/
│   ├── auth/
│   │   ├── forms.py
│   │   ├── routes.py
│   │   └── services.py
│   ├── certificates/
│   │   ├── forms.py
│   │   ├── generator.py
│   │   ├── routes.py
│   │   ├── services.py
│   │   └── validators.py
│   ├── colleges/
│   │   └── routes.py
│   ├── dashboard/
│   │   └── routes.py
│   ├── main/
│   │   └── routes.py
│   ├── models/
│   │   ├── audit_log.py
│   │   ├── certificate.py
│   │   ├── certificate_batch.py
│   │   ├── college.py
│   │   └── user.py
│   ├── profile/
│   │   ├── forms.py
│   │   └── routes.py
│   ├── users/
│   │   ├── forms.py
│   │   ├── routes.py
│   │   └── services.py
│   ├── utils/
│   │   ├── decorators.py
│   │   ├── helpers.py
│   │   ├── security.py
│   │   └── storage.py
│   ├── static/
│   │   ├── css/
│   │   │   └── app.css
│   │   ├── js/
│   │   │   ├── app.js
│   │   │   ├── certificate.js
│   │   │   └── dashboard.js
│   │   ├── templates/
│   │   └── ...
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   ├── extensions.py
│   └── __init__.py
├── database/
│   └── database.sql
├── migrations/
├── tailwind/
│   └── input.css
├── .env.example
├── compress.py
├── pyproject.toml
├── requirements.txt
├── run.py
└── wsgi.py
```

## Requirements

Before installation, make sure the system has:

- Python 3.12+
- MySQL or MariaDB
- Node.js and npm if CSS needs to be rebuilt
- A database user with permission to create/read/write the application tables

## Installation

### 1. Clone or extract the project

```bash
git clone <repository-url>
cd eCertificate-Python
```

If the project was downloaded as a ZIP, extract it and open the project directory.

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

**Windows**

```bash
copy .env.example .env
```

**Linux / macOS**

```bash
cp .env.example .env
```

Edit `.env` and configure at least:

```env
SECRET_KEY=change-this-to-a-long-random-secret

DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=ecertificate
DB_USERNAME=root
DB_PASSWORD=
```

The application intentionally uses separate database settings:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USERNAME`
- `DB_PASSWORD`

No database URL is required.

## Database Setup

Create the MySQL/MariaDB database first.

Example:

```sql
CREATE DATABASE ecertificate
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Then import:

```bash
database/database.sql
```

For MySQL CLI:

```bash
mysql -u root -p ecertificate < database/database.sql
```

You can also import `database/database.sql` through HeidiSQL, phpMyAdmin or another MySQL administration tool.

After importing the schema, verify that the `.env` database values point to the same database.

## Create the First Administrator

Public registration creates staff accounts. Create the initial administrator through the Flask CLI:

```bash
flask create-admin
```

The command prompts for:

- Name
- Email
- Password
- Password confirmation

If the email already exists, the command promotes that account to admin, activates it, verifies it and resets its password.

## Run the Application

### Development

```bash
flask run
```

Or:

```bash
python run.py
```

The development application is configured for the local Flask workflow.

### Production with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

For a production deployment, place the application behind a reverse proxy such as Nginx or Apache and enable HTTPS.

When HTTPS is enabled, update the cookie settings in `.env`:

```env
SESSION_COOKIE_SECURE=true
REMEMBER_COOKIE_SECURE=true
```

## CSS Build

The project uses a locally compiled Tailwind CSS build. The application loads:

```text
app/static/css/app.css
```

No Tailwind CDN is required at runtime.

The source stylesheet is:

```text
tailwind/input.css
```

If templates are changed and new Tailwind utility classes are introduced, rebuild the compiled stylesheet.

Install the Node dependencies and build:

```bash
npm install
npm run build:css
```

For development/watch mode:

```bash
npm run watch:css
```

The compiled CSS should remain at:

```text
app/static/css/app.css
```

## Certificate Generation Workflow

The normal workflow is:

```text
Sign in
   ↓
Generate eCertificate
   ↓
Upload XLSX / XLS / CSV
   ↓
Validate and detect recipient columns
   ↓
Preview first 3 records
   ↓
Enter certificate title + description
   ↓
Process batch
   ↓
Generate individual PDFs
   ↓
Assign certificate numbers
   ↓
Create public certificate tokens
   ↓
Save certificate records
   ↓
Show generated certificates
   ↓
Export names / colleges / numbers / links
```

## Supported Template Variables

Certificate descriptions can contain:

- `{name}`
- `{college_name}`
- `{certificate_number}`
- `{date}`

Example:

```text
This certificate is proudly presented to {name} of {college_name}
in recognition of their participation in the event.
Certificate No: {certificate_number}
Date: {date}
```

Each recipient receives personalized certificate content.

## Supported Input Files

The generator accepts:

- `.xlsx`
- `.xls`
- `.csv`

The uploaded spreadsheet should contain recipient and college/institution information.

The application detects common column aliases instead of requiring one exact column spelling.

Typical examples include:

```text
name
student_name
student
recipient
recipient_name
```

and:

```text
college_name
college
institution
institution_name
university
```

The exact accepted aliases are handled by the certificate validation layer.

## Storage

Generated and temporary files are stored outside the application code under:

```text
storage/
├── uploads/
├── generated/
└── temp/
```

The paths can be changed through `.env`:

```env
UPLOAD_FOLDER=storage/uploads
GENERATED_FOLDER=storage/generated
TEMP_FOLDER=storage/temp
```

The directories are automatically created during application startup.

For production deployments, make sure the application process has read/write permissions for these directories.

## Configuration Reference

Important environment variables:

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Flask application secret |
| `DB_HOST` | MySQL/MariaDB host |
| `DB_PORT` | Database port |
| `DB_NAME` | Database name |
| `DB_USERNAME` | Database username |
| `DB_PASSWORD` | Database password |
| `DB_CONNECT_TIMEOUT` | Database connection timeout |
| `DB_READ_TIMEOUT` | Database read timeout |
| `DB_WRITE_TIMEOUT` | Database write timeout |
| `SESSION_COOKIE_SECURE` | Secure session cookie |
| `SESSION_COOKIE_HTTPONLY` | HTTP-only session cookie |
| `SESSION_COOKIE_SAMESITE` | SameSite session policy |
| `REMEMBER_COOKIE_SECURE` | Secure remember-me cookie |
| `REMEMBER_COOKIE_HTTPONLY` | HTTP-only remember-me cookie |
| `REMEMBER_COOKIE_SAMESITE` | SameSite remember-me policy |
| `MAX_CONTENT_LENGTH` | Maximum request/upload size |
| `UPLOAD_FOLDER` | Uploaded source files |
| `GENERATED_FOLDER` | Generated PDF storage |
| `TEMP_FOLDER` | Temporary upload storage |
| `ALLOWED_EXTENSIONS` | Accepted spreadsheet extensions |
| `COMPANY_NAME` | Company/application name |
| `COMPANY_EMAIL` | Company contact email |
| `COMPANY_PHONE` | Company contact phone |
| `COMPANY_ADDRESS` | Company address |
| `RATELIMIT_STORAGE_URI` | Flask-Limiter storage backend |

## Application Routes

Main public routes:

```text
/
```

Authentication:

```text
/auth/signin
/auth/signup
/auth/forgot-password
/auth/reset-password/<token>
/auth/signout
```

Dashboard:

```text
/dashboard/
```

Certificates:

```text
/certificates/generate
/certificates/generate/process
/certificates/generated/<batch_id>
/certificates/export/<batch_id>/<export_format>
/certificates/download/<certificate_id>

/certificates/public/<token>
/certificates/public/<token>/pdf
/certificates/public/<token>/download
```

Users:

```text
/users/
/users/create
/users/edit/<user_id>
/users/toggle/<user_id>
```

Colleges:

```text
/colleges/
/colleges/create
/colleges/toggle/<college_id>
/colleges/delete/<college_id>
```

Profile:

```text
/profile/
/profile/change-password
/profile/delete-account
```

## Security Notes

Before production deployment:

- Replace the default `SECRET_KEY` with a long cryptographically random value.
- Use a dedicated database user instead of the MySQL root account.
- Use a strong database password.
- Enable HTTPS.
- Set secure cookies to true when serving over HTTPS.
- Keep generated/storage directories protected from direct unintended filesystem access.
- Review Flask-Limiter storage configuration for multi-worker production deployments.
- Do not commit `.env` or production secrets to source control.
- Keep dependencies updated and review security advisories regularly.
- Back up the MySQL database and generated certificate storage.

## Password Reset

The password reset flow uses:

- Secure reset tokens
- Hashed token storage
- Single-use reset tokens
- One-hour token expiry

No external email provider is configured by default.

Until an email service is integrated, the reset URL is written to the Flask application log. The email integration point is located in:

```text
app/auth/routes.py
```

## Production Deployment

A typical deployment architecture is:

```text
Internet
   ↓
HTTPS / Reverse Proxy
   ↓
Gunicorn
   ↓
Flask Application
   ↓
PyMySQL
   ↓
MySQL / MariaDB
```

Generated certificates and uploaded files remain in the configured storage directories.

For cPanel or other hosting environments, configure the Python application to use the project's WSGI entry point:

```text
wsgi:app
```

and ensure the server uses Python 3.12+ with all dependencies installed.

## Troubleshooting

### Database connection errors

Verify:

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
```

Make sure the database exists and the configured user can access it.

### CSS looks unstyled

Rebuild the stylesheet:

```bash
npm install
npm run build:css
```

Then confirm that this file exists and is updated:

```text
app/static/css/app.css
```

### Upload rejected

Check:

```env
ALLOWED_EXTENSIONS=xlsx,xls,csv
```

and:

```env
MAX_CONTENT_LENGTH=16777216
```

The uploaded file must use one of the configured extensions and remain within the configured request size.

### Reset link not received by email

The project does not include an outbound email provider by default. Check the Flask application log for the generated reset link.

## License

This project is proprietary software developed for GAMKERS.

Unauthorized redistribution, resale or reuse of the application source code is not permitted without permission from the copyright owner.

## Company

GAMKERS

eCertificate Platform — digital certificate generation, management and distribution.