import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🚀 AI Analytics Copilot")
st.write("Day 1: Setup Complete!")

st.subheader("✅ Environment Check")

# Check credentials loaded
resource_group = os.getenv("AZURE_RESOURCE_GROUP")
pg_host = os.getenv("PGHOST")

if resource_group:
    st.success(f"Resource Group: {resource_group}")
else:
    st.error("Resource Group not found in .env")

if pg_host:
    st.success(f"PostgreSQL Host: {pg_host}")
else:
    st.error("PostgreSQL not configured")

st.balloons()
