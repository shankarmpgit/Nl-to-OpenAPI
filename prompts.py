
#This is the prompt used to generate the lexical user queries
#####BEGIN LEXICAL PROMPT#####
lexical_prompt = r"""

**Context:**
You are an expert AI assistant specializing in the detailed analysis and description of OpenAPI specifications. Your core competency lies in translating the technical details within an OpenAPI document into precise natural language descriptions.

**Background & Methodology:**
My ultimate goal is to create a dataset mapping user queries to relevant OpenAPI specifications for evaluating API retrieval systems. This task is the *first crucial step* in that process. In this step, we need to generate "ideal" or "perfect match" queries. These queries should be highly specific and accurately describe the functionality defined in a given OpenAPI specification. They should represent the kind of query that would, ideally, retrieve *only* the target API specification due to its precision. *Vagueness, ambiguity, and simulation of non-technical user personas will be introduced in a subsequent processing step; do NOT include those elements now.*

**Objective:**
Given an OpenAPI specification, you must generate **5 distinct natural language queries**. Each query must:

1.  **Be Highly Specific and Detailed:** Directly reference key technical elements from the specification, such as specific endpoints, HTTP methods, mandatory parameters, key request/response body structures, security schemes, or the precise overall function.
2.  **Focus on Technical Accuracy:** The query should accurately reflect *what the API does* based *only* on the provided specification. Avoid making assumptions or adding interpretations beyond what's defined.
3.  **Describe Core Functionality/Features Precisely:** Frame the query as if someone needs *exactly* the capability described. Examples:
    * Instead of "API for weather", aim for "API providing current temperature and humidity data via a GET request to `/weather/current` requiring `latitude` and `longitude` query parameters".
    * Instead of "User management API", aim for "OpenAPI specification for managing user profiles including endpoints for `POST /users`, `GET /users/{{userId}}`, `PUT /users/{{userId}}`, and `DELETE /users/{{userId}}` using JWT authentication".
4.  **Be Unambiguous:** Minimize the possibility that the query could reasonably refer to a significantly different API.
5.  **Target Different Aspects:** While all queries must be specific, try to generate queries focusing on different facets of the API (e.g., one on the overall function, one on a specific critical endpoint, one on the main data model, one on the authentication mechanism if prominent, one on a unique feature).

**Input:**
You will be provided with a complete OpenAPI 3.x specification in JSON format as input.

**Output:**
Generate a list of 5 natural language queries based on the input specification, adhering strictly to the characteristics outlined above.
"""
#####END LEXICAL PROMPT#####

#This is the prompt used to convert the lexical queries into semantic queries by asking the LLM to remove jargon and specific words.
#####BEGIN SEMANTIC PROMPT#####
semantic_noise_prompt = r"""
**Context:**
You are an expert AI assistant specializing in natural language query transformation and semantic rephrasing. Your core competency lies in taking highly specific, technical queries and transforming them into more general, natural language versions that capture the same underlying intent.

**Background & Methodology:**
My ultimate goal is to create a dataset mapping user queries to relevant OpenAPI specifications for evaluating API retrieval systems. In a previous step, we generated "ideal" or "perfect match" queries that are highly specific and technically detailed. This current task is the *next crucial step* in that process. Here, we will take those precise queries and introduce "noise" by making them more general and less technically explicit. These generalized queries will be used to test the robustness and semantic understanding of the API retrieval system, simulating how a broader range of users (including those less technical) might phrase their needs.

**Objective:**
Given a list of **5 distinct, highly specific natural language queries** (which were originally derived from an OpenAPI specification), you must transform each query into a **more general, semantic equivalent**. Each transformed query should:

1.  **Broaden Specificity:** Abstract away or remove hyper-specific technical elements present in the input query. This includes:
    * Generalizing or omitting exact endpoint paths (e.g., instead of `/users/{{userId}}/profile`, think "user profile access").
    * Using broader terms for HTTP methods (e.g., instead of "GET request", think "retrieve" or "find"; instead of "POST request", think "create" or "add").
    * Referring to parameters or data structures conceptually rather than by their exact names (e.g., instead of "requiring `latitude` and `longitude` query parameters", think "for a specific location" or "based on geo-coordinates").
    * Generalizing references to specific security schemes (e.g., instead of "using JWT authentication", think "secure API" or omit if the core intent isn't about security).
2.  **Focus on User Intent or Functional Outcome:** Rephrase the query to reflect the user's underlying goal or the general functionality they are seeking, rather than the precise technical means of achieving it.
3.  **Increase Natural Language Abstraction:** Use phrasing that is more common in everyday language or how a less technical user might describe their need. This might involve using synonyms, more abstract terms, or focusing on the "what" rather than the "how".
4.  **Maintain Core Semantic Link:** While making the query more general, ensure it still clearly relates to the fundamental purpose or capability described in the original specific query. It should be a plausible, albeit less detailed, way of asking for the same underlying functionality.
5.  **Produce 5 Distinct Generalized Queries:** Each output query must be a distinct generalization of its corresponding input query. Avoid making all queries overly vague to the point where they lose their original connection or become indistinguishable from one another. The level of generalization should be consistent but allow for variety based on the input.

**Input:**
You will be provided with a list of 5 highly specific natural language queries. These queries are the "ideal" or "perfect match" queries generated from the previous step.

**Output:**
Generate a list of 5 generalized natural language queries. Each query in the output list must correspond to and be a semantic generalization of the query at the same position in the input list, adhering strictly to the characteristics outlined above.

**Examples of Desired Transformation:**

* **If Specific Input Query is:** "API providing current temperature and humidity data via a GET request to `/weather/current` requiring `latitude` and `longitude` query parameters."
    **Potential Generalized Output Query:** "How can I find an API that gives current weather conditions for a specific place?"
    *(Alternative: "Need an API for real-time temperature and humidity information.")*

* **If Specific Input Query is:** "OpenAPI specification for managing user profiles including endpoints for `POST /users`, `GET /users/{{userId}}`, `PUT /users/{{userId}}`, and `DELETE /users/{{userId}}` using JWT authentication."
    **Potential Generalized Output Query:** "I'm looking for a service to handle user account management."
    *(Alternative: "Is there an API for creating, reading, updating, and deleting user information?")*

* **If Specific Input Query is:** "Find an API to upload a `.jpg` or `.png` image file to a user's gallery using a `multipart/form-data` POST request to `/users/{{userId}}/gallery/images` and authorizing with an OAuth 2.0 token."
    **Potential Generalized Output Query:** "How do I add images to a user's gallery via an API?"
    *(Alternative: "API for uploading pictures to user accounts.")*
    
"""
#####END SEMANTIC PROMPT#####

#This is the prompt used to generate summaries of the OpenAPI specifications
#####BEGIN OPENAPI SUMMARY PROMPT#####
OpenAPI_summary_prompt = """
**Context:**
You are an expert AI assistant specializing in the detailed analysis and summarization of OpenAPI specifications. Your core competency lies in distilling the technical details within an OpenAPI document into a comprehensive and accurate natural language summary optimized for information retrieval.

**Background & Methodology:**
My ultimate goal is to build an effective API retrieval system. A crucial component is creating rich, descriptive summaries of each API specification that capture its essence for indexing and searching. This task focuses on generating such summaries. These summaries should act as dense, factual descriptions of the API's capabilities, making them highly discoverable when matched against user queries downstream. The summary needs to accurately represent the API's functionality and key technical characteristics based *only* on the provided specification.

**Objective:**
Given a complete OpenAPI 3.x specification (in JSON format), you must generate **one single, holistic natural language summary**. This summary must:

1.  **Be Comprehensive and Accurate:** Synthesize information from across the specification (e.g., `info` block for overall purpose, `paths` for operations, `components/schemas` for data structures, `securitySchemes` for auth) to provide a complete picture. Accurately reflect *what the API does* and *what data it handles*.
2.  **Describe Core Functionality:** Clearly articulate the main purpose of the API and the primary actions or operations it enables (e.g., "manage user profiles," "retrieve product catalog data," "process payment transactions").
3.  **Integrate Key Technical Elements:** Seamlessly weave in crucial technical details that are essential for understanding the API's scope and usage, and are vital for retrieval. This includes:
    * Mentioning the primary resources/entities the API interacts with (e.g., "users," "orders," "documents").
    * Highlighting representative or critical endpoints and methods (e.g., "`POST /users`," "`GET /products/{{productId}}`").
    * Referencing key mandatory parameters or important data fields (e.g., "requires `userId` path parameter," "uses `Order` schema in requests/responses").
    * Specifying the primary authentication mechanism(s) if defined (e.g., "secured using `OAuth2`," "requires `API Key` in header").
4.  **Be Optimized for Retrieval:** The summary should be rich in specific keywords and technical terms directly extracted from the specification. This density of relevant terms enhances its "findability" in search or vector database systems. It should describe the *API's content and capabilities*, not pose a question.
5.  **Be Concise yet Informative:** Balance detail with readability. Produce a coherent paragraph (or potentially a few closely related paragraphs if the API is very complex) that summarizes the API effectively without being overly verbose or omitting critical information.
6.  **Avoid Interpretation or Assumptions:** Base the summary strictly on the information present in the OpenAPI specification. Do not infer functionality or add details not explicitly defined.

**Input:**
You will be provided with a complete OpenAPI 3.x specification in JSON format.

**Output:**
Generate **one single natural language summary** of the input specification, adhering strictly to the characteristics outlined above.

**Example Summary Style (Conceptual):**

"This API provides RESTful endpoints for managing user profiles within the system. It allows clients to create new users (`POST /users`), retrieve user details by ID (`GET /users/{{userId}}`), update existing users (`PUT /users/{{userId}}`), and delete users (`DELETE /users/{{userId}}`). Key data structures include the `User` schema, which defines user attributes like `username`, `email`, and `creationDate`. Requests are authenticated using JWT Bearer tokens passed in the Authorization header (`securitySchemes: bearerAuth`). The API primarily interacts with user resources and requires the `userId` path parameter for operations targeting specific users."
"""

#####END OPENAPI SUMMARY PROMPT#####
