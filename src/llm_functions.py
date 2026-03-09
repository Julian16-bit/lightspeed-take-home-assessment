import pandas as pd
from src.prompts import THEME_EXTRACTION_PROMPT, FEEDBACK_SUMMARY_PROMPT, ExtractTheme, FeedbackSummary
from src.llm_config import get_structured_response
import time

def extract_theme(feedback_text: str):
    response =  get_structured_response(
        prompt=THEME_EXTRACTION_PROMPT.format(feedback_text=feedback_text),
        text_format=ExtractTheme,
        system_message="You are a product feedback classification assistant."
    )

    return response

def create_feedback_summary(feedback_data: str):
    response = get_structured_response(
        prompt=FEEDBACK_SUMMARY_PROMPT.format(feedback_data=feedback_data),
        text_format=FeedbackSummary,
        system_message="You are a product insight analyst.",
        model="gpt-5-mini"
    )

    return response

def create_ai_generated_fields(df):
    df_copy = df.copy()
    feedback_list = df_copy["content"].to_list()

    sentiments = []
    subjects = []
    failed_indices = []

    start_time = time.time()
    total = len(feedback_list)

    for index, feedback_text in enumerate(feedback_list):
        try:
            print(f"Processing {index + 1}/{total}: {feedback_text}")

            # Handle empty or null feedback
            if pd.isna(feedback_text) or str(feedback_text).strip() == "":
                print(f"Skipping empty feedback at index {index}")
                sentiments.append("Neutral")
                subjects.append("Other")
                continue

            llm_output = extract_theme(feedback_text)
            subjects.append(llm_output.subject)
            sentiments.append(llm_output.sentiment)

        except Exception as e:
            print(f"Error at index {index}: {e}")
            failed_indices.append(index)
            sentiments.append("Neutral")
            subjects.append("Other")

    end_time = time.time()
    total_time = end_time - start_time

    print(f"Total time: {total_time}s")
    print(f"Successfully processed: {total - len(failed_indices)}/{total}")
    if failed_indices:
        print(f"Failed indices: {failed_indices}")

    df_copy['sentiment'] = sentiments
    df_copy['subject'] = subjects

    return df_copy


if __name__ == "__main__":
    # df = pd.read_csv("output.csv")
    # df = create_ai_generated_fields(df)
    # df.to_csv("output_with_generated_fields.csv")
    # print(df)
    feedback_data = """
    M001,app_store,Great POS system but reporting is slow during peak hours.,4.0,2024-01-02,Neutral,Reporting & Analytics
    M001,app_store,Inventory sync is sometimes delayed.,3.0,2024-01-12,Negative,Reliability & Stability
    M001,support,Stock levels not updating in real time.,,2024-01-12,Negative,Reliability & Stability
    """
    output = create_feedback_summary(feedback_data)
    print(output)


    




    