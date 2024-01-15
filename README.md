
# CYSA+ Question SMS Application

## Project Overview
This Flask application integrates with the OpenAI API to generate CYSA+ multiple-choice questions and send them via SMS using the Vonage API. Users can respond to the SMS with their answers, and the application validates these responses using OpenAI and sends back a confirmation SMS indicating whether the response was correct or incorrect. Open-AI API does come witha cost it may be a few cents but do want to mention that, Vonage API has 

## Technologies Used
- **Python**: The primary programming language used for the backend.
- **Flask**: A lightweight WSGI web application framework in Python, used for setting up the server and endpoints.
- **OpenAI API**: Used for generating CYSA+ multiple-choice questions.
- **Vonage (formerly Nexmo) API**: Used for sending and receiving SMS messages.
- **ngrok**: (Optional) For exposing the local server to the internet, useful in development and testing phases.

## Setup and Installation
1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Ensure Python is installed, then install Flask, OpenAI, and Vonage Python libraries.
   ```
   pip install Flask openai vonage
   ```
3. **Environment Variables**: Set up the following environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key.
   - `VONAGE_API_KEY`: Your Vonage API key.
   - `VONAGE_API_SECRET`: Your Vonage API secret.
   - `VONAGE_PHONE_NUMBER`: Your Vonage virtual phone number.
   - `TARGET_PHONE_NUMBER`: The target phone number for sending and receiving SMS.

4. **Run the Application**: Start the Flask server.
   ```
   python app.py
   ```

## Usage
Once the server is running, the application will:
- Generate CYSA+ questions and send them to the specified target phone number via SMS.
- Receive SMS responses from users.
- Validate the responses and send a follow-up SMS indicating if the answer was correct or incorrect.

### Executing the `/send_sms` Endpoint
To trigger the sending of a CYSA+ question via SMS:
1. Ensure the Flask server is running.
2. Access the `/send_sms` endpoint via a browser or a tool like curl:
   ```
   curl http://localhost:5000/send_sms
   ```
   This will generate and send a CYSA+ question to the target phone number set in your environment variables.

### Setting Up a Cronjob
To execute the `/send_sms` endpoint every two hours from Monday to Friday between 9 AM to 4 PM EST, follow these steps:

#### Create a Script to Call the Endpoint
1. Create a file named `call_endpoint.sh`.
2. Add the following content to it:
   ```bash
   #!/bin/bash
   curl http://localhost:5000/send_sms
   ```
3. Make the script executable:
   ```bash
   chmod +x call_endpoint.sh
   ```

#### Schedule the Cronjob
1. Open your crontab file:
   ```bash
   crontab -e
   ```
2. Add the following line to the crontab file:
   ```cron
   0 9-16/2 * * 1-5 /path/to/call_endpoint.sh
   ```
   - This schedule runs the script every 2 hours from 9 AM to 4 PM EST, Monday to Friday.

#### Important Notes
- Ensure your server's time zone is correctly set to EST.
- Adjust the URL in the script if your Flask application is running on a different URL.
- Test the script manually before relying on the cronjob.

## Expansion and Further Development
- **Database Integration**: For production use, integrate a database to store questions and answers persistently.
- **User Authentication**: Implement user authentication to handle multiple users with personalized experiences.
- **Advanced Answer Parsing**: Enhance the `extract_correct_answer` function for more complex parsing logic.
- **Web Interface**: Develop a web interface for users to interact with the application beyond SMS.
- **Analytics and Reporting**: Add functionality to track user performance and generate reports.
- **Scaling**: Prepare the application for scaling and handling high volumes of messages.

## Troubleshooting
- **SMS Delivery Issues**: Check the Vonage dashboard for logs and error messages.
- **API Limitations**: Be aware of rate limits for both OpenAI and Vonage APIs.
- **Debugging**: Utilize logs and debugging tools to trace any issues in the application.

## License
 MIT License


---

> This project is a demonstration of integrating various APIs with a Flask application to create an interactive SMS-based quiz system.
