from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from KrillApp.forms import ImageForm,TripForm
from KrillApp.models import Image, Trip

def Upload_Image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST ,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_name = request.user.username
            instance.user=request.user
            instance.save()
            return HttpResponseRedirect('/images_successful')
    else:
        form = ImageForm()
    return render(request, 'images_upload.html', {'form':form})

def Create_Trip(request):
    if request.method == 'POST':
        form  = TripForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user=request.user
            instance.save()
            return HttpResponseRedirect('/view_trips')
    else:
        form = TripForm()
    return render(request,'create_trip.html', {'form':form})


def Get_User_Images(request):
    sql = 'SELECT * FROM Krillapp_image WHERE user_id="' + str(request.user.id) + '";'
    urls = []
    images = Image.objects.raw(sql)
    for image in images:
        urls.append(str(image.image_file).replace("user_"+str(request.user.id),""))
    return render(request ,'images_view.html', {'images':images,'urls':urls})

def Get_User_Trips(request):
    #sql = 'SELECT * FROM Krillapp_trip WHERE user_id="' + str(request.user.id) + '";'
    sql = 'SELECT * FROM Krillapp_trip;'
    trip_list = []
    trips = Trip.objects.raw(sql)
    for trip in trips:
        trip_list.append(str(trip.trip_name))
    return render(request ,'view_trips.html', {'trip_list':trip_list})

def Get_Trip_Image_List(request):
    sql = 'SELECT * FROM Krillapp_image WHERE trip_name_id="' + str(request.POST['trip_to_get']) + '";'
    trip_image_list = []
    images = Image.objects.raw(sql)
    for image in images:
        trip_image_list.append(str(image.image_file))
    return JsonResponse({
        'trip_image_list':trip_image_list,
    })

def Delete_Trip(request):
    Trip.objects.filter(trip_name_id=request.POST['trip_to_delete']).delete()
    return HttpResponseRedirect('/view_trips')


def Upload_Image_To_Trip(request):
    if request.method == 'POST':
        form = ImageForm(request.POST ,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_name = request.user.username
            instance.user=request.user
            instance.save()
            return HttpResponseRedirect('/view_trips')
    else:
        form = ImageForm()
    return render(request,'upload_image_to_trip.html',{'form':form})




def Delete_User_Image(request):
    Image.objects.filter(image_file=request.POST['image_url']).delete()
    return HttpResponseRedirect('/view_trips')


def View_Trip_Image(request):
    html = render_to_string('view_trip_image.html',{'image_url':request.POST['image_url']},request=request)
    return HttpResponse(html)
