import streamlit as st
import requests
import json

# Access the OpenAI API key from secrets
openai_api_key = st.secrets["openai"]["api_key"]

# Function to call OpenAI API
def get_chat_response(role):
    try:
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        #     messages=[
        #         {"role": "user", "content": prompt}
        #     ]
        # )

        # print(response)
        # # Check if the response is valid and contains choices
        # if 'choices' in response and len(response.choices) > 0:
        #     # Get the content of the first choice
        #     return response.choices[0].message.content
        # else:
        #     return json.dumps({"error": "No choices returned in the response."})

        url = "https://api.openai.com/v1/chat/completions"

        payload = json.dumps({
            "model": "gpt-4o",
            "messages": [
                {
                "role": "system",
                "content": "You are an expert in various professional fields, with extensive real-world experience in different industries. You are able to provide practical, strategic, and experiential insights relevant to any job role."
                },
                {
                "role": "user",
                "content": "What areas of most 12 relevant experiential knowledge can be transferred by a senior "+role+"? Provide the response as a valid JSON string with a root property 'experiential_knowledge', containing an array of JSON objects. Each object should have a 'title' and 'description' field, focusing on practical skills, strategic insights, common challenges, and effective solutions based on real-world experience. The response should be output directly as a JSON string, without any code block formatting or explanations."
                }
            ],
            "temperature": 0,
            "top_p": 0
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response_json = response.json()

        # Check if the response is valid and contains choices
        if 'choices' in response_json and len(response_json['choices']) > 0:
            # Get the content of the first choice
            return response_json['choices'][0]['message']['content']
        else:
            return json.dumps({"error": "No choices returned in the response."})


    except Exception as e:
        # Return error as JSON string
        return json.dumps({"error": str(e)})

# Streamlit UI
st.title("GenAI-Based Utility - Job Role Insights")
st.write("Enter a job role, and the AI will generate experiential knowledge insights.")

# Text input for job role
job_role = st.text_input("Job Role", placeholder="e.g., Data Scientist, Senior Manager, Software Engineer")

# Generate button
if st.button("Generate Insights"):
    
    if job_role:
        st.write(f"Generating insights for **{job_role}**...")
        insights = get_chat_response(job_role)

        # Try to parse the JSON response
        try:
            insights_json = json.loads(insights)
            # Ensure that 'experiential_knowledge' is in the JSON
            if 'experiential_knowledge' in insights_json:
                st.subheader(f"Experiential Knowledge for {job_role}")
                
                # Iterate over each object in the 'experiential_knowledge' array
                for item in insights_json['experiential_knowledge']:
                    # Ensure each item has both 'title' and 'description'
                    if 'title' in item and 'description' in item:
                        with st.expander(item['title']):
                            st.write(item['description'])
                    else:
                        st.warning("Some items are missing 'title' or 'description'.")
            else:
                st.error("No 'experiential_knowledge' key found in the response.")
        except json.JSONDecodeError:
            st.error("Error parsing response: {}".format(insights))
    else:
        st.error("Please enter a job role.")
