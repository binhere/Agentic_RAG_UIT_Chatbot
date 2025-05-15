This is updated version of "RAG-UIT-QA-Chatbot"
Leveraging Qdrant vector database from "RAG-UIT-QA-Chatbot" project, I turn the old project into Agentic system supporting searching extra information on internet.
However, in some cases, it is difficult to control this multi-agent system's behavior. 
Take a look two demos to see more.

# System architecture

**Filter_Agent -> Retrieve_Agent -> Search_Agent**

Filter_Agent: filters all input queries to avoid wasting resources to retrieve toxic, out-of-domain, abused or English queries. <br>
Retrieve_Agent: use a tool to retrieve the vector database to find out the top k relevant documents. <br>
Search_Agent: use a tool to search for extra information that does not exist in the database.

