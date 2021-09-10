Feature: Scraping

    Scenario: Single run against all providers
        Given we have a test configuration with sqlite store and Telegram notifications
        When we scrape all configured providers
        Then we will receive one Telegram notification per property