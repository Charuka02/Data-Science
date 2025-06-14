# -*- coding: utf-8 -*-
"""Academic Support Assistant

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mcuoqTYrc9fYzhRYluQh7AVVVSwXSiLC
"""

# STEP 1: Install Required Libraries
!pip install huggingface_hub transformers gradio -q

# STEP 2: Import Libraries
from transformers import pipeline
import gradio as gr
import random

# STEP 3: Define Academic Strategies
strategies = {
    "group_study": {
        "title": "Join Study Groups",
        "description": "Studying with peers helps reinforce learning, exposes you to new perspectives, and keeps you accountable.",
        "tags": ["group", "discussion", "engagement", "motivation"]
    },
    "time_management": {
        "title": "Use a Study Planner",
        "description": "Organizing tasks using a calendar or planner can reduce stress and help meet deadlines.",
        "tags": ["overwhelm", "schedule", "procrastination", "deadlines"]
    },
    "active_learning": {
        "title": "Practice Active Recall",
        "description": "Using flashcards or testing yourself improves long-term retention compared to passive reading.",
        "tags": ["memory", "recall", "revision", "focus"]
    },
    "conceptual_focus": {
        "title": "Focus on Core Concepts",
        "description": "Understanding key principles in difficult subjects helps with problem-solving and applications.",
        "tags": ["struggle", "confusion", "machine learning", "math"]
    }
}

# STEP 4: Load Text Generation Model
generator = pipeline("text-generation", model="distilgpt2")

# STEP 5: Recommendation Logic
def recommend_strategy(feeling, prep_method, study_hours, struggling_subject):
    matches = []
    combined_input = f"{feeling} {prep_method} {study_hours} {struggling_subject}".lower()

    for strategy in strategies.values():
        if any(tag in combined_input for tag in strategy["tags"]):
            matches.append(strategy)

    if not matches:
        return "❌ Sorry, I couldn't find any relevant strategies for your current situation."

    chosen = random.choice(matches)

    prompt = f"A student feels '{feeling}', studies by '{prep_method}', studies {study_hours} hours daily, and struggles with '{struggling_subject}'. Explain how the strategy '{chosen['title']}' can help them improve academically."

    explanation = generator(prompt, max_length=100, do_sample=True, temperature=0.7)[0]['generated_text']

    return f"""
📘 **Suggested Strategy**: {chosen['title']}

💡 **Why this might help?**
{explanation}
"""

# STEP 6: Advisor Function
def academic_assistant(name, feeling, prep_method, study_hours, struggling_subject):
    recommendation = recommend_strategy(feeling, prep_method, study_hours, struggling_subject)
    return f"""
👋 Hi **{name}**,

📚 **How you're feeling**: {feeling}
📝 **Your study method**: {prep_method}
⏳ **Study time per day**: {study_hours}
📌 **Subject you're struggling with**: {struggling_subject}

---

{recommendation}
"""

# STEP 7: Gradio Interface
iface = gr.Interface(
    fn=academic_assistant,
    inputs=[
        gr.Textbox(label="Your Name"),
        gr.Textbox(label="How are you feeling about your studies today?"),
        gr.Textbox(label="How do you usually prepare for exams or assignments?"),
        gr.Textbox(label="How many hours do you typically study each day?"),
        gr.Textbox(label="What subjects or topics are you struggling with?")
    ],
    outputs="markdown",
    title="🎓 Academic Support Assistant",
    description="AI-powered tips for improving study or teaching strategies based on your current state. For students and teachers alike!",
    theme="default"
)

# STEP 8: Launch the App
iface.launch(share=True)