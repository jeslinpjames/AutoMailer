import ollama
import csv
import subprocess
import multiprocessing
import urllib.parse

def clean_text(text):
    """Helper function to clean up the text by removing unnecessary characters."""
    return text.replace('**', '').strip()

def generate_email(name, job_description, details, expertise, result_queue):
    prompt = f"""
    Please generate a professional email with the following structure. It's crucial that the format matches exactly as described below:
    
    1. **Subject:** A concise and relevant subject line for an email introducing a candidate for the {job_description} position at the company represented by {name}.
    
    2. **Body:** 
    - **Introduction:** Begin with a friendly greeting, mention my name and that I am from [Your Company Name]. 
    - **Main Content:** Clearly state that I am reaching out because we have a highly qualified candidate who would be an excellent fit for the {job_description} role. Mention that they specialize in {expertise} and that I would like to discuss further or arrange an interview.
    - **Closing:** End with a warm closing, inviting further communication, and expressing optimism about potential collaboration.
    
    This is the role of the person {name}: {details}
    
    The response **must** be formatted clearly with the subject prefixed by 'Subject:' and the body prefixed by 'Body:'. It is very important that this format is followed.
    """

    while True:
        response = ollama.chat(
            model='llama3.1',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        if response and "message" in response and response['message']['content']:
            email_text = response['message']['content']
            
            try:
                # Attempt to parse the subject and body from the response
                subject = email_text.split("Subject:")[1].split("Body:")[0].strip()
                body = email_text.split("Body:")[1].strip()
                
                # If parsing succeeds, exit the loop
                subject = clean_text(subject)
                body = clean_text(body)
                result_queue.put((subject, body))
                break
            except IndexError:
                # If parsing fails, inform that we are retrying
                print("Unexpected format in the response. Retrying...")
        else:
            print(f"Failed to generate email for {name}. Retrying...")

def open_mail_app(to_email, subject, body):
    """Function to open the mail client with the subject and body."""
    # Properly encode the subject and body for the mailto link
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)
    
    # Open the mail client with the subject and body
    command = f'start "" "mailto:{to_email}?subject={subject_encoded}&body={body_encoded}"'
    subprocess.run(command, shell=True)

def email_generation_process(csv_file, result_queue):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            name = row['name']
            job_description = row['job description']
            details = row['details']
            expertise = row['expertise']
            to_email = row['email']
            
            # Generate the email and save it to the queue
            generate_email(name, job_description, details, expertise, result_queue)
    
    # Indicate that generation is done by putting a sentinel value in the queue
    result_queue.put(None)

def email_sending_process(result_queue, csv_file):
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            to_email = row['email']
            item = result_queue.get()
            if item is None:
                break  # Sentinel value to stop the process

            subject, email_body = item
            if subject and email_body:
                # Open the mail client with pre-populated email fields
                print(f"Preparing email for {to_email}...")
                open_mail_app(to_email, subject, email_body)
                
                # Wait for the user to review the email before moving on
                input("Review the email and press Enter to prepare the next one...")

if __name__ == "__main__":
    # Path to your CSV file
    file_path = "sample_contacts.csv"
    
    # Create a queue for communication between processes
    email_queue = multiprocessing.Queue()

    # Start the email generation process
    generation_process = multiprocessing.Process(target=email_generation_process, args=(file_path, email_queue))
    
    # Start the email generation process in a separate process
    generation_process.start()

    # Run the email sending process in the main process
    email_sending_process(email_queue, file_path)

    # Wait for the generation process to finish
    generation_process.join()
