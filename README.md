# The One Where Friends Feels Real: Friends RAG Guide

A Retrieval-Augmented Generation (RAG) assistant that helps users explore *Friends* as a reflection of real adult life, especially themes like friendship as chosen family, relationship dynamics, emotional growth, nostalgia, and humor as a coping mechanism.

This assistant is designed to generate grounded, thoughtful responses by retrieving relevant passages from a curated document collection and synthesizing them into an explanation-oriented answer.

---

## Domain Overview & Problem Statement

**Domain:** The TV show *Friends* (1994–2004), treated as a cultural and emotional reflection of real adult life.

**Problem:** Many tools and discussions about *Friends* tend to be surface-level (e.g., trivia, favorite moments, quotes) or opinion-based without grounding. At the same time, there is a wide range of analysis, academic papers, cultural essays, and commentary, about why the show feels emotionally relevant, but those insights are scattered across different sources.

**Solution:** This RAG assistant makes those insights easier to access in one place by retrieving relevant passages from a curated database and generating responses that connect the show to real-life experiences.

---

## Architecture Overview 
![Architecture Overview](LASTNAME_LPP_Rag/ASSETS/architechture.png)

---

## Document Collection Summary

The knowledge base is intentionally mixed so the assistant can synthesize multiple perspectives.

### Document Types Included
- **PDFs**
  - Deeper analysis of humor, psychology, and communication patterns
- **Articles & Web Pages**
  - Broader commentary on friendship, nostalgia, and why the show still resonates
- **YouTube Transcripts**
  - Captures how people naturally discuss *Friends* and its impact

### Why These Documents?
These sources repeatedly touch on themes central to the agent’s purpose:
- Friendship as lived experience and chosen family
- Clique/group dynamics
- Emotional comfort and nostalgia
- Humor as a coping mechanism
- Generational connection (especially millennials)

---

## Agent Configuration (Persona & Rationale)
![Agent Configuration](LASTNAME_LPP_Rag/ASSETS/configuration.png)

### Role
A reflective guide that helps users explore how *Friends* mirrors real-life experiences.

### Goal
To answer questions using retrieved evidence while explaining themes like friendship, relationships, emotional growth, nostalgia, and humor as coping.

### Backstory
The assistant has access to a curated document collection that analyzes *Friends* from academic, cultural, and opinion-based perspectives, and uses retrieval to ground its explanations in source material.

### Why This Agent?
This persona matches the dataset and improves response quality because it:
- Encourages retrieval from multiple sources
- Supports synthesis and interpretation rather than summarization
- Produces answers that feel thoughtful, grounded, and explainable

---

## Installation & Setup

### 1) Clone the repository
git clone <YOUR_GITHUB_REPO_URL>
cd <YOUR_REPO_FOLDER>

### 2) Install Dependencies
pip install -r requirements.txt

### 3) Ensure Database Is Available 
backend/friends.duckdb

### 4) Run the Streamlit Application
streamlit run app.py

### 5) Enter Your OpenAI API Key 
Once the app is running:
1. Enter OpenAI API key in the sidebar
2. Confirm the database connection
3. Start asking questions about Friends

Link to streamlit deployment: [Friends Assistant]([http://localhost:8501/](https://nlp-eschmid9.streamlit.app/))
