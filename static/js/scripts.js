// Lấy tất cả các checkbox ảnh
const deleteButton = document.getElementById("delete-selected-images");

// Xử lý khi nhấn nút xóa ảnh
deleteButton.addEventListener('click', function() {
    // Lấy tất cả checkbox đã được chọn
    const selectedImages = document.querySelectorAll('.image-checkbox:checked');
    
    // Tạo danh sách ID ảnh đã chọn
    const imageIds = Array.from(selectedImages).map(checkbox => checkbox.dataset.imageId);

    if (imageIds.length > 0) {
        const confirmed = confirm(`Bạn có chắc muốn xóa ${imageIds.length} ảnh đã chọn?`);
        if (confirmed) {
            showLoading("Đang xóa ảnh...");
            deleteImages(imageIds);
        }
    } else {
        alert('Vui lòng chọn ít nhất một ảnh để xóa!');
    }
});

// Gửi yêu cầu xóa ảnh
function deleteImages(imageIds) {
    fetch('/delete_images/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Đảm bảo lấy đúng CSRF token
        },
        body: JSON.stringify({ image_ids: imageIds })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Lỗi khi gửi yêu cầu xóa ảnh.');
        }
        return response.json();
    })
    .then(data => {
        // Kiểm tra phản hồi từ server
        if (data.status === 'success') {
            alert(data.message || 'Xóa ảnh thành công!');
            // Xóa các ảnh khỏi DOM
            imageIds.forEach(id => {
                const imageElement = document.getElementById('image-' + id);
                if (imageElement) {
                    imageElement.remove();
                }
            });
        } else {
            alert(data.message || 'Có lỗi xảy ra, không thể xóa ảnh.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Có lỗi xảy ra khi xóa ảnh. Vui lòng thử lại!');
    })
    .finally(() => {
        hideLoading();
    });
}

// Hàm lấy CSRF token từ cookie
function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
    return cookieValue ? decodeURIComponent(cookieValue) : null;
}

// Hiển thị ảnh khi click vào tên ảnh
function showImage(imageUrl, imageName) {
    const imageDisplay = document.getElementById('image-display');
    const displayedImage = document.getElementById('displayed-image');
    
    displayedImage.src = imageUrl;
    imageDisplay.style.display = 'block';
}

// Ẩn ảnh hiển thị
function hideImage() {
    const imageDisplay = document.getElementById('image-display');
    const displayedImage = document.getElementById('displayed-image');

    displayedImage.src = '';
    imageDisplay.style.display = 'none';
}

// Hiển thị trạng thái loading
function showLoading(message = "Đang xử lý...") {
    let loader = document.getElementById('loader');
    if (!loader) {
        loader = document.createElement('div');
        loader.id = 'loader';
        loader.style.position = 'fixed';
        loader.style.top = '50%';
        loader.style.left = '50%';
        loader.style.transform = 'translate(-50%, -50%)';
        loader.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        loader.style.color = '#fff';
        loader.style.padding = '20px 40px';
        loader.style.borderRadius = '5px';
        loader.style.zIndex = '1000';
        loader.style.textAlign = 'center';
        document.body.appendChild(loader);
    }
    loader.innerHTML = message;
    loader.style.display = 'block';
}

// Ẩn trạng thái loading
function hideLoading() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'none';
    }
}
