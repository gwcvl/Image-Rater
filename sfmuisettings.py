# setup info

DATA_FILE = "test_webcam_data.csv"
HAS_HEADER = True
ID_INDEX = 0
URL_INDEX = 2
IGNORE_INDICES = [5,6,7]
SFMUI_URL = "http://jlsm.io/sfmui/"

# paths

FINALRESULTS_FILE = "finalresults.csv"
PENDING_FILE = "pending.pickle"
INPROGRESS_FILE = "inprogress.pickle"
COMPLETED_FILE = "completed.pickle"

# HTML stuff

QUESTION = "KEEP THIS WEBCAM?"

INPUTS = "<input type=\"radio\" name=\"score\" value=\"1\" required><label>Yes</label>" + \
	 "<input type=\"radio\" name=\"score\" value=\"0\" required><label>No</label>"

FOOTER = "contact: somebodyatsomewhere.edu"

ASK_PAGE_STRING = "<!DOCTYPE html>" + \
"<html>" + \
"<head>" + \
"<meta charset=\"utf-8\" />" + \
"<title>Prototype SFMUI Frame</title>" + \
"<link rel=\"stylesheet\" type=\"text/css\" href=\"sfmui.css\">" + \
"</head>" + \
"<body>" + \
"<div id=\"content-wrapper\">" + \
"<div id=\"question\">!QUESTION!</div>" + \
"<div id=\"display-area\">" + \
"<table>" + \
"<tr>" + \
"<td>" + \
"<div class=\"image-display-area\">" + \
"<img class=\"image\" src=\"!URL!\" alt=\"!ALTTEXT!\">" + \
"<div class=\"response\">" + \
"<form action=\"sfmui.py\" method=\"get\">" + \
"<input type=\"hidden\" name=\"action\" value=\"submit\">" + \
"<input type=\"hidden\" name=\"id\" value=\"!ID!\">" + \
"!INPUTS!" + \
"<br>" + \
"<input type=\"submit\" value=\"Submit\">" + \
"</form>" + \
"</div>" + \
"</div>" + \
"<div id=\"meta\">!METADATA!</div>" + \
"</td>" + \
"</tr>" + \
"</table>" + \
"</div>" + \
"<div id=\"footer\">!FOOTER!</div>" + \
"</div>" + \
"</body>" + \
"</html>"

RESPONSE_RECORDED_PAGE_STRING = "<!DOCTYPE html>" + \
"<html>" + \
"<head>" + \
"<meta charset=\"utf-8\" />" + \
"<title>Prototype SFMUI Frame</title>" + \
"<link rel=\"stylesheet\" type=\"text/css\" href=\"sfmui.css\">" + \
"</head>" + \
"<body>" + \
"<div id=\"content-wrapper\">" + \
"<div id=\"response-recorded\">" + \
"<p>You scored record !ID! as !SCORE!</p>" + \
"<table>" + \
"<tr>" + \
"<td>" + \
"<form action=\"sfmui.py\" method=\"get\">" + \
"<input type=\"hidden\" name=\"action\" value=\"get\">" + \
"<input type=\"submit\" value=\"Next\">" + \
"</form>" + \
"</td>" + \
"<td>" + \
"<form action=\"sfmui.py\" method=\"get\">" + \
"<input type=\"hidden\" name=\"action\" value=\"quit\">" + \
"<input type=\"submit\" value=\"Quit\">" + \
"</form>" + \
"</td>" + \
"</tr>" + \
"</table>" + \
"</div>" + \
"<div id=\"footer\">!FOOTER!</div>" + \
"</div>" + \
"</body>" + \
"</html>"
