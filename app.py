import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

# Configure API key
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Model
model = genai.GenerativeModel("gemini-1.5-flash")


# Prompt function
def get_response(resume_file, job_desc, optional_prompt):
    resume_file = genai.upload_file(resume_file)
    response = model.generate_content(["I have this resume", resume_file,
                                       "And I want to apply for this job", job_desc,
                                       "How much percentage my profile will be match with the job? Answer directly on percentage numbers, no need for explanation.",
                                       optional_prompt, "Answer in one paragraph."])
    return response.text


# CSS for center page Title
css = '''
h1 {
    text-align: center;
    display: block;
}
'''

# Gradio Blocks
with gr.Blocks(title="Job Match", css=css) as demo:
    gr.Markdown("# Job Match")
    with gr.Row():
        with gr.Column():
            resume_file = gr.File()

            job_desc = gr.Textbox(
                label="Job Description",
                info="Paste job description you want to apply!",
                lines=10
            )

            # Add optional prompt 
            optional_prompt = gr.Textbox(
                label="Optional Prompt",
                info="Add an optional prompt for your job match review.",
                lines=2
            )

            gr.Examples(
                examples=["What to improve?", "What skills am I missing?"],
                inputs=optional_prompt
            )

            submit_btn = gr.Button("Submit")

        with gr.Column():
            job_match_percentage = gr.Text(
                label="Job Match Percentage",
                value="0%"
            )

    submit_btn.click(get_response, inputs=[resume_file, job_desc, optional_prompt], outputs=job_match_percentage)

if __name__ == "__main__":
    demo.launch()
