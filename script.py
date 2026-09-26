'''
from dotenv import load_dotenv
import os
import csv
from typing import TypedDict, List

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
import streamlit as st


load_dotenv()
api_key = os.getenv("my_api_key")

news_data = []
with open("news_feed_dataset.csv",newline='', mode ='r') as news:
    news_reader = list(csv.DictReader(news))
    news_data = news_reader

supply_data = ""
with open("enterprise_supply_chain.csv", mode ='r') as supply:
    
    supply_data= supply.read()

class SupplyChainState(TypedDict):
    disruption_report: str
    impacted_components: List[str]
    remediation_plans: List[dict]

#define agents
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=api_key)

def monitor_agent(state: SupplyChainState):
    current_disruption = state["disruption_report"]

    system_instruction = "You are a Supply Chain monitor that will track locations, ports, and news and keep track of anything that can disrupt service in the file I give you."
    combined_prompt = f"{system_instruction}\n\nAnalyze this report: {current_disruption}"

    llm_response = llm.invoke(combined_prompt)

    return {"disruption_report": llm_response.content}

def impact_anaylyst_agent(state: SupplyChainState):
    current_disruption  = state["disruption_report"]

    system_instruction = """You are a Supply Chain remediation planner. Read the list of affected components and backup options. 
You must output your response in EXACTLY the following structure so a computer program can split it cleanly. Do not add any extra intro text, brackets, or signatures.

COST_START
[Insert only the primary cost delta or premium calculated from the data, e.g., +$15,000 flat premium]
COST_END

EMAIL_START
[Insert the fully drafted professional procurement email template here]
EMAIL_END
"""

    combined_prompt = f"{system_instruction}\n\nAnalyze this report: {current_disruption}, {supply_data}"

    llm_response = llm.invoke(combined_prompt)
    return {"impacted_components": llm_response.content}

def planner_analyst_agent(state: SupplyChainState):
    current_disruption = state["impacted_components"]

    if "NONE" in current_disruption:
        return {"remeditation_plans": "No action required"}
    
    system_instruction = "Read this list of affected components and backup options. Draft a professional procurement email to these backup suppliers requesting urgent capacity, and summarize the overall cost adjustment listed in the data. Also make list of affected parts."
    combined_prompt = f"{system_instruction}\n\nAnalyze this report {current_disruption}"

    llm_response = llm.invoke(combined_prompt)
    return {"remediation_plans": llm_response.content}

#Connect agets via graph

workflow = StateGraph(SupplyChainState) # Create graph of agent state

workflow.add_node("monitor", monitor_agent)
workflow.add_node("analyst",impact_anaylyst_agent)
workflow.add_node("planner", planner_analyst_agent)

workflow.set_entry_point("monitor")
workflow.add_edge("monitor", "analyst")
workflow.add_edge("analyst", "planner")
workflow.add_edge("planner", END)
app = workflow.compile()



st.set_page_config(page_title ="Supply Chain Disruption Planner", layout="wide")
st.title("Agentic Supply Chain Risk Engine")
st.caption("Powered by Gemini Pro and LangGraph Workflow")

if st.button("Begin Global Logistics Audit"):
    with st.spinner("Processing automated audit"):
        for incident in news_data:
            with st.container(border=True):
                raw_bulletin = incident["bulletin"]

                inputs = {"disruption_report": raw_bulletin, "impacted_components": [], "remediation_plans": []}
                outputs = app.invoke(inputs)

                analyst_finding = outputs["impacted_components"]
                if "None" not in analyst_finding.upper():
                    with st.container(border=True):
                    
                    # Split header section into location title and an alert flag
                        title_col, badge_col = st.columns([3, 1])
                        title_col.write(f"### 📍 Disruption Flagged: {incident['location']}")
                        badge_col.error("🚨 CRISIS IMPLICATIONS")

                        # Draw a clean dropdown list showing the affected parts
                        with st.expander("🔍 View Affected Component Supply Chain Lines"):
                            st.markdown(analyst_finding)

                        # --- MODERN GRAPH OF COST ADJUSTMENT ---
                        st.write("**Financial Mitigation Cost Projections:**")
                        
                        # Mock interactive data map for chart display based on your database cost deltas
                        chart_data = {
                            "Primary Cost": [10.0, 15.0, 8.0],
                            "Rerouted Backup Premium": [14.5, 22.0, 11.2]
                        }

                        st.bar_chart(chart_data)

                        # Draw the secondary nested dropdown dedicated purely to the vendor email template
                        with st.expander("📬 Open Auto-Generated Supplier Procurement Email"):
                            st.markdown(outputs["remediation_plans"])


'''
from dotenv import load_dotenv
import os
import csv
from typing import TypedDict, List

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
import streamlit as st

# Load hidden local keys securely
load_dotenv()
api_key = os.getenv("my_api_key")

# 1. LOAD DATASETS AS CLEAN DICTIONARY LISTS
news_data = []
with open("news_feed_dataset.csv", newline='', mode='r') as news:
    news_data = list(csv.DictReader(news))

supply_data = []
with open("enterprise_supply_chain.csv", mode='r') as supply:
    supply_data = list(csv.DictReader(supply))

# 2. DEFINE SYSTEM STATE VARIABLES
class SupplyChainState(TypedDict):
    disruption_report: str
    impacted_components: str
    remediation_plans: str

# 3. INITIALIZE STABLE, FREE PRODUCTION MODEL DIRECTLY FROM GOOGLE
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", google_api_key=api_key)

def monitor_agent(state: SupplyChainState):
    llm_response = llm.invoke(f"Summarize this news headline: {state['disruption_report']}")
    return {"disruption_report": llm_response.text}

def impact_anaylyst_agent(state: SupplyChainState):
    system_instruction = "Verify if the city in this news bulletin matches the origin city of this product. If yes, output details. If no, output 'NONE'."
    llm_response = llm.invoke(f"{system_instruction}\n\nNews: {state['disruption_report']}\n\nProduct: {state['impacted_components']}")
    return {"impacted_components": llm_response.text}

def planner_analyst_agent(state: SupplyChainState):
    system_instruction = "Draft a single, highly professional emergency procurement email template to this specific backup supplier requesting urgent capacity for the attached components."
    llm_response = llm.invoke(f"{system_instruction}\n\nGrouped Products Data:\n{state['impacted_components']}")
    return {"remediation_plans": llm_response.text}

# 4. WIRE THE LANGGRAPH FLOW PATHS
workflow = StateGraph(SupplyChainState)
workflow.add_node("monitor", monitor_agent)
workflow.add_node("analyst", impact_anaylyst_agent)
workflow.add_node("planner", planner_analyst_agent)

workflow.set_entry_point("monitor")
workflow.add_edge("monitor", "analyst")
workflow.add_edge("analyst", "planner")
workflow.add_edge("planner", END)
app = workflow.compile()

# 5. UI VIEW CONFIGURATION
st.set_page_config(page_title="Supply Chain Disruption Planner", layout="wide")
st.title("🛡️ Agentic Supply Chain Risk Engine")
st.caption("⚡ Powered by Gemini and LangGraph Workflow Architecture")

if st.button("Begin Global Logistics Audit"):
    with st.spinner("Processing automated audit..."):
        
        # LOOP 1: Go through each news incident row
        for incident in news_data:
            st.write(f"## 📍 News Wire Intelligence: {incident['location']}")
            
            # Create a dictionary to automatically group affected items by their unique backup vendor
            grouped_supplier_data = {}
            
            # LOOP 2: Scan products to find matches and group them first
            for product in supply_data:
                if product["origin_city"].split(",")[0].strip().lower() in incident["location"].lower():
                    vendor = product["backup_supplier"]
                    
                    # If this vendor isn't in our dictionary yet, initialize their list
                    if vendor not in grouped_supplier_data:
                        grouped_supplier_data[vendor] = []
                        
                    grouped_supplier_data[vendor].append(product)
            
            # --- DISPLAY INTERFACE BLOCKS ONLY IF AFFECTED ITEMS EXIST ---
            if grouped_supplier_data:
                
                # Loop through our clean, grouped supplier data blocks
                for supplier, items in grouped_supplier_data.items():
                    
                    with st.container(border=True):
                        st.write(f"### 🏢 Backup Supplier Group: {supplier}")
                        st.write(f"**Backup Facility Location:** {items[0]['backup_location']}")
                        
                        # List out all items going to this specific supplier
                        st.write("**Exposed Components in Transition & Cost Surcharges:**")
                        for item in items:
                            st.write(f"• `{item['part_id']}` - {item['component_name']} (Premium: **{item['alternative_cost_delta']}**)")
                        
                        # --- RUN AGENT FOR THE COMBINED SUPPLIER EMAIL PACKAGE ---
                        inputs = {
                            "disruption_report": incident["bulletin"],
                            "impacted_components": str(items),
                            "remediation_plans": ""
                        }
                        outputs = app.invoke(inputs)
                        
                        # Dropdown displays perfectly grouped supplier email template blocks
                        with st.expander(f"📬 Open Unified Procurement Brief for {supplier}"):
                            st.markdown(outputs["remediation_plans"])
            else:
                st.info("Status Clear. No supply chain components exposed along this corridor.")
            
            st.divider() # Separate news wire entries cleanly
