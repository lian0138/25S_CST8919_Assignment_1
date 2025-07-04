
# Assignment 1: Flask Web App with Auth0 and Structured Logging

This README covers the setup for a Flask app with Auth0 authentication, Azure deployment, structured logging, and alerting for unauthorized access or excessive usage.

## ✅ Setup Instructions

### Auth0 Setup
1. Log in to [Auth0](https://auth0.com/) and create a new **Regular web application** under Applications.
2. Configure the app (after deploying the app on Azure) with:
   - **Allowed Callback URLs**: `http://your-app-name.azurewebsites.net/callback`
   - **Allowed Logout URLs**: `http://your-app-name.azurewebsites.net/`
3. Record the **Domain**, **Client ID**, and **Client Secret** for use in `.env`.

### Environment Variables (.env File)
Create a `.env` file at the project root with the following:
```env
AUTH0_DOMAIN=your-auth0-domain.auth0.com
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
APP_SECRET_KEY=ALongRandomlyGeneratedString
```

### Azure Deployment
1. In VS Code, press **F1** and select **Azure App Service: Create New Web App**.
2. Follow prompts to name the app and select a resource group.
3. After creation, press **F1** again and select **Azure App Service: Deploy to Web App** to deploy your Flask app to Azure.
4. Ensure **Application Logging (stdout/stderr)** is enabled in **App Service Logs** under **Monitoring** in Azure Portal.

## 📌 Logging and Detection Logic

### Logging (As Per Code)
The app uses `app.logger` to emit structured JSON logs for key events with visual indicators as seen in the provided code:
- **Successful Login**: Logs `"✅ Successful login"` and structured JSON (timestamp, user_id, email, route, ip) for every successful login at `/callback`.
- **Failed Login**: Logs `"⚠️ Failed login attempt"` with error details and structured JSON on OAuth errors at `/callback`.
- **Authorized Access to /protected**: Logs `"✅ Authorized access to protected route"` with user details in structured JSON.
- **Unauthorized Access to /protected**: Logs `"⚠️ Unauthorized access attempt to protected route"` with structured JSON for unauthorized attempts.

Logs are output to stdout and captured by Azure App Service for analysis.

### Detection Logic
Detection focuses on identifying suspicious activity based on the code:
- **Failed logins** (`login_failure`) or **unauthorized accesses** to `/protected` (`unauthorized_access`) are marked with `"WARNING: ⚠️"` in logs.
- **Excessive usage** by a single user (tracked via `user_id` in logs) triggers an alert if accesses exceed a defined threshold.

## 📊 KQL Query and Alert Logic

### KQL Query 1 (Filter Warnings for Failed Logins/Unauthorized Access)
This query filters logs containing warnings for failed logins or unauthorized access attempts:
```kusto
AppServiceConsoleLogs 
| where ResultDescription contains "WARNING: ⚠️"
| where Level contains "Informational"
| order by TimeGenerated desc
```

### KQL Query 2 (Detect Excessive Access by User)
This query detects if any user exceeds 10 accesses in 15 minutes:
```kusto
AppServiceConsoleLogs  
| where ResultDescription contains "WARNING: ⚠️"  
| where Level contains "Informational"  
| order by TimeGenerated desc
```

### Alert Logic (Azure)
1. In Azure Portal, go to **Log Analytics Workspace** > **Alerts** > **+ New Alert Rule**.
2. Create an alert with this KQL:
```KQL
AppServiceConsoleLogs  
| where ResultDescription contains "WARNING: ⚠️"  
| where Level contains "Informational"  
| order by TimeGenerated desc
```
Trigger alert if **any user** exceeds 10 accesses in 15 minutes

## Youtube
This is the youtube link
https://youtu.be/sJcZ7JbeQ-Y