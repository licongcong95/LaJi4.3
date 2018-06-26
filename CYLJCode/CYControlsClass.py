#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import random

class CYControlsClass(object):
    def show(self,viewName,ViewType):
        viewStr = ''

        #    这里实现view的各种方法
        #    frame
        orig_x = random.randint(0,100)
        orig_y = random.randint(0,300)
        view_width = random.randint(100,375)
        view_height = random.randint(100,625)
        viewStr +=  '      _'+viewName+' = [['+ViewType+' alloc] initWithFrame:CGRectMake('+str(orig_x)+', '+str(orig_y)+', '+str(view_width)+', '+str(view_height)+')];\n\n'
    
        viewStr += '      _'+viewName+'.alpha = 1;\n\n'
    
        userState = random.randint(0,1)
    
        if(userState == 1):
            viewStr += '      _'+viewName+'.userInteractionEnabled = YES;\n\n'
    
    
        centerState = random.randint(0,1)

        if(centerState == 1):
            viewStr += '      _'+viewName+'.center = self.view.center;\n\n'
    
    
        layerState = random.randint(0,1)
    
        if(layerState == 1):
            viewStr += '      _'+viewName+'.layer.masksToBounds = YES;\n\n';
            viewStr += '      _'+viewName+'.layer.cornerRadius = '+ str(random.randint(5,10))+';\n\n';


        color = ['blackColor','darkGrayColor','lightGrayColor','whiteColor','grayColor','redColor','greenColor','blueColor','cyanColor','yellowColor','magentaColor','orangeColor','purpleColor','brownColor']

        viewStr += '      _'+viewName+'.backgroundColor = [UIColor '+color[random.randint(0,13)]+'];\n\n'

        return viewStr

