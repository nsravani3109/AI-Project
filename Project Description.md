Project Description
# use Python 

FDE Technical Challenge: Inbound Carrier Sales
Overview
You are meeting with a customer (played by the interviewer) to present a solution you built using
the HappyRobot platform. The customer is evaluating vendors to handle inbound carrier load
sales automation. Your agent will receive calls from carriers looking to book loads. Your task is
to show a working proof of concept and demonstrate both technical depth and customer-centric
thinking.
📦 Goals
🤖 Objective 1: Implement Inbound Use Case
●
●
A freight brokerage wants to automate inbound carrier calls. Carriers call in
to request loads. The system must authenticate them, match them to viable
loads, and negotiate pricing automatically.
Use the HappyRobot platform to create an inbound agent where the AI assistant gets
calls from carriers.
The loads will be searched using an API in a file or DB which will contain the context
within the following fields for each load:
Field Description
load
_
id Unique identifier for the load
origin Starting location
destination Delivery location
pickup_
datetime Date and time for pickup
delivery_
datetime Date and time for delivery
equipment
_
type Type of equipment needed
loadboard
rate Listed rate for the load
_
notes Additional information
weight Load weight
commodity_
type Type of goods
num
of
_
_pieces Number of items
miles Distance to travel
dimensions Size measurements
●
The assistant must:
○
Get their MC number and verify they are eligible to work with using the FMCSA
API.
○
Search the load and pitch the details.
○
Ask if they’re interested in accepting the load.
○
If they make a counter offer evaluate it. Handle up to 3 back and forth’s
negotiating the offer.
○
If a price is agreed, transfer the call to a sales rep.
○
Extract from the call the most relevant data for the offer.
○
Classify the call based in it’s outcome.
○
Classify the sentiment of the carrier in the call.
📊 Objective 2: Metrics
●
You must create a dashboard/report mechanism to show use case metrics
⚙ Objective 3: Deployment and infrastructure
●
Containerize the solution with Docker.
🧪 Deliverables
1. An email to your prospect client, Carlos Becker (c.becker@happyrobot.ai with your
recruiter in cc) indicating your latest advancements ahead of your meeting with them.
2. Write a document as if you were submitting the build description to a real freight broker
(e.g.,
“Acme Logistics”).
3. 4. 5. Link to your code repository.
Link to the configured outbound campaign in the HappyRobot platform.
A short video (5 mins) walking through:
○
Use case setup
○
Short demo
○
Dashboard
🛡Additional Considerations
1. Security:
If you’re creating an API, add basic security features such as:
○
HTTPS (self-signed locally is fine, use Let’s Encrypt or equivalent if deployed)
○
API key authentication for all endpoints
2. Deployment:
○
○
Deploy your API to a cloud provider of your choice (e.g., AWS, Google Cloud,
Azure, Fly.io, Railway, etc.)
Provide clear instructions on how to:
■ Access the deployment.
■ Reproduce your deployment if needed (e.g., Terraform, shell script, or
manual steps)
3. Calls:
○
Do not buy a phone number on the platform. Use the web call trigger feature.