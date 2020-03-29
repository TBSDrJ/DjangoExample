def htmlHead(title="", additions=""):
    httpStr = '<!DOCTYPE html>\n'
    httpStr += '<html>\n'
    httpStr += '\t<head>\n'
    httpStr += '\t\t<title>\n'
    httpStr += "\t\t\t" + title + "\n"
    httpStr += '\t\t</title>\n'
    httpStr += '\t\t<!-- Latest compiled and minified CSS -->\n'
    httpStr += '\t\t<link rel="stylesheet" '
    httpStr += 'href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">\n'
    httpStr += '\t\t<!-- jQuery library -->\n'
    httpStr += '\t\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>\n'
    httpStr += '\t\t<!-- Popper JS -->\n'
    httpStr += '\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>\n'
    httpStr += '\t\t<!-- Latest compiled JavaScript -->\n'
    httpStr += '\t\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>\n'
    httpStr += additions
    httpStr += '\t</head>\n'
    return httpStr

def htmlBody(rows=[]):
    httpStr = '\t<body>\n'
    httpStr += '\t\t<div class="container">\n'
    for row in rows:
        httpStr += str(row)
    httpStr += '\t\t</div>\n'
    httpStr += '\t</body>\n'
    httpStr += '</html>\n'
    return httpStr

class Row():
    def __init__(self, columns):
        self.columns = columns

    def __str__(self):
        rowStr = '\t\t\t<div class="row border border-dark">\n'
        for column in self.columns:
            rowStr += str(column)
        rowStr += '\t\t\t</div>\n'
        return rowStr

class Column():
    def __init__(self, numCols=1, content="&nbsp", bgColor=None, textColor=None):
        self.numCols = numCols
        self.content = content
        self.bgColor = bgColor
        self.textColor = textColor

    def __str__(self):
        httpStr = '\t\t\t\t<div class="col-' + str(self.numCols)
        if self.bgColor:
            httpStr += ' bg-' + self.bgColor
        if self.textColor:
            httpStr += ' text-' + self.textColor
        httpStr += '">\n'
        httpStr += '\t\t\t\t\t' + self.content + '\n'
        httpStr += '\t\t\t\t</div>\n'
        return httpStr
