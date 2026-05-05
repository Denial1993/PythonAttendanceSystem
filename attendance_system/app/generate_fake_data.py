import os
import random
from datetime import date, timedelta, time, datetime
from passlib.context import CryptContext

from app.database import SessionLocal, engine
from app.models import User, Attendance, LeaveRequest, LeaveBalances, Holidays, Base
from app.routers.auth import get_password_hash

# 確保資料表已建立
Base.metadata.create_all(bind=engine)

def generate_fake_data():
    db = SessionLocal()
    try:
        # Check if users already exist
        if db.query(User).filter(User.username == "AD001").first():
            print("資料庫中已有使用者資料，為了避免重複，將略過部分資料或你可以先清空資料庫。")
            return
        
        print("開始產生假資料...")
        
        # 1. 建立使用者
        users_data = [
            {"username": "AD001", "name": "王管理", "role": 1, "salary": 80000},
            {"username": "MA001", "name": "李經理", "role": 2, "salary": 65000},
            {"username": "EM001", "name": "陳員工", "role": 3, "salary": 45000},
            {"username": "EM002", "name": "林員工", "role": 3, "salary": 42000},
            {"username": "EM003", "name": "張員工", "role": 3, "salary": 40000},
            {"username": "EM004", "name": "黃員工", "role": 3, "salary": 46000},
            {"username": "EM005", "name": "吳員工", "role": 3, "salary": 38000},
        ]
        
        db_users = []
        for ud in users_data:
            user = User(
                username=ud["username"],
                password_hash=get_password_hash("123456"), # 預設密碼 123456
                employee_name=ud["name"],
                role=ud["role"],
                phone=f"09{random.randint(10000000, 99999999)}",
                address=random.choice(["台北市信義區", "新北市板橋區", "台北市大安區", "新北市中和區", "桃園市桃園區"]) + "某某路" + str(random.randint(10, 200)) + "號",
                salary=ud["salary"],
                hire_date=date.today() - timedelta(days=random.randint(100, 1000))
            )
            db.add(user)
            db_users.append(user)
            
        db.commit()
        for u in db_users:
            db.refresh(u)
        
        print(f"已建立 {len(db_users)} 名使用者 (預設密碼皆為: 123456)")
        
        # 2. 建立請假額度
        for u in db_users:
            for leave_type in ["特休", "事假", "病假"]:
                lb = LeaveBalances(
                    user_id=u.id,
                    leave_type=leave_type,
                    total_hours=80.0 if leave_type == "特休" else 112.0,
                    used_hours=0.0,
                    valid_from=date(2026, 1, 1),
                    valid_until=date(2026, 12, 31)
                )
                db.add(lb)
        db.commit()
        print("已建立每位員工的請假額度 (特休/事假/病假)")
        
        # 3. 建立出勤紀錄 (過去 30 天)
        today = date.today()
        for i in range(30):
            record_date = today - timedelta(days=i)
            # 六日先簡單跳過
            if record_date.weekday() >= 5:
                continue
                
            for u in db_users:
                # 隨機請假/未打卡
                if random.random() < 0.05:
                    continue
                
                # 隨機決定上班時間 (08:45 ~ 09:15)
                check_in_h = 8
                check_in_m = random.randint(45, 59) if random.random() > 0.3 else random.randint(0, 15)
                if check_in_m < 60 and random.random() < 0.3:
                    check_in_h = 9 # 遲到
                
                check_in_t = time(check_in_h, check_in_m)
                
                # 隨機決定下班時間 (18:00 ~ 19:30)
                check_out_h = random.randint(18, 19)
                check_out_m = random.randint(0, 59) if check_out_h == 18 else random.randint(0, 30)
                check_out_t = time(check_out_h, check_out_m)
                
                # 隨機微調經緯度
                lat = 25.0330 + random.uniform(-0.001, 0.001)
                lng = 121.5654 + random.uniform(-0.001, 0.001)

                att = Attendance(
                    employee_name=u.employee_name,
                    date=record_date,
                    check_in_time=check_in_t,
                    lunch_out_time=time(12, random.randint(0, 5)),
                    lunch_in_time=time(12, random.randint(55, 59)),
                    check_out_time=check_out_t,
                    check_in_lat=lat,
                    check_in_lng=lng,
                    check_out_lat=lat,
                    check_out_lng=lng,
                    status="已下班"
                )
                db.add(att)
        db.commit()
        print("已建立過去 30 天的出勤紀錄")
        
        # 4. 建立請假單 (隨機幾位員工請假)
        for u in db_users:
            if u.role == 3 and random.random() > 0.3:
                lr_date = today - timedelta(days=random.randint(1, 15))
                if lr_date.weekday() < 5:
                    start_str = datetime.combine(lr_date, time(9, 0)).isoformat()
                    end_str = datetime.combine(lr_date, time(18, 0)).isoformat()
                    status = random.choice(["pending", "approved", "rejected"])
                    lr = LeaveRequest(
                        user_id=u.id,
                        leave_type=random.choice(["事假", "病假", "特休"]),
                        start_time=start_str,
                        end_time=end_str,
                        reason=random.choice(["家裡有事", "看醫生", "出去玩", "身體不適"]),
                        status=status,
                        created_at=datetime.now().isoformat(),
                        updated_at=datetime.now().isoformat()
                    )
                    db.add(lr)

                    # 如果狀態是 approved，順便扣除餘額
                    if status == "approved":
                        balance = db.query(LeaveBalances).filter(
                            LeaveBalances.user_id == u.id,
                            LeaveBalances.leave_type == lr.leave_type,
                            LeaveBalances.valid_from <= lr_date,
                            LeaveBalances.valid_until >= lr_date
                        ).first()
                        if balance:
                            balance.used_hours += 8.0 # 假設請一天 8 小時
        db.commit()
        print("已建立隨機的請假單紀錄")
        
        print("✅ 假資料建立完成！")
        
    except Exception as e:
        import traceback
        print(f"❌ 發生錯誤: {e}")
        print(traceback.format_exc())
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_fake_data()
