import time

import streamlit as st
from google import genai
from google.genai.errors import APIError, ServerError
from google.genai import types



# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Receipt & Expense Tracker",
    page_icon="🧾",
    layout="centered"
)

# -----------------------------
# Gemini Client
# -----------------------------
api_key = st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None

# -----------------------------
# App Title
# -----------------------------
st.title("🧾 Receipt & Expense Tracker")
st.caption("Snap it. Track it. Understand your spending.")

st.write(
    "Upload a receipt image and AI will extract the "
    "expense details automatically."
)

# -----------------------------
# Upload Receipt
# -----------------------------
uploaded_file = st.file_uploader(
    "📸 Upload your receipt",
    type=["jpg", "jpeg", "png", "webp"]
)

if client is None:
    st.warning("Add GEMINI_API_KEY to .streamlit/secrets.toml to enable receipt analysis.")

# -----------------------------
# Display and Analyze Receipt
# -----------------------------
if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded Receipt",
        width="stretch"
    )

    if st.button("🔍 Analyze Receipt", type="primary", disabled=client is None):

        with st.spinner("Analyzing your receipt..."):

            try:
                # Read image
                image_bytes = uploaded_file.getvalue()

                # AI prompt
                prompt = """
                Analyze this receipt carefully.

                Extract the following information:

                1. Merchant name
                2. Merchant address
                3. Receipt number
                4. Date
                5. Time
                6. Items purchased
                7. Quantity of each item
                8. Price of each item
                9. Subtotal
                10. Discount
                11. GST/Tax
                12. CGST
                13. SGST
                14. IGST
                15. Total amount
                16. Currency
                17. Payment method
                18. Expense category

                Categorize the expense as one of:

                - Food & Dining
                - Groceries
                - Transportation
                - Shopping
                - Healthcare
                - Education
                - Entertainment
                - Utilities
                - Travel
                - Bills
                - Personal Care
                - Electronics
                - Other

                IMPORTANT RULES:

                - Do not guess information.
                - If information is not visible, write "Not detected".
                - If text is unclear, write "Uncertain".
                - Preserve the currency shown on the receipt.
                - Check whether the subtotal, discount, tax and total
                  are mathematically consistent.
                - If the uploaded image is not a receipt, say:
                  "This image does not appear to be a receipt."

                Return the result in this format:

                MERCHANT:
                Date:
                Time:
                Receipt Number:
                Currency:

                ITEMS:
                - Item | Quantity | Price | Total

                SUBTOTAL:
                DISCOUNT:
                TAX:
                CGST:
                SGST:
                IGST:
                TOTAL:

                PAYMENT METHOD:
                CATEGORY:

                VALIDATION:
                CONSISTENCY:

                CONFIDENCE:
                """

                # Send image + prompt to Gemini
                contents = [
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=uploaded_file.type
                    ),
                    prompt
                ]

                response = None
                last_server_error = None
                for model_name in ("gemini-3.8-flash", "gemini-3.1-flash-lite"):
                    for attempt in range(2):
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=contents
                            )
                            break
                        except ServerError as error:
                            last_server_error = error
                            if attempt == 0:
                                time.sleep(1)
                    if response is not None:
                        break

                if response is None and last_server_error is not None:
                    raise last_server_error

                # -----------------------------
                # Display Result
                # -----------------------------
                st.success("Receipt analyzed successfully!")

                st.subheader("📋 Expense Details")

                st.write(response.text or "Gemini returned an empty response.")

            except ServerError as e:
                st.error(
                    "Gemini is temporarily overloaded. The app retried the request "
                    "and tried a fallback model; please try again shortly."
                )
                st.caption(f"Gemini server error ({e.code}): {e.message}")

            except APIError as e:
                if e.code == 429:
                    st.error(
                        "The Gemini API quota or rate limit was reached. "
                        "Check the quota for this API key and try again later."
                    )
                elif e.code in (400, 401, 403):
                    st.error(
                        "Gemini rejected the request. Check that the API key is "
                        "valid and allowed to use the selected models."
                    )
                else:
                    st.error(f"Gemini API request failed ({e.code}).")
                st.caption(e.message or str(e))

            except Exception as e:

                st.error(
                    "Something went wrong while analyzing the receipt."
                )

                st.code(str(e))