# MedAI Assistant for TiDB Hackathon

Welcome to the **MedAI Assistant** project! This repository is designed for the TiDB Hackathon hosted by Devpost and leverages state-of-the-art technology to provide advanced healthcare insights using AI. Our application integrates a React frontend with a Django backend, incorporating Langchain AI agents and OpenAI’s GPT-4 to deliver valuable health information.

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Agents](#agents)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

MedAI Assistant is designed to assist users with healthcare-related information through AI-powered analysis. It offers features like heart rate data analysis, prescription interpretation, and medicine information retrieval. This project combines the power of modern frontend technologies with robust backend services and intelligent agents.

## Technologies Used

- **Frontend**: React
- **Backend**: Django
- **AI Integration**: Langchain AI agents, OpenAI GPT-4
- **Database**: TiDB (distributed SQL database)

## Agents

Our application includes the following AI agents:

- **HeartRateAnalyzerAgent**
  - **Name**: Heart_Rate_Analyzer
  - **Description**: Fetches the heart rate data of the user for the last 7 days.

- **PrescriptionAnalyzerAgent**
  - **Name**: Prescription_Analyzer
  - **Description**: Extracts medicine names and other meaningful information from a computer-generated prescription image provided by the user.

- **MedicineSearchAgent**
  - **Name**: Medicine_Search_Agent
  - **Description**: Retrieves detailed information about a medicine if the PrescriptionAnalyzerAgent cannot retrieve it.

## Frontend Setup

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Run the Development Server**:
   ```bash
   npm start
   ```
   The application will be accessible at `http://localhost:3000`.

## Backend Setup

1. **Navigate to the Backend Directory**:
   ```bash
   cd backend
   ```

2. **Create a Virtual Environment** (if using virtualenv):
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the Django Development Server**:
   ```bash
   python manage.py runserver
   ```
   The API will be accessible at `http://localhost:8000`.

## Contributing

We welcome contributions to enhance MedAI Assistant! If you have suggestions, improvements, or bug fixes, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for checking out MedAI Assistant. We hope you find it helpful and innovative! For any questions or support, feel free to open an issue or contact us.

Happy coding!

