# Assignment 1: Securing and Monitoring an Authenticated Flask App

## Overview

You’ve already:
- Implemented SSO with Auth0 in **Lab 1**
- Deployed and monitored a Flask app using Azure in **Lab 2**

Now, you'll **combine both** to build a production-ready secure app:
- Deploy your **Auth0-authenticated Flask app** to Azure
- Add **custom logging** for user activities (logins, protected route access)
- Use **Azure Monitor + KQL** to detect suspicious activity (e.g., excessive access to protected routes)
- Create **alerts** based on your queries

---


## Scenario

You're part of a DevSecOps team for a cloud-based SaaS platform. The app uses SSO (Auth0) and is hosted on Azure. You're tasked with:
- Monitoring authenticated user activity
- Detecting and alerting on excessive access to sensitive endpoints (e.g., `/protected`)
- Demonstrating secure integration between identity and observability systems

---

## Tasks

### Part 1: App Enhancements & Deployment
1. **Enhance your Flask App from Lab 1**:
   - Use your existing Auth0 integration.
   - Add logging for:
     - Every login (capture `user_id`, `email`, `timestamp`)
     - Access to `/protected` route
     - Any unauthorized attempts
   - Use `app.logger.info()` or `app.logger.warning()` to emit structured logs.

2. **Deploy to Azure App Service**:
   - Reuse Azure setup from Lab 2.
   - Ensure AppServiceConsoleLogs is enabled and logs are sent to Log Analytics.

---

### Part 2: Monitoring & Detection
1. **Simulate traffic** by accessing the `/protected` route multiple times with valid Auth0 logins.

2. **KQL Query**:
   - Write a KQL query that identifies:
     - Any user who accessed `/protected` more than **10 times** in the past **15 minutes**.
   - Display `user_id`, `timestamp`, and count of accesses.



3. **Create Azure Alert**:
   - Trigger alert if **any user** exceeds 10 accesses in 15 minutes.
   - Send email notification using an **Action Group**.
   - Alert severity: **3 (Low)**

---

### Part 3: GitHub Repo + Demo

#### Repo structure:
- `app.py` or similar main file
- `requirements.txt`
- `.env.example` (without secrets)
- `README.md` with:
  - Setup steps (Auth0, Azure, .env)
  - Explanation of logging, detection logic
  - KQL query and alert logic
- `test-app.http` file simulating valid and invalid accesses

#### YouTube Demo (10 min max):
- App deployed on Azure with working Auth0 login
- Logging behavior on login and route access
- Azure Monitor: Run your KQL query
- Show triggered alert email (if possible)
- Reflection: What worked, what you'd improve

---

## 📦 Submission Instructions

Submit the link to your **public GitHub repo** on Brightspace, including the **YouTube demo link** in your `README.md`.

**Due Date**: **Sunday, July 6, 2025 by 11:59 PM**

---
