# Running locally

## Install Python libraries and extra dependencies

This was tested with Python 3.10.

To install dependencies:

`pip3 install -r requirements.txt`

In Linux, this might fail if you don't have some libraries. Install them like this in Debian-like distros:

`sudo apt-get install libxml2-dev libxmlsec1-dev libffi-dev`

If you're still getting errors, I recommend running via Docker, because all dependencies are handled automatically. However, if you still want to run the app locally, please file a Github isue and I will look into it.

## Running/scheduling

This can be done by calling main.py manually, or using something like crontab to schedule it. For example, to run once every hour, the crontab file line to add would be:

`0 * * * * cd /<PATH_TO_PROJECT>/housing_tracker && python3 main.py >> run.log 2>&1`
