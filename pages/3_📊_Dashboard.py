import streamlit as st
import json
import cv2
import numpy as np
from pathlib import Path
import shutil
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="User Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        color: white;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .user-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    .metric-card {
        background: linear-gradient(45deg, #4b6cb7, #182848);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize paths
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
root_dir = current_dir.parent
FACES_DIR = root_dir / "faces"
SCREENSHOTS_DIR = root_dir / "screenshots"

def load_user_data():
    """Load all user data from json files"""
    users = []
    if FACES_DIR.exists():
        for json_file in FACES_DIR.glob("*.json"):
            with open(json_file, "r") as f:
                user_data = json.load(f)
                # Remove encoding from display data
                display_data = {k: v for k, v in user_data.items() if k != 'encoding'}
                display_data['registration_date'] = datetime.fromtimestamp(json_file.stat().st_ctime).strftime("%Y-%m-%d %H:%M:%S")
                users.append(display_data)
    return users

def delete_user(name):
    """Delete user data and files"""
    try:
        # Delete JSON file
        json_file = FACES_DIR / f"{name}.json"
        if json_file.exists():
            json_file.unlink()
        
        # Delete image file
        img_file = FACES_DIR / f"{name}.jpg"
        if img_file.exists():
            img_file.unlink()
            
        # Delete related screenshots
        for screenshot in SCREENSHOTS_DIR.glob(f"{name.split()[0]}_screenshot_*.png"):
            screenshot.unlink()
            
        st.success(f"Successfully deleted user: {name}")
        return True
    except Exception as e:
        st.error(f"Error deleting user: {str(e)}")
        return False

def display_metrics(users):
    """Display key metrics"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Users</div>
        </div>
        """.format(len(users)), unsafe_allow_html=True)
        
    with col2:
        today = datetime.now().date()
        today_users = sum(1 for user in users 
                         if datetime.strptime(user['registration_date'], "%Y-%m-%d %H:%M:%S").date() == today)
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">New Users Today</div>
        </div>
        """.format(today_users), unsafe_allow_html=True)
        
    with col3:
        screenshots = len(list(SCREENSHOTS_DIR.glob("*.png")))
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Verifications</div>
        </div>
        """.format(screenshots), unsafe_allow_html=True)

def display_charts(users):
    """Display analytics charts"""
    if not users:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Registration timeline
        df = pd.DataFrame(users)
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        df_daily = df.groupby(df['registration_date'].dt.date).size().reset_index(name='count')
        
        fig = px.line(df_daily, x='registration_date', y='count',
                     title='User Registrations Over Time',
                     labels={'registration_date': 'Date', 'count': 'Number of Registrations'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Card expiration analysis
        df['expiration_date'] = pd.to_datetime(df['expiration_date'].apply(lambda x: f"20{x.split('/')[1]}-{x.split('/')[0]}-01"))
        months_to_expire = ((df['expiration_date'] - pd.Timestamp.now()).dt.days / 30).round()
        
        fig = px.histogram(x=months_to_expire, nbins=20,
                          title='Card Expiration Distribution',
                          labels={'x': 'Months until expiration', 'y': 'Number of cards'})
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("👥 User Management Dashboard")
    
    # Load user data
    users = load_user_data()
    
    # Display metrics
    display_metrics(users)
    
    # Display charts
    st.markdown("### 📊 Analytics")
    display_charts(users)
    
    # User management section
    st.markdown("### 👤 User Management")
    
    # Search functionality
    search_term = st.text_input("🔍 Search users by name", "").lower()
    filtered_users = [user for user in users if search_term in user['name'].lower().replace(" ", "")]
    
    # Add a message to show search results count
    if search_term:
        st.write(f"Found {len(filtered_users)} matching users")
    
    # Display users
    for user in filtered_users:
        with st.container():
            st.markdown(f"""
            <div class="user-card">
                <h3>{user['name']}</h3>
                <p>Registration Date: {user['registration_date']}</p>
                <p>Card Expiration: {user['expiration_date']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("🗑️ Delete", key=f"delete_{user['name']}"):
                    if delete_user(user['name']):
                        st.rerun()
            
            with col2:
                if st.button("🔄 View Activity", key=f"activity_{user['name']}"):
                    screenshots = list(SCREENSHOTS_DIR.glob(f"{user['name'].split()[0]}_screenshot_*.png"))
                    if screenshots:
                        st.markdown("#### Recent Verifications")
                        for screenshot in sorted(screenshots, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                            img = cv2.imread(str(screenshot))
                            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            st.image(img, caption=f"Verification on {datetime.fromtimestamp(screenshot.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        st.info("No verification history found")
            
            with col3:
                # Display face image if available
                face_img_path = FACES_DIR / f"{user['name']}.jpg"
                if face_img_path.exists():
                    img = cv2.imread(str(face_img_path))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    st.image(img, caption="Registered Face", width=200)
    
    # Export functionality
    if st.button("📥 Export User Data"):
        export_data = [{k: v for k, v in user.items() if k != 'encoding'} for user in users]
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"user_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main() 