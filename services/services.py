from models.dataobjects import DXR, Code
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
import time

global considerations
global hvac_abbreviations

considerations = []
hvac_abbreviations = [{'chw':'chilled water'},{'hhw':'heating hot water'}]

class Services(object):

    def __init__(self):  # setup db connection
        client = connect(db='pztcetool', host='localhost', port=27017)
        self.db = client['pztcetool']

    def saveCode(self, **kwargs):  # save code to db
        code = Code()
        code.job_number = kwargs.get('job_number', None)
        code.program_file_name = kwargs.get('program_file_name', None)
        code.program_file_name = code.job_number + code.program_file_name.split('\\')[2]
        code.soo_file_name = kwargs.get('soo_file_name', None)
        code.soo_file_name = code.job_number + code.soo_file_name.split('\\')[2]
        # files are base64 string
        program_file = kwargs.get('program_file', None)
        soo_file = kwargs.get('soo_file', None)
        if program_file:
            try:
                program_file = program_file.split(',')[1]  # remove up to comma
                convertedFile = Services.convertBase64(program_file)  # convert back
                Services.saveFile(convertedFile, code.program_file_name, app.config['CODE_SOO_UPLOAD_FOLDER'])  # save
            except Exception as e:
                raise ValueError(str(e))
        if soo_file:
            try:
                soo_file = soo_file.split(',')[1]  # remove up to comma
                convertedFile = Services.convertBase64(soo_file)  # convert back
                Services.saveFile(convertedFile, code.soo_file_name, app.config['CODE_SOO_UPLOAD_FOLDER'])  # save
            except Exception as e:
                raise ValueError(str(e))
        try:
            code.save()
        except Exception as e:
            raise ValueError(str(e))
        return str(code['id'])

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
        dxr.file_name = dxr.template_name + "_" + str(time.time()) + "." + file_extension
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
        raw = open(app.config['CODE_SOO_UPLOAD_FOLDER'] + file).read()
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
        return self.cosSim(v1, v2)

    def replaceWords(self, filename, *args, **kwargs):
        path = Path(app.config['CODE_SOO_UPLOAD_FOLDER'] + filename)
        try:
            text = path.read_text(encoding='cp1252')
        except Exception as e:
            raise ValueError(str(e))
        ic(app.config['CODE_SOO_UPLOAD_FOLDER'] + filename)
        for i in hvac_abbreviations:
            for key, val in i.items():
                text = text.replace(key,val)
                path.write_text(text)

    def compareSoo(self,filename,*args,**kwargs):
        # print("filename is: " + str(filename))
        file_to_compare = filename
        if file_to_compare is None:
            raise ValueError('Must supply a file to compare')
        # ic(file_to_compare)
        self.replaceWords(filename=file_to_compare)
        dict1 = self.process(file_to_compare)
        arr_txt = [x for x in os.listdir(app.config['CODE_SOO_UPLOAD_FOLDER']) if x.endswith(".txt")]
        # ic(file_to_compare)
        # print(len(arr_txt))
        for txt in range(0,len(arr_txt)):
            if arr_txt[txt] != file_to_compare:
                self.replaceWords(arr_txt[txt])
                dict2 = self.process(arr_txt[txt])
                similarity = self.getSimilarity(dict1,dict2) * 100
                similarity = float(f"{similarity:.2f}")
                if similarity < 100.00:
                    considerations.append({'Name':arr_txt[txt], 'Similarity':str(similarity) + "%"})
                else:
                    considerations.insert(0,{'Name':arr_txt[txt], 'Similarity':str(similarity) + "%"})
        considerations_sorted = sorted(considerations, key = lambda i: i['Similarity'],reverse=True)
        return considerations_sorted

    def findSimilarSequences(self, **kwargs):
        # file is a base64 string
        file = kwargs.get('file', None)
        # folder = 'soo/file_to_compare/'
        folder = app.config['CODE_SOO_UPLOAD_FOLDER']
        file_name = kwargs.get('file_name', None)
        file_name = file_name.split('\\')[2]
        if file is not None:
            try:
                pass
                # file = file.split(',')[1]  # remove up to comma Commenting out on 02/11/2021
                convertedFile = Services.convertBase64(file)  # convert back Commenting out on 02/11/2021
                Services.saveFile(convertedFile, file_name, folder)  # save Commenting out on 02/11/2021
            except Exception as e:
                raise ValueError(str(e))
        else:
            raise ValueError('No file data supplied')
        results = self.compareSoo(filename=file_name)
        # for result in results:
            # ic(result)
        return results
