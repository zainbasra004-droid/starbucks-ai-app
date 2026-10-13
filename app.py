

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Starbucks AI",
    page_icon="☕",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f5f3eb;
}
h1, h2, h3 {
    color: #006241;
}
[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("☕ Starbucks AI Intelligence")
st.caption("Food & Drink Category Predictor")

st.sidebar.title("☕ Starbucks")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "EDA Analysis", "Category Predictor"]
)

# Sample dataset for demonstration
data = {
    "Item": [
        "Caffe Latte", "Cappuccino", "Cold Brew",
        "Caramel Frappuccino", "Blueberry Muffin",
        "Croissant", "Chocolate Cookie", "Egg Sandwich"
    ],
    "Type": [
        "Drink", "Drink", "Drink", "Drink",
        "Food", "Food", "Food", "Food"
    ],
    "Category": [
        "Coffee", "Coffee", "Cold Coffee",
        "Frappuccino", "Bakery", "Bakery",
        "Dessert", "Breakfast"
    ],
    "Calories": [190, 140, 5, 380, 360, 260, 360, 450],
    "Sugar": [18, 12, 0, 54, 30, 5, 29, 5]
}

df = pd.DataFrame(data)

if page == "Dashboard":
    st.header("Executive Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Items", len(df))
    c2.metric("Food Items", len(df[df["Type"] == "Food"]))
    c3.metric("Drink Items", len(df[df["Type"] == "Drink"]))

    st.subheader("Food vs Drink Distribution")

    counts = df["Type"].value_counts().reset_index()
    counts.columns = ["Type", "Count"]

    fig = px.pie(
        counts,
        names="Type",
        values="Count",
        hole=0.55,
        color_discrete_sequence=["#006241", "#C8A878"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Menu Dataset")
    st.dataframe(df, use_container_width=True)

elif page == "EDA Analysis":
    st.header("Exploratory Data Analysis")

    st.subheader("Calories by Menu Item")

    fig = px.bar(
        df,
        x="Item",
        y="Calories",
        color="Type",
        color_discrete_sequence=["#006241", "#C8A878"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sugar vs Calories")

    fig = px.scatter(
        df,
        x="Sugar",
        y="Calories",
        color="Type",
        hover_name="Item"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Statistical Summary")
    st.write(df[["Calories", "Sugar"]].describe())

elif page == "Category Predictor":
    st.header("AI Food & Drink Predictor")

    item = st.text_input("Enter menu item name")

    description = st.text_input(
        "Enter ingredients or description"
    )

    if st.button("Predict Category"):
        if not item.strip():
            st.warning("Please enter an item name.")
        else:
            text = (item + " " + description).lower()

            drink_words = [
                "coffee", "latte", "tea", "drink",
                "frappuccino", "espresso", "brew",
                "cappuccino", "juice", "mocha"
            ]

            food_words = [
                "muffin", "cake", "cookie", "bread",
                "sandwich", "croissant", "bagel",
                "pastry", "salad", "wrap"
            ]

            drink_score = sum(
                word in text for word in drink_words
            )

            food_score = sum(
                word in text for word in food_words
            )

            if drink_score > food_score:
                st.success("Predicted Category: DRINK")
            elif food_score > drink_score:
                st.success("Predicted Category: FOOD")
            else:
                st.info(
                    "Prediction uncertain. Add more details."
                )

            st.caption(
                "This starter uses keyword rules, not a trained "
                "machine-learning model."
            )

st.divider()
st.caption(
    "Starbucks AI Analytics | Educational Project"
)
