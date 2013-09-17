from T_Rax_Data import TraxData

data = TraxData()
data.load_exp_data('SPE test vers3\\test_075.spe')


#for w in xrange(400, 600):
#    i= data.calculate_ind(w)
#    new_w = data.get_wavelength(i)
#    if not w==new_w:
#        print w


w = 500

ind = data.calculate_ind(w)
new_w = data.get_wavelength(ind)

print int(new_w)