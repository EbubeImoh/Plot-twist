import pandas as pd
import matplotlib.pyplot as plt
import os
import tempfile
from dotenv import load_dotenv
import google.generativeai as genai
import io

def get_gemini_plot_suggestion(df, user_query, api_key):
    prompt = (
        "You are a data visualization expert.  Given a pandas DataFrame (represented as a CSV string) and a user's request for a plot, "
        "generate Python code using matplotlib to create that plot.  The code should be concise, directly executable, and use the DataFrame variable 'df'.  "
        "If the request is ambiguous, make reasonable assumptions.  Provide a brief description (1-2 sentences) of the plot's purpose and key insights as a comment at the beginning of the code.\n\n"
        f"Here's the user's request: '{user_query}'\n\n"
        f"And here's a sample of the data (first 20 rows as CSV):\n{df.head(20).to_csv(index=False)}"
    )
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model
    response = model.generate_content(prompt, request_options={'timeout': 60}) # Increased timeout
    code = response.text.strip()
    
    # Extract code from markdown if necessary
    if code.startswith("```python"):
        code = code[9:-3].strip()
    elif code.startswith("```"):
        code = code[3:-3].strip()

    return code  

def plot_from_csv(csv_file, user_query, gemini_api_key=None, show_code=False):
    if gemini_api_key is None:  
        load_dotenv()
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file or as argument.")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{csv_file}' not found.")
    
    plot_code = get_gemini_plot_suggestion(df, user_query, gemini_api_key)
    if show_code:
        print("Generated Code:\n", plot_code)
    try:
        exec_globals = {'df': df, 'plt': plt, 'io': io}
        exec(plot_code.replace('pd.compat.StringIO', 'io.StringIO'), exec_globals)  

        # Save the plot to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            plt.savefig(tmpfile.name)
            image_path = tmpfile.name

        plt.close()  # Close the plot to release resources

        # In a real application, you'd upload the image and get a URL.
        # For this example, we'll just return the local file path.
        return image_path

    except Exception as e:
        print("Error executing generated plot code:", e)
        return None

# Optional: CLI entry point
if __name__ == "__main__":
   import sys
   if len(sys.argv) != 3:
       print("Usage: python plotwist.py <csv_file> <user_query>")
       sys.exit(1)

   csv_file = sys.argv[1]
   user_query = sys.argv[2]
   plot_from_csv(csv_file, user_query, show_code=True)