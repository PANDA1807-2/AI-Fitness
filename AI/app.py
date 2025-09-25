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
    st.session_state.current_page = 'home'
    st.session_state.current_page = page_name


# --- Custom CSS for Professional Design ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background-color: #f5f7fa;
}

.header {
    background-color: #ffffff;
    padding: 30px;
    border-bottom: 2px solid #e0e0e0;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}
.header h1 {
    color: #1a1a1a;
    font-size: 2.5rem;
    font-weight: 600;
}

.footer {
    background-color: #333333;
    color: #ffffff;
    padding: 20px;
    text-align: center;
    font-size: 14px;
    margin-top: 50px;
    border-radius: 8px;
}

.blog-post {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
    margin-bottom: 25px;
    transition: transform 0.2s ease-in-out;
}
.blog-post:hover {
    transform: translateY(-5px);
}
.blog-post h3 {
    color: #3366ff;
    font-weight: 600;
}
.blog-post p {
    color: #555555;
    line-height: 1.6;
}

.stButton>button {
    background-color: #3366ff;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.2s, transform 0.2s;
}
.stButton>button:hover {
    background-color: #254ac9;
    transform: translateY(-2px);
}

.centered-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 80vh; /* Use viewport height to center vertically */
}
.form-container {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
    width: 100%;
    max-width: 600px;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)


# --- Define the Header and Footer functions ---
def show_header():
    st.markdown('<div class="header"><h1>AI-Fitness Assistant</h1></div>', unsafe_allow_html=True)
    st.markdown("---")


def show_footer():
    st.markdown('<div class="footer">© 2025 AI-Fitness Assistant. All rights reserved.</div>', unsafe_allow_html=True)


# --- Define the Home Page Content ---
def home_page():
    # Header
    show_header()

    # Hero image and main text
    st.image("https://images.unsplash.com/photo-1571019613454-1cb2fcdb467e?q=80&w=1740&auto=format&fit=crop",
             caption="Achieve your fitness goals with AI.",
             use_column_width=True)

    # Title and buttons section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("Your Personal Health & Fitness Guide")
        st.write("Get a personalized health plan based on your unique data and goals.")

        # Centering the buttons
        button_col1, button_col2, button_col3 = st.columns([1, 1, 1])
        with button_col1:
            reg_button = st.button("Register")
        with button_col3:
            login_button = st.button("Login")

        st.markdown(
            """
            <div style="text-align: center; margin-top: 10px;">
                <p style="margin: 0; font-size: 14px; color: #555;">Already have an account?</p>
            </div>
            """, unsafe_allow_html=True
        )

    # The Logic for the buttons
    if reg_button:
        set_page('register')
    if login_button:
        set_page('login')

    # Information Blog Section
    st.markdown("---")
    st.subheader("Fitness Blog")

    # Blog Post 1
    st.markdown('<div class="blog-post">', unsafe_allow_html=True)
    st.markdown("<h3>The Importance of Consistency</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p>Consistency is key in any fitness journey. Discover how to build a routine that works for you and leads to long-term success.</p>",
        unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Blog Post 2
    st.markdown('<div class="blog-post">', unsafe_allow_html=True)
    st.markdown("<h3>Understanding Macronutrients</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p>Learn about the role of proteins, carbohydrates, and fats in your diet and how to balance them for your fitness goals.</p>",
        unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    show_footer()


# --- Registration Page ---
def register_page():
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Create Your Account")
        st.write("Join the AI-Fitness Assistant to get a personalized health plan.")

        with st.form("registration_form"):
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

        text_col, button_col = st.columns([1, 1])
        with text_col:
            st.markdown(
                """
                <div style="text-align: right; margin-top: 20px;">
                    <p style="margin: 0; font-size: 14px; color: #555;">Already have an account?</p>
                </div>
                """, unsafe_allow_html=True
            )
        with button_col:
            if st.button("Login", key="login_reg"):
                set_page('login')

    if st.button("Back to Home", key="back_reg"):
        set_page('home')

    show_footer()


# --- Login Page ---
def login_page():
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("Login to Your Account")
        st.write("Welcome back! Please enter your credentials to log in.")

        with st.form("login_form"):
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if login_user(login_username, login_password):
                    st.session_state.username = login_username
                    st.success(f"Welcome back, {login_username}!")
                    set_page('profile_page')
                else:
                    st.error("Invalid username or password.")

        st.markdown(
            """
            <div style="text-align: center; margin-top: 20px;">
                <p style="margin: 0; font-size: 14px; color: #555;">Don't have an account?</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Register", key="reg_login"):
            set_page('register')

    if st.button("Back to Home", key="back_login"):
        set_page('home')

    show_footer()


# --- User Profile Page ---
def profile_page():
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("Your Health Profile")

        user_id = get_user_id_by_username(st.session_state.username)
        if user_id:
            profile_data = get_health_profile(user_id)

            if profile_data:
                st.subheader("Your Current Profile")
                st.info("This is the data stored in your health profile. You can edit it if needed.")
                st.write(f"**Age:** {profile_data[2]} years")
                st.write(f"**Height:** {profile_data[3]} feet, {profile_data[4]} inches")
                st.write(f"**Weight:** {profile_data[5]} kg")
                st.write(f"**Activity Level:** {profile_data[6]}")
                st.write(f"**Fitness Goal:** {profile_data[7]}")
                st.write(f"**Dietary Preference:** {profile_data[8]}")
                st.write(f"**Physical Injury:** {profile_data[9] if profile_data[9] else 'None'}")
                st.write(f"**Medical Illness:** {profile_data[10] if profile_data[10] else 'None'}")

                # Option to edit or view health plan
                col_edit, col_plan = st.columns(2)
                with col_edit:
                    if st.button("Edit Profile", key="edit_profile"):
                        set_page('edit_profile')
                with col_plan:
                    if st.button("Get Health Plan", key="get_plan"):
                        st.session_state.profile_data = profile_data
                        set_page('health_plan')

            else:
                st.subheader("Complete Your Health Profile")
                st.write("Please provide the following information to receive a personalized health plan.")

                with st.form("health_profile_form"):
                    age = st.number_input("Age", min_value=1, max_value=120, step=1, key="profile_age")
                    col_height_ft, col_height_in = st.columns(2)
                    with col_height_ft:
                        height_ft = st.number_input("Height (feet)", min_value=0, max_value=8, step=1, key="profile_ft")
                    with col_height_in:
                        height_in = st.number_input("Height (inches)", min_value=0, max_value=11, step=1,
                                                    key="profile_in")

                    weight_kg = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, step=0.1,
                                                key="profile_weight")

                    activity_level = st.selectbox(
                        "Your typical weekly activity level?",
                        ["Select Level", "Sedentary", "Lightly Active", "Moderately Active", "Very Active",
                         "Super Active"],
                        key="profile_activity"
                    )

                    fitness_goal = st.selectbox(
                        "Your primary fitness goal?",
                        ["Select Goal", "Lose Weight", "Gain Muscle", "Improve Endurance", "Maintain Fitness"],
                        key="profile_goal"
                    )

                    dietary_preference = st.selectbox(
                        "Your dietary preference?",
                        ["Select Preference", "Vegetarian", "Non-Vegetarian"],
                        key="profile_diet"
                    )

                    physical_injury = st.text_area("Any physical injuries? (e.g., knee pain, shoulder injury)")
                    medical_illness = st.text_area("Any medical illnesses? (e.g., high blood pressure, diabetes)")

                    submitted = st.form_submit_button("Save Profile")

                    if submitted:
                        if age and height_ft and height_in and weight_kg and activity_level != "Select Level" and fitness_goal != "Select Goal" and dietary_preference != "Select Preference":
                            add_health_profile(user_id, age, height_ft, height_in, weight_kg, activity_level,
                                               fitness_goal, dietary_preference, physical_injury, medical_illness)
                            st.success("Your health profile has been saved successfully!")
                            st.experimental_rerun()  # Rerun to show the saved data
                        else:
                            st.error("Please fill in all the fields.")

        if st.button("Log out"):
            st.session_state.username = None
            set_page('home')

    show_footer()


# --- Edit Profile Page ---
def edit_profile_page():
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("Edit Your Health Profile")

        user_id = get_user_id_by_username(st.session_state.username)
        profile_data = get_health_profile(user_id)

        if profile_data:
            # Recreate the form with pre-filled values
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

                age = st.number_input("Age", min_value=1, max_value=120, step=1, value=current_age, key="edit_age")
                col_height_ft, col_height_in = st.columns(2)
                with col_height_ft:
                    height_ft = st.number_input("Height (feet)", min_value=0, max_value=8, step=1,
                                                value=current_height_ft, key="edit_ft")
                with col_height_in:
                    height_in = st.number_input("Height (inches)", min_value=0, max_value=11, step=1,
                                                value=current_height_in, key="edit_in")

                weight_kg = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, step=0.1,
                                            value=current_weight_kg, key="edit_weight")

                activity_levels = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"]
                activity_index = activity_levels.index(
                    current_activity_level) if current_activity_level in activity_levels else 0
                activity_level = st.selectbox(
                    "Your typical weekly activity level?",
                    activity_levels,
                    index=activity_index,
                    key="edit_activity"
                )

                fitness_goals = ["Lose Weight", "Gain Muscle", "Improve Endurance", "Maintain Fitness"]
                goal_index = fitness_goals.index(current_fitness_goal) if current_fitness_goal in fitness_goals else 0
                fitness_goal = st.selectbox(
                    "Your primary fitness goal?",
                    fitness_goals,
                    index=goal_index,
                    key="edit_goal"
                )

                dietary_preferences = ["Vegetarian", "Non-Vegetarian"]
                diet_index = dietary_preferences.index(
                    current_dietary_preference) if current_dietary_preference in dietary_preferences else 0
                dietary_preference = st.selectbox(
                    "Your dietary preference?",
                    dietary_preferences,
                    index=diet_index,
                    key="edit_diet"
                )

                physical_injury = st.text_area("Any physical injuries?", value=current_physical_injury,
                                               key="edit_injury")
                medical_illness = st.text_area("Any medical illnesses?", value=current_medical_illness,
                                               key="edit_illness")

                submitted = st.form_submit_button("Save Changes")
                if submitted:
                    update_health_profile(user_id, age, height_ft, height_in, weight_kg, activity_level, fitness_goal,
                                          dietary_preference, physical_injury, medical_illness)
                    st.success("Your health profile has been updated successfully!")
                    st.session_state.profile_data = get_health_profile(user_id)  # Update session state with new data
                    set_page('profile_page')  # Redirect to the profile page

        if st.button("Back to Profile", key="back_edit"):
            set_page('profile_page')
        if st.button("Log out", key="logout_edit"):
            st.session_state.username = None
            set_page('home')

    show_footer()


def health_plan_page():
    show_header()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.header("Your Personalized Health Plan")
        st.write("Here are your recommendations based on your health profile.")

        if st.session_state.get('profile_data'):
            plan = generate_health_plan(st.session_state.profile_data)

            st.subheader("Overview")
            st.info(f"**Goal:** {plan['goal']}")
            st.info(f"**Recommended Daily Calories:** {plan['calories']} kcal")

            st.subheader("Workout Plan")
            st.markdown(plan['workout_plan'], unsafe_allow_html=True)

            st.subheader("Dietary Recommendations")
            st.markdown(plan['diet_plan'], unsafe_allow_html=True)

            st.subheader("Important Health Information")
            st.warning(plan['health_warning'])

        else:
            st.warning("Please complete your health profile first.")
            if st.button("Go to Profile Page"):
                set_page('profile_page')

        if st.button("Back to Profile", key="back_to_profile"):
            set_page('profile_page')

    show_footer()


# --- Placeholder AI/Analysis Logic ---
def generate_health_plan(profile_data):
    """
    This is a placeholder for your AI/analysis logic.
    It takes the user's profile data and returns a personalized plan.
    """
    # Example rule-based logic
    goal = profile_data[7]
    weight_kg = profile_data[5]
    height_cm = (profile_data[3] * 30.48) + (profile_data[4] * 2.54)
    age = profile_data[2]
    activity_level = profile_data[6]
    dietary_preference = profile_data[8]
    physical_injury = profile_data[9]
    medical_illness = profile_data[10]

    # Simple BMR calculation (Mifflin-St Jeor)
    # This is a basic example; for a real app, use a more robust formula
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5  # Male
    # Adjust for activity level
    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.9,
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)

    if goal == "Lose Weight":
        calories = int(tdee - 500)
        workout_plan = """
            <p><strong>Workout Plan:</strong> Focus on a mix of cardio and strength training.</p>
            <ul>
                <li><strong>Cardio:</strong> 3-4 times a week (e.g., running, cycling for 30-45 minutes).</li>
                <li><strong>Strength Training:</strong> 2-3 times a week (full-body workouts with moderate weights and higher repetitions).</li>
            </ul>
        """
    elif goal == "Gain Muscle":
        calories = int(tdee + 500)
        workout_plan = """
            <p><strong>Workout Plan:</strong> Focus on progressive overload with heavy lifting.</p>
            <ul>
                <li><strong>Strength Training:</strong> 4-5 times a week (split routines targeting different muscle groups).</li>
                <li><strong>Cardio:</strong> 1-2 times a week (optional, to maintain cardiovascular health).</li>
            </ul>
        """
    else:
        calories = int(tdee)
        workout_plan = "<p><strong>Workout Plan:</strong> A balanced routine to maintain your current fitness level.</p>"

    # Dietary plan based on preference
    if dietary_preference == "Vegetarian":
        diet_plan = """
            <p><strong>Dietary Recommendations (Vegetarian):</strong> Aim for a balanced diet focusing on plant-based protein.</p>
            <ul>
                <li><strong>Protein Sources:</strong> Lentils, chickpeas, tofu, paneer, and Greek yogurt.</li>
                <li><strong>Healthy Fats:</strong> Avocado, nuts, seeds, and olive oil.</li>
                <li><strong>Complex Carbs:</strong> Oats, brown rice, whole-wheat bread, and quinoa.</li>
                <li><strong>Fruits:</strong> Berries, apples, bananas, oranges, and grapes.</li>
            </ul>
        """
    else:  # Non-Vegetarian
        diet_plan = """
            <p><strong>Dietary Recommendations (Non-Vegetarian):</strong> Incorporate lean protein for muscle repair and growth.</p>
            <ul>
                <li><strong>Protein Sources:</strong> Chicken breast, fish (salmon, tuna), eggs, and lean beef.</li>
                <li><strong>Healthy Fats:</strong> Avocado, nuts, seeds, and olive oil.</li>
                <li><strong>Complex Carbs:</strong> Oats, brown rice, whole-wheat bread, and sweet potatoes.</li>
                <li><strong>Fruits:</strong> Berries, apples, bananas, oranges, and grapes.</li>
            </ul>
        """

    # Health warnings based on injuries and illnesses
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


# --- Database functions ---

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

    # Check if the dietary_preference column exists and add it if not
    try:
        cursor.execute("SELECT dietary_preference FROM health_profiles LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE health_profiles ADD COLUMN dietary_preference TEXT")

    # Check and add new columns for physical injury and medical illness
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

    # Check for uniqueness of username
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Username already exists.")

    # Check for uniqueness of contact and email
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
        # bcrypt.checkpw expects bytes
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
if st.session_state.current_page == 'home':
    home_page()
elif st.session_state.current_page == 'register':
    register_page()
elif st.session_state.current_page == 'login':
    login_page()
elif st.session_state.current_page == 'profile_page':
    if st.session_state.username:
        profile_page()
    else:
        set_page('home')
elif st.session_state.current_page == 'edit_profile':
    if st.session_state.username:
        edit_profile_page()
    else:
        set_page('home')
elif st.session_state.current_page == 'health_plan':
    if st.session_state.username:
        health_plan_page()
    else:
        set_page('home')
