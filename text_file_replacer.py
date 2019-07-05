class text_file_replacer:
    # define default value
    def __init__(self, lines = []):
        self.origin_lines    = lines
        self.target_lines    = []
        self.replace_control = {}

    # set replace rules
    def add_replace_rule(self, mark = '', lines = []):
        # add rule
        self.replace_control[mark + '\n'] = lines

    # run replace
    def replace_file(self):
        # start to check origin lines
        for current_ori_line in self.origin_lines:
            # check if mark
            if current_ori_line in self.replace_control.keys():
                # line need replace
                for line in self.replace_control[current_ori_line]:
                    self.target_lines.append(line)
            else:
                # line need keep
                self.target_lines.append(current_ori_line)
        # return new lines
        return self.target_lines
