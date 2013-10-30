




class TRaxModuleController():
    def __init__(self, parent,data, control_widget):
        self.parent = parent
        self.data = data
        self.control = control_widget
        self._create_signals()

    def _create_signals(self):
        self.create_exp_file_signals()
        self.create_roi_view_signals()
        self.create_auto_process_signal()
    
    def create_exp_file_signals(self):
        self.connect_click_function(self.main_view.ruby_control_widget.load_exp_data_btn, self.load_exp_data)        
        self.connect_click_function(self.main_view.ruby_control_widget.load_next_exp_data_btn, self.load_next_exp_data)        
        self.connect_click_function(self.main_view.ruby_control_widget.load_previous_exp_data_btn, self.load_previous_exp_data)
    
    def create_roi_view_signals(self):
        self.connect_click_function(self.main_view.ruby_control_widget.roi_setup_btn, self.load_roi_view)
    
    def create_auto_process_signal(self):
        self.main_view.ruby_control_widget.auto_process_cb.clicked.connect(self.auto_process_cb_click)
        self.autoprocess_timer = QtCore.QTimer(self.main_view)
        self.autoprocess_timer.setInterval(100)
        self.main_view.connect(self.autoprocess_timer,QtCore.SIGNAL('timeout()'), self.check_files)

    def load_exp_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Experiment SPE", 
                                          directory = self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1]) + '/'
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)]) #reset for the autoprocessing
            self.data.load_exp_data(filename)

    def load_next_exp_data(self):
        self.data.load_next_exp_data()

    def load_previous_exp_data(self):
        self.data.load_previous_exp_data()

    def auto_process_cb_click(self):
        if self.main_view.ruby_control_widget.auto_process_cb.isChecked():
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)])
            self.autoprocess_timer.start()
        else:
            self.autoprocess_timer.stop()

    def check_files(self):
        self._files_now = dict([(f,None) for f in os.listdir(self._exp_working_dir)])
        self._files_added = [f for f in self._files_now if not f in self._files_before]
        self._files_removed = [f for f in self._files_before if not f in self._files_now]
        if len(self._files_added) > 0:
            new_file_str = self._files_added[-1]
            if self.file_is_spe(new_file_str) and not self.file_is_raw(new_file_str):
                file_info = os.stat(self._exp_working_dir + new_file_str)
                if file_info.st_size > 1000:
                    path = self._exp_working_dir + new_file_str
                    self.data.load_exp_data(path)
                    self._files_before = self._files_now
            
    def file_is_spe(self, filename):
        return filename.endswith('.SPE') or filename.endswith('.spe')
    
    def file_is_raw(self, filename):
        try:
            #checks if file contains "-raw" string at the end
            return filename.split('-')[-1].split('.')[0] == 'raw'
        except:
            return false