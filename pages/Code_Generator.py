import streamlit as st
import google.generativeai as genai
from Navigation import sidebar

sidebar()

# Initialize Generative AI model

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Configure Streamlit page
# st.set_page_config(page_title="Code Generation", page_icon="💻")

# Templates for different platforms
platform_templates = {
    "React": {
        "prompt_template": """Generate a React component for the given feature: {input_query}.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Concisely state the user's main goal.
   - **Category:** Select the appropriate business category (strategy, marketing, sales, finances, legal, IT, HR, Ops, CX).
   - **Sentiment:** Indicate the user's sentiment (positive, neutral, negative).

2. **REQUIREMENTS:**
   - **Language/Platform:** Specify the programming language or platform for the code.
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any dependencies or libraries required for the code.
   - **System Capabilities:** Mention the minimum system capabilities required to run this component effectively (e.g., browser compatibility, performance considerations).
   - **Required Versions:** Specify the required versions of frameworks, libraries, or other software components needed to use this component effectively.

3. **SOLUTION:** 
   - Provide a detailed response to the user’s query, including the code snippet. Use markdown code blocks to format the code appropriately.

4. **STEP-BY-STEP PROCESS:**
   - **Step 1:** Describe the initial setup steps (e.g., installing Node.js and creating a new React project).
   - **Step 2:** Provide instructions for integrating the generated component into an existing React project.
   - **Step 3:** Include tips or customization options to adapt the component for different use cases.

5. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions to set up the environment for running the code.
     - Ensure Node.js node_version or higher is installed.
     - Install necessary packages using `npm` or `yarn`.
   - **Run:** Steps to execute the code.
   - **Example:** Provide an example usage scenario if applicable.

6. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.
"""
    },
    "ASP.NET MVC": {
        "prompt_template": """Generate an ASP.NET MVC controller and corresponding views.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Create a controller with views to handle {input_query}.
   - **Category:** IT
   - **Sentiment:** 😃 Positive

2. **REQUIREMENTS:**
   - **Language/Platform:** ASP.NET MVC
   - **Functionality/Feature:** {input_query}
   - **Dependencies:** Entity Framework, ASP.NET Core libraries

3. **SOLUTION:** 
```csharp
// Example ASP.NET MVC controller code
public class ControllerName Controller : Controller
{{
    public IActionResult Index()
    {{
        return View();
    }}
}}
```

4. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions to set up the environment for running the code.
   - **Run:** Steps to execute the code.
   - **Example:** Provide an example usage scenario if applicable.

5. **RESOURCES:**
   - Include references to any sources or relevant resources.
   - Format each reference as `[Source](link)`.

"""

    },
    "Sitecore": {
"prompt_template": """Generate a solution using Sitecore for the given feature: {input_query}.
Explanation of Each Section:
PROBLEM:

Rephrase user query: Restate the user's query to confirm understanding.
Intent: Concisely state the user's main goal.
Category: Select the appropriate business category (strategy, marketing, sales, finances, legal, IT, HR, Ops, CX).
Sentiment: Indicate the user's sentiment (positive, neutral, negative).
REQUIREMENTS:

Platform: Sitecore
Functionality/Feature: Describe the specific functionality or feature needed.
Dependencies: Outline any necessary modules or integrations required.
SOLUTION:

Provide a detailed response to the user’s query, including the approach and key components.
USAGE INSTRUCTIONS:

Setup: Instructions to set up the Sitecore environment for the solution.
Run: Steps to deploy and test the solution.
Example: Provide a usage scenario or use case.
RESOURCES:

Include references to any sources or relevant resources related to Sitecore.
Format each reference as [Source](link).

"""
},
"XMCLOUD": {
"prompt_template": """Generate a solution using XMCloud for the given feature: {input_query}.
Explanation of Each Section:
PROBLEM:

Rephrase user query: Restate the user's query to confirm understanding.
Intent: Concisely state the user's main goal.
Category: Select the appropriate business category (strategy, marketing, sales, finances, legal, IT, HR, Ops, CX).
Sentiment: Indicate the user's sentiment (positive, neutral, negative).
REQUIREMENTS:

Platform: XMCloud
Functionality/Feature: Describe the specific functionality or feature needed.
Dependencies: Outline any necessary modules or integrations required.
SOLUTION:

Provide a detailed response to the user’s query, including the approach and key components.
USAGE INSTRUCTIONS:

Setup: Instructions to set up the XMCloud environment for the solution.
Run: Steps to deploy and test the solution.
Example: Provide a usage scenario or use case.
RESOURCES:

Include references to any sources or relevant resources related to XMCloud.
Format each reference as [Source](link).
"""
},
"Contentstack": {
"prompt_template": """Generate a solution using Contentstack for the given feature: {input_query}.
Explanation of Each Section:
PROBLEM:

Rephrase user query: Restate the user's query to confirm understanding.
Intent: Concisely state the user's main goal.
Category: Select the appropriate business category (strategy, marketing, sales, finances, legal, IT, HR, Ops, CX).
Sentiment: Indicate the user's sentiment (positive, neutral, negative).
REQUIREMENTS:

Platform: Contentstack
Functionality/Feature: Describe the specific functionality or feature needed.
Dependencies: Outline any necessary modules or integrations required.
SOLUTION:

Provide a detailed response to the user’s query, including the approach and key components.
USAGE INSTRUCTIONS:

Setup: Instructions to set up the Contentstack environment for the solution.
Run: Steps to deploy and test the solution.
Example: Provide a usage scenario or use case.
RESOURCES:

Include references to any sources or relevant resources related to Contentstack.
Format each reference as [Source](link).

"""
},
"C#":{

"prompt_template": """Generate a C# component for the given feature: {input_query}.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Concisely state the user's main goal.
   - **Category:** Select the appropriate category (e.g., data processing, web development, desktop application).
   - **Sentiment:** Indicate the user's sentiment (positive, neutral, negative).

2. **REQUIREMENTS:**
   - **Platform:** Specify the .NET framework version or platform.
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any libraries or NuGet packages required for the code.
   - **System Capabilities:** Mention the minimum system capabilities required to run this component effectively.
   - **Required Versions:** Specify the required versions of frameworks, libraries, or other components.

3. **SOLUTION:** 
   - Provide a detailed response to the user’s query, including the C# code snippet. Use markdown code blocks to format the code appropriately.

4. **STEP-BY-STEP PROCESS:**
   - **Step 1:** Describe the initial setup steps (e.g., installing Visual Studio and creating a new project).
   - **Step 2:** Provide instructions for integrating the generated component into an existing C# project.
   - **Step 3:** Include tips or customization options to adapt the component for different use cases.

5. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions to set up the environment for running the code.
     - Ensure .NET framework_version or higher is installed.
     - Install necessary packages using NuGet.
   - **Run:** Steps to execute the code.
   - **Example:** Provide an example usage scenario if applicable.

6. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.

"""
},
"Java": {
    "prompt_template": """Generate a Java component for the given feature: {input_query}.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Concisely state the user's main goal.
   - **Category:** Select the appropriate category (e.g., backend service, data processing, Android application).
   - **Sentiment:** Indicate the user's sentiment (positive, neutral, negative).

2. **REQUIREMENTS:**
   - **Platform:** Specify the Java version or platform (e.g., Java SE 11, Android API level 30).
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any external libraries or Maven dependencies required for the code.
   - **System Capabilities:** Mention the minimum system requirements needed to run this component effectively.
   - **Required Versions:** Specify the required versions of libraries, frameworks, or other components.

3. **SOLUTION:** 
   - Provide a detailed response to the user’s query, including the Java code snippet. Use markdown code blocks to format the code appropriately.

4. **STEP-BY-STEP PROCESS:**
   - **Step 1:** Describe the initial setup steps (e.g., installing JDK, setting up IDE).
   - **Step 2:** Provide instructions for integrating the generated component into an existing Java project.
   - **Step 3:** Include tips or customization options to adapt the component for different use cases.

5. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions to set up the environment for running the code.
     - Ensure JDK version is installed (specify version).
     - Include steps to manage dependencies with Maven or Gradle.
   - **Run:** Steps to compile and execute the code.
   - **Example:** Provide an example usage scenario if applicable.

6. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.

"""
}
,
"Js":{
   "prompt_template": """Generate a JavaScript component for the given feature: {input_query}.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Concisely state the user's main goal.
   - **Category:** Select the appropriate category (e.g., frontend development, backend scripting, Node.js application).
   - **Sentiment:** Indicate the user's sentiment (positive, neutral, negative).

2. **REQUIREMENTS:**
   - **Language/Platform:** Specify the JavaScript version or platform (e.g., Node.js, browser).
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any libraries or packages required for the code.
   - **System Capabilities:** Mention the minimum system capabilities required to run this component effectively.
   - **Required Versions:** Specify the required versions of frameworks, libraries, or other software components.

3. **SOLUTION:** 
   - Provide a detailed response to the user’s query, including the JavaScript code snippet. Use markdown code blocks to format the code appropriately.

4. **STEP-BY-STEP PROCESS:**
   - **Step 1:** Describe the initial setup steps (e.g., installing Node.js and creating a new project).
   - **Step 2:** Provide instructions for integrating the generated component into an existing JavaScript project.
   - **Step 3:** Include tips or customization options to adapt the component for different use cases.

5. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions to set up the environment for running the code.
     - Ensure Node.js node_version or higher is installed.
     - Install necessary packages using `npm` or `yarn`.
   - **Run:** Steps to execute the code.
   - **Example:** Provide an example usage scenario if applicable.

6. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.

"""

},
"Python":{
   "prompt_template": """Generate a Python component for the given feature: {input_query}.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Concisely state the user's main goal.
   - **Category:** Select the appropriate category (e.g., data processing, web scraping, automation, machine learning).
   - **Sentiment:** Indicate the user's sentiment (positive, neutral, negative).

2. **REQUIREMENTS:**
   - **Language/Platform:** Specify the Python version or platform (e.g., Python 3.x, Anaconda).
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any libraries or packages required for the code.
   - **System Capabilities:** Mention the minimum system capabilities required to run this component effectively.
   - **Required Versions:** Specify the required versions of frameworks, libraries, or other software components.

3. **SOLUTION:** 
   - Provide a detailed response to the user’s query, including the Python code snippet. Use markdown code blocks to format the code appropriately.

4. **STEP-BY-STEP PROCESS:**
   - **Step 1:** Describe the initial setup steps (e.g., installing Python and setting up a virtual environment).
   - **Step 2:** Provide instructions for integrating the generated component into an existing Python project.
   - **Step 3:** Include tips or customization options to adapt the component for different use cases.

5. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions to set up the environment for running the code.
     - Ensure Python python_version or higher is installed.
     - Install necessary packages using `pip`.
   - **Run:** Steps to execute the code.
   - **Example:** Provide an example usage scenario if applicable.

6. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.

"""
},
"Next.Js":{
   "prompt_template": """Generate a Next.js component for the given feature: {input_query}.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Concisely state the user's main goal.
   - **Category:** Select the appropriate category (e.g., frontend development, server-side rendering, static site generation).
   - **Sentiment:** Indicate the user's sentiment (positive, neutral, negative).

2. **REQUIREMENTS:**
   - **Language/Platform:** Specify the Next.js version or platform.
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any libraries or packages required for the code.
   - **System Capabilities:** Mention the minimum system capabilities required to run this component effectively (e.g., browser compatibility, performance considerations).
   - **Required Versions:** Specify the required versions of frameworks, libraries, or other software components needed to use this component effectively.

3. **SOLUTION:** 
   - Provide a detailed response to the user’s query, including the code snippet. Use markdown code blocks to format the code appropriately.

4. **STEP-BY-STEP PROCESS:**
   - **Step 1:** Describe the initial setup steps (e.g., installing Node.js and creating a new Next.js project).
   - **Step 2:** Provide instructions for integrating the generated component into an existing Next.js project.
   - **Step 3:** Include tips or customization options to adapt the component for different use cases.

5. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions to set up the environment for running the code.
     - Ensure Node.js node_version or higher is installed.
     - Install necessary packages using `npm` or `yarn`.
   - **Run:** Steps to execute the code.
   - **Example:** Provide an example usage scenario if applicable.

6. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.

"""

},
"SQL":{
   "prompt_template": {
      "prompt_template": """Generate a SQL query for the given feature: {input_query}.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Concisely state the user's main goal.
   - **Category:** Select the appropriate category (e.g., data retrieval, data manipulation, database administration).
   - **Sentiment:** Indicate the user's sentiment (positive, neutral, negative).

2. **REQUIREMENTS:**
   - **Platform:** Specify the SQL dialect or database system (e.g., MySQL, PostgreSQL, SQL Server).
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any additional tools or libraries required for executing the query.
   - **System Capabilities:** Mention any system requirements for executing the query effectively (e.g., database server version).

3. **SOLUTION:** 
   - Provide the SQL query and a brief explanation of its functionality. Use markdown code blocks to format the query appropriately.

4. **STEP-BY-STEP PROCESS:**
   - **Step 1:** Describe any prerequisites or setup steps required (e.g., connecting to the database).
   - **Step 2:** Explain how to execute the SQL query.
   - **Step 3:** Include tips or additional considerations for optimizing or modifying the query.

5. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions for setting up the environment to execute the SQL query.
     - Ensure the database system is installed and accessible.
   - **Execution:** Steps to run the SQL query.
   - **Example:** Provide an example scenario demonstrating the use of the SQL query.

6. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.

"""

   }
},
"AEM":{
   "prompt_template": """Generate an AEM component for the given feature: {input_query}.
### Explanation of Each Section:

1. **PROBLEM:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Intent:** Concisely state the user's main goal.
   - **Category:** Select the appropriate category (e.g., content management, digital asset management, personalization).
   - **Sentiment:** Indicate the user's sentiment (positive, neutral, negative).

2. **REQUIREMENTS:**
   - **Platform:** Specify the AEM version or platform.
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any additional components or APIs required for the AEM component.
   - **System Capabilities:** Mention any system requirements for the AEM component (e.g., Java version, AEM compatibility).

3. **SOLUTION:** 
   - Provide a detailed response to the user’s query, including the necessary configuration and code snippet. Use markdown code blocks to format the code appropriately.

4. **STEP-BY-STEP PROCESS:**
   - **Step 1:** Describe the initial setup steps (e.g., accessing AEM author instance, configuring necessary permissions).
   - **Step 2:** Provide instructions for creating or modifying the AEM component.
   - **Step 3:** Include tips or customization options to adapt the AEM component for different use cases.

5. **USAGE INSTRUCTIONS:**
   - **Setup:** Instructions to set up the environment for deploying the AEM component.
     - Ensure Java java_version or higher is installed.
     - Deploy the package to AEM using CRX Package Manager.
   - **Integration:** Steps to integrate the AEM component into a web page or application.
   - **Example:** Provide an example usage scenario if applicable.

6. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.

"""
},
"Html and CSS":{
    "prompt_template": """Generate HTML and CSS for the following feature: {input_query}.
### Explanation of Each Section:

1. **FEATURE DESCRIPTION:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Purpose:** State the main purpose or functionality of the feature.
   - **Design Requirements:** Describe any specific design requirements or goals.

2. **HTML STRUCTURE:**
   - Provide the HTML structure required for implementing the feature.
   - Use HTML tags and attributes to define elements and their hierarchy.
   - Include placeholders or dynamic content areas if applicable.

3. **CSS STYLING:**
   - Define the CSS styles necessary to achieve the desired visual appearance.
   - Use classes, IDs, or element selectors as needed.
   - Consider responsiveness and browser compatibility.

4. **USAGE INSTRUCTIONS:**
   - **Integration:** Steps to integrate the HTML and CSS into a web page or application.
   - **Example Usage:** Provide an example usage scenario if applicable.
   - **Customization:** Tips for modifying the HTML and CSS for different use cases.

5. **RESOURCES:**
   - Include references to any sources or relevant resources for further reading.
     - Format each reference as `[Source](link)`.

"""
},
"Flutter": {
    "prompt_template": """Generate a Flutter widget or component for the following feature: {input_query}.
### Explanation of Each Section:

1. **FEATURE DESCRIPTION:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Purpose:** State the main purpose or functionality of the feature.
   - **Design Requirements:** Describe any specific design requirements or goals.

2. **FLUTTER WIDGET:**
   - Provide the Dart code for the Flutter widget or component required for implementing the feature.
   - Use Flutter widgets, layout elements, and any necessary packages.
   - Include placeholders or dynamic content areas if applicable.

3. **STYLING AND THEMING:**
   - Define the styling and theming necessary to achieve the desired visual appearance.
   - Use Flutter's `ThemeData`, `Container`, `TextStyle`, and other relevant classes.
   - Consider responsiveness and platform differences.

4. **USAGE INSTRUCTIONS:**
   - **Integration:** Steps to integrate the Flutter widget or component into a Flutter application.
   - **Example Usage:** Provide an example usage scenario if applicable.
   - **Customization:** Tips for modifying the widget or component for different use cases.

5. **RESOURCES:**
   - Include references to any sources or relevant resources for further reading.
     - Format each reference as `[Source](link)`.

"""
}
,
"React Native": {
    "prompt_template": """Generate a React Native component for the following feature: {input_query}.
### Explanation of Each Section:

1. **FEATURE DESCRIPTION:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Purpose:** State the main purpose or functionality of the feature.
   - **Design Requirements:** Describe any specific design requirements or goals.

2. **REACT NATIVE COMPONENT:**
   - Provide the JavaScript (or TypeScript) code for the React Native component required for implementing the feature.
   - Use React Native components, styles, and any necessary libraries.
   - Include placeholders or dynamic content areas if applicable.

3. **STYLING AND THEMING:**
   - Define the styles necessary to achieve the desired visual appearance using `StyleSheet`.
   - Consider responsiveness and platform-specific styling (iOS vs. Android).

4. **USAGE INSTRUCTIONS:**
   - **Integration:** Steps to integrate the React Native component into a React Native application.
   - **Example Usage:** Provide an example usage scenario if applicable.
   - **Customization:** Tips for modifying the component for different use cases.

5. **RESOURCES:**
   - Include references to any sources or relevant resources for further reading.
     - Format each reference as `[Source](link)`.

"""
}
,
"Kotlin": {
    "prompt_template": """Generate Kotlin code for the following feature: {input_query}.
### Explanation of Each Section:

1. **FEATURE DESCRIPTION:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Purpose:** State the main purpose or functionality of the feature.
   - **Design Requirements:** Describe any specific design requirements or goals.

2. **KOTLIN CODE:**
   - Provide the Kotlin code required to implement the feature.
   - Use appropriate Kotlin syntax and libraries.
   - Include placeholders or dynamic content areas if applicable.

3. **STYLING AND THEMING (if applicable):**
   - Define any styling or theming required if the feature involves UI elements.
   - Use Android views and styles where necessary.

4. **USAGE INSTRUCTIONS:**
   - **Integration:** Steps to integrate the Kotlin code into an Android application.
   - **Example Usage:** Provide an example usage scenario if applicable.
   - **Customization:** Tips for modifying the code for different use cases.

5. **RESOURCES:**
   - Include references to any sources or relevant resources for further reading.
     - Format each reference as `[Source](link)`.

"""
}
,
"Swift": {
    "prompt_template": """Generate Swift code for the following feature: {input_query}.
### Explanation of Each Section:

1. **FEATURE DESCRIPTION:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Purpose:** State the main purpose or functionality of the feature.
   - **Design Requirements:** Describe any specific design requirements or goals.

2. **SWIFT CODE:**
   - Provide the Swift code required to implement the feature.
   - Use appropriate Swift syntax and frameworks.
   - Include placeholders or dynamic content areas if applicable.

3. **STYLING AND THEMING (if applicable):**
   - Define any styling or theming required if the feature involves UI elements.
   - Use SwiftUI or UIKit components as needed.

4. **USAGE INSTRUCTIONS:**
   - **Integration:** Steps to integrate the Swift code into an iOS application.
   - **Example Usage:** Provide an example usage scenario if applicable.
   - **Customization:** Tips for modifying the code for different use cases.

5. **RESOURCES:**
   - Include references to any sources or relevant resources for further reading.
     - Format each reference as `[Source](link)`.

"""
}
,
"Xamarin": {
    "prompt_template": """Generate a Xamarin component or code snippet for the following feature: {input_query}.
### Explanation of Each Section:

1. **FEATURE DESCRIPTION:** 
   - **Rephrase user query:** Restate the user's query to confirm understanding.
   - **Purpose:** State the main purpose or functionality of the feature.
   - **Design Requirements:** Describe any specific design requirements or goals.

2. **XAMARIN CODE:**
   - Provide the C# code required to implement the feature using Xamarin.
   - Include Xamarin.Forms or platform-specific components as needed.
   - Include placeholders or dynamic content areas if applicable.

3. **STYLING AND THEMING (if applicable):**
   - Define any styling or theming required if the feature involves UI elements.
   - Use Xamarin.Forms styles or platform-specific styles where necessary.

4. **USAGE INSTRUCTIONS:**
   - **Integration:** Steps to integrate the Xamarin component or code into a Xamarin application.
   - **Example Usage:** Provide an example usage scenario if applicable.
   - **Customization:** Tips for modifying the code for different use cases.

5. **RESOURCES:**
   - Include references to any sources or relevant resources for further reading.
     - Format each reference as `[Source](link)`.

"""
}

}


st.title('Auto Code Generation')

st.session_state.input_query = st.text_area("Please enter your query below. ", key="query_input")

category = st.radio("Select Category", ["Code Generation","Code Generation Mobile","CMS"])

if category == "Code Generation":
   input_query = st.session_state.input_query + "Generate code for this query"
# If "Code Generation" selected, show platform options for React and ASP.NET MVC
   selected_platform = st.selectbox("Select Platform", ["React", "Html and CSS","ASP.NET MVC","Sitecore","C#","Java","Js","Next.Js","Python","SQL","AEM"])
elif category == "Code Generation Mobile":
   input_query = st.session_state.input_query + "Generate code for this query"
# If "Code Generation" selected, show platform options for React and ASP.NET MVC
   selected_platform = st.selectbox("Select Platform", ["Flutter","React Native","Kotlin","Swift","Xamarin"])
else:
# If "Normal" selected, show other platform options like Sitecore, XMCloud, Contentstack
   selected_platform = st.selectbox("Select Platform", ["Sitecore", "XMCLOUD", "Contentstack","AEM"])




if st.button("Generate response"):
   with st.spinner("Generating ..."):
      if input_query and selected_platform:
         platform_text = platform_templates[selected_platform]["prompt_template"].format(input_query=input_query)
         response = model.generate_content(platform_text)
         if response.candidates[0].content.parts[0] is not None:
            st.markdown(response.candidates[0].content.parts[0].text, unsafe_allow_html=True)
      else:
         st.error("Kindly specify your query and choose a platform.")