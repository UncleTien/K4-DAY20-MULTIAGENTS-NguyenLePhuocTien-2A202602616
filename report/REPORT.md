## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Lê Phước Tiến | 2A202602616 | Cài đặt subagents, agent/backend, runner, skill curator; chạy thực nghiệm và phân tích kết quả |

- Mô hình: OpenRouter qua OpenAI-compatible gateway, deployment `openrouter/free`; `LAB_TEMPERATURE=0`; `recursion_limit=60`.
- Môi trường: Deep Agents `0.7.21`, Python `3.13.11`, macOS, chạy trực tiếp trong Python virtual environment, không dùng Docker.
- Số lần chạy tác vụ đã dùng / ngân sách: sẽ cập nhật sau khi hoàn tất thực nghiệm.
- Commit của tag `freeze`: sẽ cập nhật sau Phần 4.0.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Dự đoán `subagents` có thể cải thiện độ chính xác trên các tác vụ cần nhiều bước hoặc cần kiểm tra độc lập, nhưng sẽ sử dụng nhiều token và thời gian hơn `baseline` do phát sinh thêm các lần gọi mô hình.
- H2 (skills-auto so với baseline): Dự đoán `skills-auto` có thể cải thiện các check liên quan đến quy trình/quy ước đã xuất hiện trong lỗi của learning tasks, nhưng mức cải thiện trên evaluation tasks có thể thấp hơn nếu skill bị quá khớp với lỗi của learning set.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán cải thiện trên learning tasks sẽ lớn hơn evaluation tasks vì skill được sinh trực tiếp từ feedback của learning tasks; nếu chênh lệch lớn, đây có thể là dấu hiệu overfitting và khả năng khái quát hạn chế.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Deep Agents cung cấp các công cụ thao tác tệp gồm `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`; công cụ `execute` dùng để chạy lệnh shell trong sandbox.
2. Công cụ `task` cho phép tác tử chính giao một tác vụ phức tạp cho subagent. Subagent mặc định `general-purpose` có khả năng tương tự tác tử chính, trong khi các subagent tự định nghĩa nhận system prompt và vai trò riêng.
3. Mỗi lần gọi subagent mặc định là một phiên độc lập và chỉ nhận thông tin được truyền trong lời giao việc. Vì vậy tác tử chính phải truyền đầy đủ yêu cầu và đường dẫn cần thiết; việc dùng subagent cũng làm tăng số lần gọi mô hình và chi phí token.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa:
  - `explorer`: khảo sát repository, README, docstring, specification và dữ liệu mẫu; chỉ báo cáo thông tin, không sửa tệp.
  - `implementer`: thực hiện thay đổi khi yêu cầu đã rõ, sau đó chạy test hoặc lệnh kiểm tra và báo cáo kết quả.
  - `reviewer`: kiểm tra độc lập implementation theo yêu cầu và edge cases; không sửa tệp.
- Lý do thiết kế: tách ba giai đoạn khảo sát, thực thi và kiểm tra để tác tử chính có thể giao các tác vụ nhiều bước cho vai trò phù hợp.
- `subagent_calls` ở từng tác vụ và nhận xét: cập nhật sau khi chạy điều kiện `subagents`.
- Thông tin thiếu hoặc thừa khi giao việc: cập nhật từ `trace.md`.
- Ảnh hưởng đến token và thời gian: cập nhật sau khi có kết quả thực nghiệm.

## 9. Hạn chế và tính hợp lệ

1. Mỗi cấu hình chỉ được đánh giá trên một số lượng nhỏ tác vụ, nên kết quả có thể chưa đại diện cho các bài toán agentic khác.
2. Mô hình sinh có tính không xác định; một lần chạy cho mỗi cấu hình có thể chịu ảnh hưởng của nhiễu và làm thay đổi điểm, số tool call, token và thời gian.
3. Thí nghiệm sử dụng một cấu hình mô hình chính qua OpenRouter, nên chưa thể kết luận kết quả sẽ giữ nguyên khi thay đổi mô hình hoặc nhà cung cấp.
4. Skill được sinh từ lỗi của learning tasks nên có nguy cơ overfitting; cải thiện trên learning set không đồng nghĩa với khả năng khái quát sang evaluation set.

## Phụ lục

- Lệnh đã chạy theo thứ tự:
  - `pytest tests/test_01_provided.py`
  - `python scripts/tour.py`
  - `pytest tests/test_02_agent.py -k subagents -v`
  - `pytest tests/test_02_agent.py -v`
  - `pytest tests/test_03_runner.py -v`
  - `pytest tests/ -v`
  - `pytest tests/test_04_curator.py -v`
  - `pytest tests/ -v`
  - `python -m lab.runner --condition baseline --tasks data-learn`
- Thử thách mở rộng: chưa thực hiện.