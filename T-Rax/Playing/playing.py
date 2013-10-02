import pickle


class test_class():
    def __init__(self):
        self.temp='blub'
        self.temp2='blub3'

test_obj=test_class()
pickle.dump(test_obj,open('settings/test.tra',"w"))