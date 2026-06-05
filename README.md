# Ogury Streamlit App

This is a Streamlit dashboard for Ogury One API.

## Files

- `streamlit_app.py` - main Streamlit app
- `requirements.txt` - Python dependencies for deployment
- `requirements_streamlit.txt` - same dependency list
- `.gitignore` - excludes local environment files

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and push this project.
2. Go to https://streamlit.io/cloud and sign in.
3. Create a new app and select the GitHub repo.
4. Set the app file to `streamlit_app.py`.
5. Streamlit Cloud will install dependencies from `requirements.txt`.

## Important

- Do not commit API credentials to GitHub.
- Use Streamlit secrets for private values in Streamlit Cloud:

```toml
# .streamlit/secrets.toml (do not commit)
OGURY_CLIENT_ID = "your-client-id"
OGURY_CLIENT_SECRET = "your-client-secret"
```

Then access them from `streamlit_app.py` with:

```python
st.secrets["OGURY_CLIENT_ID"]
st.secrets["OGURY_CLIENT_SECRET"]
```

## Local run

```bash
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
```
