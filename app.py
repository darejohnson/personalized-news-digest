import streamlit as st
import requests
import os
import time

# Configuration with better error handling
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI News Digest",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI-Powered News Digest - DEBUG MODE")
st.markdown("Get personalized news summaries powered by AI")

# Debug information
with st.expander("🔧 Debug Information", expanded=True):
    st.write(f"**API Base URL:** {API_BASE_URL}")
    
    # Test backend connection
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ Backend API is running and accessible")
            st.json(health_response.json())
        else:
            st.error(f"❌ Backend returned status: {health_response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure it's running on port 8000")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    topic = st.text_input("Topic", value="artificial intelligence")
    max_articles = st.slider("Max Articles", 5, 20, 10)
    
    if st.button("Get News Digest"):
        st.session_state.get_news = True

# Main content area
if st.session_state.get('get_news', False):
    with st.spinner("🔄 Fetching and summarizing news..."):
        try:
            # Test connection first
            health_check = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if health_check.status_code != 200:
                st.error("Backend is not healthy. Please check if the API server is running.")
                st.stop()
            
            # Make the actual news request
            response = requests.get(
                f"{API_BASE_URL}/news/{topic}", 
                timeout=30  # Longer timeout for news processing
            )
            
            st.write(f"**Response Status:** {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Display summary
                st.success(f"📊 Found {data['article_count']} articles. Summarized {data['summarized_count']}.")
                
                # Display cost info
                cost = data['cost_metrics']
                st.info(f"💰 Cost: ${cost['daily_spent']} | Remaining: ${cost['remaining_budget']}")
                
                # Display articles
                if data['articles']:
                    for i, article in enumerate(data['articles'][:max_articles]):
                        with st.expander(f"📰 {article['title']}", expanded=i==0):
                            col1, col2 = st.columns([3, 1])
                            
                            with col1:
                                if article.get('ai_summary'):
                                    st.write("**AI Summary:**", article['ai_summary'])
                                else:
                                    st.write("**Description:**", article.get('description', 'No description available'))
                            
                            with col2:
                                st.write("**Source:**", article.get('source', 'Unknown'))
                                if article.get('url'):
                                    st.markdown(f"[Read Full Article]({article['url']})")
                else:
                    st.warning("No articles found or summarized. Try a different topic.")
            
            else:
                st.error(f"API returned error: {response.status_code}")
                st.json(response.json())  # Show error details
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to the backend server. Make sure:")
            st.error("1. The FastAPI server is running on port 8000")
            st.error("2. You used: uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
        except requests.exceptions.Timeout:
            st.error("⏰ Request timed out. The backend might be processing slowly.")
        except Exception as e:
            st.error(f"💥 Unexpected error: {str(e)}")
    
    # Reset the button state
    st.session_state.get_news = False

else:
    # Welcome screen
    st.markdown("""
    ## Welcome to AI News Digest!
    
    This app uses AI to:
    - 📨 Fetch latest news on any topic
    - 🧠 Summarize articles with OpenAI GPT
    - 💰 Control costs with smart budgeting
    - 🔄 Handle API failures gracefully
    
    **How to use:**
    1. Enter a topic in the sidebar
    2. Adjust article count if needed  
    3. Click "Get News Digest"
    4. Read AI-generated summaries!
    
    **Troubleshooting:**
    - Make sure the backend API is running on port 8000
    - Check that your OpenAI API key is valid
    - Verify your NewsAPI key is working
    """)