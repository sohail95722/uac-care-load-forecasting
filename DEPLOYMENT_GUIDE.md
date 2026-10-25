# Run locally
1. Install Python.
2. Open a terminal in this folder.
3. Install dependencies:
   pip install -r requirements.txt
4. Start the app:
   streamlit run app.py
5. Upload `UAC_Cleaned_Dataset.csv` in the app, or place that CSV beside `app.py`.

# Deploy on Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and your cleaned CSV (if you want automatic loading) to your GitHub repository.
2. Open https://share.streamlit.io/
3. Sign in with GitHub and choose **Create app**.
4. Select repository `sohail95722/uac-care-load-forecasting`, branch `main`, and main file path `app.py`.
5. Click **Deploy** and wait for the app URL.
6. Test the public app link in a private/incognito browser window.

# Important
- Confirm the cleaned dataset filename and column names before deployment.
- If you do not want the dataset publicly accessible in GitHub, do not commit it; upload it through the app's CSV uploader instead.
- This is a simple educational baseline, not an official or validated operational forecast.
