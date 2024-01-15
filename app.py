from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import vonage

questions_and_answers = {}

app = Flask(__name__)

# Instantiate the OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Vonage configuration
vonage_client = vonage.Client(key=os.environ.get('VONAGE_API_KEY'),
                             secret=os.environ.get('VONAGE_API_SECRET'))
sms = vonage.Sms(vonage_client)


def extract_correct_answer(question_content):
    """
    Extracts the correct answer from the CYSA+ question content.
    Implement the logic based on how OpenAI formats the answers.
    """
    # Placeholder logic: Modify this to suit your answer format
    correct_answer = "A"  # Replace with actual extraction logic
    return correct_answer


@app.route('/')
def index():
    print("Hit /send_sms to trigger a SMS")
    return "Message displayed in the command line. Check your console."



@app.route('/send_sms', methods=['GET'])
def send_sms():
    # Generate a CYSA+ multiple-choice question using OpenAI
    try:
        question_prompt = "Create a multiple-choice question for the CYSA+ exam covering cybersecurity concepts:"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": question_prompt}]
        )
        question_content = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    correct_answer = extract_correct_answer(question_content)

    phone_number = os.environ.get('TARGET_PHONE_NUMBER')
    questions_and_answers[phone_number] = {'question': question_content, 'answer': correct_answer}

    try:
        responseData = sms.send_message({
            "from": os.environ.get('VONAGE_PHONE_NUMBER'),
            "to": phone_number,
            "text": question_content,
        })

        if responseData["messages"][0]["status"] == "0":
            return jsonify({"message": "Question sent successfully.", "message_id": responseData["messages"][0]["message-id"]})
        else:
            return jsonify({"error": responseData['messages'][0]['error-text']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@app.route('/incoming_sms', methods=['GET', 'POST'])
def incoming_sms():
    sender = request.form.get('msisdn') if request.method == 'POST' else request.args.get('msisdn')
    user_response = request.form.get('text') if request.method == 'POST' else request.args.get('text')

    # Retrieve the original question
    question_data = questions_and_answers.get(sender, {})
    original_question = question_data.get('question', '')

    # Combine the original question and user's response into a query
    query = f"Question: {original_question} \nUser's response: {user_response}. Is this correct?"

    # Send the query to OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": query}]
        )
        verification_result = response.choices[0].message.content
    except Exception as e:
        verification_result = str(e)

    # Send validation result back via SMS
    try:
        responseData = sms.send_message({
            "from": os.environ.get('VONAGE_PHONE_NUMBER'),
            "to": sender,
            "text": verification_result  # Response indicating correctness of the answer
        })

        if responseData["messages"][0]["status"] == "0":
            return jsonify({"message": "Verification response sent successfully."}), 200
        else:
            return jsonify({"error": responseData['messages'][0]['error-text']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

