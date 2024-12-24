from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import requests
from .models import AnnotatedImage
from .forms import ImageUploadForm
from django.http import JsonResponse
from .models import Region, AnnotatedImage
import json
from .models import Image
from django.http import Http404

@login_required
def home(request):
    return render(request, 'main/home.html')

# View để xử lý đăng nhập
def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('home') 

    if 'logged_out' in request.GET:
        messages.info(request, "Bạn đã đăng xuất thành công.")
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Sau khi đăng nhập thành công, chuyển đến trang chủ
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')  # Hiển thị lỗi đăng nhập
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

# View để xử lý đăng xuất
def logout_view(request):
    logout(request)
    return redirect('login')  # Chuyển hướng đến trang login sau khi đăng xuất

# View để xử lý đăng ký người dùng
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Bạn có thể đăng nhập ngay.")
            return redirect('login')
        else:
            messages.error(request, "Đăng ký không thành công. Vui lòng kiểm tra lại.")
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# View đã có cho việc upload file
@login_required
def upload_file_ocr(request):
    result_text = ""  # Biến này để lưu kết quả trả về từ API
    result_data = []  # Danh sách chứa tất cả kết quả từ API
    error_message = None  # Biến này để lưu thông báo lỗi nếu có

    if request.method == 'POST' and request.FILES.get('file'):
        # Nhận tệp từ yêu cầu POST
        file = request.FILES['file']

        try:
            # Lưu tệp vào hệ thống file
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)  # URL để hiển thị tệp đã tải lên trong trình duyệt

            # Lấy đường dẫn hệ thống đầy đủ của tệp
            file_path = fs.path(filename)  # Sử dụng fs.path thay vì fs.url để lấy đường dẫn hệ thống

            # Gọi API với tệp đã tải lên
            api_url = 'http://127.0.0.1:8003/upload_pdf'
            with open(file_path, 'rb') as f:  # Mở tệp từ đường dẫn hệ thống
                files = {'file': f}
                response = requests.post(api_url, files=files)
                
                # Kiểm tra trạng thái HTTP trả về
                if response.status_code == 200:
                    try:
                        result = response.json()  # Giả sử API trả về JSON
                        
                        # In ra kết quả trả về từ API để kiểm tra cấu trúc
                        print(result)

                        # Xử lý và hiển thị kết quả theo cấu trúc trả về từ API
                        if isinstance(result, list):
                            result_text = []
                            for item in result:
                                label = item.get('label', 'No label')
                                text = item.get('text', 'No text')

                                # Nếu 'text' là một danh sách, nối các phần tử trong danh sách thành chuỗi
                                if isinstance(text, list):
                                    text = " ".join(text)
                                elif isinstance(text, dict):
                                    text = " ".join(f"{key}: {value}" for key, value in text.items())

                                # Kết hợp label và text vào một chuỗi dễ đọc
                                result_text.append(f"{label}: {text}")

                            # Nối các phần tử lại thành một chuỗi
                            result_text = "\n".join(result_text)
                        else:
                            error_message = "API response không phải là danh sách hợp lệ."
                    except ValueError:
                        error_message = "Không thể parse JSON từ API."
                else:
                    error_message = f"API lỗi: {response.status_code}"

        except Exception as e:
            # Xử lý lỗi khi lưu tệp hoặc các lỗi khác
            error_message = f"Lỗi khi tải tệp lên: {str(e)}"

    elif request.method == 'POST' and not request.FILES.get('file'):
        error_message = "Vui lòng chọn một tệp để tải lên."

    return render(request, 'main/ocr_data.html', {'result_text': result_text, 'error_message': error_message})

def upload_and_annotate(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ImageUploadForm()
    
    images = AnnotatedImage.objects.all()
    return render(request, 'annotate.html', {'form': form, 'images': images})

def save_annotations(request, image_id):
    if request.method == 'POST':
        try:
            image = AnnotatedImage.objects.get(id=image_id)
        except AnnotatedImage.DoesNotExist:
            raise Http404("Image not found.")
        
        regions = request.POST.getlist('regions')
        for region_data in regions:
            data = json.loads(region_data)
            Region.objects.create(
                image=image,
                x=data['x'],
                y=data['y'],
                width=data['width'],
                height=data['height'],
                label=data['label']
            )
        return JsonResponse({'status': 'success'})   

def delete_image(request):
    if request.method == 'POST':
        # Nhận danh sách ID ảnh cần xóa
        data = json.loads(request.body)
        image_ids = data.get('image_ids', [])
        
        if image_ids:
            # Lọc các ảnh cần xóa theo ID
            images = Image.objects.filter(id__in=image_ids)
            
            # Xóa các ảnh
            images.delete()
            
            return JsonResponse({'status': 'success', 'message': 'Images deleted successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No images selected for deletion.'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)