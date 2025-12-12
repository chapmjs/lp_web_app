"""
LINEAR PROGRAMMING WEB APP FOR STUDENTS
Interactive Product-Mix Problem Solver

Run with: streamlit run lp_web_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, lpSum, value
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="LP Product Mix Solver",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background-color: #f0f2f6;
        border-left: 5px solid #1f77b4;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">📊 Linear Programming: Product Mix Solver</div>', unsafe_allow_html=True)

# Initialize session state
if 'problem_configured' not in st.session_state:
    st.session_state.problem_configured = False
if 'solution' not in st.session_state:
    st.session_state.solution = None

# Sidebar for problem configuration
with st.sidebar:
    st.header("🎯 Problem Setup")
    
    st.markdown("### Basic Configuration")
    
    # Problem name
    problem_name = st.text_input("Problem Name", value="My Product Mix Problem")
    
    # Number of products and resources
    num_products = st.number_input("Number of Products", min_value=1, max_value=10, value=2, step=1)
    num_resources = st.number_input("Number of Resources/Constraints", min_value=1, max_value=10, value=3, step=1)
    
    # Objective type
    objective_type = st.radio("Objective", ["Maximize (Profit)", "Minimize (Cost)"])
    
    # Variable type
    variable_type = st.radio("Variable Type", ["Continuous (Decimals OK)", "Integer (Whole Numbers Only)"])
    
    st.markdown("---")
    
    # Example problems
    st.markdown("### 📚 Load Example Problem")
    if st.button("🏭 Wyndor Glass Example"):
        st.session_state.load_example = "wyndor"
        st.session_state.problem_configured = False
        st.rerun()
    
    if st.button("🍪 Bakery Example"):
        st.session_state.load_example = "bakery"
        st.session_state.problem_configured = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ Instructions")
    st.info("""
    1. Set number of products and resources
    2. Choose maximize or minimize
    3. Enter product and resource details in the main area
    4. Click 'Solve Problem' to get the optimal solution
    """)

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📝 Input Data", "✅ Solve", "📊 Results", "📖 Help"])

with tab1:
    st.markdown('<div class="section-header">Step 1: Define Products</div>', unsafe_allow_html=True)
    
    # Load example if requested
    if 'load_example' in st.session_state:
        if st.session_state.load_example == "wyndor":
            num_products = 2
            num_resources = 3
            objective_type = "Maximize (Profit)"
            variable_type = "Continuous (Decimals OK)"
        elif st.session_state.load_example == "bakery":
            num_products = 2
            num_resources = 3
            objective_type = "Maximize (Profit)"
            variable_type = "Continuous (Decimals OK)"
        del st.session_state.load_example
    
    # Product names and profits
    st.markdown("#### Product Information")
    col1, col2 = st.columns([2, 1])
    
    products = {}
    for i in range(num_products):
        with col1:
            if 'load_example' in st.session_state and st.session_state.load_example == "wyndor":
                default_name = ["Doors", "Windows"][i] if i < 2 else f"Product_{i+1}"
            elif 'load_example' in st.session_state and st.session_state.load_example == "bakery":
                default_name = ["Cookies", "Cakes"][i] if i < 2 else f"Product_{i+1}"
            else:
                default_name = f"Product_{i+1}"
            
            prod_name = st.text_input(f"Product {i+1} Name", value=default_name, key=f"prod_name_{i}")
        
        with col2:
            if objective_type == "Maximize (Profit)":
                if 'load_example' in st.session_state and st.session_state.load_example == "wyndor":
                    default_profit = [300, 500][i] if i < 2 else 100
                elif 'load_example' in st.session_state and st.session_state.load_example == "bakery":
                    default_profit = [2, 8][i] if i < 2 else 10
                else:
                    default_profit = 100
                
                profit = st.number_input(f"Profit per Unit ($)", value=default_profit, key=f"profit_{i}", min_value=0.0, step=10.0)
            else:
                cost = st.number_input(f"Cost per Unit ($)", value=50.0, key=f"cost_{i}", min_value=0.0, step=10.0)
                profit = cost
        
        products[prod_name] = profit
    
    st.markdown('<div class="section-header">Step 2: Define Resources and Constraints</div>', unsafe_allow_html=True)
    
    # Resource names and capacities
    st.markdown("#### Resource Availability")
    resources = {}
    resource_names = []
    
    for i in range(num_resources):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if 'load_example' in st.session_state and st.session_state.load_example == "wyndor":
                default_res_name = ["Plant_1", "Plant_2", "Plant_3"][i] if i < 3 else f"Resource_{i+1}"
            elif 'load_example' in st.session_state and st.session_state.load_example == "bakery":
                default_res_name = ["Oven_Time", "Mixing_Time", "Ingredients"][i] if i < 3 else f"Resource_{i+1}"
            else:
                default_res_name = f"Resource_{i+1}"
            
            res_name = st.text_input(f"Resource {i+1} Name", value=default_res_name, key=f"res_name_{i}")
        
        with col2:
            if 'load_example' in st.session_state and st.session_state.load_example == "wyndor":
                default_avail = [4, 12, 18][i] if i < 3 else 100
            elif 'load_example' in st.session_state and st.session_state.load_example == "bakery":
                default_avail = [40, 30, 50][i] if i < 3 else 100
            else:
                default_avail = 100
            
            available = st.number_input(f"Available Amount", value=float(default_avail), key=f"avail_{i}", min_value=0.0, step=10.0)
        
        resources[res_name] = {"available": available, "usage": {}}
        resource_names.append(res_name)
    
    st.markdown('<div class="section-header">Step 3: Resource Usage Matrix</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <strong>💡 Tip:</strong> Enter how much of each resource is required to produce one unit of each product.
    For example, if Product A uses 2 hours of Machine 1, enter 2 in that cell.
    </div>
    """, unsafe_allow_html=True)
    
    # Create usage matrix
    usage_data = []
    product_names = list(products.keys())
    
    # Load example data if needed
    if 'load_example' in st.session_state and st.session_state.load_example == "wyndor":
        example_usage = [
            [1, 0],  # Plant 1
            [0, 2],  # Plant 2
            [3, 2]   # Plant 3
        ]
    elif 'load_example' in st.session_state and st.session_state.load_example == "bakery":
        example_usage = [
            [0.5, 2],    # Oven
            [0.3, 1],    # Mixing
            [0.2, 1.5]   # Ingredients
        ]
    else:
        example_usage = [[0.0] * num_products for _ in range(num_resources)]
    
    for i, res_name in enumerate(resource_names):
        row = []
        cols = st.columns(num_products)
        for j, prod_name in enumerate(product_names):
            with cols[j]:
                default_val = example_usage[i][j] if i < len(example_usage) and j < len(example_usage[i]) else 0.0
                usage = st.number_input(
                    f"{res_name} per {prod_name}",
                    value=default_val,
                    key=f"usage_{i}_{j}",
                    min_value=0.0,
                    step=0.5
                )
                resources[res_name]["usage"][prod_name] = usage
                row.append(usage)
        usage_data.append(row)
    
    # Display as DataFrame for clarity
    st.markdown("#### 📋 Summary Table")
    df = pd.DataFrame(usage_data, columns=product_names, index=resource_names)
    st.dataframe(df, use_container_width=True)
    
    # Store in session state
    st.session_state.config = {
        "problem_name": problem_name,
        "products": products,
        "resources": resources,
        "objective": "maximize" if "Maximize" in objective_type else "minimize",
        "variable_type": "Continuous" if "Continuous" in variable_type else "Integer"
    }
    st.session_state.problem_configured = True

with tab2:
    st.markdown('<div class="section-header">Solve the Problem</div>', unsafe_allow_html=True)
    
    if st.session_state.problem_configured:
        # Display problem summary
        st.markdown("### 📋 Problem Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Products", num_products)
        with col2:
            st.metric("Resources", num_resources)
        with col3:
            obj_label = "Maximize Profit" if st.session_state.config["objective"] == "maximize" else "Minimize Cost"
            st.metric("Objective", obj_label)
        
        st.markdown("---")
        
        # Solve button
        if st.button("🚀 Solve Problem", type="primary", use_container_width=True):
            with st.spinner("Solving optimization problem..."):
                config = st.session_state.config
                
                # Create problem
                if config["objective"] == "maximize":
                    problem = LpProblem(config["problem_name"], LpMaximize)
                else:
                    problem = LpProblem(config["problem_name"], LpMinimize)
                
                # Create variables
                variables = {}
                for product_name in config["products"].keys():
                    variables[product_name] = LpVariable(
                        product_name.replace(" ", "_"),
                        lowBound=0,
                        cat=config["variable_type"]
                    )
                
                # Objective function
                objective = lpSum([
                    config["products"][product] * variables[product]
                    for product in config["products"].keys()
                ])
                problem += objective, "Objective"
                
                # Constraints
                for resource_name, resource_data in config["resources"].items():
                    constraint = lpSum([
                        resource_data["usage"].get(product, 0) * variables[product]
                        for product in config["products"].keys()
                    ])
                    problem += constraint <= resource_data["available"], resource_name
                
                # Solve
                status = problem.solve()
                
                # Store results
                st.session_state.solution = {
                    "status": status,
                    "status_text": ['Not Solved', 'Optimal', 'Infeasible', 'Unbounded', 'Undefined'][status],
                    "variables": {},
                    "objective_value": None,
                    "resource_usage": {},
                    "shadow_prices": {},
                    "problem": problem
                }
                
                if status == 1:  # Optimal
                    for product_name, var in variables.items():
                        st.session_state.solution["variables"][product_name] = value(var)
                    
                    st.session_state.solution["objective_value"] = value(problem.objective)
                    
                    for resource_name, resource_data in config["resources"].items():
                        used = sum(
                            resource_data["usage"].get(product, 0) * st.session_state.solution["variables"][product]
                            for product in config["products"].keys()
                        )
                        available = resource_data["available"]
                        slack = available - used
                        
                        st.session_state.solution["resource_usage"][resource_name] = {
                            "used": used,
                            "available": available,
                            "slack": slack,
                            "binding": abs(slack) < 0.001
                        }
                    
                    for name, constraint in problem.constraints.items():
                        st.session_state.solution["shadow_prices"][name] = constraint.pi
                
                st.rerun()
        
    else:
        st.warning("⚠️ Please configure the problem in the 'Input Data' tab first.")

with tab3:
    st.markdown('<div class="section-header">Solution Results</div>', unsafe_allow_html=True)
    
    if st.session_state.solution:
        sol = st.session_state.solution
        config = st.session_state.config
        
        # Status
        if sol["status"] == 1:
            st.markdown(f'<div class="success-box"><strong>✅ Status:</strong> {sol["status_text"]} Solution Found!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box"><strong>⚠️ Status:</strong> {sol["status_text"]}</div>', unsafe_allow_html=True)
            if sol["status"] == 2:
                st.error("The problem is **INFEASIBLE**. This means the constraints are too restrictive and no solution exists that satisfies all constraints.")
            elif sol["status"] == 3:
                st.error("The problem is **UNBOUNDED**. This means the objective function can grow infinitely. Check that all necessary constraints are included.")
        
        if sol["status"] == 1:
            # Optimal production plan
            st.markdown("### 🎯 Optimal Production Plan")
            
            prod_df = pd.DataFrame([
                {"Product": prod, "Quantity": qty, "Unit Value": f"${config['products'][prod]:,.2f}"}
                for prod, qty in sol["variables"].items()
            ])
            st.dataframe(prod_df, use_container_width=True, hide_index=True)
            
            # Visualize production plan
            fig_prod = px.bar(
                prod_df,
                x="Product",
                y="Quantity",
                title="Production Quantities by Product",
                labels={"Quantity": "Units to Produce"},
                color="Quantity",
                color_continuous_scale="Blues"
            )
            st.plotly_chart(fig_prod, use_container_width=True)
            
            # Objective value
            st.markdown("### 💰 Optimal Objective Value")
            obj_type = "Profit" if config["objective"] == "maximize" else "Cost"
            st.metric(f"Total {obj_type}", f"${sol['objective_value']:,.2f}")
            
            # Resource utilization
            st.markdown("### 📊 Resource Utilization")
            
            resource_df = pd.DataFrame([
                {
                    "Resource": res,
                    "Used": f"{data['used']:.2f}",
                    "Available": f"{data['available']:.2f}",
                    "Slack": f"{data['slack']:.2f}",
                    "Utilization %": f"{(data['used']/data['available']*100):.1f}%",
                    "Status": "🔴 Binding" if data['binding'] else "🟢 Slack"
                }
                for res, data in sol["resource_usage"].items()
            ])
            st.dataframe(resource_df, use_container_width=True, hide_index=True)
            
            # Visualize resource utilization
            util_data = []
            for res, data in sol["resource_usage"].items():
                util_data.append({"Resource": res, "Type": "Used", "Amount": data['used']})
                util_data.append({"Resource": res, "Type": "Available", "Amount": data['slack']})
            
            util_df = pd.DataFrame(util_data)
            fig_util = px.bar(
                util_df,
                x="Resource",
                y="Amount",
                color="Type",
                title="Resource Utilization: Used vs. Slack",
                barmode="stack",
                color_discrete_map={"Used": "#1f77b4", "Available": "#d3d3d3"}
            )
            st.plotly_chart(fig_util, use_container_width=True)
            
            # Shadow prices
            st.markdown("### 💡 Shadow Prices (Marginal Values)")
            
            st.markdown("""
            <div class="info-box">
            <strong>What are Shadow Prices?</strong><br>
            Shadow prices tell you how much the objective function would improve if you had one more unit of a resource.
            Only binding constraints (fully utilized resources) have meaningful shadow prices.
            </div>
            """, unsafe_allow_html=True)
            
            shadow_df = pd.DataFrame([
                {
                    "Resource": res.replace("_", " "),
                    "Shadow Price": f"${price:.2f}",
                    "Interpretation": f"Gaining 1 more unit would {'increase profit' if config['objective'] == 'maximize' else 'decrease cost'} by ${abs(price):.2f}" if abs(price) > 0.01 else "Not binding (has slack)"
                }
                for res, price in sol["shadow_prices"].items()
            ])
            st.dataframe(shadow_df, use_container_width=True, hide_index=True)
            
            # Download results
            st.markdown("### 📥 Export Results")
            
            # Create comprehensive report
            report = f"""
LINEAR PROGRAMMING SOLUTION REPORT
{'='*60}

Problem: {config['problem_name']}
Objective: {config['objective'].capitalize()} {'Profit' if config['objective'] == 'maximize' else 'Cost'}
Status: {sol['status_text']}

OPTIMAL PRODUCTION PLAN:
{'-'*60}
"""
            for prod, qty in sol["variables"].items():
                report += f"{prod}: {qty:.2f} units\n"
            
            report += f"\nOPTIMAL {'PROFIT' if config['objective'] == 'maximize' else 'COST'}: ${sol['objective_value']:,.2f}\n"
            
            report += f"\nRESOURCE UTILIZATION:\n{'-'*60}\n"
            for res, data in sol["resource_usage"].items():
                status = "[BINDING]" if data['binding'] else ""
                report += f"{res}: {data['used']:.2f} / {data['available']:.2f} (Slack: {data['slack']:.2f}) {status}\n"
            
            report += f"\nSHADOW PRICES:\n{'-'*60}\n"
            for res, price in sol["shadow_prices"].items():
                if abs(price) > 0.01:
                    report += f"{res}: ${price:.2f} per unit\n"
            
            st.download_button(
                label="📄 Download Report (TXT)",
                data=report,
                file_name=f"{config['problem_name'].replace(' ', '_')}_solution.txt",
                mime="text/plain"
            )
    
    else:
        st.info("👈 Configure and solve the problem to see results here.")

with tab4:
    st.markdown('<div class="section-header">How to Use This App</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📖 Step-by-Step Guide
    
    #### 1️⃣ Configure Your Problem (Sidebar)
    - Enter the **number of products** you want to produce
    - Enter the **number of resources/constraints** you have
    - Choose whether to **maximize** (profit) or **minimize** (cost)
    - Select **continuous** (decimals) or **integer** (whole numbers) variables
    
    #### 2️⃣ Input Data (Input Data Tab)
    - **Products**: Name each product and enter its profit (or cost) per unit
    - **Resources**: Name each resource and enter how much is available
    - **Usage Matrix**: Enter how much of each resource is needed per unit of each product
    
    #### 3️⃣ Solve (Solve Tab)
    - Review your problem summary
    - Click the "Solve Problem" button
    - The app will find the optimal solution
    
    #### 4️⃣ Analyze Results (Results Tab)
    - View the optimal production quantities
    - See which resources are fully utilized (binding constraints)
    - Understand shadow prices to identify valuable resources
    - Download a complete report
    
    ---
    
    ### 📊 Understanding the Results
    
    #### Optimal Production Plan
    This tells you how many units of each product to produce to achieve the best objective value.
    
    #### Resource Utilization
    - **Used**: Amount of resource consumed by the optimal plan
    - **Available**: Total amount of resource you have
    - **Slack**: Unused resource (Available - Used)
    - **Binding**: A resource with zero slack (fully utilized)
    
    #### Shadow Prices
    The marginal value of having one more unit of a resource:
    - **High shadow price** = Very valuable resource; getting more would significantly improve your objective
    - **Zero shadow price** = Resource has slack; getting more won't help right now
    - Only meaningful for binding constraints
    
    ---
    
    ### 💡 Tips for Success
    
    1. **Start with an example**: Click "Wyndor Glass Example" to see a working problem
    2. **Check your data**: Make sure all numbers are non-negative
    3. **Logical consistency**: Resource usage should make sense (e.g., if a product doesn't use a resource, enter 0)
    4. **Units matter**: Make sure all your units are consistent (hours, dollars, etc.)
    
    ---
    
    ### ⚠️ Common Issues
    
    #### Infeasible Problem
    Your constraints are too restrictive. Possible fixes:
    - Increase resource availability
    - Reduce resource usage requirements
    - Check for contradictory constraints
    
    #### Unbounded Problem
    Your solution can grow infinitely. Possible fixes:
    - Add missing constraints
    - Check that all necessary limitations are included
    - Verify objective function is correct
    
    ---
    
    ### 🎓 For Students
    
    This tool helps you:
    - ✅ Verify your hand calculations
    - ✅ Explore "what-if" scenarios
    - ✅ Understand sensitivity to changes
    - ✅ Learn optimization concepts interactively
    
    **Remember**: The computer finds the optimal solution, but YOU need to:
    - Formulate the problem correctly
    - Interpret the results
    - Make informed business decisions
    
    ---
    
    ### 📚 Example Problems
    
    Use the sidebar to load pre-configured examples:
    - **Wyndor Glass**: Classic 2-product, 3-resource problem
    - **Bakery**: Production planning with multiple constraints
    
    ---
    
    ### 🆘 Need Help?
    
    If you encounter issues:
    1. Double-check all input values
    2. Try loading an example problem first
    3. Make sure resource usage values are realistic
    4. Contact your instructor if problems persist
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
    <p>📊 Linear Programming Web App | Built for Operations Management Students</p>
    <p><small>Powered by Streamlit and PuLP</small></p>
    </div>
""", unsafe_allow_html=True)
