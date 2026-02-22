# 𝗜𝗻𝘀𝗶𝗴𝗵𝘁𝗘𝗻𝗴𝗶𝗻𝗲: 𝗦𝘁𝗼𝗰𝗸 𝗦𝗲𝗻𝘁𝗶𝗺𝗲𝗻𝘁 𝘁𝗵𝗮𝘁 𝗔𝗰𝘁𝘂𝗮𝗹𝗹𝘆 𝗪𝗼𝗿𝗸𝘀

𝗠𝗼𝘀𝘁 𝗳𝗶𝗻𝗮𝗻𝗰𝗶𝗮𝗹 𝘁𝗼𝗼𝗹𝘀 𝗮𝗿𝗲 𝘁𝗼𝗼 𝗰𝗼𝗺𝗽𝗹𝗶𝗰𝗮𝘁𝗲𝗱 𝗼𝗿 𝘁𝗼𝗼 𝗲𝘅𝗽𝗲𝗻𝘀𝗶𝘃𝗲. 𝗜 𝗯𝘂𝗶𝗹𝘁 𝗜𝗻𝘀𝗶𝗴𝗵𝘁𝗘𝗻𝗴𝗶𝗻𝗲 𝘁𝗼 𝗰𝘂𝘁 𝘁𝗵𝗿𝗼𝘂𝗴𝗵 𝘁𝗵𝗲 𝗻𝗼𝗶𝘀𝗲 𝗯𝘆 𝘁𝘂𝗿𝗻𝗶𝗻𝗴 𝗿𝗮𝘄 𝘀𝘁𝗼𝗰𝗸 𝗻𝗲𝘄𝘀 𝗶𝗻𝘁𝗼 𝗮 𝗰𝗹𝗲𝗮𝗿 𝘀𝗲𝗻𝘁𝗶𝗺𝗲𝗻𝘁 𝘀𝗰𝗼𝗿𝗲. 𝗜𝘁 𝗵𝗲𝗹𝗽𝘀 𝘆𝗼𝘂 𝘂𝗻𝗱𝗲𝗿𝘀𝘁𝗮𝗻𝗱 𝗶𝗳 𝘁𝗵𝗲 𝗺𝗮𝗿𝗸𝗲𝘁 𝗳𝗲𝗲𝗹𝘀 𝗯𝘂𝗹𝗹𝗶𝘀𝗵 𝗼𝗿 𝗯𝗲𝗮𝗿𝗶𝘀𝗵 𝗮𝗯𝗼𝘂𝘁 𝗮 𝗰𝗼𝗺𝗽𝗮𝗻𝘆 𝗿𝗶𝗴𝗵𝘁 𝗻𝗼𝘄.

## 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝗦𝘁𝗮𝘁𝘂𝘀 The project is fully functional and hosted on GitHub. It currently scrapes live data from Yahoo Finance and stores it in a local database for analysis.

## 𝗧𝗲𝗰𝗵 𝗦𝘁𝗮𝗰𝗸
•	𝗟𝗮𝗻𝗴𝘂𝗮𝗴𝗲: Python
•	𝗕𝗮𝗰𝗸𝗲𝗻𝗱: FastAPI
•	𝗗𝗮𝘁𝗮𝗯𝗮𝘀𝗲: PostgreSQL
•	𝗡𝗟𝗣: VADER (Sentiment Analysis)
•	𝗙𝗿𝗼𝗻𝘁𝗲𝗻𝗱: Streamlit
•	𝗗𝗮𝘁𝗮 𝗩𝗶𝘀𝘂𝗮𝗹𝗶𝘇𝗮𝘁𝗶𝗼𝗻: Plotly

## 𝗛𝗼𝘄 𝗶𝘁 𝗪𝗼𝗿𝗸𝘀 
The system has three main parts. First, the scraper gathers news headlines. Second, the backend runs those headlines through a sentiment model to give them a score between -1 and 1. Third, the frontend displays these scores as interactive charts.
I added some smart features to make it reliable. The engine checks the database first before scraping the web. If the data is less than 15 minutes old, it pulls from the database to save time. I also added random delays to the scraper so it acts more like a human and less like a bot.

## 𝗛𝗼𝘄 𝘁𝗼 𝗥𝘂𝗻 (𝗟𝗼𝗰𝗮𝗹 𝗦𝗲𝘁𝘂𝗽)
1.	Clone the repository to your computer.
2.	Create a .env file and add your DATABASE_URL.
3.	Install the dependencies using the command: uv sync.
4.	Open two terminals.
5.	In terminal one, start the backend: uv run fastapi dev app/main.py.
6.	In terminal two, start the dashboard: uv run streamlit run dashboard/ui.py.
7.	Open your browser to the local address shown in the terminal.

## 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 
If you have questions about the code or the logic behind the sentiment scoring, feel free to reach out.
* [Linkedin](https://linkedin.com/in/qudusoseni82)
* [E-mail](oseniqudus1965@gmail.com)

