#!/usr/bin/env python

import os
import csv
from math import ceil
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

datadir = '/Users/anil/GoogleDrive/SAIL/Research/MICA/BiasUsingText/v1/Data/movies_deliverable/input/scripts/'
outfile = '/Users/anil/GoogleDrive/SAIL/Research/MICA/HumorFromText/Data/movie_dic_scenes/scenes.csv'
scene_dir = '../Data/movie_dic_scenes/scenes/'

fileslist = os.listdir(datadir)

outptr = open(outfile, 'w')
csvwriter = csv.writer(outptr)

for filename in fileslist:
    with open(datadir+filename) as inptr:
        soup = BeautifulSoup(inptr.read(), 'lxml') 

    counter = 1 
    for diag in soup.find_all('dialogue'):
        #extract dialogues and contexts
        children = diag.find_all()
        cur_ind = 0; out_text = []
        scene_out_file = scene_dir + filename[:-4] + '_' + str(counter) + '.txt'
        scene_out_ptr = open(scene_out_file, 'w')
        while cur_ind < len(children):
            assert(children[cur_ind].name=='speaker' and children[cur_ind+1].name=='mode' and children[cur_ind+2].name=='context' and children[cur_ind+3].name=='utterance')
            speaker = children[cur_ind].get_text()
            context = children[cur_ind+2].get_text()
            utterance = children[cur_ind+3].get_text()

            scene_out_ptr.write(context+'\n')
            scene_out_ptr.write('\t'+speaker.upper()+': '+utterance+'\n\n')
            cur_ind += 4
        scene_out_ptr.close()

#        csvwriter.writerow([filename, counter, str(diag)])
        counter += 1
    
    print("Done with {0}".format(filename))

outptr.close()
