class Agenda:
    folder = "D:\Germany_Erasmus\Arduino\pythonProject\dailyProgram"
    already_sent = False
    def __init__(self, date):
        self.date = date
        file_to_found = self.folder + "\\" + str(self.date) + ".txt"
        print(file_to_found)
        try:
            my_file = open(file_to_found, 'r+')
            self.plan = my_file.readlines()
            first_line = ""
            for line in self.plan:
                first_line = line
                break
            if(first_line == "Already sent!\n"):
                self.already_sent = True
            else:
                self.already_sent = False
                my_file.seek(0,0)
                new_text = "Already sent!\n"
                my_file.write(new_text + ''.join(self.plan))

        except:
            self.already_sent = False
            self.plan = "Sir, I did not find any file for today!"


    def printAgenda(self):
        print("This is your plan for today:")
        print(''.join(self.plan))







