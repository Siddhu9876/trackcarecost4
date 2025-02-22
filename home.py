import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

def show():
    st.header("Welcome to Track Care Cost")
    st.write("Upload a csv file to track you expenditures")
    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

    if uploaded_file is not None:
        # Read the uploaded CSV into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Show the data preview
        st.write("### Preview of the uploaded data")
        st.dataframe(df.head())
        
        # Navigate through different pages
        page = st.radio("Select a page to view analysis", ["📂 Data Entered", "📊 Visual Representation of Expenditure", "📈 Future Expenditures Prediction", "💡 Suggestions to Reduce Expenditure"])
        
        # Call respective page functions based on the radio selection
        if page == "📂 Data Entered":
            page1(df)
        elif page == "📊 Visual Representation of Expenditure":
            page2(df)
        elif page == "📈 Future Expenditures Prediction":
            page3(df)
        elif page == "💡 Suggestions to Reduce Expenditure":
            suggest_to_reduce_expenditure(df)


def page1(df):
    st.header("📂 Data Entered")
    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

def page2(df):
    st.header("📊 Visual Representation of Expenditure")
    st.write("### Cost Distribution (Over Time)")

    # Convert 'Start Date' and 'End Date' to 'Date' for time-series analysis
    if "Start Date" in df.columns and "End Date" in df.columns:
        # Create a 'Date' range based on 'Start Date' and 'End Date'
        # We will create a new column that contains all dates between Start and End dates
        all_dates = []

        for index, row in df.iterrows():
            start_date = pd.to_datetime(row['Start Date'])
            end_date = pd.to_datetime(row['End Date'])
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            all_dates.extend(date_range)

        # Create a DataFrame with all dates and corresponding cost entries
        cost_data = []
        for index, row in df.iterrows():
            start_date = pd.to_datetime(row['Start Date'])
            end_date = pd.to_datetime(row['End Date'])
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            cost_data.extend([row['Cost']] * len(date_range))

        # Combine into a DataFrame with 'Date' and 'Cost'
        date_cost_df = pd.DataFrame({
            'Date': all_dates,
            'Cost': cost_data
        })

        # Set 'Date' as index
        date_cost_df.set_index('Date', inplace=True)
        date_cost_df.sort_index(inplace=True)

        # Plot time-series of costs over time
        fig, ax = plt.subplots(figsize=(10, 6))
        date_cost_df['Cost'].plot(ax=ax)
        ax.set_title('Expenditure Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cost')
        st.pyplot(fig)

        # Bar chart for amount spent on different health conditions
        if "Condition Name" in df.columns:
            condition_grouped = df.groupby('Condition Name')['Cost'].sum()
            st.write("### Expenditure for Different Health Conditions")
            fig, ax = plt.subplots(figsize=(8, 5))
            condition_grouped.plot(kind='bar', ax=ax)
            ax.set_title('Expenditure per Health Condition')
            ax.set_xlabel('Health Condition')
            ax.set_ylabel('Amount Spent')
            st.pyplot(fig)

            # Pie chart for amounts spent on different health conditions
            st.write("### Expenditure Distribution by Health Conditions (Pie Chart)")
            fig, ax = plt.subplots(figsize=(8, 8))
            condition_grouped.plot(kind='pie', autopct='%1.1f%%', ax=ax)
            ax.set_title('Expenditure Distribution by Health Conditions')
            st.pyplot(fig)
        else:
            st.warning("Your dataset must contain a 'Condition Name' column.")
    else:
        st.warning("Your dataset must contain both 'Start Date' and 'End Date' columns.")
###FUTURE EXPENDITURE PAGE3
def page3(df):
    st.header("📈 Future Expenditures Prediction")

    # Simple Future Cost Prediction based on past data
    df['Predicted_Cost'] = df['Cost'].rolling(window=3, min_periods=1).mean()
    
    # Bar chart for predicted costs
    st.write("### Predicted Costs for the Upcoming Periods")
    fig, ax = plt.subplots(figsize=(8, 6))
    df['Predicted_Cost'].plot(kind='bar', ax=ax)
    ax.set_title('Predicted Future Expenditures')
    ax.set_xlabel('Time Period')
    ax.set_ylabel('Predicted Cost')
    st.pyplot(fig)
    
    # Line chart for comparison between actual and predicted costs
    st.write("### Actual vs Predicted Costs")
    st.line_chart(df[['Cost', 'Predicted_Cost']])

    


def suggest_to_reduce_expenditure(df):
    st.header("💡 Suggestions to Reduce Health Expenditure")
    
    # Calculate total cost for each condition
    if "Condition Name" in df.columns and "Cost" in df.columns:
        condition_grouped = df.groupby('Condition Name')['Cost'].sum()
        
        st.write("### Total Expenditure on Each Condition")
        st.dataframe(condition_grouped)
        
        # Suggestions based on expenditure and condition
        for condition, total_cost in condition_grouped.items():
            st.write(f"#### Suggestions for {condition}")
            
            # Suggest applying insurance if total expenditure is more than 50,000
            if total_cost > 50000:
                st.write(f"💰 You have spent more than 50,000 on {condition}. It's advisable to consider applying for insurance.")
                st.write("- **Apply for Health Insurance**: It’s recommended that you apply for health insurance with coverage that is at least three times your total expenditure (e.g., if you spent 50,000, aim for insurance coverage of at least 150,000).")
            
            # Condition-specific advice
            if condition.lower() in ["fever"]:
                st.write("- **Eat Healthy Food**: Eating a balanced diet rich in vitamins and minerals can help strengthen your immune system and prevent recurring fevers.")
                st.write("- **Hydrate Well**: Drink plenty of water and fluids to help your body recover from fever.")
                
            elif condition.lower() in ["heart", "kidney", "brain","leg injury","hand injury","injury"]:
                st.write("- **Apply for Health Insurance**: Given the nature of your condition, having comprehensive insurance is highly recommended.")
                st.write("- **Healthy Habits**: Adopt regular exercise, quit smoking (if applicable), and maintain a healthy weight to reduce the strain on your body organs.")
                st.write("- **Food & Diet**: Include foods rich in omega-3 fatty acids (e.g., fish, walnuts) to support heart health, foods high in antioxidants (e.g., berries, leafy greens) for brain health, and foods that promote kidney health (e.g., berries, red bell peppers).")
            elif condition.lower() in ["eye"]:
                st.write("- **Rest Your Eyes**: Follow the **20-20-20 rule**: Every 20 minutes, look at something 20 feet away for 20 seconds. Reduce screen time and take breaks from digital devices.")
                st.write("- **Stay Hydrated & Eat Well**: Drink plenty of **water** to keep your eyes moist. Eat foods rich in **Vitamin A (carrots, sweet potatoes), Omega-3 (fish, walnuts), and Lutein (leafy greens, eggs).**")
                st.write("- **Avoid Eye Strain**: Adjust **screen brightness** and use **blue-light filters** on devices. Ensure **proper lighting** when reading or working.")
                st.write("- **Monitor Symptoms**: Redness, pain, swelling, or vision changes? → **See a doctor immediately.** If symptoms persist for **more than 2-3 days**, consult an **eye specialist (ophthalmologist).**")
            elif condition.lower() in ["lung"]:
                st.write("- **Practice Deep Breathing**: Engage in deep breathing exercises to improve lung capacity and oxygen flow.")
                st.write("- **Stay Hydrated**: Drink plenty of water to keep your airways clear and prevent mucus buildup.")
                st.success("Maintaining a healthy lifestyle and avoiding lung irritants can help improve lung function and prevent complications.")
            elif condition.lower() in ["skin"]:
                st.write("- **Keep Your Skin Clean**: Wash the affected area with **mild soap and lukewarm water**. Avoid harsh chemicals or scrubbing.")
                st.write("- **Moisturize Regularly**: Use a **fragrance-free, hypoallergenic moisturizer** to prevent dryness and irritation.")
            elif condition.lower() in ["stomach"]:
                st.write("- **Stay Hydrated**: Drink **warm water or herbal teas (like ginger or peppermint tea)** to aid digestion.")
                st.write("- **Eat Light & Avoid Spicy Foods**: Stick to **bland foods** like bananas, rice, toast, and applesauce to avoid irritation.")
                st.write("- **Avoid Overeating**: Eat small, frequent meals instead of large portions to prevent bloating and discomfort.")
                st.write("- **Rest & Relax**: Avoid strenuous activities after eating; instead, try **light walking** to help digestion.")
            elif condition.lower() in ["ear"]:
                st.write("- **Keep Your Ears Clean (But Gently!)**: Clean the **outer ear** with a damp cloth but avoid inserting cotton swabs or sharp objects inside.")
                st.write("- **Avoid Loud Noises**: Prolonged exposure to loud music or noise can damage your hearing. Use **earplugs or noise-canceling headphones** in noisy environments.")
                st.write("- **Chew or Yawn for Pressure Relief**: If you experience **ear pressure (like on flights)**, chewing gum or yawning can help equalize pressure.")
            elif condition.lower() in ["teeth"]:
                st.write("- **Brush Twice a Day**: Use a **fluoride toothpaste** and brush for at least **2 minutes** in the morning and before bed.")
                st.write("- **Avoid Sugary & Acidic Foods**: Limit candies, soda, and citrus fruits as they can erode enamel and cause tooth decay.")
                st.write("- **Replace Your Toothbrush Every 3 Months**: Worn-out bristles are less effective at cleaning teeth.")
            elif condition.lower() in ["hair"]:
                st.write("- **Wash Your Hair Properly**: Use a **mild shampoo** suitable for your hair type and wash **2-3 times a week** to prevent dryness or oil buildup.")
                st.write("- **Eat a Nutrient-Rich Diet**: Consume foods rich in **biotin (eggs, nuts), protein (fish, lentils), and iron (spinach, beans)** for strong and healthy hair.")
                st.write("- **Avoid Harsh Chemicals**: Stay away from shampoos containing **sulfates and parabens** that can cause hair thinning.")
            elif condition.lower() in ["blood"]:
                st.write("- **Stay Hydrated**: Drink **plenty of water** to keep blood circulation smooth and prevent clotting issues.")
                st.write("- **Increase Vitamin C Intake**: Foods like **citrus fruits, bell peppers, and tomatoes** help the body absorb iron efficiently.")
                st.write("- **Exercise Regularly**: Engage in **walking, jogging, or yoga** to improve blood flow and oxygen supply to organs.")
                st.write("- **Avoid Smoking & Alcohol**: These can **thicken blood**, reduce oxygen levels, and increase clot risks.")




            else:
                st.write("- **General Suggestion**: For conditions that aren't directly related to vital organs, it’s still good to monitor your health closely.")
                st.write("- **Prevention**: Adopt healthy eating habits, stay active, and consider regular check-ups to avoid any future costs related to this condition.")
    
    else:
        st.warning("Your dataset must contain both 'Condition Name' and 'Cost' columns.")


