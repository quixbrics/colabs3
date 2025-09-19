# Deploying to Streamlit Cloud

1. **Sign up / log in to [Streamlit Cloud](https://streamlit.io/cloud).**
2. **Create a new app and connect your GitHub repo containing this project.**
3. **Add your OpenAI API key:**
   - Go to your app's settings in Streamlit Cloud.
   - Add a new environment variable named `OPENAI_API_KEY` with your OpenAI key value.
4. **Requirements:**
   - Make sure `requirements.txt` is present in your repo (already included).
5. **Run the app:**
   - The main file is `app.py`.
   - Streamlit Cloud will automatically install dependencies and launch the app.

**No login or advanced configuration required.**

---

## Local Development

1. Install dependencies:
   ```zsh
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key:
   ```zsh
   export OPENAI_API_KEY=sk-...
   ```
3. Run the app:
   ```zsh
   streamlit run app.py
   ```
