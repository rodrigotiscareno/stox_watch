import streamlit as st
from modelling.portfolio_optimization import main as portfolio_optimization

Z = 0.95
HIGH_RISK_STD = 0.45
MEDIUM_RISK_STD = 0.20
LOW_RISK_STD = 0.15


def submit():
    st.session_state.display_recommendations = True


def portfolio_page():
    st.title("Stock Portfolio Recommendations")
    budget = st.number_input(
        "Enter your budget:", min_value=50000, step=1000, format="%d"
    )
    diversification = st.radio(
        "Level of Forecast:",
        ("Short-term", "Medium-term", "Long-term"),
    )

    st.button("Submit", on_click=submit)

    if st.session_state.display_recommendations:

        st.header("Recommendations:")

        clause = {"Short-term": "short", "Medium-term": "medium", "Long-term": "long"}
        columns = [
            "ticker",
            "shares",
            "price",
            "investment",
            "total_expected_return",
            "industries",
        ]

        high_risk_df = portfolio_optimization(
            budget=int(budget),
            p=1,
            lambda_risk_coefficient=0.1,
            unique_companies=1,
            unique_industries=1,
            N=15,
            save_df=False,
            term=clause[diversification],
        )[columns]

        high_risk_expected_return = (
            high_risk_df["total_expected_return"].sum()
            / high_risk_df["investment"].sum()
            / 100
        )

        high_risk_worst_case = budget + (
            budget * (high_risk_expected_return - Z * HIGH_RISK_STD)
        )

        medium_risk_df = portfolio_optimization(
            budget=int(budget),
            p=0.7,
            lambda_risk_coefficient=0.5,
            unique_companies=4,
            unique_industries=3,
            N=15,
            save_df=False,
            term=clause[diversification],
        )[columns]

        medium_risk_expected_return = (
            medium_risk_df["total_expected_return"].sum()
            / medium_risk_df["investment"].sum()
            / 100
        )

        medium_risk_worst_case = budget + (
            budget * (medium_risk_expected_return - Z * MEDIUM_RISK_STD)
        )

        low_risk_df = portfolio_optimization(
            budget=int(budget),
            p=0.5,
            lambda_risk_coefficient=1,
            unique_companies=8,
            unique_industries=4,
            N=20,
            save_df=False,
            term=clause[diversification],
        )[columns]

        low_risk_expected_return = (
            low_risk_df["total_expected_return"].sum()
            / low_risk_df["investment"].sum()
            / 100
        )

        low_risk_worst_case = budget + (
            budget * (low_risk_expected_return - Z * LOW_RISK_STD)
        )

        st.subheader("High Risk Portfolio")
        st.dataframe(high_risk_df)
        high_risk_investment = high_risk_df["investment"].sum()
        high_risk_return = high_risk_df["total_expected_return"].sum()
        st.write(f"Total Expected Investment: ${high_risk_investment:,.2f}")
        st.write(f"Total Expected Return: ${high_risk_return:,.2f}")
        st.markdown(
            f"**Worst Case Return**: <span style='color:red'>${high_risk_worst_case:,.2f}</span>",
            unsafe_allow_html=True,
        )

        st.subheader("Medium Risk Portfolio")
        st.dataframe(medium_risk_df)
        medium_risk_investment = medium_risk_df["investment"].sum()
        medium_risk_return = medium_risk_df["total_expected_return"].sum()
        st.write(f"Total Expected Investment: ${medium_risk_investment:,.2f}")
        st.write(f"Total Expected Return: ${medium_risk_return:,.2f}")
        st.markdown(
            f"**Worst Case Return**: <span style='color:red'>${medium_risk_worst_case:,.2f}</span>",
            unsafe_allow_html=True,
        )

        st.subheader("Low Risk Portfolio")
        st.dataframe(low_risk_df)
        low_risk_investment = low_risk_df["investment"].sum()
        low_risk_return = low_risk_df["total_expected_return"].sum()
        st.write(f"Total Expected Investment: ${low_risk_investment:,.2f}")
        st.write(f"Total Expected Return: ${low_risk_return:,.2f}")
        st.markdown(
            f"**Worst Case Return**: <span style='color:red'>${low_risk_worst_case:,.2f}</span>",
            unsafe_allow_html=True,
        )
