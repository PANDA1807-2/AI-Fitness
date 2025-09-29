import streamlit as st
import sqlite3
import bcrypt
import re
import math

# Set the page layout to wide for a full-screen appearance
st.set_page_config(layout="wide")

# --- Page Management using Session State ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'username' not in st.session_state:
    st.session_state.username = None


def set_page(page_name):
    st.session_state.current_page = page_name


# --- Custom CSS for Professional Dark Design (Fixes Metric Block Visibility) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
}

/* --- Global Dark Mode Background (Deep Contrast Color: Dark Blue/Gray) --- */
.stApp {
    background-color: #101419; /* Deep dark blue/gray for contrast */
    color: #f0f0f0;
}
/* Main content area background */
.main .block-container {
    background-color: #101419;
}

/* --- Header/Navbar Styling (Minimal) --- */
.header {
    background-color: #1a1f26; /* Slightly lighter header background */
    padding: 10px 30px;
    border-bottom: 1px solid #333333;
    text-align: center; /* Centering the website name */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}
.header h1 {
    color: #00ff99; /* Bright accent color for branding */
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
    text-align: center; /* Ensuring text is centered within h1 */
}

/* --- Footer Styling --- */
.footer {
    background-color: #0a0e12;
    color: #999999;
    padding: 15px;
    text-align: center;
    font-size: 12px;
    margin-top: 50px;
    border-radius: 4px;
}

/* --- Card/Content Styling (Faint, contrasting background) --- */
.content-card {
    background-color: #1a1f26; /* Faint contrasting color for main blocks */
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0, 255, 153, 0.05); /* Subtle neon glow */
    margin-bottom: 25px;
    border: 1px solid #333333;
}
.content-card h3 {
    color: #00ff99; /* Accent color for subheadings */
    font-weight: 600;
}
.content-card p, .content-card li {
    color: #cccccc;
    line-height: 1.6;
}

/* --- Button Styling (Bright accent and Hover Fix) --- */
.stButton>button {
    background-color: #00ff99; /* Bright green/neon accent */
    color: #1a1a1a;
    font-weight: 700;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    box-shadow: 0 0 10px rgba(0, 255, 153, 0.4);
    transition: background-color 0.2s, transform 0.2s;
}
.stButton>button:hover {
    background-color: #00cc7a; /* Distinct darker green for hover state */
    transform: translateY(-1px);
}

/* --- Streamlit Specific Overrides (Input/Metric Fixes) --- */

/* Sidebar */
[data-testid="stSidebarContent"] {
    background-color: #0a0e12; /* Darkest sidebar for max contrast */
    color: #f0f0f0;
}

/* Target all Input/Textarea/Select bases for dark background */
div[data-baseweb="input"] div[data-baseweb="baseinput"], 
div[data-baseweb="textarea"] textarea,
div[data-baseweb="select"] div[role="button"] {
    background-color: #333333 !important;
    border-radius: 6px;
    border: 1px solid #555555 !important;
    color: #f0f0f0 !important;
}

/* Specific styling for the actual text input area */
input, textarea {
    background-color: #333333 !important;
    color: #f0f0f0 !important;
    caret-color: #00ff99 !important; /* Cursor color */
}

/* Text label color (General fix) */
.st-emotion-cache-10trblm {
    color: #f0f0f0;
}

/* Expander/Accordion */
.st-expander {
    border: 1px solid #333333 !important;
    background-color: #1a1f26; /* Card background */
    border-radius: 8px;
}
.st-expander details summary {
    color: #f0f0f0 !important;
    font-weight: 600;
}

/* FIX: Metric/Info Boxes Background (Distinct contrast) */
div[data-testid="stMetric"], div[data-testid="stAlert"] > div {
    background-color: #374151 !important; /* Lighter, distinct grayish-blue background */
    border-radius: 8px;
    border: 1px solid #4b5563 !important;
}

/* FIX: Metric Value Text Color */
/* Targeting the metric value */
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #00ff99 !important; /* Bright neon green for the main number */
    font-weight: 700 !important;
    font-size: 1.5rem !important;
}

/* FIX: Metric Label Text Color - MODIFIED FOR BETTER CONTRAST */
/* Targeting the metric label (e.g., "Weight (kg)") */
div[data-testid="stMetric"] div[data-testid="stMetricLabel"] {
    color: #f0f0f0 !important; /* Changed to bright white for visibility */
    font-weight: 400 !important;
}

/* ADDED ROBUSTNESS FIX: Ensure any internal text within the metric is visible */
div[data-testid="stMetric"] * {
    color: #f0f0f0 !important;
}


/* --- SPECIFIC LOGIN BUTTON TARGET (To override Streamlit form behavior) --- */
/* Targeting the submit button inside the login/registration forms */
[data-testid="stForm"] .stButton button {
    background-color: #00ff99 !important; 
    color: #1a1a1a !important;
}
[data-testid="stForm"] .stButton button:hover {
    background-color: #00cc7a !important; 
}

/* --- LOGIN PAGE BACKGROUND CLASS --- */
.login-background {
    background-image: url('AI.jpg'); /* Reference the local image */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.3; /* Set visibility to 30% (0.3) */
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1; /* Place behind all content */
}
</style>
""", unsafe_allow_html=True)


# --- Define the Header and Footer functions ---
def show_header():
    # Simple, non-intrusive header for the top of the main content
    st.markdown('<div class="header"><h1>AI-Fitness Assistant</h1></div>', unsafe_allow_html=True)


def show_footer():
    # --- FINAL MODIFIED FOOTER LAYOUT (Using Links and minimal logic) ---
    st.markdown("---")

    # 1. Create a container for the hidden buttons (must be visible in the Streamlit flow)
    col_hidden = st.columns([1])[0]




    # 2. Inject styled HTML links and copyright text
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; align-items: center; padding: 10px 0; font-size: 12px;">
            <a href="#" onclick="parent.window.document.querySelector('[data-testid=stVerticalBlock] button[title=\\'About\\']').click(); return false;" class="footer-link">About Us</a>
            <span style="margin: 0 10px; color: #555555;">|</span>
            <a href="#" onclick="parent.window.document.querySelector('[data-testid=stVerticalBlock] button[title=\\'Contact\\']').click(); return false;" class="footer-link">Contact Us</a>
            <span style="margin-left: 20px; color: #999999;">© 2025 AI-Fitness Assistant. All rights reserved.</span>
        </div>

        <style>
            .footer-link {{
                color: #cccccc !important; 
                text-decoration: none;
            }}
            .footer-link:hover {{
                color: #00ff99 !important;
                text-decoration: underline;
            }}
            /* This targets and hides the entire block where the hidden buttons are generated */
            [data-testid=stVerticalBlock] > div:nth-child(1) [data-testid=stVerticalBlock] {{ 
                display: none; 
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


def show_sidebar_navigation():
    # Dynamic sidebar for logged-in users (NOW INCLUDES ABOUT AND CONTACT)
    with st.sidebar:
        st.markdown(f"## Welcome, {st.session_state.username} 👋")
        st.markdown("---")

        # Keys are now explicitly suffixed with '_sidebar' to guarantee uniqueness
        st.button("👤 Profile", key="nav_profile_sidebar", use_container_width=True, on_click=set_page,
                  args=('profile_page',))
        st.button("📈 Health Plan", key="nav_plan_sidebar", use_container_width=True, on_click=set_page,
                  args=('health_plan',))
        st.button("⚙️ Edit Profile", key="nav_edit_sidebar", use_container_width=True, on_click=set_page,
                  args=('edit_profile',))
        st.markdown("---")
        # NEW NAVIGATION BUTTONS IN SIDEBAR
        st.button("ℹ️ About Us", key="nav_about_sidebar", use_container_width=True, on_click=set_page,
                  args=('about',))
        st.button("📞 Contact Us", key="nav_contact_sidebar", use_container_width=True, on_click=set_page,
                  args=('contact',))
        st.markdown("---")
        # END NEW NAVIGATION BUTTONS

        # Logout button
        if st.button("🚪 Log out", key="nav_logout_sidebar", use_container_width=True):
            st.session_state.username = None
            set_page('home')


def add_fitness_images():
    """Adds a row of contrasting fitness images below the profile snapshot."""
    image_col1, image_col2, image_col3 = st.columns(3)

    # Using high-contrast, relevant placeholder images
    with image_col1:
        st.image("https://images.unsplash.com/photo-1549576490-b0b4831ef60a?q=80&w=600&auto=format&fit=crop",
                 caption="Strength Training", use_container_width=True)
    with image_col2:
        # Endurance Focus - Using local file placeholder
        st.image("ef.jpg",
                 caption="Endurance Focus", use_container_width=True)
    with image_col3:
        # Active Recovery - Using local file placeholder
        st.image("ar1.jpg",
                 caption="Active Recovery", use_container_width=True)
    st.markdown("---")


# --- Define the Home Page Content ---
def home_page():
    # The home page remains standard but adopts the new dark theme
    show_header()

    # Hero section with large, contrasting elements
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    # FIRST IMAGE TAG: Gym and fitness related photo
    st.image("AI.jpg",
             caption="Achieve your fitness goals with AI.",
             use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Title and buttons section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h2 style="color:#f0f0f0; font-weight: 600;">Your Personal Health & Fitness Guide</h2>',
                    unsafe_allow_html=True)
        st.write("Get a personalized health plan based on your unique data and goals.")

        # Centering the buttons
        button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
        with button_col1:
            reg_button = st.button("Register", key="home_register_btn")
        with button_col3:
            login_button = st.button("Login", key="home_login_btn")

    # The Logic for the buttons
    if reg_button:
        set_page('register')
    if login_button:
        set_page('login')

    # Information Blog Section
    st.markdown("---")
    st.subheader("Fitness Blog")

    # Blog Post 1 - Using the new card style
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h3>The Importance of Consistency</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p>Consistency is paramount in achieving long-term success, as even small, consistent actions build the necessary momentum for progress and effectively prevent setbacks. This steady, repeated effort is what reinforces desired behaviors, ultimately solidifying them into sustainable habits. By ensuring reliable application of effort over time, consistency directly drives superior results, refining skills, and leading to genuine mastery in any endeavor.</p>",
        unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Blog Post 2
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h3>Understanding Macronutrients</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p>Macronutrients—Carbohydrates, Proteins, and Fats—are the three essential components of food your body needs in large quantities for energy and overall health. Carbohydrates are the primary fuel source, broken down into glucose for energy. Protein acts as the body's structural material, vital for muscle repair, growth, and immune function. Fats are crucial for long-term energy storage, hormone regulation, and absorbing key vitamins. Understanding and balancing these three macros is fundamental to optimizing your nutrition and achieving your fitness and health objectives.</p>",
        unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    show_footer()


# --- ABOUT US Page (NEW) ---
def about_page():
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h2 style="color:#00ff99;">About AI-Fitness Assistant</h2>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Our Mission")
        st.markdown(
            "<p>We are dedicated to democratizing personalized health. Our mission is to provide cutting-edge, **AI-driven fitness and nutrition plans** tailored to your unique profile, goals, and limitations. We believe everyone deserves access to expert guidance without the premium cost.</p>",
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Why Choose AI-Fitness?")
        st.markdown(
            """
            <ul>
                <li>**Personalized Plans:** Algorithms calculate your exact TDEE, macronutrients, and workout split based on your data.</li>
                <li>**Safety First:** Built-in health warnings ensure you consult professionals regarding injuries or illnesses before training.</li>
                <li>**Data Security:** Your profile and health data are secured using industry-standard hashing and database practices.</li>
            </ul>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Back to Home", key="back_about_page_btn", use_container_width=True):
            set_page('home')

    show_footer()


# --- CONTACT US Page (NEW) ---
def contact_page():
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h2 style="color:#00ff99;">Contact Our Support Team</h2>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Get in Touch")

        st.markdown(
            """
            <p>If you have any questions, require technical support, or need assistance with your fitness plan, please reach out to us using the details below or fill out the contact form.</p>

            <p><strong>General Support:</strong> support@ai-fitness-assistant.com</p>
            <p><strong>Technical Issues:</strong> tech@ai-fitness-assistant.com</p>
            <p><strong>Phone:</strong> +91 1234 567890 (M-F, 9 AM - 5 PM IST)</p>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Contact Form
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Send Us a Message")
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            reason = st.selectbox("Reason for Contact",
                                  ["Technical Support", "Billing Query", "General Inquiry", "Feature Suggestion"])
            message = st.text_area("Your Message")

            contact_submitted = st.form_submit_button("Submit Message")

            if contact_submitted:
                if name and email and message:
                    # Placeholder for sending email/saving contact message
                    st.success(f"Thank you, {name}! Your message regarding '{reason}' has been submitted.")
                else:
                    st.error("Please fill in all required fields (Name, Email, and Message).")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Back to Home", key="back_contact_page_btn", use_container_width=True):
            set_page('home')

    show_footer()


# --- Registration Page ---
def register_page():
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h2 style="color:#f0f0f0;">Create Your Account</h2>', unsafe_allow_html=True)

        with st.form("registration_form"):
            # Form elements remain functional, inheriting new input styling
            username = st.text_input("Username", key="reg_username")
            contact = st.text_input("Contact Number", key="reg_contact")
            email = st.text_input("Email", key="reg_email")
            gender = st.selectbox("Gender", ["Select Gender", "Male", "Female", "Other"], key="reg_gender")
            address = st.text_area("Address", key="reg_address")
            password = st.text_input("Password", type="password", key="reg_password")
            re_password = st.text_input("Re-enter Password", type="password", key="reg_re_password")

            submitted = st.form_submit_button("Register")

            if submitted:
                if not all([username, contact, email, gender, address, password,
                            re_password]) or gender == "Select Gender":
                    st.error("Please fill in all the fields.")
                elif password != re_password:
                    st.error("Passwords do not match.")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                    st.error("Please enter a valid email address.")
                elif not re.match(r"^\d{10}$", contact):
                    st.error("Contact number must be a 10-digit number.")
                else:
                    try:
                        register_user(username, contact, email, gender, address, password)
                        st.success("Registration successful! You can now log in.")
                        set_page('login')
                    except ValueError as e:
                        st.error(str(e))

    if st.button("Back to Home", key="back_reg_page_btn"):
        set_page('home')

    show_footer()


# --- Login Page (FIXED WITH BACKGROUND) ---
def login_page():
    # Inject the HTML and CSS for the background only on this page
    st.markdown('<div class="login-background"></div>', unsafe_allow_html=True)

    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h2 style="color:#f0f0f0;">Login to Your Account</h2>', unsafe_allow_html=True)

        with st.form("login_form"):
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")

            # The Login button benefits from the new targeted CSS style applied globally to forms
            submitted = st.form_submit_button("Login")

            if submitted:
                if login_user(login_username, login_password):
                    st.session_state.username = login_username
                    st.success(f"Welcome back, {login_username}!")
                    set_page('profile_page')
                else:
                    st.error("Invalid username or password.")

        # --- Register button placed beside the question ---
        col_text, col_button = st.columns([1, 1])
        with col_text:
            st.markdown(
                """
                <div style="text-align: right; margin-top: 20px;">
                    <p style="margin: 0; font-size: 14px; color: #999999;">Don't have an account?</p>
                </div>
                """, unsafe_allow_html=True
            )
        with col_button:
            if st.button("Register", key="reg_login_page_btn"):
                set_page('register')
        # -----------------------------------------------------------

    if st.button("Back to Home", key="back_login_page_btn"):
        set_page('home')

    show_footer()


# --- User Profile Page (SIMPLIFIED with Images) ---
def profile_page():
    # Sidebar navigation is shown by the main loop logic

    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h2 style="color:#00ff99;">Your Health Profile</h2>', unsafe_allow_html=True)

        user_id = get_user_id_by_username(st.session_state.username)
        if user_id:
            profile_data = get_health_profile(user_id)

            if profile_data:
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.subheader("Current Profile Snapshot")

                # --- Simplified Data Display ---
                col_info1, col_info2, col_info3 = st.columns(3)

                # Row 1: Key Metrics (Metrics are simple and high-contrast)
                col_info1.metric("Goal", profile_data[7])
                col_info2.metric("Weight (kg)", f"{profile_data[5]}")
                col_info3.metric("Age (years)", f"{profile_data[2]}")

                st.markdown("---")

                # Row 2: Secondary Metrics/Status
                st.markdown(f"**Height:** {profile_data[3]} ft, {profile_data[4]} in")
                st.markdown(f"**Activity Level:** {profile_data[6]}")
                st.markdown(f"**Dietary Preference:** {profile_data[8]}")

                # Row 3: Warnings/Special Conditions (use markdown for direct visibility)
                if profile_data[9] or profile_data[10]:
                    st.markdown("---")
                    st.markdown(f"⚠️ **Injuries/Illness Reported:**")
                    if profile_data[9]:
                        st.markdown(f"- **Injury:** {profile_data[9]}")
                    if profile_data[10]:
                        st.markdown(f"- **Illness:** {profile_data[10]}")

                st.markdown('</div>', unsafe_allow_html=True)

                # --- ADDED FITNESS IMAGES SECTION (FIXED) ---
                add_fitness_images()
                # ------------------------------------

                # --- Action Buttons ---
                col_edit, col_plan = st.columns(2)
                with col_edit:
                    if st.button("Edit Profile Data", key="profile_edit_btn", use_container_width=True):
                        set_page('edit_profile')
                with col_plan:
                    if st.button("Generate Health Plan", key="profile_get_plan_btn", use_container_width=True):
                        st.session_state.profile_data = profile_data
                        set_page('health_plan')

            else:
                # --- Complete Profile Form (Unchanged) ---
                st.markdown('<div class="content-card">', unsafe_allow_html=True)
                st.subheader("Complete Your Health Profile")
                st.write("Please provide the following information to receive a personalized health plan.")

                with st.form("health_profile_form"):
                    age = st.number_input("Age", min_value=1, max_value=120, step=1, key="profile_age_input")
                    col_height_ft, col_height_in = st.columns(2)
                    with col_height_ft:
                        height_ft = st.number_input("Height (feet)", min_value=0, max_value=8, step=1,
                                                    key="profile_ft_input")
                    with col_height_in:
                        height_in = st.number_input("Height (inches)", min_value=0, max_value=11, step=1,
                                                    key="profile_in_input")

                    weight_kg = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, step=0.1,
                                                key="profile_weight_input")

                    activity_level = st.selectbox(
                        "Your typical weekly activity level?",
                        ["Select Level", "Sedentary", "Lightly Active", "Moderately Active", "Very Active",
                         "Super Active"],
                        key="profile_activity_input"
                    )

                    fitness_goal = st.selectbox(
                        "Your primary fitness goal?",
                        ["Select Goal", "Lose Weight", "Gain Muscle", "Improve Endurance", "Maintain Fitness"],
                        key="profile_goal_input"
                    )

                    dietary_preference = st.selectbox(
                        "Your dietary preference?",
                        ["Select Preference", "Vegetarian", "Non-Vegetarian"],
                        key="profile_diet_input"
                    )

                    physical_injury = st.text_area("Any physical injuries? (e.g., knee pain, shoulder injury)",
                                                   key="profile_injury_input")
                    medical_illness = st.text_area("Any medical illnesses? (e.g., high blood pressure, diabetes)",
                                                   key="profile_illness_input")

                    submitted = st.form_submit_button("Save Profile")

                    if submitted:
                        if age and height_ft and height_in and weight_kg and activity_level != "Select Level" and fitness_goal != "Select Goal" and dietary_preference != "Select Preference":
                            add_health_profile(user_id, age, height_ft, height_in, weight_kg, activity_level,
                                               fitness_goal, dietary_preference, physical_injury, medical_illness)
                            st.success("Your health profile has been saved successfully!")
                            st.experimental_rerun()  # Rerun to show the saved data
                        else:
                            st.error("Please fill in all the fields.")
                st.markdown('</div>', unsafe_allow_html=True)

    show_footer()


# --- Edit Profile Page ---
def edit_profile_page():
    # Sidebar navigation is shown by the main loop logic
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h2 style="color:#00ff99;">Edit Your Health Profile</h2>', unsafe_allow_html=True)

        user_id = get_user_id_by_username(st.session_state.username)
        profile_data = get_health_profile(user_id)

        if profile_data:
            with st.form("edit_profile_form"):
                current_age = profile_data[2]
                current_height_ft = profile_data[3]
                current_height_in = profile_data[4]
                current_weight_kg = profile_data[5]
                current_activity_level = profile_data[6]
                current_fitness_goal = profile_data[7]
                current_dietary_preference = profile_data[8]
                current_physical_injury = profile_data[9]
                current_medical_illness = profile_data[10]

                age = st.number_input("Age", min_value=1, max_value=120, step=1, value=current_age,
                                      key="edit_age_input")
                col_height_ft, col_height_in = st.columns(2)
                with col_height_ft:
                    height_ft = st.number_input("Height (feet)", min_value=0, max_value=8, step=1,
                                                value=current_height_ft, key="edit_ft_input")
                with col_height_in:
                    height_in = st.number_input("Height (inches)", min_value=0, max_value=11, step=1,
                                                value=current_height_in, key="edit_in_input")

                weight_kg = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, step=0.1,
                                            value=current_weight_kg, key="edit_weight_input")

                activity_levels = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"]
                activity_index = activity_levels.index(
                    current_activity_level) if current_activity_level in activity_levels else 0
                activity_level = st.selectbox(
                    "Your typical weekly activity level?",
                    activity_levels,
                    index=activity_index,
                    key="edit_activity_input"
                )

                fitness_goals = ["Lose Weight", "Gain Muscle", "Improve Endurance", "Maintain Fitness"]
                goal_index = fitness_goals.index(current_fitness_goal) if current_fitness_goal in fitness_goals else 0
                fitness_goal = st.selectbox(
                    "Your primary fitness goal?",
                    fitness_goals,
                    index=goal_index,
                    key="edit_goal_input"
                )

                dietary_preferences = ["Vegetarian", "Non-Vegetarian"]
                diet_index = dietary_preferences.index(
                    current_dietary_preference) if current_dietary_preference in dietary_preferences else 0
                dietary_preference = st.selectbox(
                    "Your dietary preference?",
                    dietary_preferences,
                    index=diet_index,
                    key="edit_diet_input"
                )

                physical_injury = st.text_area("Any physical injuries?", value=current_physical_injury,
                                               key="edit_injury_input")
                medical_illness = st.text_area("Any medical illnesses?", value=current_medical_illness,
                                               key="edit_illness_input")

                submitted = st.form_submit_button("Save Changes")
                if submitted:
                    update_health_profile(user_id, age, height_ft, height_in, weight_kg, activity_level, fitness_goal,
                                          dietary_preference, physical_injury, medical_illness)
                    st.success("Your health profile has been updated successfully!")
                    st.session_state.profile_data = get_health_profile(user_id)
                    set_page('profile_page')

        if st.button("Back to Profile", key="back_edit_page_btn", use_container_width=True):
            set_page('profile_page')

    show_footer()


def health_plan_page():
    # Sidebar navigation is shown by the main loop logic
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<h2 style="color:#00ff99;">Your Personalized Health Plan</h2>', unsafe_allow_html=True)

        if st.session_state.get('profile_data'):
            plan = generate_health_plan(st.session_state.profile_data)

            # --- Overview Metrics ---
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader("Plan Summary")
            col_goal, col_cal = st.columns(2)
            col_goal.metric("Goal", plan['goal'])
            col_cal.metric("Daily Calories", f"{plan['calories']} kcal")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Workout Plan ---
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader("🏋️ Detailed Workout Plan")
            st.markdown(plan['workout_plan'], unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Dietary Plan ---
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader("🍎 Dietary Recommendations")

            # If Muscle Gain, structure the 6 meals explicitly for clear reading
            if plan['goal'] == "Gain Muscle":
                # Print the summary before the meals
                plan_parts = plan['diet_plan'].split('<hr>')
                st.markdown(plan_parts[0], unsafe_allow_html=True)

                # Print each meal section directly
                meal_sections = ('<hr>'.join(plan_parts[1:])).split('<h4>')[1:]
                for section in meal_sections:
                    title = section.split('</h4>')[0]
                    content = section.split('</h4>')[1]

                    st.markdown(f'**{title.strip()}**', unsafe_allow_html=True)
                    st.markdown(content, unsafe_allow_html=True)

            else:
                st.markdown(plan['diet_plan'], unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Health Warning (Explicitly styled via CSS) ---
            st.error(plan['health_warning'])

        else:
            st.warning("Please complete your health profile first.")
            if st.button("Go to Profile Page", key="plan_to_profile_btn", use_container_width=True):
                set_page('profile_page')

        if st.button("Back to Profile", key="back_to_profile_btn", use_container_width=True):
            set_page('profile_page')

    show_footer()


# --- Placeholder AI/Analysis Logic (Unchanged) ---
def generate_health_plan(profile_data):
    """
    Generates a goal-specific plan:
    - Lose Weight: Calorie deficit, higher cardio, moderate strength.
    - Gain Muscle: Fixed 3000 kcal, detailed 4-Day Split, 6-meal macro plan.
    - Improve Endurance: Maintenance calories, high cardio/endurance focus.
    - Maintain Fitness: Maintenance calories, balanced workout.
    """
    # Extract data from profile_data
    goal = profile_data[7]
    weight_kg = profile_data[5]
    height_cm = (profile_data[3] * 30.48) + (profile_data[4] * 2.54)
    age = profile_data[2]
    activity_level = profile_data[6]
    dietary_preference = profile_data[8]
    physical_injury = profile_data[9]
    medical_illness = profile_data[10]

    # Mifflin-St Jeor TDEE Calculation (Simplified for this script to use male BMR formula only)
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.9,
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    tdee = int(tdee)  # Maintenance calories

    # --- Calorie and Workout Plan Logic based on Goal ---

    # 1. Gain Muscle: Fixed 3000 kcal and detailed splits/diet
    if goal == "Gain Muscle":
        calories = 3000  # Fixed as per user request for this specific goal
        # Target Macros: P: 260g, C: 365g, F: 67g (Approximate for 3000 kcal)

        workout_plan = f"""
            <p><strong>Goal:</strong> Muscle Hypertrophy (Growth) via Progressive Overload.</p>
            <p><strong>Target Calories:</strong> {calories} kcal (Surplus)</p>
            <p><strong>Training Split:</strong> 4-Day Upper/Lower Split. Rest periods should be 60-90 seconds between sets.</p>
            <hr>
            <h4>Day 1: Upper Body (Push/Chest Focus)</h4>
            <ul>
                <li><strong>Bench Press (Barbell or Dumbbell):</strong> 4 Sets, 6-8 Reps (Heavy compound)</li>
                <li><strong>Bent-Over Rows (Barbell):</strong> 4 Sets, 8-10 Reps</li>
                <li><strong>Dumbbell Overhead Press (Shoulders):</strong> 3 Sets, 10-12 Reps</li>
                <li><strong>Cable Pullovers (for Chest/Back extension):</strong> 3 Sets, 12-15 Reps</li>
                <li><strong>Dumbbell Flyes (Chest Isolation):</strong> 3 Sets, 12-15 Reps</li>
                <li><strong>Triceps Pushdowns:</strong> 3 Sets, 10-12 Reps</li>
            </ul>
            <hr>
            <h4>Day 2: Lower Body (Quads/Hams Focus)</h4>
            <ul>
                <li><strong>Squats (Barbell or Hack):</strong> 4 Sets, 6-8 Reps (Heavy compound)</li>
                <li><strong>Romanian Deadlifts (RDLs - Hamstrings):</strong> 3 Sets, 10-12 Reps</li>
                <li><strong>Leg Press:</strong> 3 Sets, 10-12 Reps</li>
                <li><strong>Leg Extensions (Quads Isolation):</strong> 3 Sets, 12-15 Reps</li>
                <li><strong>Seated or Standing Calf Raises:</strong> 4 Sets, 15 Reps (High volume)</li>
            </ul>
            <hr>
            <h4>Day 3: Active Rest or Complete Rest</h4>
            <hr>
            <h4>Day 4: Upper Body (Pull/Back Focus)</h4>
            <ul>
                <li><strong>Deadlifts (Conventional or Sumo):</strong> 3 Sets, 5-8 Reps (Focus on perfect form)</li>
                <li><strong>Pull-Ups or Lat Pulldowns:</strong> 4 Sets, 8-12 Reps</li>
                <li><strong>Incline Dumbbell Press (Chest):</strong> 3 Sets, 10-12 Reps</li>
                <li><strong>Single-Arm Dumbbell Rows:</strong> 3 Sets per arm, 10 Reps</li>
                <li><strong>Lateral Raises (Shoulders):</strong> 4 Sets, 15-20 Reps (High volume)</li>
                <li><strong>Bicep Curls (Barbell or Dumbbell):</strong> 3 Sets, 12 Reps</li>
            </ul>
            <hr>
            <h4>Day 5: Lower Body (Glutes/Hams Focus)</h4>
            <ul>
                <li><strong>Leg Press (High Stance/Glute focus):</strong> 4 Sets, 8-12 Reps</li>
                <li><strong>Bulgarian Split Squats (Dumbbell):</strong> 3 Sets per leg, 10-12 Reps</li>
                <li><strong>Lying Leg Curls (Hamstrings Isolation):</strong> 3 Sets, 12-15 Reps</li>
                <li><strong>Abdominal Crunches or Hanging Leg Raises:</strong> 3 Sets, 15-20 Reps</li>
                <li><strong>Hip Thrusts (Glutes):</strong> 3 Sets, 10-12 Reps</li>
            </ul>
            <hr>
            <h4>Day 6 & 7: Rest/Low-Intensity Cardio</h4>
        """

        # Detailed 6-Meal, 3000-Calorie Diet Plan
        meal_plan_details = """
            <p><strong>Daily Goal:</strong> ~3000 kcal | Protein: 260g | Fat: 67g | Carbs: 365g</p>
            <p>This plan is high in protein and carbohydrates, optimized for muscle recovery and energy.</p>
            <hr>
            <h4>Meal 1 (Breakfast - Pre-Workout)</h4>
            <ul>
                <li>**Ingredients:** 1 cup Dry Rolled Oats (cooked with 1.5 cups water/skim milk), 1 scoop **Whey Protein**, 1 medium Banana.</li>
                <li>**Approx. Macros:** **Calories:** 600 | **Protein:** 50g | **Fat:** 10g | **Carbs:** 75g</li>
            </ul>
            <hr>
            <h4>Meal 2 (Post-Workout Shake/Snack)</h4>
            <ul>
                <li>**Ingredients:** 1.5 scoops **Whey Protein**, 1.5 cups Skim Milk or Almond Milk, 1 cup frozen Mixed Berries.</li>
                <li>**Approx. Macros:** **Calories:** 350 | **Protein:** 45g | **Fat:** 5g | **Carbs:** 35g</li>
            </ul>
            <hr>
            <h4>Meal 3 (Lunch)</h4>
            <ul>
                <li>**Ingredients:** 175g Cooked **Chicken Breast** or **Paneer/Tofu** (Veg option), 1.5 cups Cooked Brown Rice, 1 cup Mixed Steamed Vegetables.</li>
                <li>**Approx. Macros:** **Calories:** 650 | **Protein:** 60g | **Fat:** 7g | **Carbs:** 85g</li>
            </ul>
            <hr>
            <h4>Meal 4 (Mid-Afternoon Snack)</h4>
            <ul>
                <li>**Ingredients:** 1 scoop **Whey Protein**, 1 Large Apple or Pear, 2 Rice Cakes.</li>
                <li>**Approx. Macros:** **Calories:** 300 | **Protein:** 25g | **Fat:** 2g | **Carbs:** 45g</li>
            </ul>
            <hr>
            <h4>Meal 5 (Dinner)</h4>
            <ul>
                <li>**Ingredients:** 175g **Lean Steak** or **Fish** / **Lentil Curry** (Veg option), 1 Large Baked Sweet Potato, Large Green Salad with 1 tbsp Olive Oil.</li>
                <li>**Approx. Macros:** **Calories:** 700 | **Protein:** 55g | **Fat:** 25g | **Carbs:** 75g</li>
            </ul>
            <hr>
            <h4>Meal 6 (Pre-Bed)</h4>
            <ul>
                <li>**Ingredients:** 1 cup Low-Fat **Greek Yogurt** or **Cottage Cheese**, 1/4 cup Walnuts/Almonds.</li>
                <li>**Approx. Macros:** **Calories:** 400 | **Protein:** 25g | **Fat:** 18g | **Carbs:** 50g</li>
            </ul>
            <hr>
            <p><strong>DAILY TOTAL (Approx.):</strong> **Calories:** 3000 | **Total Protein:** 260g | **Total Fat:** 67g | **Total Carbs:** 365g</p>
        """

        if dietary_preference == "Vegetarian":
            diet_plan = f"""
                <p><strong>Dietary Recommendations (Vegetarian - {calories} kcal):</strong> Focus on a calorie deficit while maintaining high protein intake (around 30% of calories) to protect muscle mass.</p>
                <ul>
                    <li>**Protein Sources:** Lentils, chickpeas, tofu, paneer (in moderation), and Greek yogurt.</li>
                    <li>**Meal Frequency:** 4-5 smaller meals/snacksto manage hunger.</li>
                    <li>**Avoid:** Sugary drinks and excessive processed foods.</li>
                </ul>
            """
        else:
            diet_plan = f"""
                <p><strong>Dietary Recommendations (Non-Vegetarian - {calories} kcal):</strong> Focus on a calorie deficit while maintaining high protein intake (around 30% of calories) to protect muscle mass.</p>
                <ul>
                    <li>**Protein Sources:** Lean chicken breast, fish (salmon, tuna), eggs, and lean beef.</li>
                    <li>**Focus:** High-fiber vegetables and lean protein at every meal for satiety.</li>
                    <li>**Hydration:** Drink plenty of water throughout the day.</li>
                </ul>
            """

    # 2. Lose Weight: Calorie Deficit (TDEE - 500 kcal) and high-volume workout
    elif goal == "Lose Weight":
        calories = int(tdee - 500)

        workout_plan = """
            <p><strong>Goal:</strong> Fat Loss and Muscle Retention.</p>
            <p><strong>Target Calories:</strong> TDEE - 500 kcal (Calorie Deficit)</p>
            <p><strong>Training Split:</strong> 3-Day Full Body or Upper/Lower Split. Focus on high-intensity and high-volume (12-15 reps) to maximize calorie burn and preserve muscle.</p>
            <hr>
            <ul>
                <li><strong>Strength Training:</strong> 3 times a week (Full-Body or Upper/Lower). Focus on **compound movements** like Squats, Deadlifts, Bench Press, and Rows.</li>
                <li><strong>Cardio:</strong> 3-4 times a week. Include **High-Intensity Interval Training (HIIT)** (20-25 mins) or steady-state cardio (30-45 mins).</li>
                <li><strong>Reps/Sets:</strong> Strength training at 3 Sets of 12-15 Reps.</li>
            </ul>
        """
        if dietary_preference == "Vegetarian":
            diet_plan = f"""
                <p><strong>Dietary Recommendations (Vegetarian - {calories} kcal):</strong> Focus on a calorie deficit while maintaining high protein intake (around 30% of calories) to protect muscle mass.</p>
                <ul>
                    <li>**Protein Sources:** Lentils, chickpeas, tofu, paneer (in moderation), and Greek yogurt.</li>
                    <li>**Meal Frequency:** 4-5 smaller meals/snacksto manage hunger.</li>
                    <li>**Avoid:** Sugary drinks and excessive processed foods.</li>
                </ul>
            """
        else:
            diet_plan = f"""
                <p><strong>Dietary Recommendations (Non-Vegetarian - {calories} kcal):</strong> Focus on a calorie deficit while maintaining high protein intake (around 30% of calories) to protect muscle mass.</p>
                <ul>
                    <li>**Protein Sources:** Lean chicken breast, fish (salmon, tuna), eggs, and lean beef.</li>
                    <li>**Focus:** High-fiber vegetables and lean protein at every meal for satiety.</li>
                    <li>**Hydration:** Drink plenty of water throughout the day.</li>
                </ul>
            """

    # 3. Improve Endurance: Maintenance calories and endurance-based workout
    elif goal == "Improve Endurance":
        calories = tdee  # Maintenance

        workout_plan = """
            <p><strong>Goal:</strong> Improve Cardiovascular and Muscular Endurance.</p>
            <p><strong>Target Calories:</strong> TDEE (Maintenance) to fuel high activity levels.</p>
            <p><strong>Training Split:</strong> 5-6 Days of Cardio/Hybrid Training with light strength work.</p>
            <hr>
            <ul>
                <li><strong>Endurance/Cardio:</strong> 3-4 times a week (running, cycling, swimming) for 45-90 minutes. Gradually increase duration.</li>
                <li><strong>Strength Training:</strong> 2 times a week (Full-Body). Focus on **high repetitions (15-20)** with lighter weights to build muscular endurance.</li>
                <li>**Example:** Circuit Training, Kettlebell workouts, and Pilates.</li>
            </ul>
        """
        if dietary_preference == "Vegetarian":
            diet_plan = f"""
                <p><strong>Dietary Recommendations (Vegetarian - {calories} kcal):</strong> Focus on high complex carbohydrates (60-65%) to fuel long training sessions, balanced with protein.</p>
                <ul>
                    <li>**Carbs:** Oats, whole-wheat pasta/bread, brown rice, sweet potatoes.</li>
                    <li>**Protein:** Beans, quinoa, legumes.</li>
                    <li>**Timing:** Prioritize complex carbs before long workouts and replenish with simple carbs/protein post-workout.</li>
                </ul>
            """
        else:
            diet_plan = f"""
                <p><strong>Dietary Recommendations (Non-Vegetarian - {calories} kcal):</strong> Focus on high complex carbohydrates (60-65%) to fuel long training sessions, balanced with protein.</p>
                <ul>
                    <li>**Carbs:** Oats, whole-wheat pasta/bread, brown rice, sweet potatoes.</li>
                    <li>**Protein:** Chicken, eggs, fish.</li>
                    <li>**Timing:** Prioritize complex carbs before long workouts and replenish with simple carbs/protein post-workout.</li>
                </ul>
            """

    # 4. Maintain Fitness: Maintenance calories and balanced workout
    else:  # Maintain Fitness
        calories = tdee  # Maintenance

        workout_plan = """
            <p><strong>Goal:</strong> Maintain Current Strength and Cardiovascular Health.</p>
            <p><strong>Target Calories:</strong> TDEE (Maintenance).</p>
            <p><strong>Training Split:</strong> 3-4 Days of Balanced Full-Body or Upper/Lower Split.</p>
            <hr>
            <ul>
                <li><strong>Strength Training:</strong> 2-3 times a week (Full-Body). Moderate weight, 8-12 reps.</li>
                <li><strong>Cardio:</strong> 2-3 times a week (Moderate intensity) for 30 minutes.</li>
                <li>**Focus:** Enjoyable activity and consistency in both strength and cardio.</li>
            </ul>
        """
        if dietary_preference == "Vegetarian":
            diet_plan = f"""
                <p><strong>Dietary Recommendations (Vegetarian - {calories} kcal):</strong> Focus on balanced macronutrients (e.g., Carbs 50%, Protein 20%, Fat 30%) to support overall health.</p>
                <ul>
                    <li>**Emphasis:** Variety in fruits, vegetables, whole grains, and lean plant protein sources.</li>
                    <li>**Healthy Fats:** Nuts, seeds, avocado, and olive oil.</li>
                </ul>
            """
        else:
            diet_plan = f"""
                <p><strong>Dietary Recommendations (Non-Vegetarian - {calories} kcal):</strong> Focus on balanced macronutrients (e.g., Carbs 50%, Protein 20%, Fat 30%) to support overall health.</p>
                <ul>
                    <li>**Emphasis:** Lean meats, fish, whole grains, and a high intake of vegetables.</li>
                    <li>**Monitoring:** Pay attention to hunger/satiety to ensure maintenance calorie goal is accurate.</li>
                </ul>
            """

    # --- Health Warning Logic (Unchanged) ---
    health_warning = "No specific health concerns reported. Please proceed with your plan as outlined."
    if physical_injury or medical_illness:
        warning_message = "### **Important Health Warning**\n\n"
        warning_message += "Your health plan has been generated based on the information provided, but your reported conditions require caution.\n\n"
        if physical_injury:
            warning_message += f"- **Physical Injury:** You reported having **{physical_injury}**. Please consult a medical professional or physical therapist before starting any new exercise routine. Avoid exercises that cause pain or discomfort.\n"
        if medical_illness:
            warning_message += f"- **Medical Illness:** You reported having **{medical_illness}**. It is crucial to consult your doctor before making any significant changes to your diet or exercise routine. They can provide guidance to ensure your plan is safe and effective for your specific condition.\n"
        warning_message += "\n**Always listen to your body and prioritize safety.**"
        health_warning = warning_message

    return {
        "goal": goal,
        "calories": calories,
        "workout_plan": workout_plan,
        "diet_plan": diet_plan,
        "health_warning": health_warning
    }


# --- Database functions (Unchanged) ---

def init_db():
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY,
                       username
                       TEXT
                       NOT
                       NULL
                       UNIQUE,
                       contact
                       TEXT
                       NOT
                       NULL
                       UNIQUE,
                       email
                       TEXT
                       NOT
                       NULL
                       UNIQUE,
                       gender
                       TEXT
                       NOT
                       NULL,
                       address
                       TEXT
                       NOT
                       NULL,
                       password_hash
                       TEXT
                       NOT
                       NULL
                   )
                   ''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS health_profiles
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY,
                       user_id
                       INTEGER
                       NOT
                       NULL
                       UNIQUE,
                       age
                       INTEGER,
                       height_ft
                       INTEGER,
                       height_in
                       INTEGER,
                       weight_kg
                       REAL,
                       activity_level
                       TEXT,
                       fitness_goal
                       TEXT,
                       dietary_preference
                       TEXT,
                       physical_injury
                       TEXT,
                       medical_illness
                       TEXT,
                       FOREIGN
                       KEY
                   (
                       user_id
                   ) REFERENCES users
                   (
                       id
                   )
                       )
                   ''')

    # Check and add new columns if necessary
    try:
        cursor.execute("SELECT dietary_preference FROM health_profiles LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE health_profiles ADD COLUMN dietary_preference TEXT")

    try:
        cursor.execute("SELECT physical_injury FROM health_profiles LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE health_profiles ADD COLUMN physical_injury TEXT")

    try:
        cursor.execute("SELECT medical_illness FROM health_profiles LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE health_profiles ADD COLUMN medical_illness TEXT")

    conn.commit()
    conn.close()


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def register_user(username, contact, email, gender, address, password):
    init_db()
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()

    # Check for uniqueness
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Username already exists.")

    cursor.execute("SELECT COUNT(*) FROM users WHERE contact = ? OR email = ?", (contact, email))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Contact or email already exists. Please use a different one.")

    hashed_password = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, contact, email, gender, address, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (username, contact, email, gender, address, hashed_password))
        conn.commit()
    finally:
        conn.close()


def login_user(username, password):
    init_db()
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hash = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

    return False


def get_user_id_by_username(username):
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_health_profile(user_id):
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_profiles WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def add_health_profile(user_id, age, height_ft, height_in, weight_kg, activity_level, fitness_goal, dietary_preference,
                       physical_injury, medical_illness):
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO health_profiles (user_id, age, height_ft, height_in, weight_kg, activity_level, fitness_goal, dietary_preference, physical_injury, medical_illness) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, age, height_ft, height_in, weight_kg, activity_level, fitness_goal, dietary_preference,
         physical_injury, medical_illness)
    )
    conn.commit()
    conn.close()


def update_health_profile(user_id, age, height_ft, height_in, weight_kg, activity_level, fitness_goal,
                          dietary_preference, physical_injury, medical_illness):
    conn = sqlite3.connect('credentials.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE health_profiles
        SET age                = ?,
            height_ft          = ?,
            height_in          = ?,
            weight_kg          = ?,
            activity_level     = ?,
            fitness_goal       = ?,
            dietary_preference = ?,
            physical_injury    = ?,
            medical_illness    = ?
        WHERE user_id = ?
        """,
        (age, height_ft, height_in, weight_kg, activity_level, fitness_goal, dietary_preference, physical_injury,
         medical_illness, user_id)
    )
    conn.commit()
    conn.close()


# --- Main App Logic to display the correct page ---
if st.session_state.username:
    show_sidebar_navigation()
    if st.session_state.current_page == 'profile_page':
        profile_page()
    elif st.session_state.current_page == 'edit_profile':
        edit_profile_page()
    elif st.session_state.current_page == 'health_plan':
        health_plan_page()
    elif st.session_state.current_page == 'about':
        about_page()
    elif st.session_state.current_page == 'contact':
        contact_page()
    else:  # Default to profile page if logged in but on an undefined state
        profile_page()
else:
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'register':
        register_page()
    elif st.session_state.current_page == 'login':
        login_page()
    elif st.session_state.current_page == 'about':
        about_page()
    elif st.session_state.current_page == 'contact':
        contact_page()
    else:  # If trying to access a restricted page, go to home
        home_page()