import streamlit as st
import pandas as pd
import io

def show():
    st.header("📝 Fill the Form to Create a CSV File")

    # Initialize session state variables
    if "form_page" not in st.session_state:
        st.session_state.form_page = 1  # Start at Page 1
        st.session_state.personal_data = {}  # Store personal details
        st.session_state.conditions = []  # Store multiple conditions

    # ------------------- PAGE 1: PERSONAL DETAILS -------------------
    if st.session_state.form_page == 1:
        st.subheader("Personal Details")

        with st.form("personal_details_form"):
            name = st.text_input("Full Name")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            sex = st.selectbox("Sex", ["Male", "Female", "Other"])
            height = st.number_input("Height (cm)", min_value=50, max_value=250, step=1)
            weight = st.number_input("Weight (kg)", min_value=10, max_value=300, step=1)
            city = st.text_input("City")
            state = st.text_input("State")
            country = st.text_input("Country")

            next_page = st.form_submit_button("Next ➡️")

        if next_page:
            st.session_state.personal_data = {
                "Name": name, "Age": age, "Sex": sex, "Height": height,
                "Weight": weight, "City": city, "State": state, "Country": country
            }
            st.session_state.form_page = 2
            st.rerun()

    # ------------------- PAGE 2: HEALTH EXPENDITURE -------------------
    elif st.session_state.form_page == 2:
        st.subheader("Expenditure on Health")

        # Input fields for a single condition
        with st.form("health_expenditure_form"):
            condition_name = st.text_input("Condition Name")
            start_date = st.date_input("Condition Start Date")
            end_date = st.date_input("Condition End Date")
            hospitalized_type = st.radio("Hospitalized Type", ["Home", "Hospital"])
            hospital_name = st.text_input("Hospital Name") if hospitalized_type == "Hospital" else "N/A"
            cost = st.number_input("Cost (Total Amount Spent)", min_value=0.0, step=100.0)

            add_condition = st.form_submit_button("➕ Add Another Condition")
            submit = st.form_submit_button("✅ Submit")

        # Check if 'Date' fields (start_date, end_date) are filled correctly
        if start_date and end_date:
            if end_date < start_date:
                st.error("End date cannot be earlier than start date.")
            else:
                # If form is valid, append condition data to session state
                if add_condition:
                    st.session_state.conditions.append({
                        "Condition Name": condition_name, "Start Date": start_date, "End Date": end_date,
                        "Hospitalized Type": hospitalized_type, "Hospital Name": hospital_name, "Cost": cost
                    })
                    st.rerun()  # Rerun the app to display updated conditions

                if submit:
                    # Store the final entered condition before submitting
                    st.session_state.conditions.append({
                        "Condition Name": condition_name, "Start Date": start_date, "End Date": end_date,
                        "Hospitalized Type": hospitalized_type, "Hospital Name": hospital_name, "Cost": cost
                    })
                    st.session_state.form_page = 3
                    st.rerun()

        # Show stored conditions in a table before submission
        if st.session_state.conditions:
            st.write("### Added Conditions")
            st.dataframe(pd.DataFrame(st.session_state.conditions))

    # ------------------- PAGE 3: CSV DOWNLOAD -------------------
    elif st.session_state.form_page == 3:
        st.subheader("✅ Submission Complete! Download Your Data")

        # Check if 'Date' columns are present in the conditions data before proceeding to CSV download
        if all('Start Date' in condition and 'End Date' in condition for condition in st.session_state.conditions):
            # Combine Personal & Condition Data
            data = [st.session_state.personal_data] * len(st.session_state.conditions)
            df_personal = pd.DataFrame(data)
            df_conditions = pd.DataFrame(st.session_state.conditions)

            final_df = pd.concat([df_personal, df_conditions], axis=1)

            # Convert to CSV
            csv_buffer = io.StringIO()
            final_df.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue().encode()

            # Show CSV Download Button
            st.download_button(
                label="📥 Download CSV File",
                data=csv_bytes,
                file_name="health_expenses.csv",
                mime="text/csv"
            )
        else:
            st.error("Please make sure each condition has a valid 'Start Date' and 'End Date'.")

        # Reset Form for New Entry
        if st.button("🔄 Start New Entry"):
            st.session_state.form_page = 1
            st.session_state.personal_data = {}
            st.session_state.conditions = []
            st.rerun()
