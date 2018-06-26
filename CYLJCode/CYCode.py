#!/usr/bin/python
# _*_ coding:utf-8 _*_
import os
import random
import string
from CYControlsClass import *
from PIL import Image


#定义属性及修饰关键字
AttributesConfig = [[['copy'],['NSString'],['*']],
                    [['copy'],['NSDictionary'],['*']],
                    [['copy'],['NSArray'],['*']],
                    [['copy'],['NSMutableDictionary'],['*']],
                    [['copy'],['NSMutableArray'],['*']],
                    [['assign'],['NSInteger'],['']],
                    [['assign'],['bool'],['']],
                    [['assign'],['float'],['']]
                    ]

#定义UI层次属性关键字
#数组第一个名字是控件名字   第二个是需要实现的代理协议     第三个是需要实现的数据源      第四个是一个数组【包括需要实现的代理方法，及需要返回的数据类型】    第五个是数据源需要实现的代理方法和需要返回的数据
#AttributesUIConfig = [['UIView','','',[],[]],
#                      ['UILabel','','',[],[]],
#                      ['UIButton','','',[],[]],
#                      ['UIImageView','','',[],[]],
#                      ['UITableView','UITableViewDelegate','UITableViewDataSource',[],[['- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section','NSInteger'],['- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath','UITableViewCell']]],
#                      ['UIScrollView','UIScrollViewDelegate','',[['- (void)scrollViewDidScroll:(UIScrollView *)scrollView','']],[]],
#                      ['UITextView',]
#                      ]
#原计划生成一个配置文件数组创建。但发现代理构成过于麻烦  重新思考。生成控件方法 代理协议完全独立

#AttributesUIConfig = ['UIView','UILabel','UIButton','UIImageView','UITableView','UIScrollView','UITextView','UIActivityIndicatorView']
AttributesUIConfig = ['UIView','UILabel','UIButton','UIImageView','UITableView','UITextView','UIActivityIndicatorView']

indexNum = 0

def main():
    print "code start"
    print "create OC files"
#    for i in range(0,50):
    startCont = createFileName()
    CreateContFile(startCont)
    
    SFile = './File/Header/'+ startCont + '.txt'
    SFileCreator = open(SFile,'w')
    SFileCreator.write(startCont)

#    模块测试===================================
#    createAttributesForHFile()
#    print  UIButtonFun('viewName')
#    xs = CYControlsClass()
#    res = xs.show('123')
#    print res
#    createImage()
#    print UITableViewFun('viewName')
#    createImage()

#生成Model类型文件
def CreateModelFile():

    fileName = createFileName()
    #   生成.h 和 .m文件
    HFile = './File/Model/'+ fileName + '.h'
    MFile = './File/Model/'+ fileName + '.m'
    HFileCreator = open(HFile,'w')
    MFileCreator = open(MFile,'w')
    
#       生成model类
    Htext = createFileText(fileName,1,'','','')
    print Htext[2]
    for item in Htext[0]:
        HFileCreator.write(item)
    Mtext = createFileText(fileName,2,Htext[1],Htext[2],Htext[3])
    for item in Mtext:
        MFileCreator.write(item)
    return fileName

#生成Controller类型文件
def CreateContFile(fileName):
    
    #   生成.h 和 .m文件
    HFile = './File/Controller/'+ fileName + '.h'
    MFile = './File/Controller/'+ fileName + '.m'
    HFileCreator = open(HFile,'w')
    MFileCreator = open(MFile,'w')
    
    #       生成model类
    Htext = createFileContText(fileName,1,'','','')
    print Htext[2]
    for item in Htext[0]:
        HFileCreator.write(item)
    Mtext = createFileContText(fileName,2,Htext[1],Htext[2],Htext[3])
    for item in Mtext:
        MFileCreator.write(item)


#生成文件内容（model类）
#1 .h文件。 2  .m文件
def createFileContText(fileName,fileType,MInfoFun,MinfoAttr,MparaName):
    #    print "文件类型为"
    #    print(fileType)
    if fileType == 1:
        attrText = createAttributesForHFile(1)
        funcName = createFileName()
        paraName = createFileName()
        text =  [
                 '#import <Foundation/Foundation.h>\n',
                 '#import <UIKit/UIKit.h>\n\n',
                 '@interface '+fileName+' : UIViewController\n'+attrText[0]+'\n',
                 '@end\n'
                 ]
        return [text,'',attrText[1],paraName]
    else:
        print MinfoAttr
        funBodyStr = '';
        
#        ['UIView','','','','','','']
        delegate = '@interface '+fileName+' ()'
        viewLoadSwitch = ''
        importModelName = ''
        
        global indexNum
        indexNum = indexNum + 1
        print (indexNum)
        TiaoZhuan = ''
        nextCont = ''
        importNextCon = ''
        if(indexNum < 50):
            nextCont = createFileName()
            CreateContFile(nextCont)
        #        这里执行跳转方法
            TiaoZhuan = '[self presentViewController:['+nextCont+' new] animated:YES completion:^{\n\n    NSLog(@\"跳转\");\n\n   }];'
            importNextCon = '#import \"'+nextCont+'.h\"\n\n'
        

#       判断是否需要生成数据源
        flag = False

        for item in MinfoAttr:
            if(item[1] == 'UIView'):
                funBodyStr += UIViewFun(item[0])+'\n\n'
            elif(item[1] == 'UILabel'):
                funBodyStr += UILabelFun(item[0])+'\n\n'
            elif(item[1] == 'UIButton'):
                funBodyStr += UIButtonFun(item[0],TiaoZhuan)+'\n\n'
            elif(item[1] == 'UIImageView'):
                funBodyStr += UIImageViewFun(item[0])+'\n\n'
            elif(item[1] == 'UITableView'):
                funBodyStr += UITableViewFun(item[0],TiaoZhuan)+'\n\n'
                delegate += '<UITableViewDataSource,UITableViewDelegate>\n\n'
                modelName = CreateModelFile()
                importModelName += '#import \"'+modelName+'.h\"'
                delegate += '@property (nonatomic,copy)NSMutableArray<'+modelName+'*>* dataSourceArr;'
                flag = True
            elif(item[1] == 'UITextView'):
                funBodyStr += UITextViewFun(item[0])+'\n\n'
            elif(item[1] == 'UIActivityIndicatorView'):
                funBodyStr += UIActivityIndicatorViewFun(item[0])+'\n\n'
            viewLoadSwitch += '   [self.view addSubview:self.'+item[0]+'];\n\n'
#        print funBodyStr
        delegate += '\n\n@end'

        sourceBodyFun = ''
        sourceFuncName = createFileName()
        ViewLoadAddSource = ''
        if(flag == True):
            sourceBodyFun += '- (void)'+sourceFuncName+'{\n\n   for (int i = 0;i<10;i++){\n\n       '+modelName+'* model = [['+modelName+' alloc] init'+modelName+':@{}];\n\n       [self.dataSourceArr addObject:model];\n\n   }   \n}'
            ViewLoadAddSource += '[self '+sourceFuncName+'];'
        viewLoad = '- (void)viewDidLoad {\n\n   [super viewDidLoad];\n\n    '+ViewLoadAddSource+'\n\n'+viewLoadSwitch+'\n\n}'

        text = [
                '#import \"'+fileName+'.h\"\n\n',
                importNextCon,
                importModelName+'\n',
                delegate+'\n',
                '@implementation '+fileName+'\n',
                viewLoad + '\n',
                sourceBodyFun + '\n',
                funBodyStr+'\n',
                '\n',
                '@end\n'
                ]


        return  text


#创建UI控件方法   使用懒加载形式
def UIViewFun(viewName):
    bodyStr = CYControlsClass()
    res = bodyStr.show(viewName,'UIView')
    viewStr = '   if (!_'+viewName+') {\n\n' + res + '   }\n'
    str = '- (UIView *)'+viewName+' {\n\n'+viewStr+'\n   return _'+viewName+';\n}'
    return str


def UILabelFun(viewName):
    bodyStr = CYControlsClass()
    viewStr = bodyStr.show(viewName,'UILabel')
    viewStr += '      _'+viewName+'.text = @"'+createFileName()+createFileName()+'";\n\n'
    color = ['blackColor','darkGrayColor','lightGrayColor','whiteColor','grayColor','redColor','greenColor','blueColor','cyanColor','yellowColor','magentaColor','orangeColor','purpleColor','brownColor']
    viewStr += '      _'+viewName+'.textColor = [UIColor '+color[random.randint(0,13)]+'];\n\n'
    adjustState = random.randint(0,1)
    if(adjustState == 1):
        viewStr += '      _'+viewName+'.adjustsFontSizeToFitWidth = YES;\n\n'
    textAligmentState = random.randint(0,1)
    if(textAligmentState == 1):
        viewStr += '      _'+viewName+'.textAlignment = NSTextAlignmentCenter;\n\n'
    viewStr = '   if (!_'+viewName+') {\n\n' + viewStr + '   }\n'
    str = '- (UILabel *)'+viewName+' {\n\n'+viewStr+'\n   return _'+viewName+';\n}'
    return str


def UIButtonFun(viewName,btnClick):
    bodyStr = CYControlsClass()
    viewStr = bodyStr.show(viewName,'UIButton')
#    [btn addTarget:self action:@selector(123) forControlEvents:UIControlEventTouchUpInside];
    btnClickName = createFileName()
    viewStr += '      [_'+viewName+' addTarget:self action:@selector('+btnClickName+') forControlEvents:UIControlEventTouchUpInside];\n\n'
    viewStr = '   if (!_'+viewName+') {\n\n' + viewStr + '   }\n'
    str = '- (UIButton *)'+viewName+' {\n\n'+viewStr+'\n   return _'+viewName+';\n}'
#    定义点击事件
    clickEvent = '-(void)'+btnClickName+'{\n\n  '+btnClick+'\n\n}'
    str = str + '\n' +clickEvent
    return str


def UIImageViewFun(viewName):
    bodyStr = CYControlsClass()
    viewStr = bodyStr.show(viewName,'UIImageView')
#    img.image = [UIImage imageNamed:@""];
    viewStr += '      _'+viewName+'.image = [UIImage imageNamed:@"'+createImage()+'"];'
    viewStr = '   if (!_'+viewName+') {\n\n' + viewStr + '\n   }\n'
    str = '- (UIImageView *)'+viewName+' {\n\n'+viewStr+'\n   return _'+viewName+';\n}'
    return str


def UITextViewFun(viewName):
    bodyStr = CYControlsClass()
    viewStr = bodyStr.show(viewName,'UITextView')
    viewStr += '      _'+viewName+'.text = @"'+createFileName()+createFileName()+'";\n\n'
    color = ['blackColor','darkGrayColor','lightGrayColor','whiteColor','grayColor','redColor','greenColor','blueColor','cyanColor','yellowColor','magentaColor','orangeColor','purpleColor','brownColor']
    viewStr += '      _'+viewName+'.textColor = [UIColor '+color[random.randint(0,13)]+'];\n\n'
    textAligmentState = random.randint(0,1)
    if(textAligmentState == 1):
        viewStr += '      _'+viewName+'.textAlignment = NSTextAlignmentCenter;\n\n'
    viewStr = '   if (!_'+viewName+') {\n\n' + viewStr + '   }\n'
    str = '- (UITextView *)'+viewName+' {\n\n'+viewStr+'\n   return _'+viewName+';\n}'
    return str


def UIActivityIndicatorViewFun(viewName):
    bodyStr = CYControlsClass()
    viewStr = bodyStr.show(viewName,'UIActivityIndicatorView')
    viewStr += '      _'+viewName+'.hidesWhenStopped = YES;\n\n'
    
    viewStr += '      [_'+viewName+' startAnimating];\n\n'
    viewStr = '   if (!_'+viewName+') {\n\n' + viewStr + '   }\n'
    str = '- (UIActivityIndicatorView *)'+viewName+' {\n\n'+viewStr+'\n   return _'+viewName+';\n}'
    return str

def UITableViewFun(viewName,btnClick):
    bodyStr = CYControlsClass()
    viewStr = bodyStr.show(viewName,'UITableView')
    viewStr += '      _'+viewName+'.delegate = self;\n\n'
    viewStr += '      _'+viewName+'.dataSource = self;\n\n'
    viewStr = '   if (!_'+viewName+') {\n\n' + viewStr + '   }\n'
    str = '- (UITableView *)'+viewName+' {\n\n'+viewStr+'\n   return _'+viewName+';\n}\n'
    delegateStr = '- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section{\n\n return [self.dataSourceArr count];\n\n}\n';
    statcCellId = createFileName()
    tableViewCell = '   UITableViewCell* cell = [tableView dequeueReusableCellWithIdentifier:@"'+statcCellId+'"];\n\n   if (cell == nil) {\n\n      cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:@"'+statcCellId+'"];\n\n   }\n\n   return cell;'
    delegateStr += '- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath{\n\n'+tableViewCell+' \n}\n';
    str += delegateStr;
    return str


#生成文件内容（model类）
#1 .h文件。 2  .m文件
def createFileText(fileName,fileType,MInfoFun,MinfoAttr,MparaName):
#    print "文件类型为"
#    print(fileType)
    if fileType == 1:
        attrText = createAttributesForHFile(0)
        paraName = createFileName()
        funStr = '- (instancetype)init'+fileName+':(NSDictionary*)'+paraName
        text =  [
                '#import <Foundation/Foundation.h>\n',
                '@interface '+fileName+' : NSObject\n'+attrText[0]+'\n',
                 funStr +';\n'
                '\n'
                '@end\n'
                ]
        return [text,funStr,attrText[1],paraName]
    else:
        print MinfoAttr
        FuncStr = '    self = [super init];\n\n    if(self){\n\n'
        for info in MinfoAttr:
#            print info[1] == 'NSInteger'
            if(info[1] == 'NSInteger'):
                FuncStr += '        self.'+info[0]+' = [['+MparaName+' objectForKey:@"'+info[0]+'"] integerValue];\n\n'
            elif (info[1] == 'float'):
                FuncStr += '        self.'+info[0]+' = [['+MparaName+' objectForKey:@"'+info[0]+'"] floatValue];\n\n'
            elif (info[1] == 'bool'):
                FuncStr += '        self.'+info[0]+' = [['+MparaName+' objectForKey:@"'+info[0]+'"] boolValue];\n\n'
            else:
                FuncStr += '        self.'+info[0]+' = ['+MparaName+' objectForKey:@"'+info[0]+'"];\n\n'

        FuncStr += '    }\n\n    return self;'

        text = [
                '#import \"'+fileName+'.h\"\n\n',
                '@implementation '+fileName+'\n'+MInfoFun+'{\n\n',
                FuncStr +'\n'
                '}',

                '\n',
                '@end\n'
                ]
        return  text

#    print fileName


#定义属性字符串
def createAttributesForHFile(fileType):
    resurtText = ''
    nameList = []
    if(fileType == 0):
        AttrNum = random.randint(4,7)
        for i in range(AttrNum):
            AttrDetail = random.randint(0,7)
            attrName = createFileName()
            attrType = AttributesConfig[AttrDetail][1][0]
            nameList.append([attrName,attrType])
            resurtText += '@property (nonatomic,'+AttributesConfig[AttrDetail][0][0]+')'+attrType+AttributesConfig[AttrDetail][2][0]+' '+attrName+';\n\n'
    else:
        AttrNum = random.randint(4,10)
        flag = False
        for i in range(AttrNum):
            AttrDetail = random.randint(0,6)
            if(flag==False or AttrDetail!=4):
                attrName = createFileName()
                attrType = AttributesUIConfig[AttrDetail]
                nameList.append([attrName,attrType])
                resurtText += '@property (nonatomic,strong)'+attrType+'* '+attrName+';\n\n'
                if(AttrDetail == 4):
                    flag = True


    return [resurtText,nameList]





#生成文件名  或者属性名
def createFileName():
#    文件名中单词的个数
    DCNum = random.randint(2,4)
    FileName = ''
    for i in range(DCNum):
#        print i
#     每个单词存在的字母数
        charS = ''
        DCCharsetNum = random.randint(2,7)
        for j in range(DCCharsetNum):
                s = string.ascii_letters
                r = random.choice(s)
                charS = charS + r
        
        charS = charS.capitalize()
#        print charS
        FileName = FileName + charS
    return FileName


def createImage():
    imageName = createFileName()
    extType = random.randint(0,2)
    extTypeName = '';
    if(extType == 0):
        extTypeName = '.jpg'
    elif(extType == 1):
        extTypeName = '.jpeg'
    else:
        extTypeName = '.png'
    w = random.randint(100, 150)
    h = random.randint(30,50)
    image = Image.new('RGB', (w, h), getRandomColor())
    image.save(open('./File/Resouce/' + imageName + extTypeName,'wb'))

    return imageName + extTypeName

def getRandomColor():
    '''获取一个随机颜色(r,g,b)格式的'''
    c1 = random.randint(0, 255)
    c2 = random.randint(0, 255)
    c3 = random.randint(0, 255)
    return (c1, c2, c3)


if __name__ == "__main__":
    main()
