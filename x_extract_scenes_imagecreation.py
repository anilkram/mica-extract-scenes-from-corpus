#!/usr/bin/env python

import os
import csv
from math import ceil
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

datadir = '/Users/anil/GoogleDrive/SAIL/Research/MICA/BiasUsingText/v1/Data/movies_deliverable/input/scripts/'
outfile = '/Users/anil/GoogleDrive/SAIL/Research/MICA/HumorFromText/Data/movie_dic_scenes/scenes.csv'
img_dir = '../Data/movie_dic_scenes/scene_images/'

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
        while cur_ind < len(children):
            assert(children[cur_ind].name=='speaker' and children[cur_ind+1].name=='mode' and children[cur_ind+2].name=='context' and children[cur_ind+3].name=='utterance')
            speaker = children[cur_ind].get_text()
            context = children[cur_ind+2].get_text()
            utterance = children[cur_ind+3].get_text()
            if len(context) > 80:
                num_lines = ceil(len(context)/80)
                for i in range(num_lines):
                    lower_i = i*80
                    upper_i = lower_i + 79
                    out_text.append(context[lower_i:upper_i])
            else:   
                out_text.append(context)

            if len(utterance) > 60:
                num_lines = ceil(len(utterance)/60)
                for i in range(num_lines):
                    lower_i = i*60
                    upper_i = lower_i + 59
                    if i==0:
                        out_text.append('\t'+speaker+': '+utterance[lower_i:upper_i])
                    else:
                        out_text.append('\t\t'+utterance[lower_i:upper_i])
            else:
                out_text.append('\t'+speaker+': '+utterance)
        
            cur_ind += 4

        num_rows = len(out_text) * 25+50
        num_cols = 0
        num_cols = [len(line) for line in out_text if len(out_text) > num_cols]
        x_dim = (num_rows*15) + 100
        y_dim = 90*15
        img = Image.new('RGB', (num_rows,500), (255,255,255))
        d = ImageDraw.Draw(img)
        font=ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf', 15)
        d.text((10,10), '\n'.join(out_text), (0,0,0), font=font)
        img.save(img_dir+filename+'_'+str(counter), 'jpeg')
#        csvwriter.writerow([filename, counter, str(diag)])
        counter += 1

outptr.close()
