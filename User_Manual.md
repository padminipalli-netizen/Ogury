# ⚡ Ogury One API - User Manual

Welcome to the **Ogury One API**! This interactive dashboard allows you to easily connect to the Ogury API, test pre-configured endpoints across different modules (Personas, Accounts, Deals, Reporting), and build custom API requests.

---

## 1. Authentication & Configuration (Sidebar)
Before you can make any API calls, you need to authenticate your session. 

1. Locate the **Configuration** section on the left side of the screen.
2. Enter your **Client ID** and **Client Secret**.
3. Click the **Generate Token** button.
4. Check the **Status** indicator:
   - 🟢 **Authenticated:** The connection is successful. It will display the time remaining before the token expires (tokens usually last 60 minutes).
   - 🔴 **Not Authenticated:** Missing or incorrect credentials.
5. The sidebar also features a **History** log where you can see the last 10 requests you made during your session.

---

## 2. API Playground (Pre-configured Endpoints)
The middle column of the dashboard is the **Playground**, divided into 4 main tabs. Clicking any button in these tabs will automatically populate the **Custom Request Builder** at the bottom of the screen with the necessary Method, Endpoint, and Payload, making it ready to send.

### 🔹 Tab 1: Personas
Explore and manage Ogury audience personas.
* **GET Persona:** Retrieves the entire catalog of available personas. (`GET v1/personas`)
* **GET Basic Persona:** Filters the catalog to only show basic personas. (`GET v1/personas?personaType=basic-persona`)
* **GET Vertical: Tech:** Retrieves personas categorized under "interest" and the "technology" vertical.
* **GET Persona by ID:** Fetches details for a specific persona ID (defaults to `7781`).
* **POST Save Persona:** Saves a custom audience to "My Personas". Prepops an example payload including Country, Expression (Operands, Operator), Age, Gender, and Metadata.
* **POST Combine:** Simulates the audience reach for combining specific personas.
* **POST Translate (Text / PQL):** Translates either plain text (e.g., *"Tech enthusiasts who travel frequently"*) or PQL (Persona Query Language) into targeted audience segments.
* **GET Countries:** Retrieves a list of supported countries for personas.

### 🔹 Tab 2: Accounts & Brands
Manage your organizational entities.
* **GET All Accounts:** Retrieves a list of all your associated Ogury Accounts. (`GET v1/accounts`)
* **GET All Brands:** Retrieves a list of all Brands associated with your accounts. (`GET v1/brands`)

### 🔹 Tab 3: Deals & DSPs
Manage programmatic Deals and Demand-Side Platforms.
* **GET List Deals:** Retrieves a list of all configured deals. (`GET v1/deals`)
* **GET Deal by ID:** Retrieves details for a specific Deal. *(Note: Replace `DEAL_ID_HERE` in the Endpoint box before sending)*.
* **POST Create Deal:** Creates a new deal. Pre-populates a JSON payload (requires Account ID, Brand ID, Seat ID, Dates, and Price configuration).
* **PUT Update Deal:** Updates an existing deal. *(Note: Replace `DEAL_ID_HERE` before sending)*.
* **GET List DSPs:** Retrieves the list of available DSPs. (`GET v1/dsps`)

### 🔹 Tab 4: Reporting
Pull delivery, performance, and geographic reports. 

**How to use:**
1. Use the input fields at the top of the tab to specify your report parameters:
   - **Start Date / End Date** (Required)
   - **Account ID(s)** 
   - **Brand ID(s)**
   - **Campaign ID(s)** (Optional)
   - **Country Code** (ISO format, e.g., US, FR, SG - Optional)
2. Click on the desired report granularity button to execute the query immediately:
   - **Account, Campaigns, Creatives, Geography, Region, Devices, Daily.**
   
*(Note: Clicking a reporting button will automatically trigger the API call, unlike the other tabs which just populate the builder).*

---

## 3. Custom Request Builder (Bottom Center)
If you have a custom request, need to tweak a payload, or want to hit an endpoint not listed in the tabs, use the **Custom Request Builder** located just below the Playground.

1. **Method:** Select the HTTP method from the dropdown (`GET`, `POST`, `PUT`, `DELETE`).
2. **Endpoint:** Enter the endpoint route (e.g., `v1/personas?country=US`). You do not need to include `https://api.ogury.com/`, the app handles the base URL automatically.
3. **Payload:** If making a `POST` or `PUT` request, paste your JSON body in this text area. Ensure it is valid JSON formatting.
4. **Send:** Click the blue **Send** button to execute the request.

---

## 4. Terminal Output Panel (Right Sidebar)
All API responses will be printed in the dark **Terminal Output Panel** on the right side of your screen. 

* **Response Details:** Displays the HTTP Method used, the full executed URL, the HTTP Status Code (e.g., `200` for success, `400` for Bad Request), and the exact timestamp.
* **JSON Viewer:** The JSON response payload is rendered below the request details. 
* **Download Button:** Click this to instantly download the current JSON response as a `.json` file to your local computer.
* **Clear Button:** Wipes the terminal screen clean to prepare for a fresh request.
