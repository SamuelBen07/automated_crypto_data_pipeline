**Automated Cryptocurrency Data Pipeline**

Overview:
This project implements an automated data pipeline designed to extract real-time cryptocurrency market data and load it into a SQLite data warehouse. The primary goal is to provide analysts with readily available, up-to-date cryptocurrency information without manual intervention, facilitating easier analysis of market trends and potential buying opportunities at lower costs. The pipeline fetches data from the CoinGecko API, performs basic transformations, and stores it in a structured format for efficient querying.

Key Features
Real-time Data Ingestion: Fetches the latest cryptocurrency market data from the CoinGecko API.

Broad Cryptocurrency Coverage: Captures price information for a wide range of cryptocurrencies available on the CoinGecko API at the time of execution.

Data Transformation: Converts the raw API response into a structured JSON format for better readability and processing.

Automated Operation: Utilizes the schedule library to run the data pipeline automatically every hour.

Data Persistence: Stores the extracted and transformed data in a local SQLite database, creating a structured data warehouse.

Key Market Metrics: Extracts and stores essential cryptocurrency data points including ID, symbol, name, current price, market capitalization, and total volume.

Structured Data for Analysis: Provides a well-structured data source that enhances the scope for data analysts to perform in-depth analysis.

Architecture Diagram :
https://drive.google.com/file/d/14B__2bFGiwO4ElTGRLRtP6VVoL0tYeRy/view?usp=sharing

Installation
Clone the repository:
git clone https://github.com/SamuelBen07/automated_crypto_data_pipeline.git
Navigate to the project directory:
cd automated_crypto_data_pipeline
Install required dependencies:
pip install -r requirements.txt

Configuration
API Key: This project utilizes the CoinGecko public API, which does not require an API key for the specific endpoint used (/coins/markets). However, if you intend to use other CoinGecko API endpoints that require a key in the future, you should handle it securely using environment variables or a dedicated configuration file (not committed to the repository).
Database Configuration: The project uses a local SQLite database named crypto_data.db (or a name you define in your code). The database file will be created automatically if it doesn't exist. You can modify the database file name in your code if needed.

Usage
Run the main script:
python pipeline.py
Ensure that you are project's root directory while running.
Once the script is running, the data pipeline will automatically execute every hour as per the schedule defined using the schedule library.
The extracted and transformed cryptocurrency data will be stored in the crypto_data.db SQLite database. Analysts can then connect to this database using SQL tools or Python libraries like sqlite3 or pandas to query and analyze the data.

Technologies Used
Python
logging: For logging application events.

os: For interacting with the operating system.

requests: For making HTTP requests to the CoinGecko API.

json: For working with JSON data.

datetime: For handling date and time information.

sqlalchemy: For interacting with the SQLite database in an ORM-like fashion.

sqlalchemy.create_engine: To create the database engine.

sqlalchemy.text: To write and execute raw SQL queries (if needed).

pandas: For data manipulation and analysis (can be used to interact with the SQLite database).

schedule: For scheduling the data pipeline to run automatically.

time: For time-related functionalities.

sqlalchemy.types: Specifically using String, BigInteger, DECIMAL, and DateTime for defining database schema.

Challenges and Solutions
"Initially, handling potential API rate limits was a concern. The current implementation includes basic error handling and a 1-hour schedule which helps to stay within the free tier limits of the CoinGecko API."

"During the data loading phase, initial attempts were made using MySQL. However, challenges related to database setup, including authentication and server-side configuration, were encountered. To streamline the project and ensure feasibility, the data warehouse was subsequently switched to SQLite, which offers a simpler setup and is suitable for the project's current scope."

Improvements thought of :
Implementing more robust error handling and logging.
Adding support for configuring the schedule through environment variables or a configuration file.
Allowing users to specify the cryptocurrencies they are interested in.
Integrating data visualization capabilities.
Exploring other data storage options or data warehouses.
Contributing
"Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes. Please ensure your code adheres to the project's coding style and includes relevant tests."
License
This project is licensed under the MIT License.
Contact:
jacinthsj7@gmail.com
