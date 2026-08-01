import os
import re

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)



# =====================================================
# STATIC BUSINESS KNOWLEDGE
# =====================================================

BUSINESS_CONTEXT = """
You are an AI customer assistant inside a CRM system.

Company services:
- SEO
- Google Ads
- Social Media Management
- Content Creation
- Landing Page Design
- Data Analysis
- AI Automation

Rules:
- Answer in English only.
- Be professional and friendly.
- Help customers understand services.
- Help collect customer information.
- Help schedule meetings.
- Never say you are a chatbot.
"""





# =====================================================
# EXTRACT CUSTOMER INFORMATION
# =====================================================


def extract_lead_info(
    messages:list
):

    info = {}


    for msg in messages:


        text = msg.get(
            "content",
            ""
        )


        phone = re.search(
            r'(\+?\d{10,15})',
            text
        )


        if phone:

            info["phone"] = (
                phone.group()
            )



    return info







# =====================================================
# AI RESPONSE GENERATOR
# =====================================================


def get_ai_response(
    messages:list,
    lead_info:dict=None
):


    if lead_info is None:

        lead_info = {}



    conversation = [

        {
            "role":"system",
            "content":
                BUSINESS_CONTEXT
        }

    ]



    conversation.extend(
        messages[-15:]
    )



    response = client.chat.completions.create(

        model="gpt-4o-mini",

        temperature=0.4,

        messages=conversation

    )



    answer = (

        response
        .choices[0]
        .message
        .content
    )


    return answer








# =====================================================
# COMPATIBILITY FUNCTION
# =====================================================


def generate_response(
    message,
    lead_info=None
):


    messages = [

        {
            "role":"user",

            "content":message

        }

    ]


    return get_ai_response(

        messages,

        lead_info

    )