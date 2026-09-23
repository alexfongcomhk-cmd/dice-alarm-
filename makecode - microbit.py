is_alarming = False
user_number = 0
target_number = 0
cmd = ""
# 2. 搖晃骰子機制

def on_gesture_shake():
    global user_number, is_alarming
    if is_alarming:
        # 生成 1 到 6 的玩家數字
        user_number = randint(1, 6)
        basic.show_number(user_number)
        basic.pause(500)
        # 3. 檢查數字是否吻合
        if user_number == target_number:
            is_alarming = False
            # 關閉鬧鐘狀態
            music.stop_all_sounds()
            # 停止音樂
            basic.show_icon(IconNames.YES)
            # 傳送停止訊號給網頁，計算起床時間
            serial.write_line("STOP")
            basic.pause(2000)
            basic.clear_screen()
        else:
            # 不吻合則顯示交叉，音樂會因為 is_alarming 仍為 True 而繼續
            basic.show_icon(IconNames.NO)
            basic.pause(500)
            basic.clear_screen()
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

# 1. 接收網頁傳來的指令來啟動鬧鐘
# 設定監聽 USB 序列通訊

def on_data_received():
    global cmd, target_number, is_alarming
    # 讀取網頁發送的文字直到換行符號
    cmd = serial.read_until(serial.delimiters(Delimiters.NEW_LINE))
    if cmd == "START":
        if not (is_alarming):
            # 生成 1 到 6 的隨機目標數字
            target_number = randint(1, 6)
            basic.show_number(target_number)
            basic.pause(500)
            # 顯示 500 毫秒
            basic.clear_screen()
            is_alarming = True
serial.on_data_received(serial.delimiters(Delimiters.NEW_LINE), on_data_received)

# 4. 鬧鐘背景音樂播放

def on_forever():
    if is_alarming:
        # 播放你指定的專屬警報聲
        music.play(music.string_playable("C5 - C5 - C5 - C5 - ", 600),
            music.PlaybackMode.UNTIL_DONE)
basic.forever(on_forever)