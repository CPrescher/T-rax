'''
This helper file includes a validator for checking that only numbers are inserted into specfic text boxes
Two validators possible:
IntValidator - allowing only 1,2,3,4,5,6,7,8,9,0
FloatValidator - allowing only 1,2,3,4,5,6,7,8,9,0 and ',' and '.'

'''

import string

import wx


ALPHA_ONLY = 1
DIGIT_ONLY = 2


class IntValidator(wx.PyValidator):
    def __init__(self, flag=None, pyVar=None):
        wx.PyValidator.__init__(self)
        self.flag = flag
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return IntValidator(self.flag)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        for x in val:
            if x not in string.digits:
                return False

        return True


    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

   