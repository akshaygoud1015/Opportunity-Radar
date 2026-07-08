"""Your durable resume content -- the stuff that doesn't change per job
application. Only the skills section gets reordered/filtered per job; edit
this file directly when your actual experience changes.
"""

PROFILE = {
    "name": "Akshay Merugu",
    "email": "akshaygoud1015@gmail.com",
    "github": "github.com/akshaygoud1015",
    "portfolio": "akshaymerugu.com",
    "education": [
        {
            "school": "University of Alabama at Birmingham",
            "location": "Birmingham, AL",
            "degree": "Master of Science in Computer Science -- GPA: 3.9/4.0",
            "dates": "Aug 2024 -- May 2026",
            "coursework": [
                "Machine Learning", "Advanced Algorithms", "Software Engineering",
                "Data Mining", "Database Systems",
            ],
        },
        {
            "school": "CMR Institute of Technology",
            "location": "India",
            "degree": "Bachelor of Technology in Computer Science -- GPA: 3.3/4.0",
            "dates": "Aug 2020 -- Jun 2024",
            "coursework": [
                "Data Structures & Algorithms", "OOP", "Embedded Systems",
                "Discrete Mathematics", "Linear Algebra", "Probability & Statistics",
            ],
        },
    ],
    "experience": [
        {
            "company": "Suraksha Child Development Center",
            "role": "Full Stack Developer (Freelance)",
            "dates": "January 2024 -- January 2025",
            "bullets": [
                "Architected and deployed a production-ready web platform using Flask, MySQL, HTML/CSS, and JavaScript",
                "Designed secure authentication and role-based access workflows using bcrypt password hashing and session management",
                "Built appointment scheduling and service management modules with automated email notifications and booking confirmations",
                "Implemented relational database schemas, CRUD operations, and backend APIs to support core application workflows",
                "Managed end-to-end deployment, maintenance, and performance optimization on PythonAnywhere for production reliability",
                "Partnered directly with stakeholders to gather requirements and translate business needs into shipped features",
            ],
        },
        {
            "company": "TutorialPoint Tutoring",
            "role": "Tutor",
            "dates": "January 2023 -- January 2024",
            "bullets": [
                "Tutored students in programming, mathematics, and engineering fundamentals",
            ],
        },
    ],
    "projects": [
        {
            "name": "DocTalk -- RAG-Based Document Q&A System",
            "stack": "Python, Streamlit, ChromaDB, Gemini API, Ollama, LLaMA 3.2",
            "date": "January 2026",
            "bullets": [
                "Designed and implemented a retrieval-augmented generation (RAG) system for conversational Q&A over PDF documents",
                "Built document ingestion and chunking pipelines with semantic vector indexing using ChromaDB and Gemini embeddings",
                "Integrated Ollama-hosted LLaMA 3.2 models for fully local, privacy-preserving inference",
                "Optimized retrieval accuracy through semantic search and context-aware prompt engineering",
            ],
        },
        {
            "name": "Attention-Driven Crypto Volatility Dashboard",
            "stack": "Python, Streamlit, Scikit-learn, Pandas, Docker, APIs",
            "date": "March 2026",
            "bullets": [
                "Developed an end-to-end ML dashboard forecasting cryptocurrency volatility using market and attention-based signals",
                "Engineered predictive features from Yahoo Finance and Wikipedia Pageviews API data",
                "Containerized the application with Docker and deployed an interactive Streamlit interface for real-time analytics",
            ],
        },
    ],
}
