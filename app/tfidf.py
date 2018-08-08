# -*- coding: utf-8 -*-
'''
A Resource for falcon using TF-IDF and Ontology to do Topic Recommendation
'''

import json
import pickle
import re
from collections import Counter
from pathlib import Path, PurePath

import jieba.posseg as pseg
import numpy as np
import udicOpenData.dictionary

import falcon
import pymongo
from webargs import fields, validate
from webargs.falconparser import parser, use_args

ONTOLOGY_SET = pickle.load(open(str(PurePath(Path(__file__).resolve().parent, 'ontology.pkl')), 'rb'))
COLLECT = pymongo.MongoClient('mongodb://mongo:27017')['nlp_zh']['idf']
STOPWORD_SET = pickle.load(open(str(PurePath(Path(__file__).resolve().parent, 'stopwords.pkl')), 'rb'))

@parser.error_handler
def handle_error(error):
    """Handle webarg errors with falcon BadRequest"""
    raise falcon.HTTPBadRequest(description=error.messages, code=1004)


class TFIDFRESOURCE():
    '''TFIDF_Resource Resource'''
    argmap = {
        'context': fields.String(),
        'title': fields.String(),
        'tfidf_topk': fields.Int(missing=10, validate=validate.Range(min=1, max=15)),
        'limit': fields.Int(missing=5, validate=validate.Range(min=1, max=10))
    }

    @use_args(argmap)
    def on_post(self, req, resp, args):
        '''falcon post function'''
        # Create a JSON representation of the resource
        context = args['context']
        title = args['title']
        doc = title + context

        tfidf_topk = args['tfidf_topk']
        limit = args['limit']
        tfidf_list = self.tfidf(doc, tfidf_topk=tfidf_topk)
        recommended_topics = [
            {'name': keyword, 'postCount': 0} for keyword, score in self.ontology_filter(tfidf_list, limit)
        ]
        resp.body = json.dumps(
            {'list': recommended_topics}, ensure_ascii=False)

    def tfidf(self, doc, tfidf_topk=10):
        '''
        tfidf function
        '''
        tfs = Counter(
                (keyword for keyword, f in self.rmsw(doc, flag='n'))
            )
        # bulk select
        cursor = COLLECT.find({'key':{'$in':list(tfs.keys())}})
        idf_tuple = [(response['key'], response['value']) for response in cursor]
        # idf_tuple[0] contains keyword, idf_tuple[1] contains tfidf score
        idf_tuple = np.array(list(zip(*idf_tuple)))
        idf = idf_tuple[1].astype('float32')
        # do log calculation on batch
        tf_log = np.log(np.array([tfs[i] for i in idf_tuple[0]])) + 1
        # multiply tf and idf on batch
        idf_tuple[1] = tf_log * idf
        # return sorted index of tfidf and reverse them
        sorted_tfidf = np.argsort(idf_tuple[1].astype('float'))[::-1]
        # idf_tuple[0] contains keyword, idf_tuple[1] contains tfidf score
        return [(idf_tuple[0][index], idf_tuple[1][index]) for index in sorted_tfidf[:tfidf_topk]]

    @staticmethod
    def ontology_filter(tfidf_list, limit):
        '''
        use wiki ontology data to filter out those keyword doesn't appear in ontology set
        '''
        count = 0
        for keyword, score in tfidf_list:
            if count == limit:
                break
            if keyword not in ONTOLOGY_SET:
                continue
            else:
                yield keyword, score
                count += 1

    @staticmethod
    def rmsw(doc, flag):
        '''
        parameter:
          flag: boolean, if 'n' will return segment with pos.
        '''
        def is_chinese(keyword):
            for uchar in keyword:
                if '\u4e00' <= uchar <= '\u9fff':
                    continue
                else:
                    return False
            return True

        doc = doc.strip()

        # flag means showing part of speech
        for i in pseg.cut(doc):
            if i.flag in flag\
            and is_chinese(i.word)\
            and i.word not in STOPWORD_SET \
            and i.word not in ['\xa0', '\xc2']:
                yield i.word, i.flag
