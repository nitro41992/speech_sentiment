# Speech-to-Text Sentiment Analysis with Google Cloud

This project uses Google Cloud's Speech-to-Text API to transcribe audio files and Google Cloud's Natural Language API to perform sentiment analysis on the transcriptions.

## Prerequisites:

- Google Cloud account
- `ffmpeg` installed and added to the system's PATH
- Python 3.x installed

## Setup:

### 1. Google Cloud Setup

#### a. Create a Google Cloud project:

- Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project.

#### b. Enable the required APIs:

- In the navigation pane, navigate to APIs & Services > Library.
- Search for and enable the `Cloud Speech-to-Text API`.
- Search for and enable the `Cloud Natural Language API`.

#### c. Setup a Service Account:

- In the navigation pane, navigate to IAM & Admin > Service Accounts.
- Click "Create Service Account".
- Fill in the necessary details.
- Assign roles: 
  - `roles/speech.editor` (for Speech-to-Text)
  - `roles/cloudlanguage.admin` (for Natural Language API)
- Click "Continue" and then "Done".
- Once the service account is created, click on it.
- Under the "Keys" tab, click "Add Key" and select JSON. This will download a JSON key to your machine, which will be used for authentication.

### 2. Local Environment Setup

#### a. Clone the Repository:

If you have a repository, clone it:

```bash
git clone [Your Repository URL]
cd [Your Repository Name]
```

If not, simply navigate to the directory where your code resides.

#### b. Setup Virtual Environment:

Run the following commands:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On Linux/Mac:

```bash
source venv/bin/activate
```

#### c. Install the Required Libraries:

```bash
pip install google-cloud-speech google-cloud-language pydub
```

#### d. Set Up Authentication:

Set an environment variable pointing to the downloaded JSON key:

On Windows:

```bash
set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\keyfile.json
```

On Linux/Mac:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/keyfile.json
```

### 3. Run the Application:

With everything set up, you can now run the application:

```bash
python app.py
```

---

Remember to always keep your service account JSON key confidential. Avoid uploading it to public repositories or sharing it openly.


# FAQ

### Set up Google Cloud

1. **Create a Google Cloud Project**: If you don’t already have one, sign up for a Google Cloud account and create a new project.

2. **Enable Billing**: While there's a free tier, you might incur charges if you process a lot of data. Make sure billing is set up for your project.

3. **Activate the Speech-to-Text API and Natural Language API**: Go to the `API & Services` section in the GCP Console and enable both the Speech-to-Text API and the Natural Language API for your project.

4. **Set Up Service Account & Credentials**:
   - Create a new Service Account.
   - Download the JSON key for this account.
   - Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of the downloaded JSON key. This allows your application to authenticate with the APIs.

### Creating a Service Account

1. **Google Cloud Console**:
   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
   - Ensure that you have selected the correct project from the dropdown at the top.

2. **IAM & Admin**:
   - In the left sidebar, navigate to "IAM & Admin" > "Service accounts".
   - Click on the “CREATE SERVICE ACCOUNT” button at the top.

3. **Service Account Details**:
   - **Name**: Provide a meaningful name for your service account. This helps identify its purpose later on.
   - **Description**: Optionally, add a description.
   - Click "Create".

4. **Grant Service Account Access**:
   - Here, you assign roles to the service account. Roles determine what the account can and cannot do.
   - For our use case (Speech-to-Text and Natural Language API), grant roles like "Speech-to-Text User" and "Cloud Natural Language API User" to the service account. You can search for these roles in the search box.
   - Click "Continue".

5. **Create Key**:
   - After creating the service account, click on the row of the account in the Service Accounts dashboard.
   - Navigate to the "Keys" tab.
   - Click on the “ADD KEY” button and select “JSON”.
   - This will automatically download a JSON key file. Store it securely! Anyone with access to this file can authenticate as the service account.

### Using a Service Account in Your Application

1. **Environment Variable**:
   - Most Google Cloud client libraries (including Python) use the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to find the service account key. Set this variable to the path of your downloaded JSON key.
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path-to-your-service-account-file.json"
   ```

2. **In Your Code**:
   - When you initialize a client for a Google Cloud service in your code, the client library will automatically pick up the authentication details from the JSON key.
   ```python
   from google.cloud import language_v1
   client = language_v1.LanguageServiceClient()
   ```
   The above code will authenticate using the service account key you set in the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

### Assigning Roles for Speech-to-Text and Natural Language APIs:

1. **Go to the Service Account**:
   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
   - In the left sidebar, go to "IAM & Admin" > "Service accounts".
   - Click on the service account you created.

2. **Edit the Service Account**:
   - Click on the pencil/edit icon associated with your service account.

3. **Add Roles**:
   - In the 'Role' dropdown, you'll need to search for and select appropriate roles for your use case.

   For **Speech-to-Text**:
   - You might look for roles like:
     - "Cloud Speech-to-Text Viewer"
     - "Cloud Speech-to-Text Editor"
     - Or roles that grant broader access but include Speech-to-Text permissions.

   For **Natural Language API**:
   - Similarly, look for roles like:
     - "Cloud Natural Language Viewer"
     - "Cloud Natural Language Editor"
     - Or roles with broader access to the Natural Language API.

4. **Save**:
   - After assigning the roles, make sure to save your changes.

### Best Practices & Cautions

- **Never commit the service account key JSON to your public repositories.** It's sensitive data. If you're using version control like git, add the JSON key file to your `.gitignore`.
  
- Service accounts can have wide-ranging permissions, depending on the roles assigned. **Always follow the principle of least privilege** – only grant the permissions that are absolutely necessary for your use case.

- Periodically review and rotate service account keys. If a key is compromised, revoke it immediately.

- If your application is running on Google Cloud infrastructure (like Compute Engine, Kubernetes Engine, etc.), consider using the **default service account** associated with that service. It can be granted permissions and eliminates the need to manage service account keys manually.

This should give you a good foundation for creating and using service accounts with Google Cloud. Always refer to the official Google Cloud documentation for more detailed and up-to-date information.