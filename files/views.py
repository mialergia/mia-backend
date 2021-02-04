from django.shortcuts import HttpResponse


def send_file(request, filename):
    pdf_name = 'pdfs/{}'.format(filename)
    file_ = open(pdf_name, 'rb')
    response = HttpResponse(content=file_)
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response
