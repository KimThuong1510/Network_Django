const data = {
    chat: [
      {
        name: 'Thương',
        avatar: 'https://i.pravatar.cc/150?img=1',
        preview: 'Đây là combo mới của mình...',
        time: 'March 24',
        messages: [
          { type: 'image', content: 'https://res.cloudinary.com/dyk1tfzpk/image/upload/v1744726177/pr_combo_33k_xn8qmk.png', time: '22:00 pm' },
          { type: 'outgoing', content: 'Có gì ko em', time: '22:05 pm' },
          { type: 'incoming', content: 'Đây là combo mới của mình & anh', time: '22:06 pm' }
        ],
        isGroup: false
      },
      {
        name: 'Nam',
        avatar: 'https://i.pravatar.cc/150?img=1',
        preview: 'Dạ anh, mua em luôn',
        time: 'March 24',
        messages: [
          { type: 'incoming', content: 'Dạ anh, mua em luôn', time: '21:45 pm' }
        ],
        isGroup: false
      }
    ],
    group: [
      {
        name: 'Team A',
        avatar: 'https://i.pravatar.cc/150?img=1',
        preview: 'Cả nhóm họp lúc 3h nhé',
        time: 'March 25',
        messages: [
          { type: 'incoming', content: 'Nhớ họp đúng giờ nha team', time: '15:00' },
          { type: 'outgoing', content: 'OK đầy đủ nha', time: '15:01' }
        ],
        isGroup: true
      }
    ]
  };

  let currentTab = 'chat';

  function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelector(`.tab:nth-child(${tab === 'chat' ? 1 : 2})`).classList.add('active');
    document.getElementById('group-actions').style.display = tab === 'group' ? 'flex' : 'none';
    loadConversations();
  }

  function loadConversations() {
      const list = document.getElementById('conversation-list');
      list.innerHTML = '';  // Xóa danh sách cuộc trò chuyện hiện tại
      data[currentTab].forEach((conv, index) => {
        const item = document.createElement('div');
        item.className = 'conversation-item';
        item.innerHTML = `
          <div class="avatar"><img src="${conv.avatar}" alt="${conv.name}"></div>
          <div class="conversation-details">
            <div class="conversation-header">
              <span class="name">${conv.name}</span>
              <span class="time">${conv.time}</span>
            </div>
            <div class="preview">${conv.preview}</div>
          </div>`;
        item.onclick = () => openChat(index);
        list.appendChild(item);
      });

      // Mở cuộc trò chuyện đầu tiên trong danh sách
      if (data[currentTab].length > 0) {
        openChat(0);
      } else {
        document.getElementById('chat-header').innerHTML = '';
        document.getElementById('chat-messages').innerHTML = '<p>Không có cuộc trò chuyện nào.</p>';
      }
    }



    function openChat(index) {
      const conv = data[currentTab][index];
      document.getElementById('chat-header').innerHTML = `
        <div class="avatar"><img src="${conv.avatar}" alt="${conv.name}"></div>
        <span class="name">${conv.name}</span>
        ${conv.isGroup ? `
          <i class="fas fa-plus" title="Thêm thành viên" onclick="addMember()"></i>
          <i class="fas fa-edit" title="Đổi tên nhóm" onclick="renameGroup()"></i>
          <i class="fas fa-trash-alt" title="Xóa nhóm" onclick="deleteGroup()"></i>
        ` : ''}
      `;

      const messages = document.getElementById('chat-messages');
      messages.innerHTML = '';

      conv.messages.forEach(msg => {
        let html = '';
        if (msg.type === 'image') {
          html = `
            <div class="message-container">
              <div class="message-image">
                <img src="${msg.content}" alt="image">
              </div>
              <div class="message-time">${msg.time}</div>
            </div>`;
        } else {
          html = `
            <div class="message-container ${msg.type === 'outgoing' ? 'outgoing' : ''}">
              <div class="message">
                <div class="message-content">${msg.content}</div>
              </div>
              <div class="message-time">${msg.time}</div>
            </div>`;
        }
        messages.innerHTML += html;
      });

      document.querySelectorAll('.conversation-item').forEach((el, i) => {
        el.classList.toggle('active', i === index);
      });
    }




  function searchGroup() {
    const input = document.getElementById("group-search").value.toLowerCase();
    const items = document.querySelectorAll("#conversation-list .conversation-item");

    items.forEach(item => {
      const name = item.querySelector(".name").textContent.toLowerCase();
      item.style.display = name.includes(input) ? "flex" : "none";
    });
  }

  function openCreateGroupModal() {
    document.getElementById('groupModal').style.display = 'flex';
  }

  function closeModal() {
    document.getElementById('groupModal').style.display = 'none';
  }

  function submitGroup() {
      const name = document.getElementById('groupName').value.trim();
      const checkboxes = document.querySelectorAll('.member-list input[type="checkbox"]:checked');
      const members = Array.from(checkboxes).map(cb => cb.value);
      const avatarInput = document.getElementById('groupAvatar');
      const avatarUrl = avatarInput.files.length > 0
          ? URL.createObjectURL(avatarInput.files[0])
          : "https://i.pravatar.cc/150?img=1";

      if (!name) return alert("Vui lòng nhập tên nhóm");
      if (members.length === 0) return alert("Chọn ít nhất 1 thành viên");

      // Thêm nhóm vào mảng dữ liệu và bật các chức năng cho nhóm mới
      data.group.unshift({
        name: name,
        avatar: avatarUrl,
        preview: `Nhóm ${name} đã được tạo`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        messages: [
          { type: "incoming", content: `${name} đã được tạo bởi bạn.`, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
        ],
        isGroup: true
      });

      // Chuyển sang tab nhóm và mở nhóm mới
      switchTab('group');
      openChat(0);
      closeModal();
    }


  document.querySelector('.send-btn').addEventListener('click', () => {
    const textarea = document.querySelector('.comment-box textarea');
    const content = textarea.value.trim();
    if (!content) return;

    const newMsg = {
      type: 'outgoing',
      content: content,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    data[currentTab][0].messages.push(newMsg);  // Always push to first chat group for simplicity

    openChat(0);  // Refresh chat
    textarea.value = '';  // Clear the text area
  });

  window.onload = () => switchTab('chat');

// Mở modal thêm thành viên
function addMember() {
document.getElementById('addMemberModal').style.display = 'flex';
}

// Đóng modal thêm thành viên
function closeAddMemberModal() {
document.getElementById('addMemberModal').style.display = 'none';
}

// Xử lý khi người dùng nhấn vào nút "Thêm thành viên"
function submitAddMember() {
const selectedMembers = [];
// Lấy các thành viên đã chọn
const checkboxes = document.querySelectorAll('#member-list input[type="checkbox"]:checked');
checkboxes.forEach(cb => selectedMembers.push(cb.value));

if (selectedMembers.length === 0) {
  alert("Vui lòng chọn ít nhất một thành viên.");
} else {
  alert("Thành viên đã được thêm: " + selectedMembers.join(', '));
  closeAddMemberModal();
}
}

// Hàm tìm kiếm thành viên
function searchMembers() {
const searchInput = document.getElementById('searchMember').value.toLowerCase();
const members = document.querySelectorAll('#member-list label');

members.forEach(member => {
  const name = member.textContent.toLowerCase();
  member.style.display = name.includes(searchInput) ? 'block' : 'none';
});
}



  // Mở modal đổi tên nhóm
function renameGroup() {
  document.getElementById('renameGroupModal').style.display = 'flex';
}

// Đóng modal đổi tên nhóm
function closeRenameGroupModal() {
  document.getElementById('renameGroupModal').style.display = 'none';
}

// Xử lý khi người dùng nhấn vào nút "Lưu"
function submitRenameGroup() {
  const newGroupName = document.getElementById('newGroupName').value.trim();

  if (newGroupName === "") {
    alert("Vui lòng nhập tên nhóm mới.");
  } else {
    // Cập nhật tên nhóm (Bạn có thể thay thế phần này để lưu tên nhóm vào cơ sở dữ liệu hoặc cập nhật giao diện)
    document.getElementById('chat-header').querySelector('.name').textContent = newGroupName;
    alert("Tên nhóm đã được thay đổi thành: " + newGroupName);
    closeRenameGroupModal();
  }
}


function deleteGroup() {
  const confirmDelete = confirm("Bạn có chắc muốn xóa nhóm này không?");
  if (confirmDelete) {
    data.group.shift(); // Xóa nhóm đầu tiên (hoặc dùng .splice nếu biết chỉ số)
    alert("Nhóm đã được xóa.");
    loadConversations();
    document.getElementById('chat-header').innerHTML = '';
    document.getElementById('chat-messages').innerHTML = '<p>Chọn một nhóm để bắt đầu trò chuyện.</p>';
  }
}


