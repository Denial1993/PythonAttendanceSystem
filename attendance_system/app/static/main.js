// ============================================================
// 智能打卡系統 - 主要前端邏輯
// 從 inline script 移出為外部靜態檔案，避免 CSP 封鎖問題
// ============================================================

let currentEmployeeName = localStorage.getItem('employee_name');

// ✅ 使用 DOMContentLoaded，確保所有 include 的 HTML 片段都已載入後再執行
document.addEventListener('DOMContentLoaded', function () {
    // 初始化 chatInput 鍵盤事件
    const chatInputEl = document.getElementById('chatInput');
    if (chatInputEl) {
        chatInputEl.addEventListener('keypress', e => {
            if (e.key === 'Enter') sendChatMessage();
        });
    }

    if (currentEmployeeName) {
        setupDashboardAuth();
    } else {
        switchSection('authView');
    }
});

// --------------------------------------------------------
// 通知
// --------------------------------------------------------
function showNotification(message, isError = false) {
    const notif = document.getElementById('notification');
    if (!notif) return;
    notif.textContent = message;
    notif.style.borderLeft = isError ? "4px solid #f87171" : "4px solid #4ade80";
    notif.classList.add('show');
    setTimeout(() => notif.classList.remove('show'), 3000);
}

// --------------------------------------------------------
// Navbar 分頁切換
// --------------------------------------------------------
function switchSection(sectionId) {
    document.querySelectorAll('.section-view').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));

    const navMenu = document.getElementById('navMenu');
    const navUser = document.getElementById('navUser');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');

    if (sectionId === 'authView') {
        const authView = document.getElementById('authView');
        if (authView) authView.classList.add('active');
        if (navMenu) navMenu.style.display = 'none';
        if (navUser) navUser.style.display = 'none';
        if (mobileMenuBtn) mobileMenuBtn.style.display = 'none';
    } else {
        const sectionEl = document.getElementById('section-' + sectionId);
        if (sectionEl) sectionEl.classList.add('active');
        const activeLink = document.querySelector(`.nav-link[onclick="switchSection('${sectionId}')"]`);
        if (activeLink) activeLink.classList.add('active');

        if (navMenu) navMenu.classList.remove('show');

        if (sectionId === 'home') { loadPersonalStatus(); loadBoardData(); }
        if (sectionId === 'stats') { loadMyProfile(); loadMonthlySummary(); }
        if (sectionId === 'leave') { loadMyLeaves(); loadPendingLeaves(); }
        if (sectionId === 'staff') { loadStaffList(); }
    }
}

function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) navMenu.classList.toggle('show');
}

function setupDashboardAuth() {
    const navMenu = document.getElementById('navMenu');
    const navUser = document.getElementById('navUser');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const displayName = document.getElementById('displayEmployeeName');

    if (navMenu) navMenu.style.display = '';
    if (navUser) navUser.style.display = '';
    if (mobileMenuBtn) mobileMenuBtn.style.display = '';
    if (displayName) displayName.textContent = currentEmployeeName;

    const role = localStorage.getItem('role');
    const navStaffList = document.getElementById('navStaffList');
    const searchTarget = document.getElementById('searchTargetEmployee');
    const leaveApprovalBlock = document.getElementById('leaveApprovalBlock');
    const everyoneBoard = document.getElementById('everyoneBoardContainer');
    const profileSalaryRow = document.getElementById('profileSalaryRow');

    if (role === '1' || role === '2') {
        if (navStaffList) navStaffList.style.display = 'block';
        if (searchTarget) searchTarget.style.display = 'block';
        if (leaveApprovalBlock) leaveApprovalBlock.style.display = 'block';
        if (everyoneBoard) everyoneBoard.style.display = 'block';
    } else {
        if (navStaffList) navStaffList.style.display = 'none';
        if (searchTarget) searchTarget.style.display = 'none';
        if (leaveApprovalBlock) leaveApprovalBlock.style.display = 'none';
        if (everyoneBoard) everyoneBoard.style.display = 'none';
        if (profileSalaryRow) profileSalaryRow.style.display = 'none';
    }

    const todayStr = new Date().toLocaleDateString('en-CA');
    const searchStart = document.getElementById('searchStartDate');
    const searchEnd = document.getElementById('searchEndDate');
    const monthPicker = document.getElementById('monthPicker');
    if (searchStart) searchStart.value = todayStr;
    if (searchEnd) searchEnd.value = todayStr;
    if (monthPicker) monthPicker.value = todayStr.substring(0, 7);

    switchSection('home');
}

// --------------------------------------------------------
// Auth API
// --------------------------------------------------------
function switchAuthTab(idx) {
    const tab0 = document.getElementById('tab0');
    const tab1 = document.getElementById('tab1');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    if (tab0) tab0.classList.remove('active');
    if (tab1) tab1.classList.remove('active');
    const activeTab = document.getElementById(`tab${idx}`);
    if (activeTab) activeTab.classList.add('active');
    if (loginForm) loginForm.style.display = idx === 0 ? 'block' : 'none';
    if (registerForm) registerForm.style.display = idx === 1 ? 'block' : 'none';
}

async function performLogin() {
    const u = document.getElementById('loginUsername').value;
    const p = document.getElementById('loginPassword').value;
    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: u, password: p })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem('employee_name', data.employee_name);
            localStorage.setItem('username', u);
            localStorage.setItem('role', String(data.role));
            currentEmployeeName = data.employee_name;
            setupDashboardAuth();
        } else {
            showNotification(data.detail, true);
        }
    } catch (err) {
        showNotification("連線錯誤", true);
    }
}

async function performRegister() {
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    const employeeName = document.getElementById('regEmployeeName').value;

    if (!username || !password || !employeeName) {
        alert("請填寫所有欄位！");
        return;
    }

    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username,
                password: password,
                employee_name: employeeName
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("註冊成功！請登入。");
            switchAuthTab(0);
        } else {
            alert("註冊失敗：" + (data.detail || "未知錯誤"));
        }
    } catch (error) {
        console.error("發生錯誤:", error);
        alert("連線伺服器失敗！");
    }
}

function performLogout() {
    localStorage.clear();
    currentEmployeeName = null;
    switchSection('authView');
}

// --------------------------------------------------------
// 打卡 API
// --------------------------------------------------------
async function performAction(action) {
    try {
        const res = await fetch(
            `/api/attendance/?employee_name=${encodeURIComponent(currentEmployeeName)}&action=${encodeURIComponent(action)}`,
            { method: 'POST', headers: { 'Content-Type': 'application/json' } }
        );
        const data = await res.json();
        if (res.ok) {
            showNotification(`成功打卡：${action}`);
            loadPersonalStatus();
            loadBoardData();
        } else {
            showNotification(data.detail, true);
        }
    } catch (e) {
        showNotification("連線錯誤", true);
    }
}

async function loadPersonalStatus() {
    try {
        const res = await fetch(`/api/attendance/${encodeURIComponent(currentEmployeeName)}`);
        const data = await res.json();
        if (data.length > 0) {
            const rec = data[0];
            const statusVal = document.getElementById('statusVal');
            const valCheckIn = document.getElementById('valCheckIn');
            const valCheckOut = document.getElementById('valCheckOut');
            if (statusVal) statusVal.textContent = rec.status;
            if (valCheckIn) valCheckIn.textContent = rec.check_in_time ? rec.check_in_time.substring(0, 5) : '-';
            if (valCheckOut) valCheckOut.textContent = rec.check_out_time ? rec.check_out_time.substring(0, 5) : '-';
        }
    } catch (e) { }
}

async function loadBoardData() {
    if (localStorage.getItem('role') === '3') return;
    try {
        const res = await fetch(`/api/attendance/today?username=${localStorage.getItem('username')}`);
        const data = await res.json();
        const list = document.getElementById('boardList');
        if (list) {
            list.innerHTML = data.map(r =>
                `<div class="board-item"><span>${r.employee_name}</span> <span class="status-work">${r.status} ${r.check_in_time?.substring(0, 5) || ''}</span></div>`
            ).join('');
        }
    } catch (e) { }
}

// --------------------------------------------------------
// AI 聊天室
// --------------------------------------------------------
async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;
    const body = document.getElementById('chatBody');
    body.innerHTML += `<div class="chat-msg msg-user">${text}</div>`;
    input.value = '';
    body.scrollTop = body.scrollHeight;
    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_name: currentEmployeeName, query: text })
        });
        const data = await res.json();
        body.innerHTML += `<div class="chat-msg msg-bot">${data.reply || "錯誤"}</div>`;
        body.scrollTop = body.scrollHeight;
    } catch (e) { }
}

function toggleChat() {
    const chatPanel = document.getElementById('chatPanel');
    if (chatPanel) chatPanel.classList.toggle('open');
}

// --------------------------------------------------------
// 個人資料
// --------------------------------------------------------
let isEditingProfile = false;

function toggleEditProfile() {
    isEditingProfile = !isEditingProfile;
    if (isEditingProfile) {
        document.getElementById('profileViewMode').style.display = 'none';
        document.getElementById('profileEditMode').style.display = 'block';
        document.getElementById('editProfileBtn').style.display = 'none';

        document.getElementById('editProfileName').textContent = currentEmployeeName;
        const currentPhone = document.getElementById('profilePhone').textContent;
        const currentAddress = document.getElementById('profileAddress').textContent;
        const currentSalary = document.getElementById('profileSalary').textContent;

        document.getElementById('editProfilePhone').value = currentPhone !== '-' ? currentPhone : '';
        document.getElementById('editProfileAddress').value = currentAddress !== '-' ? currentAddress : '';
        document.getElementById('editProfileSalary').value = currentSalary !== '-' ? currentSalary : '';

        if (localStorage.getItem('role') === '3') {
            document.getElementById('editSalaryRow').style.display = 'none';
        }
    } else {
        document.getElementById('profileViewMode').style.display = 'block';
        document.getElementById('profileEditMode').style.display = 'none';
        document.getElementById('editProfileBtn').style.display = 'block';
    }
}

async function saveProfile() {
    const phone = document.getElementById('editProfilePhone').value;
    const address = document.getElementById('editProfileAddress').value;
    const salary = document.getElementById('editProfileSalary').value;
    const username = localStorage.getItem('username');

    try {
        const res = await fetch('/api/users/me', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, phone: phone, address: address, salary: salary ? parseInt(salary) : null })
        });
        const data = await res.json();

        if (res.ok) {
            showNotification("個人資料更新成功！");
            document.getElementById('profilePhone').textContent = data.phone || '-';
            document.getElementById('profileAddress').textContent = data.address || '-';
            document.getElementById('profileSalary').textContent = data.salary || '-';
            toggleEditProfile();
        } else {
            showNotification(data.detail || "更新失敗", true);
        }
    } catch (e) {
        showNotification("連線錯誤", true);
    }
}

async function loadMyProfile() {
    const username = localStorage.getItem('username');
    if (!username) return;

    try {
        const res = await fetch(`/api/users/me?username=${username}`);
        const data = await res.json();
        if (res.ok) {
            const profileName = document.getElementById('profileName');
            const profilePhone = document.getElementById('profilePhone');
            const profileAddress = document.getElementById('profileAddress');
            const profileSalary = document.getElementById('profileSalary');
            if (profileName) profileName.textContent = data.employee_name || currentEmployeeName;
            if (profilePhone) profilePhone.textContent = data.phone || '-';
            if (profileAddress) profileAddress.textContent = data.address || '-';
            if (profileSalary) profileSalary.textContent = data.salary || '-';
        }
    } catch (e) { }
}

// --------------------------------------------------------
// 其他功能（待實作）
// --------------------------------------------------------
async function loadMonthlySummary() { }
async function loadStaffList() { }
async function loadMyLeaves() { }
async function loadPendingLeaves() { }
async function performSearch() { }
async function submitLeaveRequest() { }
