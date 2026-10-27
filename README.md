# 🎓 VoiceUp — AI-Powered Student Feedback API

A RESTful student feedback management API built with **Python, Django REST Framework, and Google Gemini AI**, featuring feedback CRUD operations, token authentication, custom permissions, feedback summaries, and AI-powered sentiment and category classification.

## 📌 About the Project

VoiceUp helps students submit feedback about their departments and enables automatic classification of feedback using Google Gemini AI.

The API identifies the sentiment of each feedback entry and categorizes it into areas such as faculty, academics, infrastructure, administration, and facilities. It also provides summary statistics grouped by sentiment and category.

The project demonstrates REST API development, authentication, authorization, CRUD operations, serializer validation, Django ORM aggregation, and third-party AI integration.

## ✨ Features

- **User Registration:** Create an account using a username, email, and password.
- **Token Authentication:** Authenticate protected API requests using DRF tokens.
- **User Profile:** Retrieve the authenticated user's details.
- **Feedback Management:** Create and list student feedback records.
- **Feedback CRUD:** Retrieve, update, and delete individual feedback records.
- **Custom Permissions:** Restrict individual feedback operations to the record owner.
- **AI-Powered Classification:** Use Google Gemini AI to classify feedback automatically.
- **Sentiment Analysis:** Classify feedback as positive, negative, neutral, or unknown.
- **Category Classification:** Categorize feedback as faculty, academics, infrastructure, administration, facilities, or other.
- **Feedback Summary:** Calculate sentiment-wise and category-wise feedback counts.
- **Department Validation:** Validate department input against supported department choices.
- **Feedback Text Validation:** Reject empty feedback and feedback shorter than the configured minimum length.
- **ModelSerializer:** Use Django REST Framework ModelSerializers to serialize model data and validate input.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| Django REST Framework | REST API development |
| Google Gemini API | AI-powered feedback classification |
| Django ORM | Database queries and aggregation |
| DRF Token Authentication | API authentication |
| ModelSerializer | Serialization and validation |
| python-dotenv | Environment variable management |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
voiceup_project/
├── voiceup_project/
│   ├── settings.py
│   └── urls.py
├── feedback/
│   ├── models.py
│   ├── views.py
│   ├── serializer.py
│   ├── permission.py
│   ├── ai_integration.py
│   └── urls.py
├── .env
├── .gitignore
├── APIDOC.http
├── manage.py
└── requirements.txt
```

*This is an illustrative structure based on the code shared. Confirm the actual directory and filenames against your repository.*

## ⚙️ Installation and Setup

### Prerequisites

- Python
- Git
- pip
- A Google Gemini API key for AI classification

### 1. Clone the repository

```bash
git clone https://github.com/thefarsin12-afk/voiceup_project.git
cd voiceup_project
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_supported_gemini_model
```

The AI integration reads `GEMINI_API_KEY` and optionally `GEMINI_MODEL` from environment variables.

Replace the placeholder values with your own configuration. Never commit API keys or other secrets to GitHub.

### 5. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Base URL:

`http://127.0.0.1:8000/api/`

## 🔐 Authentication

VoiceUp uses Django REST Framework authentication classes to protect API endpoints.

### Register a user

**Endpoint:** `POST /api/signup/`

Request body:

```json
{
  "username": "student1",
  "email": "student1@example.com",
  "password": "your_password"
}
```

The registration view uses Django's `create_user()` method to create the account with a hashed password.

### Sign in

**Endpoint:** `POST /api/signin/`

Request body:

```json
{
  "username": "student1",
  "password": "your_password"
}
```

Use valid credentials to authenticate. The exact response depends on the implementation of the sign-in view.

### Include the authentication token

For token-authenticated endpoints, include the following header:

```http
Authorization: Token your_authentication_token
```

The list and create feedback endpoints currently use Basic Authentication, while the individual feedback and summary endpoints use Token Authentication. Use the authentication method configured for each endpoint.

## 🔌 API Documentation

Base URL:

`http://127.0.0.1:8000/api/`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup/` | Register a new student |
| POST | `/signin/` | Sign in |
| GET | `/me/` | Retrieve authenticated user details |
| GET | `/feedback/` | List feedback records |
| POST | `/feedback/` | Create feedback |
| GET | `/feedback/<id>/` | Retrieve a feedback record |
| PUT | `/feedback/<id>/` | Update a feedback record |
| DELETE | `/feedback/<id>/` | Delete a feedback record |
| GET | `/feedback/summary/` | Retrieve feedback summaries |

Replace `<id>` with the ID of the feedback record.

### 1. Retrieve the authenticated user's profile

```http
GET /api/me/
Authorization: Token your_authentication_token
```

Returns the authenticated user's profile details according to the configured view.

### 2. List feedback records

```http
GET /api/feedback/
Authorization: Basic your_credentials
```

Returns feedback records using the configured serializer.

**Note:** The current list view retrieves all feedback records. Restricting the queryset by user or department would require additional filtering.

### 3. Create feedback

**Endpoint:** `POST /api/feedback/`

Headers:

```http
Content-Type: application/json
Authorization: Basic your_credentials
```

Request body:

```json
{
  "department": "ece",
  "feedback_text": "The classrooms are poorly maintained."
}
```

The authenticated user is assigned as the feedback owner automatically. Gemini AI classifies the feedback and the resulting sentiment and category are saved with the record.

Example classification:

```json
{
  "sentiment": "negative",
  "category": "infrastructure"
}
```

The example shows the AI classification values, not the complete API response.

### Supported departments

- `cse` — Computer Science
- `ece` — Electronics and Communication
- `eee` — Electrical and Electronics
- `me` — Mechanical
- `ce` — Civil
- `ai_ds` — AI and Data Science
- `other` — Other

### Supported sentiments

- `positive`
- `negative`
- `neutral`
- `unknown`

### Supported categories

- `faculty`
- `academics`
- `infrastructure`
- `administration`
- `facilities`
- `other`

### 4. Retrieve an individual feedback record

```http
GET /api/feedback/1/
Authorization: Token your_authentication_token
```

The custom owner permission is intended to allow access only when the authenticated user owns the record.

### 5. Update feedback

```http
PUT /api/feedback/1/
Content-Type: application/json
Authorization: Token your_authentication_token
```

Request body:

```json
{
  "department": "ece",
  "feedback_text": "The classrooms need better maintenance."
}
```

The serializer validates the submitted department and feedback text. The current update view saves the submitted fields; it does not automatically rerun Gemini classification.

### 6. Delete feedback

```http
DELETE /api/feedback/1/
Authorization: Token your_authentication_token
```

Deletes the selected feedback record.

**Implementation note:** The current delete view retrieves the record and deletes it without explicitly calling `check_object_permissions()`. Add that check to enforce the intended owner-only restriction consistently.

### 7. Feedback summary

```http
GET /api/feedback/summary/
Authorization: Token your_authentication_token
```

The summary API groups the authenticated user's feedback records by sentiment and category and counts the records in each group.

Example response:

```json
{
  "sentiment_summary": [
    {
      "sentiment": "negative",
      "sentiment_summary": 3
    },
    {
      "sentiment": "positive",
      "sentiment_summary": 2
    }
  ],
  "category_summary": [
    {
      "category": "infrastructure",
      "category_summary": 3
    },
    {
      "category": "faculty",
      "category_summary": 2
    }
  ]
}
```

*The values above are illustrative; actual results depend on stored feedback. The current view also needs a response for users with no feedback records.*

## 🤖 AI Integration

VoiceUp integrates Google Gemini AI using the Google Gen AI Python SDK.

When a student submits feedback, the AI integration:

1. Receives the feedback text.
2. Sends a classification prompt to Gemini.
3. Requests a JSON response containing sentiment and category.
4. Parses the returned JSON.
5. Saves the classification alongside the feedback record.

Example input:

```text
The classrooms are poorly maintained.
```

Example output:

```json
{
  "sentiment": "negative",
  "category": "infrastructure"
}
```

If the Gemini client is not configured, the current function returns `unknown` sentiment and `other` category as fallback values.

AI classifications may not always be correct. Production applications should validate AI output and handle API errors and malformed responses.

## 🗄️ Feedback Model

| Field | Description |
|---|---|
| `id` | Automatically generated feedback ID |
| `student` | Foreign key to the Django user |
| `department` | Department associated with the feedback |
| `feedback_text` | Student's feedback content |
| `sentiment` | AI-generated sentiment classification |
| `category` | AI-generated feedback category |
| `created_at` | Automatically recorded creation timestamp |

The `student` field associates each feedback record with its owner. The sentiment and category fields are configured as non-editable model fields and are populated by the AI integration when feedback is created.

## 🧪 Testing

The project includes `APIDOC.http` for testing API endpoints with the REST Client extension in Visual Studio Code.

Recommended test cases:

- Register a student and verify account creation.
- Test valid and invalid login credentials.
- Create feedback with valid department and text.
- Test blank department and blank feedback text.
- Test feedback shorter than the configured minimum length.
- Verify AI sentiment and category classification.
- Retrieve, update, and delete feedback records.
- Verify owner-only access to individual records.
- Check sentiment-wise and category-wise counts.
- Test behavior when Gemini is unavailable.
- Verify that unauthenticated requests are rejected.

## 🔒 Security

- Keep API keys and secret values in environment variables.
- Never commit `.env` files or real credentials.
- Use Django's password hashing for account creation.
- Protect API endpoints with authentication and permissions.
- Verify object ownership before retrieving, updating, or deleting individual records.
- Validate AI-generated output before saving it.
- Add suitable error handling for external API failures.

## 🚀 Future Improvements

- Add automatic reclassification when feedback is updated.
- Improve error handling for Gemini API failures.
- Return consistent responses when no feedback exists.
- Add filtering by department, sentiment, and category.
- Add pagination for large feedback lists.
- Add automated tests for authentication and permissions.
- Add OpenAPI/Swagger documentation.
- Build a frontend dashboard for feedback summaries.

## 👨‍💻 Author

**Muhammad Farsin M**

GitHub: https://github.com/thefarsin12-afk

## 📂 Repository

https://github.com/thefarsin12-afk/voiceup_project

---

*VoiceUp — Turning student feedback into structured insights with AI-powered classification.*
