import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Spotify", page_icon=":tada:", layout='wide')
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

# Explanation of AWS Spot Instances
st.header("What is Spot Instances?")
st.write("AWS Spot Instances are a cost-effective option to use AWS cloud computing resources. They allow you to take advantage of unused AWS EC2 capacity at a lower cost. Spot Instances are ideal for workloads like batch processing, data analysis, rendering, and simulations. However, they can be interrupted with short notice, so it's important to design your applications to handle interruptions gracefully.")
st.write(" Amazon EC2 Spot Instances let you take advantage of unused EC2 capacity in the AWS cloud. Spot Instances are available at up to a 90% discount compared to On-Demand prices. You can use Spot Instances for various stateless, fault-tolerant, or flexible applications such as big data, containerized workloads, CI/CD, web servers, high-performance computing (HPC), and test & development workloads. Because Spot Instances are tightly integrated with AWS services such as Auto Scaling, EMR, ECS, CloudFormation, Data Pipeline and AWS Batch, you can choose how to launch and maintain your applications running on Spot Instances.")

# Create a sidebar for user input
st.sidebar.title("Settings")
instance_choice = st.sidebar.selectbox("Choose EC2 instance type:", [
    "t2.micro", "t2.small", "t2.medium", "t2.large", "t2.xlarge", "t2.2xlarge",
    "t3.nano", "t3.micro", "t3.small", "t3.medium", "t3.large", "t3.xlarge", "t3.2xlarge",
    "m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge",
    "m4.large", "m4.xlarge", "m4.2xlarge", "m4.4xlarge", "m4.10xlarge",
    "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "m5.12xlarge", "m5.24xlarge",
    "c3.large", "c3.xlarge", "c3.2xlarge", "c3.4xlarge", "c3.8xlarge",
    "c4.large", "c4.xlarge", "c4.2xlarge", "c4.4xlarge", "c4.8xlarge",
    "c5.large", "c5.xlarge", "c5.2xlarge", "c5.4xlarge", "c5.9xlarge", "c5.12xlarge", "c5.18xlarge",
    "r3.large", "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge",
    "r4.large", "r4.xlarge", "r4.2xlarge", "r4.4xlarge", "r4.8xlarge", "r4.16xlarge",
    "x1.16xlarge", "x1.32xlarge",
    "x1e.xlarge", "x1e.2xlarge", "x1e.4xlarge", "x1e.8xlarge", "x1e.16xlarge", "x1e.32xlarge",
    "i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge",
    "i3.large", "i3.xlarge", "i3.2xlarge", "i3.4xlarge", "i3.8xlarge", "i3.16xlarge",
    "d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge",
    "h1.2xlarge", "h1.4xlarge", "h1.8xlarge", "h1.16xlarge",
    "f1.2xlarge", "f1.4xlarge", "f1.16xlarge",
    "p2.xlarge", "p2.8xlarge", "p2.16xlarge",
    "p3.2xlarge", "p3.8xlarge", "p3.16xlarge",
    "g2.2xlarge", "g2.8xlarge",
    "g3.4xlarge", "g3.8xlarge", "g3.16xlarge",
    "g4dn.xlarge", "g4dn.2xlarge", "g4dn.4xlarge", "g4dn.8xlarge", "g4dn.12xlarge", "g4dn.16xlarge",
    "m6g.medium", "m6g.large", "m6g.xlarge", "m6g.2xlarge", "m6g.4xlarge", "m6g.8xlarge", "m6g.12xlarge", "m6g.16xlarge",
    "m6gd.medium", "m6gd.large", "m6gd.xlarge", "m6gd.2xlarge", "m6gd.4xlarge", "m6gd.8xlarge", "m6gd.12xlarge", "m6gd.16xlarge",
    "c6g.medium", "c6g.large"
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
