# Automated Email Generation and Sending

This project automates the generation and sending of professional emails based on details provided in a CSV file. It uses the `ollama` Python library to interact with the LLM (Llama 3.1) and generate emails following a specified format. The emails are then opened in the default mail client, allowing for manual review before sending.

## Features

- **Automated Email Generation:** Emails are generated based on details provided in a CSV file, following a structured format.
- **Email Review and Sending:** Each generated email is opened in the mail client for manual review and can be sent after confirmation.
- **Background Generation:** While you are reviewing and sending an email, the script continues to generate the next emails in the background, ensuring a smooth workflow.
- **Retry Mechanism:** If the generated email doesn't match the expected format, the script will retry until a correctly formatted email is obtained.
- **Customizable Prompt:** The prompt used to generate the email can be easily updated to meet your specific needs.

## Requirements

- Python 3
- `ollama` Python library
- A CSV file containing the necessary data (e.g., name, job description, details, email)

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/jeslinpjames/AutoMailer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd AutoMailer
    ```
3. Install the required dependencies:
    ```bash
    pip install ollama
    ```

## How to Use

1. **Prepare Your CSV File:**
   - Ensure your CSV file contains the following columns:
     - `name`: The name of the person you are addressing.
     - `job description`: The job title or description relevant to the email.
     - `details`: Additional details to be included in the email.
     - `email`: The recipient's email address.

   Here’s an example of how your `sample_contacts.csv` might look:

    ```csv
    name,job description,details,email
    John Doe,Software Engineer,We have an experienced developer who has worked on multiple large-scale projects.,johndoe@example.com
    Jane Smith,Project Manager,Our candidate has over 10 years of experience in managing complex projects in various industries.,janesmith@example.com
    Mike Johnson,Data Scientist,We can offer a skilled data scientist with expertise in machine learning and data analysis.,mikejohnson@example.com
    Emily Davis,UX Designer,Our UX designer has a strong portfolio with a focus on user-centered design and usability.,emilydavis@example.com
    ```

2. **Update the Prompt:**
   - The prompt in the `generate_email` function can be updated to better match your specific needs. Ensure that the format requirements are clearly stated in the prompt to guide the LLM to produce the desired output.

3. **Run the Script:**
   - Execute the script to start generating and sending emails:
    ```bash
    python AutoMailer.py
    ```

4. **Review and Send Emails:**
   - The script will generate an email for each row in the CSV file, open it in your mail client, and wait for you to review and confirm before moving on to the next one.
   - **Background Email Generation:** While you are reviewing and sending an email, the script continues to generate the next emails in the background. This ensures that the next email is ready to review as soon as you finish with the current one, making the process efficient and seamless.
