
import streamlit as st
import pandas as pd
import mysql.connector

# -----------------------------------
# 1. Streamlit page configuration
# -----------------------------------

st.set_page_config(
    page_title="Employee Salary Dashboard",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Employee Salary Dashboard")
st.write("Salary information fetched from MySQL Database")

# -----------------------------------
# 2. Connect to MySQL
# -----------------------------------

def get_connection():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rogers12345#",
        database="EmployeeDB",
        port=3306
    )

    return conn


# -----------------------------------
# 3. Fetch Salary table data
# -----------------------------------

def load_data():

    conn = get_connection()

    query = """
    SELECT
        Salary_ID,
        Emp_ID,
        Emp_Name,
        Department,
        Basic_Salary,
        Bonus,
        Total_Salary
    FROM Salary
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# -----------------------------------
# 4. Display dashboard
# -----------------------------------

try:

    df = load_data()

    if df.empty:

        st.warning("No salary records found.")

    else:

        # Calculate salary information

        total_employees = df["Emp_ID"].nunique()

        total_salary = df["Total_Salary"].sum()

        average_salary = df["Total_Salary"].mean()

        highest_salary = df["Total_Salary"].max()

        # -----------------------------------
        # 5. Display KPI cards
        # -----------------------------------

        st.subheader("Salary Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Employees",
            total_employees
        )

        col2.metric(
            "Total Salary",
            f"₹{total_salary:,.0f}"
        )

        col3.metric(
            "Average Salary",
            f"₹{average_salary:,.0f}"
        )

        col4.metric(
            "Highest Salary",
            f"₹{highest_salary:,.0f}"
        )

        # -----------------------------------
        # 6. Display Salary Table
        # -----------------------------------

        st.subheader("Employee Salary Details")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------------
        # 7. Department-wise salary
        # -----------------------------------

        st.subheader("Department-wise Salary")

        dept_salary = df.groupby(
            "Department"
        )["Total_Salary"].sum()

        st.bar_chart(dept_salary)

        # -----------------------------------
        # 8. Employee-wise salary
        # -----------------------------------

        st.subheader("Employee Salary Comparison")

        employee_salary = df.set_index(
            "Emp_Name"
        )["Total_Salary"]

        st.bar_chart(employee_salary)

        # -----------------------------------
        # 9. Department filter
        # -----------------------------------

        st.subheader("Search Employees by Department")

        departments = ["All"] + sorted(
            df["Department"].dropna().unique().tolist()
        )

        selected_department = st.selectbox(
            "Select Department",
            departments
        )

        if selected_department == "All":

            filtered_df = df

        else:

            filtered_df = df[
                df["Department"] == selected_department
            ]

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------------
        # 10. Refresh button
        # -----------------------------------

        if st.button("Refresh Data"):

            st.rerun()


except Exception as e:

    st.error(f"Error connecting to MySQL: {e}")
