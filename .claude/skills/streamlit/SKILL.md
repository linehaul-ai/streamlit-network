---
name: streamlit
description: When working with Streamlit web apps, data dashboards, ML/AI app UIs, interactive Python visualizations, or building data science applications with Python
---

# Streamlit Skill

Comprehensive assistance with Streamlit development, generated from official documentation covering 317 pages of content including API reference, tutorials, deployment guides, and best practices.

## When to Use This Skill

This skill should be triggered when:
- **Building web apps** with Python for data science, ML/AI, or analytics
- **Creating dashboards** with interactive visualizations and real-time data
- **Developing data apps** that need rapid prototyping and deployment
- **Implementing widgets** like buttons, sliders, file uploaders, or chat interfaces
- **Working with charts** using built-in charting or custom visualizations
- **Deploying apps** to Streamlit Community Cloud or other platforms
- **Testing Streamlit apps** with the app testing framework
- **Configuring Streamlit** apps with themes, secrets, or custom settings
- **Building multi-page apps** with navigation and routing
- **Integrating authentication** with OpenID Connect providers

## Key Concepts

### Core Architecture
**Script-based execution**: Streamlit apps run as Python scripts that rerun from top to bottom on every user interaction. This makes development simple but requires understanding state management.

**Session State**: Persistent data storage across reruns using `st.session_state`. Essential for maintaining user data, form inputs, and application state.

**Caching**: Use `@st.cache_data` for data operations and `@st.cache_resource` for expensive resources like ML models or database connections.

### App Structure
**Magic commands**: Write variables or strings standalone to display them automatically (when `magicEnabled` is True).

**Widget callbacks**: Functions that run when widget values change, useful for complex interactions and state updates.

**Fragments**: Isolated portions of your app that can rerun independently with `@st.fragment`, improving performance for partial updates.

## Quick Reference

### Example 1: Hello World & Basic Display

```python
import streamlit as st

# Simple text display
st.title("My First Streamlit App")
st.header("Welcome to Data Science")
st.write("Hello, World!")

# Magic command (displays automatically)
"This is magic!"

# Display data
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
st.dataframe(df)
```

### Example 2: Interactive Widgets & Session State

```python
import streamlit as st

# Initialize session state
if 'count' not in st.session_state:
    st.session_state.count = 0

# Button with callback
def increment():
    st.session_state.count += 1

st.button('Increment', on_click=increment)
st.write(f'Count: {st.session_state.count}')

# Various input widgets
name = st.text_input("Enter your name")
age = st.slider("Select age", 0, 100, 25)
option = st.selectbox("Choose option", ['A', 'B', 'C'])
uploaded_file = st.file_uploader("Upload CSV")
```

### Example 3: Charts & Visualizations

```python
import streamlit as st
import pandas as pd
import numpy as np

# Sample data
data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30),
    'values': np.random.randn(30).cumsum()
})

# Built-in charts
st.line_chart(data.set_index('date'))
st.area_chart(data.set_index('date'))
st.bar_chart(data.set_index('date'))

# Map visualization
map_data = pd.DataFrame({
    'lat': [37.76, 37.77, 37.78],
    'lon': [-122.4, -122.41, -122.42]
})
st.map(map_data)
```

### Example 4: Layouts & Containers

```python
import streamlit as st

# Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.header("Column 1")
    st.write("Content here")
with col2:
    st.header("Column 2")
    st.button("Click me")
with col3:
    st.header("Column 3")
    st.checkbox("Check me")

# Sidebar
with st.sidebar:
    st.header("Sidebar")
    filter_val = st.slider("Filter", 0, 100)

# Tabs
tab1, tab2 = st.tabs(["Data", "Charts"])
with tab1:
    st.write("Your data here")
with tab2:
    st.line_chart([1, 2, 3, 4, 5])

# Expander
with st.expander("Click to expand"):
    st.write("Hidden content revealed!")
```

### Example 5: Forms & User Input

```python
import streamlit as st

# Form prevents rerun on every input change
with st.form("my_form"):
    st.write("User Registration")
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, max_value=120)

    # Form submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success(f"Welcome {name}!")
        st.session_state.user_data = {
            'name': name,
            'email': email,
            'age': age
        }
```

### Example 6: Caching for Performance

```python
import streamlit as st
import pandas as pd
import time

# Cache data loading (recomputes when inputs change)
@st.cache_data
def load_data(file_path):
    time.sleep(2)  # Simulate expensive operation
    return pd.read_csv(file_path)

# Cache ML models/resources (persists across reruns)
@st.cache_resource
def load_model():
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    # Load trained model...
    return model

# Use cached functions
data = load_data("data.csv")
model = load_model()
st.write(data)
```

### Example 7: Chat Interface (LLM Apps)

```python
import streamlit as st

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display assistant response
    response = f"Echo: {prompt}"  # Replace with actual LLM call
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
```

### Example 8: App Testing with pytest

```python
# app.py
import streamlit as st

st.session_state.beans = st.session_state.get("beans", 0)
st.title("Bean counter")
addend = st.number_input("Beans to add", 0, 10)
if st.button("Add"):
    st.session_state.beans += addend
st.markdown(f"Beans counted: {st.session_state.beans}")

# tests/test_app.py
from streamlit.testing.v1 import AppTest

def test_increment_and_add():
    """Test that incrementing and adding works"""
    at = AppTest.from_file("app.py").run()
    at.number_input[0].increment().run()
    at.button[0].click().run()
    assert at.markdown[0].value == "Beans counted: 1"
```

### Example 9: User Authentication (OpenID Connect)

```python
import streamlit as st

# Check authentication status
if not st.user.is_logged_in:
    if st.button("Log in"):
        st.login()
else:
    st.write(f"Hello, {st.user.name}!")
    st.write(f"Email: {st.user.email}")

    if st.button("Log out"):
        st.logout()

# Configuration in .streamlit/secrets.toml:
# [auth]
# redirect_uri = "http://localhost:8501/oauth2callback"
# cookie_secret = "your-secret-key"
# client_id = "your-client-id"
# client_secret = "your-client-secret"
# server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

### Example 10: Configuration & Theming

```toml
# .streamlit/config.toml

[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans-serif"

[server]
port = 8501
enableCORS = false
maxUploadSize = 200

[client]
showErrorDetails = true
toolbarMode = "auto"
```

## Reference Files

This skill includes comprehensive documentation organized into focused categories:

### **api.md** (439KB, 187 pages)
Complete API reference covering all Streamlit commands:
- **Display elements**: `st.write`, `st.markdown`, `st.title`, `st.header`, `st.text`, `st.code`, `st.latex`
- **Data display**: `st.dataframe`, `st.table`, `st.metric`, `st.json`, `st.data_editor`
- **Charts**: `st.line_chart`, `st.area_chart`, `st.bar_chart`, `st.map`, `st.plotly_chart`, `st.altair_chart`
- **Input widgets**: `st.button`, `st.checkbox`, `st.radio`, `st.selectbox`, `st.slider`, `st.text_input`, `st.file_uploader`
- **Media**: `st.image`, `st.audio`, `st.video`, `st.camera_input`
- **Layouts**: `st.columns`, `st.tabs`, `st.expander`, `st.container`, `st.sidebar`
- **Chat elements**: `st.chat_message`, `st.chat_input`
- **Status elements**: `st.progress`, `st.spinner`, `st.success`, `st.error`, `st.warning`
- **Control flow**: `st.stop`, `st.rerun`, `st.form`, `st.dialog`, `@st.fragment`
- **State**: `st.session_state`, `st.query_params`
- **Caching**: `@st.cache_data`, `@st.cache_resource`
- **Connections**: `st.connection`, database integrations
- **User auth**: `st.login`, `st.logout`, `st.user`
- **Configuration**: `st.set_page_config`, `config.toml` options

### **tutorials.md** (111KB, 57 pages)
Step-by-step guides and practical examples:
- **Getting started tutorials**: Creating your first app, multi-page apps
- **LLM/Chat apps**: Building conversational interfaces, chat response feedback
- **Database connections**: AWS S3, BigQuery, MongoDB, PostgreSQL, Snowflake, TigerGraph
- **Data handling**: Dataframe row selections, working with large datasets
- **Execution flow**: Fragments, forms, multipage navigation
- **Authentication**: Google, Microsoft OAuth integration
- **Configuration**: Theming, fonts, static file serving

### **concepts.md** (103KB, 42 pages)
Deep dives into Streamlit architecture and advanced concepts:
- **Architecture**: How Streamlit runs, script execution model, app lifecycle
- **Caching**: `@st.cache_data` vs `@st.cache_resource`, cache invalidation
- **Session State**: Managing state across reruns, widget semantics
- **Multi-page apps**: Pages directory structure, navigation, dynamic routing
- **Fragments**: Partial reruns for performance optimization
- **Forms**: Batching user input to prevent excessive reruns
- **App testing**: AppTest framework, simulating user interactions
- **Custom components**: Creating reusable UI components
- **Configuration**: Environment variables, config.toml structure
- **Design patterns**: Threading, custom classes, timezone handling

### **deployment.md** (77KB, 22 pages)
Comprehensive deployment and hosting guidance:
- **Streamlit Community Cloud**: GitHub integration, workspace management, app settings
- **Deployment from templates**: Quick start guides
- **App dependencies**: requirements.txt, packages.txt, managing secrets
- **Secrets management**: secrets.toml, environment variables
- **Docker deployment**: Containerization best practices
- **Kubernetes**: Scaling and orchestration
- **Snowflake**: Deploying Streamlit in Snowflake
- **App analytics**: Monitoring usage and performance
- **SEO & indexability**: Optimizing for search engines
- **Status & troubleshooting**: Common deployment issues

### **getting_started.md** (65KB, 26 pages)
Beginner-friendly introduction to Streamlit:
- **Installation**: Command line, Anaconda, Streamlit Playground
- **Main concepts**: Script execution, data flow, widgets
- **Advanced concepts**: Session state, caching, performance
- **Summary & next steps**: Roadmap for learning

### **knowledge_base.md** (21KB, 48 pages)
Common questions, troubleshooting, and solutions:
- **Using Streamlit**: Widget behavior, file uploads, downloading data, serialization
- **Dependencies**: Module installation, package management, common errors
- **Deployment issues**: Authentication, resource limits, remote start, WSGI protocol
- **Best practices**: Sanity checks, supported browsers, camera access

### **other.md** (2.2KB)
Miscellaneous topics and utilities not fitting other categories

## Working with This Skill

### For Beginners
1. **Start here**: Read `getting_started.md` for foundational concepts
2. **First app**: Follow the "Hello World" example in Quick Reference #1
3. **Learn widgets**: Review Quick Reference #2 for interactive elements
4. **Understand state**: Study Session State in Quick Reference #2 and concepts.md

### For Intermediate Users
1. **Performance**: Master caching (Quick Reference #6, concepts.md)
2. **Layouts**: Build complex UIs with columns, tabs, sidebars (Quick Reference #4)
3. **Charts**: Create visualizations (Quick Reference #3, api.md)
4. **Multi-page apps**: Structure larger applications (concepts.md, tutorials.md)
5. **Testing**: Write tests for your apps (Quick Reference #8, concepts.md)

### For Advanced Users
1. **Fragments**: Optimize with partial reruns (concepts.md)
2. **Custom components**: Extend Streamlit's capabilities (concepts.md)
3. **Authentication**: Implement user login (Quick Reference #9, tutorials.md)
4. **Deployment**: Scale to production (deployment.md)
5. **Database integration**: Connect to data sources (tutorials.md, api.md)

### Navigation Tips
- **Need a specific widget?** Search api.md for `st.<widget_name>`
- **Error troubleshooting?** Check knowledge_base.md first
- **Deployment issues?** Consult deployment.md
- **Understanding how Streamlit works?** Read concepts.md architecture section
- **Building something specific?** Check tutorials.md for similar examples

## Best Practices

### Performance
- Use `@st.cache_data` for data loading and transformations
- Use `@st.cache_resource` for ML models and database connections
- Implement `@st.fragment` for partial updates in large apps
- Minimize work in the main script body; push to cached functions

### State Management
- Initialize session state at the top of your script
- Use widget `key` parameter to sync with session state
- Avoid putting non-serializable objects in session state

### UI/UX
- Use `st.form` to batch related inputs and reduce reruns
- Provide clear labels and help text for widgets
- Use status indicators (`st.progress`, `st.spinner`) for long operations
- Structure layouts with columns and containers for responsive design

### Development
- Test your apps with the AppTest framework
- Use `.streamlit/config.toml` for local configuration
- Keep secrets in `.streamlit/secrets.toml` (never commit to git)
- Enable `runOnSave` in config for auto-reload during development

## Common Patterns

### Data App Template
```python
import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="My Data App", layout="wide")

# Load data (cached)
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    category = st.selectbox("Category", options=['All', 'A', 'B', 'C'])

# Main content
st.title("My Data App")
data = load_data()

# Apply filters
if category != 'All':
    data = data[data['category'] == category]

# Display
col1, col2 = st.columns(2)
with col1:
    st.dataframe(data)
with col2:
    st.line_chart(data.set_index('date'))
```

### LLM Chat App Template
See Quick Reference #7 for complete chat interface implementation.

## Resources

- **Official Docs**: https://docs.streamlit.io
- **Community Forum**: https://discuss.streamlit.io
- **GitHub**: https://github.com/streamlit/streamlit
- **Gallery**: https://streamlit.io/gallery
- **Cheat Sheet**: https://docs.streamlit.io/develop/quick-reference/cheat-sheet

## Notes

- This skill was automatically generated from 317 pages of official Streamlit documentation
- All code examples are extracted from official docs and tested patterns
- Reference files preserve structure and links to source documentation
- Last updated: Based on Streamlit documentation as of October 2025
