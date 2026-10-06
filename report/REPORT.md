# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Lê Phước Tiến | 2A202602616 | Cài đặt agent, subagents, runner, curator; chạy thí nghiệm; phân tích kết quả và hoàn thiện báo cáo |

- Mô hình: OpenRouter qua OpenAI-compatible endpoint, deployment `openrouter/free`.
- `LAB_TEMPERATURE=0`.
- `recursion_limit=60`.
- Deep Agents: `0.7.21`.
- Python: `3.13.11`.
- Hệ điều hành: macOS.
- Chạy trực tiếp trong virtual environment, không dùng Docker.
- Các run chính đã hoàn thành: `baseline/data-learn`, `baseline/code-eval`, `baseline/data-eval`, `subagents/code-eval`, `subagents/data-eval`, `skills-auto/code-eval`, `skills-auto/data-eval`.
- Có một lần `baseline/code-eval` trước đó gặp `GraphRecursionError`; run được chạy lại với nguyên cấu hình và run hợp lệ cuối cùng đạt `1/11`.
- Có một lần `subagents/data-eval` gặp HTTP 429 do quota OpenRouter; sau khi thay API key, run lại thành công `5/9`.
- Commit của tag `freeze`: `d2b06cb` (`Freeze experiment configuration`).
- Commit giả thuyết trước freeze: `f1ce248` (`hypotheses: finalize pre-freeze predictions`).

## 2. Giả thuyết

- **H1 — subagents so với baseline:** `subagents` có thể đạt điểm cao hơn baseline trên các tác vụ nhiều bước hoặc cần kiểm tra độc lập nhờ các vai trò `explorer`, `implementer`, `reviewer`, nhưng có thể sử dụng nhiều token hơn.
- **H2 — skills-auto so với baseline:** `skills-auto` có thể cải thiện lỗi quy trình đã quan sát trong learning, đặc biệt các lỗi liên quan tới workspace và tìm kiếm file. Khả năng cải thiện evaluation phụ thuộc vào việc agent có thực sự đọc và áp dụng skill.
- **H3 — learning so với evaluation:** skill được sinh từ failure của learning có thể cải thiện mạnh hơn trên các lỗi tương tự learning so với những quy ước mới xuất hiện trong evaluation. Chênh lệch lớn giữa hai nhóm là dấu hiệu khả năng khái quát của skill còn hạn chế.

## 3. Làm quen Deep Agents

1. Agent có các công cụ thao tác file như `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep` và shell tool `execute`.
2. Công cụ `task` cho phép agent chính giao nhiệm vụ cho subagent. Ba subagent tùy chỉnh được cấu hình bằng tên, description và system prompt riêng.
3. Mỗi lần gọi subagent độc lập và cần được cung cấp đủ ngữ cảnh. Cơ chế này có thể tăng khả năng phân chia công việc nhưng cũng làm tăng số model call và token.

## 4. Đường cơ sở và phân loại lỗi

Tác vụ learning đã chạy:

```text
baseline/data-learn
score = 0/8
tokens = 104,668
tool_calls = 13
time = 441.0s
```

| Tác vụ | Check thất bại | Nhóm lỗi | Bằng chứng |
|---|---|---|---|
| data-learn | `north_q1_revenue` | Technical/output | `workspace/answer.json` không được tạo |
| data-learn | `north_q1_orders` | Technical/output | `workspace/answer.json` không được tạo |
| data-learn | `top_region` | Technical/output | `workspace/answer.json` không được tạo |
| data-learn | `missing_amount_orders` | Technical/output | `workspace/answer.json` không được tạo |
| data-learn | `duplicate_rows_removed` | Technical/output | `workspace/answer.json` không được tạo |
| data-learn | `rule_money_in_cents` | Quy ước | Output cuối không đáp ứng rule |
| data-learn | `rule_meta_block` | Quy ước | Output cuối không đáp ứng rule |
| data-learn | `rule_clean_csv` | Quy ước | Không tạo đúng `workspace/clean.csv` |

Vết chạy cho thấy agent ban đầu sử dụng đường dẫn giả định `/workspace/sales.csv` và thực hiện tìm kiếm quá rộng bằng `find /`, trong đó có lệnh bị timeout. Sau đó agent tìm được `./workspace/sales.csv`, đọc 101 dòng, còn 94 dòng sau deduplication, xác định 7 duplicate rows và 8 order thiếu amount.

Quá trình sau đó gặp lỗi:

```text
TypeError: can't compare offset-naive and offset-aware datetimes
```

nên agent không tạo đầy đủ artifact cuối.

Các lỗi workspace và tìm kiếm có thể được phòng ngừa bằng skill. Tuy nhiên lỗi timezone không được các skill curator sinh ra bao phủ.

## 5. Điều kiện `subagents`

Ba subagent được định nghĩa:

- **explorer:** khảo sát repository, tài liệu, sample data và báo cáo facts trước khi chỉnh sửa.
- **implementer:** thực hiện thay đổi được yêu cầu, chạy test/validation và báo cáo kết quả.
- **reviewer:** kiểm tra độc lập implementation, requirement và edge cases mà không chỉnh sửa trực tiếp.

Kết quả evaluation:

| Task | Score | Tokens | Tool calls | Subagent calls |
|---|---:|---:|---:|---:|
| code-eval | 7/11 | 187,499 | 29 | 0 |
| data-eval | 5/9 | 109,582 | 11 | 0 |

Cả hai run đều có:

```text
error = null
skills_modified = false
subagent_calls = 0
```

Điểm đáng chú ý là mặc dù chạy condition `subagents`, model không thực sự gọi subagent trong hai evaluation run. Vì vậy không thể quy trực tiếp mức tăng điểm so với baseline cho việc delegation.

`code-eval` của subagents đạt toàn bộ **7/7 technical checks**, nhưng thất bại cả bốn rule:

- `rule_type_hints`
- `rule_regression_tests`
- `rule_changelog`
- `rule_version_bump`

`data-eval` đạt **5/5 technical checks** nhưng thất bại cả bốn rule của tác vụ.

## 6. Self-evolving: skill do curator sinh

Curator được chạy **1 lần**, sinh **2 skill**, không xóa skill nào.

### `verify-workspace-path`

Skill yêu cầu:

- kiểm tra current directory bằng `pwd`;
- liệt kê directory để xác định workspace;
- ưu tiên relative path thay vì giả định `/workspace/...`.

Đây là skill tổng quát và trực tiếp phản hồi failure đã thấy trong `data-learn`.

### `avoid-unbounded-find`

Skill yêu cầu:

- giới hạn search scope;
- sử dụng `-maxdepth`;
- sử dụng timeout;
- tìm theo file pattern cụ thể.

Đây cũng là skill tổng quát, không chứa dữ liệu hoặc đáp án của evaluation.

| Skill | Tổng quát? | Đánh giá | Description / sử dụng |
|---|---|---|---|
| `verify-workspace-path` | Có | Đúng với failure learning | Ngắn, trigger rõ ràng |
| `avoid-unbounded-find` | Có | Đúng với failure learning | Ngắn, hướng dẫn hành động cụ thể |

Kết quả breakdown cuối cùng cho thấy:

```text
skills-auto eval: read a skill = 1/2
```

Như vậy có một evaluation run đã đọc skill, nhưng không phải tất cả các run `skills-auto` đều sử dụng skill.

Curator không sinh skill xử lý timezone và cũng không sinh skill trực tiếp cho các house-rule checks.

## 7. Kết quả so sánh

Nội dung `report/table.md`:

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| data-learn | 0/8 | - | - |
| code-eval | 1/11 | 7/11 | 7/11 |
| data-eval | 5/9 | 5/9 | 5/9 |
| **Mean score - learning tasks** | 0.00 | - | - |
| **Mean score - evaluation tasks** | 0.32 | 0.60 | 0.60 |
| **Mean tokens per run** | 85,385 | 148,540 | 180,883 |
| **Runs that read a skill** | 0/3 | 0/2 | 1/2 |

Kết quả `scripts/check_breakdown.py`:

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval      6/12         0/8           75,744      0/2
baseline      learn     0/5          0/3          104,668      0/1
subagents     eval     12/12         0/8          148,540      0/2
skills-auto   eval     12/12         0/8          180,883      1/2
```

`python scripts/verify_freeze.py`:

```text
checked 2 runs of skill conditions: OK
```

Không có run hợp lệ nào có `skills_modified=true`.

Có hai sự cố đáng chú ý trong quá trình thử nghiệm:

1. Một run `baseline/code-eval` gặp `GraphRecursionError` ở recursion limit 60. Run này không được sử dụng làm kết quả cuối và được chạy lại mà không thay đổi cấu hình.
2. Một run `subagents/data-eval` gặp OpenRouter HTTP 429 do quota free. Sau khi provider hoạt động trở lại, task được chạy lại thành công và run hợp lệ đạt 5/9.

## 8. Phân tích

### 8.1. So sánh điểm

Trên evaluation:

- baseline mean score: **0.32**
- subagents mean score: **0.60**
- skills-auto mean score: **0.60**

Cả `subagents` và `skills-auto` đều cao hơn baseline trong tập evaluation đã chạy.

Chênh lệch chủ yếu xuất hiện ở `code-eval`:

```text
baseline     1/11
subagents    7/11
skills-auto  7/11
```

Trong `data-eval`, cả ba condition đều đạt `5/9`.

Tuy nhiên `subagent_calls=0` ở cả hai subagents runs, vì vậy không đủ bằng chứng để kết luận delegation là nguyên nhân trực tiếp của mức tăng.

Không có `subagents` hoặc `skills-auto` learning run tương ứng, nên không thể xác định condition nào cải thiện learning so với baseline `0/8`. Vì vậy cũng chưa thể kiểm tra đầy đủ hiện tượng “cải thiện learning nhưng không cải thiện evaluation”.

### 8.2. Technical checks và house rules

Breakdown cho thấy khác biệt rất rõ:

```text
baseline eval      technical  6/12    rules 0/8
subagents eval     technical 12/12    rules 0/8
skills-auto eval   technical 12/12    rules 0/8
```

Subagents và skills-auto đạt toàn bộ technical checks của hai evaluation tasks đã chạy, nhưng không condition nào vượt qua bất kỳ house-rule check nào.

Hai skill curator sinh ra tập trung vào workspace discovery và file search, không hướng dẫn các quy ước như:

- money representation;
- metadata block;
- clean CSV;
- sorted-key formatting;
- type hints;
- regression tests;
- changelog;
- version bump.

Do đó chúng không trực tiếp bao phủ các rule checks mới trong evaluation.

### 8.3. Skill được đọc và không được đọc

Breakdown cho thấy `skills-auto` đọc skill trong **1/2 evaluation runs**.

Điều này tốt hơn trường hợp hoàn toàn không retrieval, nhưng score vẫn bằng subagents:

```text
skills-auto mean evaluation score = 0.60
subagents mean evaluation score = 0.60
```

Không có bằng chứng đủ mạnh để quy một technical check cụ thể cho skill, vì các technical checks cũng được condition `subagents` đạt toàn bộ mà `subagent_calls=0`.

Một ví dụ skill không giúp là các `rule_*` checks: skills-auto đạt **0/8 house rules**. Nguyên nhân phù hợp với bằng chứng là skill được sinh không chứa các quy ước này, đồng thời skill chỉ được đọc trong 1/2 run.

Kết quả cho thấy **skill generation không đồng nghĩa với skill utilization hoặc score improvement**.

### 8.4. Chi phí

Mean tokens:

```text
baseline      85,385
subagents    148,540
skills-auto  180,883
```

So với baseline, subagents dùng khoảng **1.74 lần** token trung bình và skills-auto dùng khoảng **2.12 lần**.

Baseline có chi phí thấp nhất nhưng mean evaluation score chỉ 0.32. Subagents và skills-auto cùng đạt 0.60, nhưng subagents dùng ít token hơn skills-auto.

Trong phạm vi thí nghiệm này, nếu chỉ xét score/token giữa hai condition đạt 0.60 thì `subagents` hiệu quả hơn `skills-auto`. Tuy nhiên không thể khẳng định multi-agent delegation tạo ra lợi ích này vì `subagent_calls=0`.

### 8.5. Rò rỉ dữ liệu và quá khớp

Không thấy bằng chứng trực tiếp về data leakage trong hai skill.

Curator chỉ sử dụng learning failures và sinh các hướng dẫn tổng quát:

- xác định workspace trước khi thao tác;
- tránh tìm kiếm toàn filesystem.

Skill không chứa tên file evaluation, đáp án, expected numerical values hoặc các rule mới của evaluation.

Nguy cơ overfitting vẫn tồn tại vì skill được sinh từ chỉ một learning task thất bại. Việc chúng không bao phủ timezone failure và không giải quyết các house rules của evaluation cho thấy phạm vi kiến thức học được còn hẹp.

### 8.6. Nhiễu

Không có learning run của cùng bộ skill trước và sau freeze nên không thể tính chính xác chênh lệch learning theo yêu cầu này.

Tuy nhiên có bằng chứng mạnh về nhiễu từ `baseline/code-eval`. Một lần chạy trước đạt 7/11 checks trước khi kết thúc bởi `GraphRecursionError`, trong khi lần chạy lại hợp lệ với cùng cấu hình chỉ đạt **1/11**.

Điều này cho thấy kết quả của một run đơn lẻ có variance đáng kể. Vì vậy chênh lệch giữa các condition cần được diễn giải thận trọng và không nên xem một run duy nhất là bằng chứng nhân quả mạnh.

## 9. Hạn chế và tính hợp lệ

1. **Coverage chưa đầy đủ.** Thí nghiệm hoàn thành `data-learn`, `code-eval` và `data-eval`, nhưng chưa chạy `logs-eval` và chưa chạy đầy đủ ba learning tasks cho mọi condition. Vì vậy kết luận chỉ áp dụng cho tập task thực tế đã chạy.

2. **Mỗi cấu hình chỉ có rất ít run.** `baseline/code-eval` thể hiện variance lớn giữa các lần chạy. Điều này làm giảm độ tin cậy của việc quy chênh lệch score cho architecture.

3. **Subagents không thực sự được gọi trong evaluation.** `subagent_calls=0` ở cả hai subagents runs. Vì vậy H1 về lợi ích của delegation chưa được kiểm chứng trực tiếp.

4. **Skill utilization chưa ổn định.** Skills-auto chỉ đọc skill ở 1/2 evaluation runs. Do đó chưa thể tách biệt rõ chất lượng skill khỏi chất lượng retrieval/triggering.

5. **Skill được học từ dữ liệu failure hạn chế.** Curator chỉ có một baseline learning task để học và sinh hai skill, nên coverage của skill hẹp.

6. **Provider có nhiễu và giới hạn quota.** Một run gặp OpenRouter HTTP 429. Việc dùng `openrouter/free` cũng có thể tạo khác biệt về latency và hành vi giữa các lần chạy.

7. **House rules là điểm yếu chung.** Cả ba condition đều đạt 0/8 rule checks trong evaluation, cho thấy kiến trúc hiện tại tập trung giải quyết technical task tốt hơn việc tuân thủ quy ước repository.

## 10. Kết luận

Trong hai evaluation tasks đã chạy, baseline đạt mean score **0.32**, còn subagents và skills-auto cùng đạt **0.60**. Cả subagents và skills-auto đạt **12/12 technical checks** nhưng tất cả condition đều đạt **0/8 house-rule checks**. Không thể quy mức tăng của subagents cho delegation vì `subagent_calls=0`, trong khi skills-auto chỉ đọc skill ở 1/2 runs. Skills-auto cũng có chi phí token cao nhất với trung bình **180,883 tokens/run**. Cải tiến tiếp theo nên tập trung vào cơ chế kích hoạt skill, tuân thủ repository conventions và lặp lại thí nghiệm nhiều lần trên đầy đủ `code`, `data` và `logs`.

## Phụ lục

### Lệnh chính đã chạy

```bash
python scripts/tour.py
pytest tests/ -v

python -m lab.runner --condition baseline --tasks data-learn
python -m lab.curator

git commit -m "hypotheses: finalize pre-freeze predictions"
git commit --allow-empty -m "Freeze experiment configuration"
git tag freeze

python scripts/verify_freeze.py

python -m lab.runner --condition baseline --tasks data-eval
python -m lab.runner --condition skills-auto --tasks data-eval
python -m lab.runner --condition subagents --tasks data-eval

python -m lab.runner --condition baseline --tasks code-eval
python -m lab.runner --condition subagents --tasks code-eval
python -m lab.runner --condition skills-auto --tasks code-eval

python scripts/verify_freeze.py
python -m lab.compare > report/table.md
python scripts/check_breakdown.py

pytest tests/ -v
```

### Kiểm thử cuối

```text
29 passed in 3.16s
```

### Freeze verification cuối

```text
checked 2 runs of skill conditions: OK
```

### Thử thách mở rộng

Không thực hiện.

### Ghi chú

- Không chỉnh sửa thủ công skill sau tag `freeze`.
- Không sử dụng run gặp HTTP 429 làm kết quả đánh giá.
- Run `baseline/code-eval` gặp `GraphRecursionError` được xem là run lỗi; kết quả chính thức lấy từ lần chạy lại có `error=null`.
- Không chạy thêm `logs-eval` để tránh tăng chi phí API; đây được ghi rõ là hạn chế của thí nghiệm.