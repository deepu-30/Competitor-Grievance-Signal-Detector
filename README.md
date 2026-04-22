
# STEPS TAKEN TO CREATE PROJECT #

Step 1 — Prerequisites
First, make sure you have Python installed. Open your terminal/command prompt and check:
      $python --version
  You need Python 3.8+. If not installed, download from python.org.

Step 2 — Create the Project Folder & Directory Structure

Run these commands to create the folders and dirctory

          mkdir signal_detector
          cd signal_detector
          mkdir signals fetchers utils data outputs
          type nul > main.py
          type nul > config.py
          type nul > signals\competitor_grievance.py
          type nul > fetchers\reddit_fetcher.py
          type nul > fetchers\rss_fetcher.py
          type nul > fetchers\serp_fetcher.py
          type nul > utils\sentiment.py
          type nul > utils\scorer.py
          type nul > utils\output.py
          type nul > data\sample_input.json
          type nul > README.md
  
  For init files
        type nul > fetchers\__init__.py
        type nul > signals\__init__.py
        type nul > utils\__init__.py

Step 3: open in VS code at the signal detector folder and also open cmd.
    Folder should now look like this:
        
        signal_detector/
        
          ├── main.py
          ├── config.py
          ├── README.md
          ├── signals/
          │   ├── __init__.py
          │   └── competitor_grievance.py
          ├── fetchers/
          │   ├── __init__.py
          │   ├── reddit_fetcher.py
          │   ├── rss_fetcher.py
          │   └── serp_fetcher.py
          ├── utils/
          │   ├── __init__.py
          │   ├── sentiment.py
          │   ├── scorer.py
          │   └── output.py
          ├── data/
          │   └── sample_input.json
          └── outputs/        ← (stays empty, auto-filled when you run)

Step 4 — Create a Virtual Environment & Install Libraries
        In your terminal (inside signal_detector/ folder):
          
          # Create virtual environment
              $ python -m venv venv
          # Activate it
          # Windows:
              $ venv\Scripts\activate
          # Install required libraries
              $ pip install requests beautifulsoup4 feedparser
              

Step 5 — Now add code in each file.

        1. config.py  // Create the array of which negative keywords, pain points & competetiors
        
        2. fetchers/
            reddit_fetcher.py  // here fetch the post from reddit 
            rss_fetcher.py //fetch data from rss posts, articles
            serp_fetcher.py //fetch data from duckduck go
        Note: All 3 fetchers don't know anything about competitors or keywords. They just receive a competitor name, fetch raw text, and return it. They don't do any analysis — that's not their job.
        
        3. utils/
        
            sentiment.py // in this call the negaitivekeyword and painpoint defined in config file and reteurn the matching results.
            score.py //in this matching keyword score from 0 to 100 
                                  Score = Source credibility pts     (Reddit = 30, RSS = 25, DDG = 20)
                                  + Number of matched keywords    (10 pts each, max 40)
                                  + Number of pain categories hit (10 pts each, max 30)
                                  ─────────────────────────────────────────────────
                                      Total capped at 100
            output.py // save the output in outputs folder in json, sqlite or both formats
            
        4. signals/
            competitor_grievance.py //call the files to fet the data and where is the source from 
                      Step 1 → Loop through each competitor from config.py
                      Step 2 → Call all 3 fetchers to collect raw posts
                      Step 3 → For each post, call sentiment.py to find keywords & pain points
                      Step 4 → Call scorer.py to calculate the score
                      Step 5 → Package everything into a structured signal dictionary
                      Step 6 → Return all signals to main.py
            main.py // this is main file which is run an it callcompetitor_grevance  and save the output in outputs folder.                       

Step 6 - Run the project

        # Basic run — outputs JSON
            python main.py

        # Output both JSON and SQLite
            python main.py --output both

        # Output only SQLite
            python main.py --output sqlite

### Final Checklist ###

    ☐ Virtual environment activated
    ☐ All 3 pip packages installed
    ☐ All files created and code pasted
    ☐ Running from inside signal_detector/ folder
    ☐ python main.py runs without errors
    ☐ outputs/signals.json is generated

### The Big Picture For This Task ###

      config.py          → defines all data (competitors, keywords, pain points)
           ↓
      fetchers/          → collect raw posts from internet (no analysis)
           ↓
      utils/sentiment.py → analyze the raw text (find keywords & pain points)
      utils/scorer.py    → give a score to each signal
           ↓
      signals/competitor_grievance.py → orchestrates ALL of the above steps
           ↓
      utils/output.py    → save final results
           ↑
      main.py            → starts everything, calls grievance detector & output

### Sample Output ###

<img width="1917" height="1079" alt="image" src="https://github.com/user-attachments/assets/60577bcb-a66b-4998-aef7-1b7a511ab07d" />


## Serverless Implementation ##

Normal Python app:     python main.py  (runs everything together)

Serverless style:      Each function is isolated & invoked independently
                       handler.py → function1, function2, function3...
                       serverless.yml → defines all functions & config

### Create these new files ###

signal_detector/

├── serverless.yml              ← NEW: defines all functions

├── handler.py                  ← NEW: lambda function entry points

├── requirements.txt            ← NEW: python dependencies

├── package.json 

### Install the serverless framework ###

`serverless --version`
`npm install -g serverless`

For error No version found for 3 then run:
 `npm install serverless@^3 --save-dev
 npx serverless offline`

### Output ###

Run server on one cmd:

`npx serverless offline`


And, on another cmd:

`curl -X POST http://localhost:4000/detect -H "Content-Type: application/json" -d "{\"output\":\"json\"}"`


Sample output: 

<img width="1919" height="929" alt="image" src="https://github.com/user-attachments/assets/ba5d54c3-a007-4f10-b4b0-6dce658ac646" />

<img width="1917" height="1059" alt="image" src="https://github.com/user-attachments/assets/7fa6c641-96ea-4ed8-8bf4-5c117ce8cdc9" />





