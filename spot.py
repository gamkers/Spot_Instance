import streamlit as st
import subprocess
import os

# Set the file permissions to allow execution
os.chmod('./spotinfo', 0o755)

# Now you can try to execute the file
try:
    subprocess.run('./spotinfo', shell=True)
except Exception as e:
    print(f"Error: {e}")

# Function to run spotinfo
def run_spotinfo(args):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')

# Set page title and add some space on the left and right
st.title(" AWS Spot Instance Calculator ")
st.write(" ")

st.header("What is Spot Instances?")
# Explanation of AWS Spot Instances
st.write("AWS Spot Instances are a cost-effective option to use AWS cloud computing resources. They allow you to take advantage of unused AWS EC2 capacity at a lower cost. Spot Instances are ideal for workloads like batch processing, data analysis, rendering, and simulations. However, they can be interrupted with short notice, so it's important to design your applications to handle interruptions gracefully.")
st.write(" ")

# Create a sidebar for user input
st.sidebar.title("Settings")
instance_choice = st.sidebar.selectbox("Choose EC2 instance type:", [
    "t2.micro", "t2.small", "t2.medium", "t3.nano",  # Add all choices
    "t3.micro", "t3.small", "t3.medium", "c5.large",
    # ... add more choices ...
], index=0)

os_choice = st.sidebar.selectbox("Choose instance operating system:", ["Windows", "Linux", "macOS"])
region = st.sidebar.text_input("Enter AWS region (use 'all' for all regions)", "us-east-1")
output = st.sidebar.selectbox("Enter output format", ["number", "text", "json", "table", "csv"], index=3)
cpu = st.sidebar.slider("Enter minimal vCPU cores", min_value=0, max_value=64, value=0)
memory = st.sidebar.slider("Enter minimal memory GiB", min_value=0, max_value=256, value=0)
price = st.sidebar.slider("Enter maximum price per hour", min_value=0.0, max_value=10.0, value=0.0)
sort = st.sidebar.selectbox("Enter sort order", ["interruption", "type", "savings", "price", "region"], index=0)
order = st.sidebar.selectbox("Enter sort order", ["asc", "desc"], index=0)

if st.sidebar.button("Run spotinfo"):
    # Prepare the arguments for the shell script
    args = [
        "./spotinfo", "--type", instance_choice, "--os", os_choice, "--region", region,
        "--output", output, "--cpu", str(cpu), "--memory", str(memory),
        "--price", str(price), "--sort", sort, "--order", order
    ]
    
    # Run the shell script and get output
    output, error = run_spotinfo(args)
    
    # Display the output and error
    st.text("Output:")
    st.code(output)
    if error:
        st.text("Error:")
        st.code(error)
