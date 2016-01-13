import os,sys
from searchengine import*
from collections import Counter
from Tkinter import*
from tkFileDialog import*
import ttk
from tkMessageBox import*
from time import time


class mini_google:

    def __init__(self,root):

        # Interface
        self.getwords = StringVar()

        root.title('Digital Library Search Engine')
        root.geometry('900x680+200+10')
        self.label_1 = Label(root,text = 'Digital Library Search Engine v1.0', padx = 70, pady = 40,font=("Helvetica", 20),fg = "blue",bg = 'pink')
        self.label_1.pack()
        self.entry = Entry(root, width = 100,textvariable = self.getwords)
        self.entry.place(x = 140, y = 160)
        self.button = Button(root, text = 'Initialize',height = 1,command = self.initialize, fg = 'blue',bg = 'pink',font=("Helvetica", 15))
        self.button.place(x = 400,y = 200)
        self.text = Text(root,width = 100,height = 20)
        self.text.place(x = 40,y = 280)
        self.next = Button(root, text = 'Next',height = 1, fg = 'blue',bg = 'pink',font=("Helvetica", 10),command = self.next)
        self.next.place(x = 810,y = 630)
        self.previous = Button(root, text = 'Previous',height = 1, fg = 'blue',bg = 'pink',font=("Helvetica", 10),command = self.previous)
        self.previous.place(x = 680,y = 630)
        self.label_1 = Label(root,text = '1', padx = 10, pady = 5,font=("Helvetica", 10),fg = "pink",bg = 'blue')
        self.label_2 = Label(root,text = '123')


    def create_wordlocation_dict(self):
        global wordlocations
        global names
        names = {}
        # This path needs to be changed from user to another
        p = "C:/metadata"
        dirs = os.listdir(p)
        wordlocations = {}

        for file in dirs:
            with open(os.path.join(p,file),'r') as openfile:
                one_line_text = ''
                for line in openfile:
                    one_line_text = one_line_text + line
                    #Create a dictionary with Ids as keys and Titles as values
                    if line[:5] == 'Title':
                        names.setdefault(file[:-4],line[7:])

                lines = crawler('')
                l = lines.separatewords(one_line_text)

                for word in l:
                    wordlocations.setdefault(word,{})

                # Create World location dictionary
                for i in range(len(l)-1):
                    wordlocations[l[i]].setdefault(file[:-4],[])
                    wordlocations[l[i]][file[:-4]].append(i)
        return wordlocations


    def create_citations_dict(self):
        global citations
        citations = {}
        with open('citations.txt','r') as openfile:
            for lines in openfile:
                line = lines.split('\t')
                # remove the first 2 lines
                if len(line) == 1 or line[0][0] == '#':
                    continue
                else:
                    # Create Citations dictionary
                    if line[1][:-1] not in citations:
                        citations[line[1][:-1]] = [line[0]]
                    else:
                        citations[line[1][:-1]].append(line[0])
        return citations


    def create_citationcounts_dict(self):
        global citationcounts
        list = []
        with open('citations.txt','r') as openfile:
            for lines in openfile:
                line = lines.split('\t')
                if len(line) == 1 or line[0][0] == '#':
                    continue
                else:
                    list.append(line[0])
        # using the collection module to count the frequencies of the words
        citationcounts = Counter(list)
        return citationcounts

    # this function calls the functions mentioned above
    def initialize(self):
        # Update the status
        self.text.delete('0.0',END)
        print ' Please Wait While The Search Engine Performs the Initialization Phase: \n'
        self.text.insert(END,'Please Wait While The Search Engine Performs the Initialization Phase: \n')

        a0 = 'Loading Paper Metadata (In progress) !\nLoading Citation Data (In Progrress) !\n' \
            'Computing PageRank Scores (In Progress) !\n><><><><><><><><><><><><'
        print a0
        self.text.insert(END,a0)
        root.update_idletasks()

        self.text.delete('0.0',END)
        print ' Please Wait While The Search Engine Performs the Initialization Phase: \n'
        self.text.insert(END,'Please Wait While The Search Engine Performs the Initialization Phase: \n')

        a1 = 'Loading Paper Metadata (Completed) !\nLoading Citation Data (In Progrress) !\n' \
            'Computing PageRank Scores (In Progress) !\n><><><><><><><><><><><><'
        self.create_wordlocation_dict()
        print a1
        self.text.insert(END,a1)
        root.update_idletasks()

        self.text.delete('0.0',END)
        print  'Please Wait While The Search Engine Performs the Initialization Phase: \n'
        self.text.insert(END,'Please Wait While The Search Engine Performs the Initialization Phase: \n')

        a2 = 'Loading Paper Metadata (Completed) !\nLoading Citation Data (Completed) !\n' \
            'Computing PageRank Scores (In Progress) !\n><><><><><><><><><><><><'
        self.create_citations_dict()
        self.create_citationcounts_dict()
        print a2
        self.text.insert(END,a2)
        root.update_idletasks()

        self.text.delete('0.0',END)
        print ' Please Wait While The Search Engine Performs the Initialization Phase: \n'
        self.text.insert(END,'Please Wait While The Search Engine Performs the Initialization Phase: \n')

        a3 = 'Loading Paper Metadata (Completed) !\nLoading Citation Data (Completed) !\n' \
            'Computing PageRank Scores (Completed) !\n><><><><><><><><><><><><'
        self.pagerank(10)
        self.button.config(text = 'Search',command = self.search)
        print a3
        self.text.insert(END,a3)
        root.update_idletasks()


    def pagerank(self,iterations = 10):
        global normalize1
        link_base_rank_dict = {}
        x = citations.keys()
        for id in x:
            # Create dictionary were keys are fromIds and toIds and values are 1
            link_base_rank_dict .setdefault(id,1)
            for bd in citations[id]:
                if bd in link_base_rank_dict :
                    continue
                else:
                    link_base_rank_dict .setdefault(bd,1)

        for i in range(iterations):
            for key in citations:
                sum = 0
                # Calculate the page ranks
                for value in citations[key]:
                    sum = sum + (link_base_rank_dict [value]/citationcounts[str(value)])
                link_base_rank_dict [key] = 0.15+0.85*sum
        c = searcher('')
        normalize1 = c.normalizescores(link_base_rank_dict )
        return normalize1


    def search(self):
        begin = time()
        global b
        global c
        global all_outputs
        self.text.delete('0.0',END)
        b = 0
        list = []
        list2 = []
        input = self.getwords.get()
        # Error box
        if len(input) == 0:
            showwarning(title = 'Error',message = 'Please Enter some words!')
        else:
            words = input.lower().split(' ')
            for i in words:
                list.append(i)

            for ii in list:
                list2.append(wordlocations[ii])

            # Finding the intersection
            inter = set(list2[0])
            for iii in range(len(list2)):
                inter = inter & set(list2[iii])

            # Calculate the content base ranking
            content_base_rank_dict = {}
            for id in inter:
                x = 1
                for word in list:
                    x = x * len(wordlocations[word][id])
                content_base_rank_dict.setdefault(id,x)
            c = searcher('')
            normalize2 = c.normalizescores(content_base_rank_dict)

            # calculate the final page rank
            final_normalize = {}
            for paper in normalize2:
                try:
                    final_normalize.setdefault(normalize2[paper]+normalize1[paper],paper)
                except:
                    pass
            final_normalize = final_normalize.items()
            final_normalize = sorted(final_normalize, reverse = True)

            all_outputs = []
            list_of_20outputs = []
            c = 0
            # crating a list of lists were these lists contains the first 20 results in order
            for iiii in final_normalize:
                x,y = iiii
                c += 1
                output = '%s- %g        %s' %(c,x,names[y])
                list_of_20outputs.append(output)
                if len(list_of_20outputs)>20:
                    all_outputs.append(list_of_20outputs)
                    list_of_20outputs = []
                    list_of_20outputs.append(output)
                else:
                    pass

            all_outputs.append(list_of_20outputs)
            # printing the first 20 results
            for page in all_outputs[0]:
                self.text.insert(END,page)

            # get the time it took it to finish searching
            finish = time()
            total_time = finish - begin
            self.label_2.config(text = '%d Pages!,  %s second!'%(c,total_time),fg = 'blue',bg = 'pink')
            self.label_2.place(x = 40,y = 250)
            self.label_1.config(text = '1/%s'%((c/20)+1))
            self.label_1.place(x = 750,y = 630)

    # when pressing the button next it shows the next 20 results
    def next(self):
        global b
        b += 1
        self.text.delete('0.0',END)
        for page in all_outputs[b]:
            self.text.insert(END,page)
        self.label_1.config(text = str(b+1))
        self.label_1.config(text = '%s/%s'%(b+1,(c/20)+1))
        self.label_1.place(x = 750,y = 630)

    # when pressing the button previous it shows the previous 20 results
    def previous(self):
        global b
        b -= 1
        self.text.delete('0.0',END)
        for page in all_outputs[b]:
            self.text.insert(END,page)
        self.label_1.config(text = str(b))
        self.label_1.config(text = '%s/%s'%(b+1,(c/20)+1))
        self.label_1.place(x = 750,y = 630)


root = Tk()
mini_google(root)
root.mainloop()


