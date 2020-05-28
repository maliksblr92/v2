import sys
from Data_Processing_Unit.models import *
from Public_Data_Acquisition_Unit.mongo_models import *
from dotmap import DotMap


class Mongo_Serializer(object):

    SUPPORTED_MODELS = [Keybase_Response_TMS,Trends]

    def __init__(self):
        pass

    def is_supported(self,model):
        if(model in Mongo_Serializer.SUPPORTED_MODELS):
            return True

        return False

    def find_model_of_object(self,object):
        return self.str_to_class(self.parse_model_name(str(object.__class__)))



    def str_to_class(self,class_name):
        return getattr(sys.modules[__name__], class_name)


    def parse_model_name(self,model_name):
        return model_name.strip("><'").split('.')[-1]


    def keybase_responce_tms_serializer(self,objects_list):

        data = []

        if(len(objects_list) > 0):
            if(self.is_supported(self.find_model_of_object(objects_list[0]))):

                for obj in objects_list:
                    obj = obj.to_mongo()
                    obj_data_list = obj['data']
                    for obj_data in obj_data_list:
                        temp_in = {}
                        for k,v in obj_data.items():
                            temp_in[k] = v


                        print({"fields":temp_in})
                        data.append({"fields":temp_in})
                        del(temp_in)
        print(len(data))
        return data

