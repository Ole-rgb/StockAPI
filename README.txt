# StockAPI

StockAPI is a simple API that exposes a stock manager. This API allows users to download stock data and cache the CSV files for efficient access.

## Features

- **Download Stock Data**: Retrieve historical stock data for a specified ticker and date range.
- **Cache Management**: Automatically cache downloaded stock data in CSV files for efficient access.
- **Update Stock Data**: Update existing stock data to the latest available data.
- **Retrieve Stock Data**: Fetch stock data for a specific date or date range.
- **JSON Conversion**: Convert stock data to JSON format for easy integration with other systems.
- **Data Validation**: Ensure the validity of ticker symbols and date formats.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/StockAPI.git
    ```
2. Navigate to the project directory:
    ```
    cd StockAPI
    ```
3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Start the API server:
    ```
    uvicorn main:app --reload
    ```
2. Use the API endpoints to interact with the stocklist

### GET /

- **Description**: Welcome message for the Stock API.
- **Response**: 
    - `200 OK`: Returns a welcome message.

### GET /stocks/{ticker}

- **Description**: Retrieve stock data for a given ticker.
- **Parameters**:
    - `ticker` (str): The stock ticker symbol.
- **Response**:
    - `200 OK`: Returns the stock data in JSON format.
    - `404 Not Found`: If the stock ticker is not found.

### PUT /stocks/{ticker}

- **Description**: Update stock data for a given ticker.
- **Parameters**:
    - `ticker` (str): The stock ticker symbol.
- **Response**:
    - `200 OK`: Returns the updated stock data in JSON format.
    - `400 Bad Request`: If there is an error updating the stock data.

### POST /stocks/

- **Description**: Add new stock data.
- **Request Body**:
    - `ticker` (str): The stock ticker symbol.
    - `start_date` (date): The start date in YYYY-MM-DD format.
    - `end_date` (date): The end date in YYYY-MM-DD format.
- **Response**:
    - `200 OK`: Returns the added stock data in JSON format.
    - `400 Bad Request`: If there is an error adding the stock data.

### DELETE /stocks/{ticker}

- **Description**: Delete stock data for a given ticker.
- **Parameters**:
    - `ticker` (str): The stock ticker symbol.
- **Response**:
    - `200 OK`: Returns a message confirming the deletion.
    - `400 Bad Request`: If there is an error deleting the stock data.


    ## TODOs and Bugs

    ### TODOs

    1. **Improve Data Validation**:
        - Enhance the validation logic for stock data to ensure the integrity and accuracy of the data.
        - Implement additional checks for the date format and range.

    2. **Optimize Data Storage**:
        - Explore more efficient ways to store and retrieve stock data, potentially using a database instead of CSV files.
        - Implement data compression techniques to reduce storage space.

    3. **Enhance Error Handling**:
        - Improve error handling mechanisms to provide more informative error messages and handle edge cases gracefully.
        - Implement logging to track errors and system behavior.

    4. **Expand API Functionality**:
        - Add more endpoints to support additional operations, such as retrieving stock data for multiple tickers at once.
        - Implement authentication and authorization mechanisms to secure the API.

    5. **Unit Testing**:
        - Write comprehensive unit tests to ensure the reliability and correctness of the code.
        - Set up continuous integration to automatically run tests on code changes.

    ### Bugs

    1. **Date Validation Issue**:
        - The `__valid_date` method currently sets the end date instead of the start date in the `__set_start_date` method. This needs to be corrected to properly validate and set the start date.

    2. **Column Parsing in CSV**:
        - The current implementation uses a hack to set the column names when reading the CSV file. This needs to be improved to dynamically read and set the correct column names from the CSV file.

    3. **File Renaming Issue**:
        - The `__update_filename_end_date` method renames the file without checking if the new filename already exists. This can lead to file conflicts and data loss.

    4. **Incomplete Data Handling**:
        - The `update` method does not handle cases where the new data download is incomplete or fails. This can result in corrupted or partial data being saved.

    5. **Metadata Row Handling**:
        - The addition of a metadata row in the `update` method is a temporary solution. A more robust approach is needed to handle metadata without affecting the stock data.

## License

This project is licensed under the MIT License.