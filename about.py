import streamlit as st

# Function to display the About page
def show():
    st.title("📊 About Track Care Cost")
    
    st.write("""
        Track Care Cost is an innovative platform designed to help individuals **monitor, predict, and manage** their healthcare expenses effectively. 
        By using this application, users can track their spending, predict future costs, and receive suggestions for cost optimization.
    """)

    # Key Features Section
    st.subheader("✨ Key Features")
    st.write("""
    - 📝 **Track Healthcare Expenses**: Monitor your medical costs over time, analyze trends, and understand where your money goes.
    - 📊 **Visualize Spending Patterns**: Use interactive charts and graphs to get a clear picture of your expenditure.
    - 🔮 **Predict Future Costs**: Based on past spending data, the app forecasts your future healthcare expenses.
    - 🎯 **Personalized Suggestions**: Receive actionable recommendations to reduce healthcare costs.
    - ☁️ **CSV Upload Support**: Easily upload and analyze your expenditure data in CSV format.
    """)

    # Why is Track Care Cost Different?
    st.subheader("🚀 Why is Track Care Cost Different?")
    st.write("""
        Unlike other healthcare tracking apps, Track Care Cost stands out due to its:
    """)
    st.write("""
    - 🔍 **Detailed Insights**: Get deep analysis of your spending habits.
    - 📈 **Advanced Predictive Analytics**: Plan ahead with accurate expenditure predictions.
    - 🖥️ **User-Friendly Experience**: A simple yet powerful interface for effortless navigation.
    - 🔑 **Secure & Reliable**: Your data is safe, ensuring privacy and security.
    """)

    # How Can Users Benefit?
    st.subheader("💡 How Can You Benefit?")
    st.write("""
        By using Track Care Cost, you can:
    """)
    st.write("""
    - 📊 **Gain a clear, visual overview** of your healthcare expenditures.
    - 💬 **Receive data-driven recommendations** to optimize your costs.
    - 🚀 **Stay ahead of unexpected medical expenses** with accurate predictions.
    - 🌱 **Improve your health and financial well-being** with actionable insights.
    """)

    st.markdown("---")

    st.write("""
    💌 **Want to learn more?** Visit our website or contact us for personalized assistance.  
    🏥 **Track Care Cost | Empowering You to Take Control of Your Healthcare Finances**
    """)

# Main function to navigate between Home and About pages
def main():
    st.sidebar.title("🔍 Navigation")
    menu = ["🏠 Home", "ℹ️ About"]
    
    choice = st.sidebar.radio("Go to", menu)
    
    if choice == "🏠 Home":
        st.title("Welcome to Track Care Cost! 🏥")
        st.write("This is the home page where you can explore our app features and benefits.")
        # You can add more content for the home page as needed
    elif choice == "ℹ️ About":
        show()

# Run the app
if __name__ == "__main__":
    main()
