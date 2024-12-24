// Lấy tất cả các checkbox ảnh
const deleteButton = document.getElementById("delete-selected-images");

// Xử lý khi nhấn nút xóa ảnh
deleteButton.addEventListener('click', function() {
    // Lấy tất cả checkbox đã được chọn
    const selectedImages = document.querySelectorAll('.image-checkbox:checked');
    
    // Tạo danh sách ID ảnh đã chọn
    const imageIds = Array.from(selectedImages).map(function(checkbox) {
        return checkbox.dataset.imageId;
    });
    
    if (imageIds.length > 0) {
        // Gửi yêu cầu xóa các ảnh đã chọn
        deleteImages(imageIds);
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
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Xóa các ảnh khỏi DOM
            imageIds.forEach(id => {
                const imageElement = document.getElementById('image-' + id);
                if (imageElement) {
                    imageElement.remove();
                }
            });

            // Gọi lại dữ liệu ảnh mới từ server (reload danh sách ảnh)
            loadImages();
        } else {
            alert('Có lỗi xảy ra khi xóa ảnh.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Hàm lấy CSRF token từ cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Hàm tải lại danh sách ảnh sau khi xóa
function loadImages() {
    fetch('/get_images/')
        .then(response => response.json())
        .then(data => {
            // Xử lý dữ liệu ảnh trả về từ server và cập nhật lại giao diện
            const imageListContainer = document.querySelector('.image-list');
            imageListContainer.innerHTML = ''; // Xóa danh sách ảnh cũ
            data.images.forEach(image => {
                const imageItem = document.createElement('div');
                imageItem.classList.add('image-item');
                imageItem.id = 'image-' + image.id;
                imageItem.innerHTML = `
                    <input type="checkbox" class="image-checkbox" data-image-id="${image.id}">
                    <a href="#" onclick="showImage('${image.url}', '${image.name}')">${image.name}</a>
                `;
                imageListContainer.appendChild(imageItem);
            });
        })
        .catch(error => console.error('Error:', error));
}


// Hàm hiển thị/ẩn ảnh khi click vào tên ảnh
function toggleImageVisibility(imageLink) {
    const imageDisplay = document.getElementById('image-display');  // Vùng hiển thị ảnh
    const displayedImage = document.getElementById('displayed-image');  // Ảnh đã hiển thị
    const imageUrl = imageLink.dataset.imageUrl;  // Lấy URL ảnh từ data attribute của tên ảnh

    // Kiểm tra nếu ảnh đang được hiển thị
    if (imageDisplay.style.display === 'block') {
        // Nếu ảnh đang hiển thị và click vào ảnh đó, thì ẩn ảnh đi
        imageDisplay.style.display = 'none';
    } else {
        // Nếu ảnh chưa hiển thị hoặc click vào một ảnh khác, hiển thị ảnh
        displayedImage.src = imageUrl;
        imageDisplay.style.display = 'block';
    }
}

// Chức năng gọi hàm khi click vào tên ảnh
function setupImageClickHandlers() {
    const imageLinks = document.querySelectorAll('.image-link');  // Chọn tất cả các tên ảnh
    
    // Duyệt qua từng tên ảnh và gán sự kiện click
    imageLinks.forEach(function(imageLink) {
        imageLink.addEventListener('click', function(event) {
            // event.preventDefault();  // Ngừng hành động mặc định (chuyển trang)
            toggleImageVisibility(imageLink);  // Gọi hàm hiển thị/ẩn ảnh
        });
    });
}

// Đảm bảo rằng hàm này được gọi khi DOM được tải đầy đủ
document.addEventListener('DOMContentLoaded', function() {
    setupImageClickHandlers();  // Thiết lập sự kiện click cho các tên ảnh
});



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

// Cập nhật lại danh sách ảnh
function updateImageList() {
    fetch('/get_image_list/')  // Gọi API để lấy danh sách ảnh mới
        .then(response => response.json())
        .then(data => {
            const imageListContainer = document.querySelector('.image-list');
            imageListContainer.innerHTML = ''; // Xóa nội dung hiện tại
            
            data.images.forEach(image => {
                // Tạo lại danh sách ảnh với ảnh mới
                const imageItem = document.createElement('div');
                imageItem.classList.add('image-item');
                imageItem.id = 'image-' + image.id;

                // Thêm checkbox
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.classList.add('image-checkbox');
                checkbox.dataset.imageId = image.id;

                // Thêm tên ảnh
                const imageLink = document.createElement('a');
                imageLink.href = '#';
                imageLink.textContent = image.name;
                imageLink.onclick = function() {
                    showImage(image.url, image.name);
                };

                // Thêm vào container danh sách
                imageItem.appendChild(checkbox);
                imageItem.appendChild(imageLink);
                imageListContainer.appendChild(imageItem);
            });
        })
        .catch(error => console.error('Error:', error));
}
