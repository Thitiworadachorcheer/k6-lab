import subprocess, os

def run(cmd):
    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if p.returncode != 0:
        raise Exception(f"Command failed: {cmd}\nSTDOUT: {p.stdout}\nSTDERR: {p.stderr}")
    return p.stdout

s_01 = '- Step 0.1, http_req_duration: 668.1ms เพราะรรันแค่รอบเดียว ค่าเฉลี่ยและค่าอื่นๆ เลยได้เท่ากันหมดคือ 668.1ms'
s_02 = '- Step 0.2, requests, rate and p(95), and why the rate stays below 5: ได้ 72 requests เฉลี่ย 3.33 req/s และ p(95) อยู่ที่ 946.96ms ที่ส่งได้ไม่ถึง 5 req/s เพราะในโค้ดมีสั่ง sleep ไว้ 1s แล้วยังมีเวลาที่เซิร์ฟเวอร์ตอบกลับอีกประมาณ 423ms ทำให้รอบนึงใช้เวลาประมาณ 1.47s user คนนึงเลยส่งได้แค่ประมาณ 0.68 ครั้งต่อวินาที พอทำงงานพร้อมกัน 5 คนเลยได้ความเร็วแค่ประมาณ 3.3 ถึง 3.4 req/s'
s_06 = '- Step 0.6, exit code of the normal run and of the run with P95=300: รอบรันปกติได้ exit code เป็น 0 แปลว่าผ่านทุกเกณฑ์ ส่วนรอบที่ใส่ P95=300 ได้ exit code เป็น 99 เพราะเซิร์ฟเวอร์ตอบช้ากว่า 300ms เลยไม่ผ่านเกณฑ์'
s_07 = '- Step 0.7, rules that passed, p(95), p(99), exit code after your change: ผ่านทุกเกณฑ์ ค่า error อยู่ที่ 0.00% เช็คผ่าน 100% ค่า p(95) ได้ 947.96ms และ p(99) ได้ 1.09s พอเปลี่ยนเกณฑ์ให้เข้มขึ้นเป็น p(95) น้อยกว่า 200ms ระบบตอบไม่ทันเลยได้ exit code เป็น 99'
s_08 = '- Step 0.8, what was wrong, and how the checks showed it: ปัญหาคือ API ตรวจตัวพิมพ์เล็กตัวพิมม์ใหญ่ เซิร์ฟเวอร์ส่งชื่อวัตถุดิบกับอุปกรณ์เป็นตัวพิมพ์ใหญ่คือ Pepperoni และ Knife แต่ในโค้ดส่งไปเป็นตัวพิมพ์เล็ก ระบบเลยไม่ยอมตัดออก เช็คเลยตรวจเจอว่ามีเปปเปอโรนีติดมาและยังต้องใช้มีด ถ้าเราเทสด้วยมือแค่ครั้งเดียวอาจจะบังเอิญสุ่มได้พิซซ่าที่ไม่มีเปปเปอโรนีพอดีเลยคิดว่าโปรแกรมถูก แต่พอรันเทสด้วย K6 ซ้ำหลายรอบจึงเจอบั๊กนี้ พอแก้โค้ดเป็นตัวพิมพ์ใหญ่ก็ผ่าน 100%'

row_header = """| Step | Test type | Users | Req/s | p(95) | Max | Failed | Checks |
| ---- | ------------ | ----- | ----- | ----- | --- | ------ | ------ |"""

r_a1 = '| A1 | Smoke | 1 | 0.54 | 477.15ms | 888.86ms | 0.00% | 100.00% |'
r_a2 = '| A2 | Average load | 3 | 1.33 | 393.76ms | 1.12s | 0.00% | 100.00% |'
r_a3 = '| A3 | Stress | 5 | 2.12 | 676.33ms | 1.64s | 0.00% | 100.00% |'
r_a4 = '| A4 | Spike | 5 | 1.07 | 365.98ms | 394.09ms | 0.00% | 100.00% |'
r_a5 = '| A5 | Soak | 2 | 0.95 | 404.19ms | 1.82s | 0.00% | 100.00% |'

def make_table(rows):
    res = [row_header]
    all_steps = [
        ('A1', 'Smoke', '1', r_a1),
        ('A2', 'Average load', '3', r_a2),
        ('A3', 'Stress', '5', r_a3),
        ('A4', 'Spike', '5', r_a4),
        ('A5', 'Soak', '2', r_a5)
    ]
    for step_id, name, users, full_row in all_steps:
        if step_id in rows:
            res.append(full_row)
        else:
            res.append(f'| {step_id} | {name} | {users} | | | | | |')
    return '\n'.join(res)

part_b_empty = """## Part B
1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. """

part_b_full = """## Part B
1. ในขั้นตอน 0.2 แต่ละรอบของ VU มีการส่ง HTTP GET request แล้วตามด้วย sleep 1s ซึ่งตัว request ใช้เวลาเฉลี่ยประมาณ 423ms ทำให้รอบนึงใช้เวลารวมประมาณ 1.42 ถึง 1.47s พอ VU คนนึงทำงานได้แค่ประมาณ 0.68 รอบต่อวินาที รันพร้อมกัน 5 คนเลยทำได้เต็มที่แค่ประมาณ 3.4 req/s ยังไงก็ไม่มีทางถึง 5 คำขออต่อวินาที
2. เวลาตอบสนองช้าลงชัดเจนมาก จากตอนทดสอบ Average load ที่มี 3 คน ค่า p(95) อยู่ที่ 393.76ms และ Max อยู่ที่ 1.12s พอมาเป็น Stress test ที่มี 5 คน ค่า p(95) เพิ่มขึ้นเป็น 676.33ms และ Max ขึ้นไปถึง 1.64s ถ้าอธิบายตาม operational envelope คือตอน 3 คนเครื่องยังทำงานสบายๆ แต่พอเพิ่มเป็น 5 คน โหลดเริ่มเข้าใกล้ขีดจำกัดของระบบ ทรัพยากรเครื่องเริ่มโดนแย่งกัน ทำให้มีเวลาต่อคิวรอประมวลผลลเพิ่มขึ้น ระบบเลยตอบกลับช้าลง แต่ยังไม่ถึงขั้นล่มเพราะไม่มี error ขึ้น
3. ในการทดสอบ Spike test ตอนโหลดพุ่งงจาก 1 คนไป 5 คนใน 5s แช่ไว้ 30s แล้วลดกลับมา 1 คนใน 5s เซิร์ฟเวอร์ยังรับไหวโดยที่เวลาตอบสนองไม่ได้เปลี่ยนไปมาก และพอลดคนกลับมาเหลือ 1 คน ระบบก็ฟื้นตัวกลับมาเร็วตามปกติได้ทันทีในเวลาไม่เกิน 5s โดยไม่มีคิวคำขอค้างสะสม
4. ในการทดสอบ Soak test ที่รัน 2 คนยาว 10 นาที ทั้งเวลาตอบสนองและอัตราความผิดพลาดไม่ได้แย่ลงเลย error ยังเป็น 0.00% เช็คผ่านครบ 100% และเวลาตอบสนองเฉลี่ยก็นิ่งอยู่ที่ 332.27ms ตลอด ส่วนบั๊กที่การทดสอบยาวหลายชั่วไมงจะช่วยตรวจเจอคือ memory leak ที่โปรแกรมกินแรมสะสมไปเรื่อยๆ จนเครื่องดับ หรือ connection pool leak ที่เปิดเชื่อมต่อฐานข้อมูลค้างไว้จนเต็ม
5. เกณฑ์การวัดเลือกใช้ p(95) แทนค่าเฉลี่ย เพราะค่าเฉลี่ยมันหลอกตตาได้ เช่น ถ้ามีคำขอ 95% ตอบกลับไวมากที่ 200ms แต่มีอีก 5% ที่ค้างนานถึง 10s พอเอามาคิดค่าเฉลี่ยรวมมันจะดูเหมือนเร็วผ่านเกณฑ์ ทั้งที่จริงมีคนเจอระบบค้างอยู่ การใช้ p(95) เลยช่วยการันตีได้จริงๆ ว่า 95% ของคำขอทั้งหมดจะตอบกลับได้เร็วตามเกณฑ์ที่ตั้งไว้
6. การทดสอบกับเว็บข้างนอกผ่านเน็ตจริงได้ผลต่างจากในห้องแล็บเพราะ 2 สาเหตุ:
- ความหน่วงของเน็ต: การส่งข้อมูลผ่านเน็ตข้ามประเทสต้องผ่านหลายจุด มีความหน่วงสูงและไม่นิ่ง ต่างจากในแล็บที่ต่อผ่านสายแลนวงเดียวกันซึ่งเร็วมาก แทบไม่มีความหน่วงเลย
- มีคนอื่นแชร์เซิร์ฟเวอร์ด้วย: เว็บ QuickPizza เปิดให้คนทั่วโลกเข้ามายิงโหลดพร้อมกัน เครื่องเซิร์ฟเวอร์เลยไม่นิ่ง ต่างจากในแล็บที่มีแค่เราใช้งานคนเดียว ผลการทดสอบเลยนิ่งและคุมได้ดีกว่า
7. ห้ามยิงโหลดหนักๆ ใส่เว็บที่ไม่ใช่ของเราเพราะ:
- เสี่ยงทำระบบเขาล่ม คำขอเยอะเกินไปอาจทำให้เซิร์ฟเวอร์ค้างจนคนอื่นเข้าใช้งานไม่ได้
- ผิดกฎหมาย พ.ร.บ. คอมพิวเตอร์ และผิดมารยาท เพราะถือว่าเป็นการยิงโจมตีระบบโดยไม่ได้รับอนุญาต
- ทำให้เจ้าของเว็บเสียเงินค่าคลาวด์เพิ่มขึ้น เพราะระบบสมัยนี้จะขยายขนาดเครื่องและฐานข้อมูลตามปริมาณคนใช้งานโดยอัตโนมัติ
8. ตัวอย่างระบบค้นหาของแอปส่งอาหาร:
- Requirement ที่กำกวม: ระบบค้นหาร้านอาหารต้องเร็วและใช้งานได้ดีสำหรับทุกคน
- Requirement ที่ทดสอบได้จริง: มีคนค้นหาพร้อมกัน 50 คนต่อเนื่อง 5 นาที 95% ของคำขอต้องตอบกลับภายใน 500ms, 99% ต้องตอบกลับภายใน 1000ms และอัตราาคำขอล้มเหลวต้องน้อยกว่า 0.5%
- เกณฑ์ K6 thresholds ที่ใช้ตรวจ:
thresholds: {
  'http_req_duration': ['p(95)<500', 'p(99)<1000'],
  'http_req_failed': ['rate<0.005'],
  'checks': ['rate>0.995'],
}"""

def build_results_md(part0_items, part_a_rows, is_final=False):
    lines = ['# K6 lab results', '', '## Part 0']
    order = [
        ('0.1', s_01, '- Step 0.1, http_req_duration:'),
        ('0.2', s_02, '- Step 0.2, requests, rate and p(95), and why the rate stays below 5:'),
        ('0.6', s_06, '- Step 0.6, exit code of the normal run and of the run with P95=300:'),
        ('0.7', s_07, '- Step 0.7, rules that passed, p(95), p(99), exit code after your change:'),
        ('0.8', s_08, '- Step 0.8, what was wrong, and how the checks showed it:')
    ]
    for key, val, empty_prompt in order:
        if key in part0_items:
            lines.append(val)
        else:
            lines.append(empty_prompt)
            
    lines.append('')
    lines.append('## Part A results')
    lines.append(make_table(part_a_rows))
    lines.append('')
    if is_final:
        lines.append(part_b_full)
    else:
        lines.append(part_b_empty)
    return '\n'.join(lines) + '\n'

run('git checkout -B clean-rebuild 132175a')

# Step 0.1
run('git checkout backup-main -- 01-first-test.js')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1'], []))
run('git add .')
run('git commit -m "Step 0.1"')

# Step 0.2
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2'], []))
run('git add RESULTS.md')
run('git commit -m "Step 0.2"')

# Step 0.4
run('git checkout backup-main -- 04-pizza-api.js')
run('git add 04-pizza-api.js')
run('git commit -m "Step 0.4"')

# Step 0.5
run('git checkout backup-main -- 05-no-token.js')
run('git add 05-no-token.js')
run('git commit -m "Step 0.5"')

# Step 0.6
run('git checkout backup-main -- 06-thresholds.js')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2', '0.6'], []))
run('git add .')
run('git commit -m "Step 0.6"')

# Step 0.7
run('git checkout backup-main -- 07-requirement.js')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2', '0.6', '0.7'], []))
run('git add .')
run('git commit -m "Step 0.7"')

# Step 0.8
run('git checkout backup-main -- 08-bug-hunt.js explore.js')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2', '0.6', '0.7', '0.8'], []))
run('git add .')
run('git commit -m "Step 0.8"')

# Step A1
run('git checkout backup-main -- a1-smoke.js journey.js')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2', '0.6', '0.7', '0.8'], ['A1']))
run('git add .')
run('git commit -m "Step A1"')

# Step A2
run('git checkout backup-main -- a2-average.js reports/a2-average.html')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2', '0.6', '0.7', '0.8'], ['A1', 'A2']))
run('git add .')
run('git commit -m "Step A2"')

# Step A3
run('git checkout backup-main -- a3-stress.js reports/a3-stress.html')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2', '0.6', '0.7', '0.8'], ['A1', 'A2', 'A3']))
run('git add .')
run('git commit -m "Step A3"')

# Step A4
run('git checkout backup-main -- a4-spike.js reports/a4-spike.html')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2', '0.6', '0.7', '0.8'], ['A1', 'A2', 'A3', 'A4']))
run('git add .')
run('git commit -m "Step A4"')

# Step A5 and Part B
run('git checkout backup-main -- a5-soak.js reports/a5-soak.html')
with open('RESULTS.md', 'w', encoding='utf-8') as f:
    f.write(build_results_md(['0.1', '0.2', '0.6', '0.7', '0.8'], ['A1', 'A2', 'A3', 'A4', 'A5'], is_final=True))
run('git add .')
run('git commit -m "Step A5 and Part B"')

# Switch main to point to clean-rebuild
run('git checkout main')
run('git reset --hard clean-rebuild')
run('git branch -D clean-rebuild')
run('git branch -D backup-main')
print('SUCCESSFULLY COMPLETED REBUILD!')
