from flask import Flask
import python_scraper as scraper

app = Flask(__name__)

@app.route('/scraping-init')
def scrape_loop():
    msg = scraper.run()
    return msg

if __name__ == '__main__':
    app.run(debug=True)