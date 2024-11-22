# doc-rag-chatbot
Application that builds local RAG chatbots out of any document


<img width="611" alt="image" src="https://github.com/user-attachments/assets/81e91a1d-e3fa-4fc8-9b4f-cf414f4bc578">



# Steps to Set Up and Run the RAG Chatbot Project

## 1. **Install Dependencies**
- Navigate to the `backend` folder in your terminal.
- Run the following command to install the necessary Python dependencies for the backend:
  ```bash
  pip install -r requirements.txt
  ```

## 2. **Set Up Ollama**
- Download and install **Ollama** from their official website.
- Ensure that Ollama is running on your system before proceeding.

## 3. **Add Data Sources**
- Place the source PDF files you want the chatbot to use under the `data_sources` folder in the `backend`.

## 4. **Update the Database**
- Process the PDFs and update your database with embeddings by running the following command from the `backend` directory:
  ```bash
  python update_db.py
  ```

## 5. **Start the Backend**
- Start the FastAPI backend server by executing:
  ```bash
  python chatbot.py
  ```

## 6. **Set Up Frontend**
- Navigate to the `frontend` folder in your terminal.
- Install the necessary frontend dependencies by running:
  ```bash
  npm install
  ```

## 7. **Run the Frontend**
- Start the React app by running:
  ```bash
  npm start
  ```
- This will launch the frontend in your default browser.

## 8. **Interact with the Chatbot**
- Open your browser and navigate to the URL where your React app is running (usually [http://localhost:3000](http://localhost:3000)).
- Start interacting with the chatbot, which will use the processed data from your PDFs.

---

### Note:
Ensure that both the backend and frontend remain running simultaneously for proper functionality.
