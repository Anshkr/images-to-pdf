import os
import json
import base64

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL = "openrouter/free"


def analyze_product(image_path, original_name=None):

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("OPENROUTER_API_KEY is missing.")
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    fallback_name = (
        original_name
        if original_name
        else os.path.splitext(os.path.basename(image_path))[0]
    )

    fallback_name = (
        fallback_name.replace("_", " ")
        .replace("-", " ")
        .title()
    )

    try:

        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode()

        response = client.chat.completions.create(

            model=MODEL,

            response_format={"type": "json_object"},

            messages=[
                {
                    "role": "user",
                    "content": [

                        {
                            "type": "text",
                            "text":
"""
Analyze this product image.

Return ONLY valid JSON.

{
  "product_name":"",
  "category":"",
  "material":"",
  "color":"",
  "description":""
}
"""
                        },

                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }

                    ]
                }
            ]

        )

        text = response.choices[0].message.content

        
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        result = json.loads(text)

        result["product_name"] = (
            result.get("product_name")
            or fallback_name
        )

        result["category"] = (
            result.get("category")
            or "General Product"
        )

        result["material"] = (
            result.get("material")
            or "Unknown"
        )

        result["color"] = (
            result.get("color")
            or "Unknown"
        )

        result["description"] = (
            result.get("description")
            or f"Premium quality {fallback_name.lower()}."
        )

        

        return result

    except Exception as e:

        
        return {
            "product_name": fallback_name,
            "category": "General Product",
            "material": "Unknown",
            "color": "Unknown",
            "description": f"Premium quality {fallback_name.lower()}."
        }