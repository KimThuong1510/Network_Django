document.addEventListener('DOMContentLoaded', function () {
  // ======= XỬ LÝ LIKE / COMMENT =======
  function toggleLike(button) {
    button.classList.toggle('liked');
    const icon = button.querySelector('i');
    icon.classList.toggle('far');
    icon.classList.toggle('fas');
  }

  function toggleComment(button) {
    const post = button.closest('.post');
    const commentInput = post.querySelector('.comment-input');
    if (commentInput) {
      const isVisible = commentInput.style.display === 'flex';
      commentInput.style.display = isVisible ? 'none' : 'flex';
      button.classList.toggle('active', !isVisible);
    }
  }

  // ======= TÌM KIẾM NGƯỜI DÙNG =======
  const users = [
    { name: 'Duy Anh', id: 1 },
    { name: 'Duy Kien', id: 2 },
    { name: 'Duy Hoang', id: 3 },
    { name: 'Nguyen Duy', id: 4 },
    { name: 'Duy Minh', id: 5 },
    { name: 'Duy Bao', id: 6 },
    { name: 'Duy Thanh', id: 7 }
  ];

  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  const overlay = document.getElementById('overlay');

  if (searchInput && searchResults && overlay) {
    searchInput.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        searchUsers();
      }
    });

    overlay.addEventListener('click', function () {
      searchResults.classList.remove('show');
      overlay.classList.remove('show');
    });
  }

  function searchUsers() {
    const query = searchInput.value.trim().toLowerCase();
    if (query.length > 0) {
      const filteredUsers = users.filter(user =>
        user.name.toLowerCase().includes(query)
      );

      let resultsHtml = '';
      const topResults = filteredUsers.slice(0, 5);
      topResults.forEach(user => {
        resultsHtml += `
          <div class="result-item">
            <span>${user.name}</span>
            <button class="add-friend-btn">Kết bạn</button>
          </div>
        `;
      });

      if (filteredUsers.length > 5) {
        resultsHtml += `<div id="view-all">Xem tất cả</div>`;
      }

      searchResults.innerHTML = resultsHtml;
      searchResults.classList.add('show');
      overlay.classList.add('show');
    } else {
      searchResults.classList.remove('show');
      overlay.classList.remove('show');
    }
  }

  // ======= XỬ LÝ GỬI BÌNH LUẬN =======
  function sendComment(postId) {
    const commentContent = document.getElementById('comment-content').value;  // Lấy nội dung bình luận

    if (commentContent.trim() === '') {
      alert('Bạn cần nhập bình luận');
      return;
    }

    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;  // Lấy CSRF token

    // Gửi yêu cầu POST đến server để lưu bình luận
    fetch(`/comment/${postId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrfToken
      },
      body: `content=${encodeURIComponent(commentContent)}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert('Có lỗi xảy ra khi thêm bình luận');
      } else {
        // Cập nhật giao diện để hiển thị bình luận mới
        const commentList = document.querySelector('.comments-list');
        const newComment = document.createElement('div');
        newComment.classList.add('comment');
        newComment.innerHTML = `
          <div class="comment" data-id="${data.id}">
            <img class="comment-avatar" src="${data.avatar_url}" alt="Avatar">
            <div class="comment-content">
              <strong>${data.user}</strong>: ${data.content}
            </div>
            <span class="comment-time">${data.created_at}</span>
          </div>
        `;
        commentList.appendChild(newComment);

        // Xóa nội dung đã nhập trong form
        document.getElementById('comment-content').value = '';

        // Ẩn form bình luận sau khi gửi
        toggleComment(document.querySelector('.comment-btn'));
      }
    })
    .catch(error => alert('Có lỗi xảy ra khi gửi bình luận'));
  }
});
