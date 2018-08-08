from udicOpenData.stopwords import rmsw

import falcon

from app.tfidf import TFIDFRESOURCE




app = application = falcon.API()

tfr = TFIDFRESOURCE()
app.add_route('/tfidf', tfr)
