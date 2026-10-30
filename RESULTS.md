# K6 lab results

## Part 0
- Step 0.1, http_req_duration: 668.1ms เพราะรรันแค่รอบเดียว ค่าเฉลี่ยและค่าอื่นๆ เลยได้เท่ากันหมดคือ 668.1ms
- Step 0.2, requests, rate and p(95), and why the rate stays below 5: ได้ 72 requests เฉลี่ย 3.33 req/s และ p(95) อยู่ที่ 946.96ms ที่ส่งได้ไม่ถึง 5 req/s เพราะในโค้ดมีสั่ง sleep ไว้ 1s แล้วยังมีเวลาที่เซิร์ฟเวอร์ตอบกลับอีกประมาณ 423ms ทำให้รอบนึงใช้เวลาประมาณ 1.47s user คนนึงเลยส่งได้แค่ประมาณ 0.68 ครั้งต่อวินาที พอทำงงานพร้อมกัน 5 คนเลยได้ความเร็วแค่ประมาณ 3.3 ถึง 3.4 req/s
- Step 0.6, exit code of the normal run and of the run with P95=300: รอบรันปกติได้ exit code เป็น 0 แปลว่าผ่านทุกเกณฑ์ ส่วนรอบที่ใส่ P95=300 ได้ exit code เป็น 99 เพราะเซิร์ฟเวอร์ตอบช้ากว่า 300ms เลยไม่ผ่านเกณฑ์
- Step 0.7, rules that passed, p(95), p(99), exit code after your change: ผ่านทุกเกณฑ์ ค่า error อยู่ที่ 0.00% เช็คผ่าน 100% ค่า p(95) ได้ 947.96ms และ p(99) ได้ 1.09s พอเปลี่ยนเกณฑ์ให้เข้มขึ้นเป็น p(95) น้อยกว่า 200ms ระบบตอบไม่ทันเลยได้ exit code เป็น 99
- Step 0.8, what was wrong, and how the checks showed it:

## Part A results
| Step | Test type | Users | Req/s | p(95) | Max | Failed | Checks |
| ---- | ------------ | ----- | ----- | ----- | --- | ------ | ------ |
| A1 | Smoke | 1 | | | | | |
| A2 | Average load | 3 | | | | | |
| A3 | Stress | 5 | | | | | |
| A4 | Spike | 5 | | | | | |
| A5 | Soak | 2 | | | | | |

## Part B
1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
