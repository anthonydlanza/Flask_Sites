from models.dataobjects import DXR
from mongoengine import *
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
import base64
# file compare  specific libs
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from icecream import ic
from pathlib2 import Path
import os

global considerations
global hvac_abbreviations

considerations = []
hvac_abbreviations = [{'chw':'chilled water'},{'hhw':'heating hot water'}]

class Services(object):

    def __init__(self):  # setup db connection
        client = connect(db='pztcetool', host='localhost', port=27017)
        self.db = client['pztcetool']

    def saveTemplate(self, **kwargs):  # save dxr to db
        dxr = DXR()
        # template name is all fields combined with underscores between
        dxr.template_name = kwargs.get('template_name', None)
        template_name_chunks = dxr.template_name.split('_')
        # template_name_chunks should always equal 7
        # and will always be in same order
        if len(template_name_chunks) < 7:
            raise ValueError('There is an issue with template_name')
        dxr.hardware_encoded = template_name_chunks[0]
        dxr.threept_encoded = template_name_chunks[1]
        dxr.zten_encoded = template_name_chunks[2]
        dxr.bo_encoded = template_name_chunks[3]
        dxr.inputs_encoded = template_name_chunks[4]
        dxr.pres_encoded = template_name_chunks[5]
        dxr.knx_encoded = template_name_chunks[6]
        dxr.threept_names = kwargs.get('threept_names', None)
        dxr.tenvolt_names = kwargs.get('tenvolt_names', None)
        dxr.binary_names = kwargs.get('binary_names', None)
        dxr.x1x4_names = kwargs.get('x1x4_names', None)
        dxr.pressure_names = kwargs.get('pressure_names', None)
        dxr.knx_names = kwargs.get('knx_names', None)
        # file is a base64 string
        file = kwargs.get('file', None)
        file_extension = kwargs.get('file_name', None)  # get file name
        file_extension = file_extension.split('.')[1]  # get file extension
        dxr.file_name = dxr.template_name + "." + file_extension
        if file:
            try:
                file = file.split(',')[1]  # remove up to comma
                convertedFile = Services.convertBase64(file)  # convert back
                Services.saveFile(convertedFile, dxr.file_name)  # save
            except Exception as e:
                raise ValueError(str(e))
        try:
            dxr.save()
        except Exception as e:
            raise ValueError(str(e))
        return self.getDXRMID(id=str(dxr['id']))

    def allowed_file(filename=None):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() \
            in app.config['ALLOWED_EXTENSIONS']

    def saveFile(file=None, filename=None, folder=None):
        print(folder)
        if file is None:
            raise ValueError("No file provided")
        if filename == '':
            raise ValueError("No filename provided")
        if file and Services.allowed_file(filename+'.txt'):
            filename = secure_filename(filename)
            if folder is None:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            else:
                filepath = os.path.join(folder, filename)
            try:
                with open(filepath, 'wb') as saveFile:
                    saveFile.write(file)
            except Exception as e:
                raise ValueError(str(e))
            return 1
            # return redirect(url_for('upload_file', filename=filename))
        else:
            raise ValueError("File name not allowed")

    def convertBase64(b64=None):
        if b64 is not None:
            b64bytes = b64.encode('utf-8')
        else:
            raise ValueError("No base 64 file provided")
        try:
            decodedB64 = base64.decodebytes(b64bytes)
        except Exception as e:
            raise ValueError(str(e))
        return decodedB64

    def getDXRMID(self, **kwargs):  # Get DXR via mongo _id
        id = kwargs.get('id')
        dxrs = DXR.objects.get(id=id)
        return {"id": str(id)}

    def getDXRTN(self, **kwargs):  # Get DXR via custom template name.
        template_name = kwargs.get('template_name')
        try:
            dxr = DXR.objects.get(template_name=template_name)
        except Exception as e:
            raise ValueError(str(e))
        return {"dxr": dxr.location, "id": str(dxr.id), "template_name": dxr.template_name}

    def templateSearch(self, **kwargs):
        # template name is all fields combined with underscores between
        template_name = kwargs.get('template_name',
            'XXX_XXXX_XXXX_XXXXXXXX_XXXXXX_XXXXX_XXXXXXXXXXXXXXXXXXXX')
        template_name_chunks = template_name.split('_')
        search_dict = {}
        # these if statement len(set()) statemens return 1 if all letters
        # in string are same character. if not one then we have valid search
        if len(set(template_name_chunks[0])) != 1:
            search_dict['hardware_encoded__icontains'] = template_name_chunks[0]
        if len(set(template_name_chunks[1])) != 1:
            search_dict['threept_encoded__icontains'] = template_name_chunks[1]
        if len(set(template_name_chunks[2])) != 1:
            search_dict['zten_encoded__icontains'] = template_name_chunks[2]
        if len(set(template_name_chunks[3])) != 1:
            search_dict['bo_encoded__icontains'] = template_name_chunks[3]
        if len(set(template_name_chunks[4])) != 1:
            search_dict['inputs_encoded__icontains'] = template_name_chunks[4]
        if len(set(template_name_chunks[5])) != 1:
            search_dict['pres_encoded__icontains'] = template_name_chunks[5]
        if len(set(template_name_chunks[6])) != 1:
            search_dict['knx_encoded__icontains'] = template_name_chunks[6]
        results = DXR.objects(**search_dict)
        result_list = []
        for result in results:
            result_list.append(result.to_json())
        return result_list

    # Create a function to open documents, and tokenize the words    
    def process(self, file, *args, **kwargs):
        raw = open(file).read()
        tokens = word_tokenize(raw)
        words = [w.lower() for w in tokens]

        # porter will stem the words i.e. reducing them to root words. For example "making" becomes "make"
        porter = nltk.PorterStemmer()
        stemmed_tokens = [porter.stem(t) for t in words]

        # Remove stop words such as "a" "the" "and"
        # Removing HVAC related words like "on" and "off" from the stop_words set
        stop_words = set(stopwords.words('english')) - set(['on', 'off', 'above','below','until'])
        filtered_tokens = [w for w in stemmed_tokens if not w in stop_words]

        # Count words
        count = nltk.defaultdict(int)
        for word in filtered_tokens:
            count[word] += 1
        return count

    # Using numpy -- create a function which gives you the cosign similarity of two documents.
    # This guy explains cosign similarity really well --> https://www.youtube.com/watch?v=Ze6A08Pw5oE
    def cosSim(self, a, b, *args, **kwargs):
        dot_product = np.dot(a,b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)

    def getSimilarity(self, dict1, dict2, *args, **kwargs):
        # Create a bag of words in the form of a list
        all_words_list = []
        # add all of the words from both documents to the list
        for key in dict1:
            all_words_list.append(key)
        for key in dict2:
            all_words_list.append(key)
        # get the length of the list
        all_words_list_size = len(all_words_list)
        # create two lists of all 0's that are the same length as your word list (bag of words)
        v1 = np.zeros(all_words_list_size,dtype=np.int)
        v2 = np.zeros(all_words_list_size,dtype=np.int)
        i = 0
        for (key) in all_words_list:
            v1[i] = dict1.get(key,0)
            v2[i] = dict2.get(key,0)
            i = i + 1
        return cos_sim(v1, v2)

    def replaceWords(self, file, *args, **kwargs):
        path = Path('new_sequence.txt')
        text = path.read_text()
        for i in hvac_abbreviations:
            for key, val in i.items():
                text = text.replace(key,val)
                path.write_text(text)

    def compareSoo(self,*args,**kwargs):
        file_to_compare = kwargs.get('filename', None)
        if file_to_compare is None:
            raise ValueError('Must supply a file to compare')
        print("The file to compare is: " + file_to_compare)
        replace_words(file_to_compare)
        dict1 = process(file_to_compare)
        arr_txt = [x for x in os.listdir() if x.endswith(".txt")]
        for txt in range(0,len(arr_txt)):
            if arr_txt[txt] != file_to_compare:
                replace_words(arr_txt[txt])
                dict2 = process(arr_txt[txt])
                similarity = get_Similarity(dict1,dict2) * 100
                similarity = float(f"{similarity:.2f}")
                ic(type(similarity))
                if similarity < 100.00:
                    considerations.append({'Name':arr_txt[txt], 'Similarity':str(similarity) + "%"})
                else:
                    considerations.insert(0,{'Name':arr_txt[txt], 'Similarity':str(similarity) + "%"})
        considerations_sorted = sorted(considerations, key = lambda i: i['Similarity'],reverse=True)
        return considerations_sorted


    # def similarFileCheck(self, **kwargs):
    #     # import files, tokenize sentences into array
    #     file_to_compare = kwargs.get('filename', None)
    #     if file_to_compare is None:
    #         raise ValueError('Must supply a file to compare')
    #     file_docs = []
    #     file2_docs = []
    #     avg_sims = []
    #     long_docs = []
    #     short_docs = []
    #     considerations = []
    #     arr_txt = [x for x in os.listdir('soo') if x.endswith(".txt")]
    #     for txt in range(0, len(arr_txt)):
    #         file_docs = []
    #         file2_docs = []
    #         with open('soo/file_to_compare/' + file_to_compare) as f:
    #             testlen = f.read()
    #             tokens = sent_tokenize(testlen)
    #             for line in tokens:
    #                 file_docs.append(line)
    #         with open('soo/' + arr_txt[txt]) as f:
    #             liblen = f.read()
    #             tokens2 = sent_tokenize(liblen)
    #             for line in tokens2:
    #                 file2_docs.append(line)
    #         if(len(testlen) >= len(liblen)):
    #             long_docs = file_docs
    #             short_docs = file2_docs
    #         else:
    #             long_docs = file2_docs
    #             short_docs = file_docs
    #         gen_docs = [[w.lower() for w in word_tokenize(text)]for text in long_docs]
    #         dictionary = gensim.corpora.Dictionary(gen_docs)
    #         corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    #         tf_idf = gensim.models.TfidfModel(corpus)
    #         sims = gensim.similarities.Similarity('soo/workdir/', tf_idf[corpus], num_features=len(dictionary))
    #         avg_sims = []
    #         for line in short_docs:
    #             query_doc = [w.lower() for w in word_tokenize(line)]
    #             query_doc_bow = dictionary.doc2bow(query_doc)
    #             query_doc_tf_idf = tf_idf[query_doc_bow]
    #             sum_of_sims =(np.sum(sims[query_doc_tf_idf], dtype=np.float32))
    #             avg = sum_of_sims / len(long_docs)
    #             # print(f'avg: {sum_of_sims / len(long_docs)}')
    #             avg_sims.append(avg)
    #         total_avg = np.sum(avg_sims, dtype=np.float)
    #         # print(total_avg)
    #         percentage_of_similarity = float(total_avg) * 100
    #         percentage_of_similarity = f"{percentage_of_similarity:.2f}"
    #         percentage_of_similarity = float(percentage_of_similarity)
    #         if percentage_of_similarity >= 100:
    #             percentage_of_similarity = 100
    #         # print("Similarity: " + str(percentage_of_similarity) + "%")
    #         considerations.append({'Name': arr_txt[txt], 'Similarity': str(percentage_of_similarity) + "%"})
    #     considerations_sorted = sorted(considerations, key = lambda i: i['Similarity'],reverse=True)
    #     return considerations_sorted

    def findSimilarSequences(self, **kwargs):
        print("Is this working...")
        # file is a base64 string
        file = kwargs.get('file', None)
        folder = 'soo/file_to_compare/'
        file_name = kwargs.get('file_name', None)
        file_name = file_name.split('\\')[2]
        print(folder)
        if file is not None:
            try:
                file = file.split(',')[1]  # remove up to comma
                convertedFile = Services.convertBase64(file)  # convert back
                Services.saveFile(convertedFile, file_name, folder)  # save
            except Exception as e:
                raise ValueError(str(e))
        else:
            raise ValueError('No file data supplied')
        results = self.compareSoo(filename=file_name)
        for result in results:
            print(result)
        return results
