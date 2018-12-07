#!/usr/bin/python

import sys
from ConfigParser import ConfigParser
from optparse import OptionParser

class MyConfigParser(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self,defaults=None)
  
    def optionxform(self, optionstr):
        return optionstr


class GenFakeData(object):

    def __init__(self):

        self.template_file = ''
        self.newdata_file = ''
        self.data_item = {}

    def read_cfg(self, cfg):
        self.conf = MyConfigParser()
        self.conf.read(cfg)

        self.template_file = self.conf.get('file', 'template_file')
        self.newdata_file = self.conf.get('file','newdata_file')
        #self.data_item = {}
        for key,value in self.conf.items('data'):
            self.data_item[key] = value
            #print("%s  %s" % (key,value))
    
    def gen_newdata_file(self):
        with open(self.newdata_file, 'w') as f_new:
             with open(self.template_file, 'r') as f_tpl:        
                  for line in f_tpl.readlines():
                      if line.split('=')[0] in self.data_item.keys():
                          continue
                      f_new.write(line)
            
             for key in self.data_item.keys():
                 if key == 'xsltxml':
                    self.data_item[key] = self.data_item[key].replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&amp;", "&").replace("&apos;", "'")
                 f_new.write("%s=\"%s\"\n" % (key, self.data_item[key]))

def parse_option_args():
    MSG_USAGE = '[-f<configfile>]'
    optParser = OptionParser(MSG_USAGE)
    optParser.add_option("-f", "--conffile", action="store", type="string", dest="conffile", help="config file")
    options, args = optParser.parse_args()
    return options

def main():
    try:
        param_input = parse_option_args()
        if param_input.conffile == None:
            print("please enter config file!\n")
            sys.exit()
     
        fakedata = GenFakeData()
        fakedata.read_cfg(param_input.conffile)
        fakedata.gen_newdata_file()
    except IOError:
        print("please check template_file or newdata_file correct")
    except Exception, e:
        print(e)


if __name__ == '__main__':
    main() 
