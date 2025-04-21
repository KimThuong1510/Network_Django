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

  // ======= FORM BÁO CÁO =======
  const overlayReport = document.getElementById('overlay-report');
  const reportForm = document.querySelector('.report-form');

  function showReportForm() {
    if (overlayReport && reportForm) {
      overlayReport.classList.add('show');
      reportForm.classList.add('show');
    }
  }

  function hideReportForm() {
    if (overlayReport && reportForm) {
      overlayReport.classList.remove('show');
      reportForm.classList.remove('show');
    }
  }

  if (overlayReport) {
    overlayReport.addEventListener('click', hideReportForm);
  }

  const reportIcons = document.querySelectorAll('.report-icon');
  reportIcons.forEach(icon => {
    icon.addEventListener('click', showReportForm);
  });

  // Expose like/comment toggle functions globally (nếu dùng inline HTML `onclick`)
  window.toggleLike = toggleLike;
  window.toggleComment = toggleComment;
});
