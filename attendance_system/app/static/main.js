// ============================================================
// 智能打卡系統 - 主要前端邏輯
// 從 inline script 移出為外部靜態檔案，避免 CSP 封鎖問題
// ============================================================

let currentEmployeeName = localStorage.getItem('employee_name');

// ✅ 使用 DOMContentLoaded，確保所有 include 的 HTML 片段都已載入後再執行
document.addEventListener('DOMContentLoaded', function () {
    // 綁定認證相關按鈕事件 (取代 HTML onclick 避免 CSP 封鎖)
    const tab0 = document.getElementById('tab0');
    if (tab0) tab0.addEventListener('click', () => switchAuthTab(0));
    const tab1 = document.getElementById('tab1');
    if (tab1) tab1.addEventListener('click', () => switchAuthTab(1));
    const btnLogin = document.getElementById('btnLogin');
    if (btnLogin) btnLogin.addEventListener('click', performLogin);
    const btnRegister = document.getElementById('btnRegister');
    if (btnRegister) btnRegister.addEventListener('click', performRegister);

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
        if (sectionId === 'settings') { loadSystemSettings(); }
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
    const navSystemSettings = document.getElementById('navSystemSettings');

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

    if (role === '1') {
        if (navSystemSettings) navSystemSettings.style.display = 'block';
    } else {
        if (navSystemSettings) navSystemSettings.style.display = 'none';
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
        showNotification("無法連接伺服器，請檢查網路", true);
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
        alert("無法連接伺服器，請檢查網路");
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
async function sendCheckInRequest(action, lat, lng) {
    try {
        let url = `/api/attendance/?employee_name=${encodeURIComponent(currentEmployeeName)}&action=${encodeURIComponent(action)}`;
        if (lat !== null && lng !== null) {
            url += `&lat=${lat}&lng=${lng}`;
        }
        const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' } });
        const data = await res.json();
        if (res.ok) {
            showNotification(`成功打卡：${action}`);
            loadPersonalStatus();
            loadBoardData();
        } else {
            showNotification(data.detail || "打卡失敗", true);
        }
    } catch (e) {
        showNotification("無法連接伺服器，請檢查網路", true);
    }
}

function getPositionWithTimeout() {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        });
        setTimeout(() => reject(new Error("Timeout")), 5000);
    });
}

async function performAction(action) {
    if (!navigator.geolocation) {
        showNotification("無法獲取定位，將以無座標模式打卡", true);
        return sendCheckInRequest(action, null, null);
    }

    showNotification("正在獲取GPS定位以進行打卡...", false);

    try {
        const position = await getPositionWithTimeout();
        sendCheckInRequest(action, position.coords.latitude, position.coords.longitude);
    } catch (error) {
        showNotification("無法獲取定位，將以無座標模式打卡", true);
        sendCheckInRequest(action, null, null);
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
            list.innerHTML = data.map(r => {
                let mapBtnStr = '';
                if (localStorage.getItem('role') === '1') {
                    if (r.check_in_lat && r.check_in_lng) {
                        mapBtnStr += ` <i class="fa fa-map-marker-alt" style="cursor:pointer;color:#4ade80;" title="上班位置" onclick="openMapModal(${r.check_in_lat}, ${r.check_in_lng}, '${r.employee_name} 上班打卡地點')"></i>`;
                    }
                    if (r.check_out_lat && r.check_out_lng) {
                        mapBtnStr += ` <i class="fa fa-map-marker-alt" style="cursor:pointer;color:#f87171;" title="下班位置" onclick="openMapModal(${r.check_out_lat}, ${r.check_out_lng}, '${r.employee_name} 下班打卡地點')"></i>`;
                    }
                }
                return `<div class="board-item"><span>${r.employee_name}</span> <span class="status-work">${r.status} ${r.check_in_time?.substring(0, 5) || ''}${mapBtnStr}</span></div>`;
            }).join('');
        }
    } catch (e) { }
}

// --------------------------------------------------------
// 地圖 Modal
// --------------------------------------------------------
let mapInstance = null;
let currentMarker = null;

function openMapModal(lat, lng, titleStr) {
    const modal = document.getElementById('mapModal');
    if (modal) {
        modal.style.display = 'flex';
        // 延遲初始化以確保容器顯示後才產生地圖
        setTimeout(() => {
            if (!mapInstance) {
                mapInstance = L.map('leafletMap').setView([lat, lng], 16);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '© OpenStreetMap'
                }).addTo(mapInstance);
            } else {
                mapInstance.setView([lat, lng], 16);
                mapInstance.invalidateSize();
            }

            if (currentMarker) {
                mapInstance.removeLayer(currentMarker);
            }

            currentMarker = L.marker([lat, lng]).addTo(mapInstance)
                .bindPopup(titleStr || "打卡位置")
                .openPopup();

        }, 200);
    }
}

function closeMapModal() {
    const modal = document.getElementById('mapModal');
    if (modal) modal.style.display = 'none';
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

    if (!currentEmployeeName) {
        body.innerHTML += `<div class="chat-msg msg-bot" style="color:#f87171;">請先登入系統才能使用智能助理喔！</div>`;
        body.scrollTop = body.scrollHeight;
        return;
    }
    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ employee_name: currentEmployeeName, query: text })
        });
        const data = await res.json();
        if (res.ok) {
            body.innerHTML += `<div class="chat-msg msg-bot">${data.reply}</div>`;
        } else {
            // 如果後端噴錯，把後端的詳細錯誤訊息 (detail) 印在畫面上
            body.innerHTML += `<div class="chat-msg msg-bot" style="color:#f87171;">系統提示：${data.detail || "發生未知錯誤"}</div>`;
        }
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
    const salaryInput = document.getElementById('editProfileSalary');
    const username = localStorage.getItem('username');
    const role = localStorage.getItem('role');

    // 準備要送出的資料，先不包含薪資
    const updateData = {
        username: username,
        phone: phone,
        address: address
    };

    // 只有當使用者是管理員 (role === '1' 或 '2') 且真的有填寫薪資時，才把 salary 加入打包清單
    if ((role === '1' || role === '2') && salaryInput && salaryInput.value) {
        updateData.salary = parseInt(salaryInput.value);
    }

    try {
        const res = await fetch('/api/users/me', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updateData) // 送出過濾後的資料
        });
        const data = await res.json();

        if (res.ok) {
            showNotification("個人資料更新成功！");
            document.getElementById('profilePhone').textContent = data.phone || '-';
            document.getElementById('profileAddress').textContent = data.address || '-';
            // 如果後端有回傳新的薪資才更新畫面（避免員工看到 null）
            if (data.salary !== undefined && document.getElementById('profileSalary')) {
                document.getElementById('profileSalary').textContent = data.salary;
            }
            toggleEditProfile();
        } else {
            // 優化錯誤顯示，解決 [object Object] 的問題
            let errorMsg = '更新失敗';
            if (typeof data.detail === 'string') {
                errorMsg = data.detail;
            } else if (Array.isArray(data.detail)) {
                // 如果是 Pydantic 的 422 錯誤，抓取第一個錯誤告訴使用者是哪個欄位出包
                errorMsg = `欄位格式錯誤 (${data.detail[0].loc[1]}: ${data.detail[0].msg})`;
            }
            showNotification(errorMsg, true);
        }
    } catch (e) {
        showNotification("無法連接伺服器，請檢查網路", true);
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
async function loadMonthlySummary() {
    const monthPicker = document.getElementById('monthPicker');
    if (!monthPicker) return;

    // 取得選擇的月份字串，格式會是 "YYYY-MM"，例如 "2026-04"
    const selectedMonth = monthPicker.value;
    const employeeName = localStorage.getItem('employee_name') || currentEmployeeName;
    const username = localStorage.getItem('username'); // 抓取當前登入者帳號

    if (!selectedMonth || !employeeName) return;

    // 💡 前端工程師的魔法：把 "2026-04" 切割成整數的 year 和 month
    const parts = selectedMonth.split('-'); // 切成 ["2026", "04"]
    const year = parseInt(parts[0], 10);    // 變成數字 2026
    const month = parseInt(parts[1], 10);   // 變成數字 4 (把 04 前面的 0 去掉)

    try {
        // 配合後端的口味，重新組合 URL
        const url = `/api/attendance/summary?year=${year}&month=${month}&employee_name=${encodeURIComponent(employeeName)}&username=${encodeURIComponent(username)}`;

        const res = await fetch(url);

        if (res.ok) {
            const data = await res.json();

            // 1. 更新上方的統計數字
            document.getElementById('statWorkDays').textContent = data.work_days || 0;
            document.getElementById('statLateCount').textContent = data.late_count || 0;

            // 2. 更新下方的每日明細列表
            const detailList = document.getElementById('dailyDetailList');
            if (detailList) {
                // 👉 修正 1：改抓 daily_details
                if (data.daily_details && data.daily_details.length > 0) {
                    detailList.innerHTML = data.daily_details.map(d => {

                        // 👉 修正 2：根據後端的 boolean 值來決定顯示的文字和顏色
                        let statusText = "正常";
                        let statusColor = "#4ade80"; // 預設綠色

                        if (d.is_missing_checkin) {
                            statusText = "未打上班卡";
                            statusColor = "#f87171"; // 紅色
                        } else if (d.is_late) {
                            // 如果遲到，還可以把遲到幾分鐘加上去
                            statusText = `遲到 (${d.late_minutes}分)`;
                            statusColor = "#fb923c"; // 橘色
                        } else if (d.is_missing_checkout) {
                            statusText = "未打下班卡";
                            statusColor = "#f87171"; // 紅色
                        }

                        // 擷取時間的小時與分鐘 (例如 "15:51")，如果是 null 則顯示 "-"
                        const checkInStr = d.check_in_time ? d.check_in_time.substring(0, 5) : "-";
                        const checkOutStr = d.check_out_time ? d.check_out_time.substring(0, 5) : "-";

                        return `
                        <li style="padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; gap: 5px;">
                            <div style="display: flex; justify-content: space-between;">
                                <span><i class="fa-regular fa-calendar"></i> ${d.date}</span>
                                <span style="color: ${statusColor}; font-weight: bold;">${statusText}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: #a0a0b0;">
                                In: ${checkInStr} | Out: ${checkOutStr}
                            </div>
                        </li>`;
                    }).join('');
                } else {
                    detailList.innerHTML = '<li style="color: #a0a0b0; text-align: center; padding: 10px;">本月尚無打卡紀錄</li>';
                }
            }
        } else {
            // 優化錯誤顯示
            const errData = await res.json();
            console.error("後端錯誤:", errData);
            document.getElementById('statWorkDays').textContent = "-";
            document.getElementById('statLateCount').textContent = "-";
            document.getElementById('dailyDetailList').innerHTML = `<li style="color: #f87171; text-align: center;">無法載入資料 (${res.status})</li>`;
        }
    } catch (e) {
        console.error("統計資料連線錯誤", e);
    }
}
async function loadStaffList() {
    const tbody = document.getElementById('staffTableBody');
    if (!tbody) return;

    // 1. 顯示載入中動畫
    tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding:15px; color:#a0a0b0;"><i class="fa-solid fa-spinner fa-spin"></i> 載入資料中...</td></tr>';

    // 2. 取得當前登入者帳號 (後端通常需要用這個來檢查是否為管理員)
    const username = localStorage.getItem('username');

    try {
        // 3. 呼叫後端 API (把 username 帶過去驗證權限)
        const url = `/api/users/?username=${encodeURIComponent(username)}`;
        const res = await fetch(url);

        if (res.ok) {
            const data = await res.json();

            // 如果查無資料 (理論上不可能，至少會有自己)
            if (!data || data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding:15px; color:#a0a0b0;">目前沒有其他員工資料</td></tr>';
                return;
            }

            // 4. 把撈回來的 JSON 陣列，轉換成 HTML 表格的 <tr>
            tbody.innerHTML = data.map(user => {
                // 處理角色顯示 (根據我們之前的邏輯：1是管理員，2是主管，3是一般員工)
                let roleName = "一般員工";
                let roleColor = "#d0d0d0"; // 預設灰色

                // 如果後端傳來的是數字或字串，稍微轉換一下讓他變好看
                if (String(user.role) === '1') {
                    roleName = "系統管理員";
                    roleColor = "#fb923c"; // 橘色
                } else if (String(user.role) === '2') {
                    roleName = "人事主管";
                    roleColor = "#4ade80"; // 綠色
                }

                // 處理空值
                const phoneStr = user.phone ? user.phone : '<span style="color:#666;">未填寫</span>';

                return `
                <tr>
                    <td style="font-weight: bold;">${user.employee_name}</td>
                    <td>${phoneStr}</td>
                    <td><span style="color: ${roleColor}; border: 1px solid ${roleColor}; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem;">${roleName}</span></td>
                </tr>`;
            }).join('');

        } else {
            // 如果後端報錯 (例如 403 權限不足)
            const errData = await res.json();
            console.error("名冊讀取失敗:", errData);
            tbody.innerHTML = `<tr><td colspan="3" style="text-align:center; padding:15px; color:#f87171;">無法載入: ${errData.detail || '權限不足'}</td></tr>`;
        }
    } catch (e) {
        console.error("載入員工名冊失敗:", e);
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; padding:15px; color:#f87171;">無法連接伺服器，請檢查網路</td></tr>';
    }
}
async function loadMyLeaves() { }
async function loadPendingLeaves() { }
async function performSearch() {
    // 1. 抓取畫面上的日期與輸入框資料
    const startDate = document.getElementById('searchStartDate').value;
    const endDate = document.getElementById('searchEndDate').value;
    const targetEmployee = document.getElementById('searchTargetEmployee').value.trim();
    const resultList = document.getElementById('searchResultList');

    // 👇 新增這行：從 localStorage 取得當前登入者的帳號 (對應後端的 username)
    const currentUsername = localStorage.getItem('username');

    // 2. 基本防呆檢查
    if (!startDate || !endDate) {
        showNotification("請選擇開始與結束日期！", true);
        return;
    }

    // 顯示載入中...
    resultList.innerHTML = '<div style="color: #a0a0b0; padding: 10px;"><i class="fa-solid fa-spinner fa-spin"></i> 查詢中...</div>';

    try {
        // 3. 組合要發送給後端 Python API 的網址參數
        const queryName = targetEmployee || currentEmployeeName;

        // 👇 修改這行：把 username 也加進網址參數裡送給後端
        const url = `/api/attendance/search?start_date=${startDate}&end_date=${endDate}&employee_name=${encodeURIComponent(queryName)}&username=${encodeURIComponent(currentUsername)}`;

        // 4. 呼叫後端 API
        const res = await fetch(url);
        const data = await res.json();

        if (res.ok) {
            // 如果查無資料
            if (!data || data.length === 0) {
                resultList.innerHTML = '<div style="color: #a0a0b0; padding: 10px;">這段期間沒有打卡紀錄喔。</div>';
                return;
            }

            // 5. 把撈回來的資料變成 HTML 塞進畫面上
            resultList.innerHTML = data.map(r => {
                const checkIn = r.check_in_time ? r.check_in_time.substring(0, 5) : '未打卡';
                const checkOut = r.check_out_time ? r.check_out_time.substring(0, 5) : '未打卡';

                return `
                <div class="board-item" style="display:flex; flex-direction:column; gap:5px; align-items: flex-start;">
                    <div style="display:flex; justify-content:space-between; width: 100%;">
                        <b><i class="fa-regular fa-calendar"></i> ${r.date}</b> 
                        <span class="status-work">${r.status}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #d0d0d0;">
                        <span><i class="fa-solid fa-user"></i> ${r.employee_name}</span> |
                        <span>In: ${checkIn}</span> |
                        <span>Out: ${checkOut}</span>
                    </div>
                </div>`;
            }).join('');
        } else {
            // 👇 新增這段：優化錯誤訊息的顯示，避免再次出現 [object Object]
            let errorMsg = '查詢失敗';
            if (typeof data.detail === 'string') {
                errorMsg = data.detail; // 如果是一般錯誤 (如 403 權限不足)，直接印出字串
            } else if (Array.isArray(data.detail)) {
                errorMsg = "後端參數驗證失敗 (422)"; // 如果是陣列，給個易懂的提示
            }
            resultList.innerHTML = `<div style="color: #f87171; padding: 10px;">錯誤: ${errorMsg}</div>`;
        }
    } catch (e) {
        resultList.innerHTML = `<div style="color: #f87171; padding: 10px;">無法連接伺服器，請檢查網路狀態。</div>`;
    }
}
async function submitLeaveRequest() { }

// --------------------------------------------------------
// 系統設定
// --------------------------------------------------------
async function loadSystemSettings() {
    try {
        const res1 = await fetch(`/api/settings/company_base_lat`);
        if (res1.ok) {
            const data = await res1.json();
            document.getElementById('settingLat').value = data.setting_value || '';
        }
        const res2 = await fetch(`/api/settings/company_base_lng`);
        if (res2.ok) {
            const data = await res2.json();
            document.getElementById('settingLng').value = data.setting_value || '';
        }
    } catch (e) { }
}

async function saveSystemSettings() {
    const lat = document.getElementById('settingLat').value;
    const lng = document.getElementById('settingLng').value;
    const username = localStorage.getItem('username');

    if (!lat || !lng) {
        showNotification("經緯度不能為空", true);
        return;
    }

    try {
        const res1 = await fetch(`/api/settings/company_base_lat?username=${username}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ setting_value: lat })
        });

        const res2 = await fetch(`/api/settings/company_base_lng?username=${username}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ setting_value: lng })
        });

        if (res1.ok && res2.ok) {
            showNotification("座標設定已儲存");
        } else {
            showNotification("儲存失敗，請檢查權限", true);
        }
    } catch (e) {
        showNotification("無法連接伺服器，請檢查網路", true);
    }
}
