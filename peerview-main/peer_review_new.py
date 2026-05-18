from flask import Flask, request, redirect, url_for, session, render_template_string
import csv
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUMMARY_FILE = os.path.join(BASE_DIR, "reading_time_summary.csv")
EVENT_FILE = os.path.join(BASE_DIR, "reading_time_events.csv")
RESPONSE_FILE = os.path.join(BASE_DIR, "text_response_data.csv")

employees = {
    "jiasheng": {
        "name": "贾盛",
        "title": "贾盛收到的同事评价内容",
        "pages": {
            "summary": {
                "label": "总结报告",
                "content": "总结报告：综合来看，贾盛共收到5条同事评价，其中2条为正面评价（绿色标签），3条为负面评价（红色标签）。该员工在决策能力和数据管理方面表现较好，但在人际关系、组织能力和冲突协调方面存在明显不足。"
            },
            "chenyu": {
                "label": "陈宇",
                "content": "陈宇：贾盛平时给人的感觉比较沉默寡言，在团队里通常不会主动关心别人，也不太会主动参与同事之间的互动。大多数情况下，他更愿意专注于自己的事情，几乎不会主动去帮助他人处理日常的困难。只有在我们明确向他提出请求，或者事情已经比较紧急的时候，他才会伸出援手。他也很少表现出对别人的关心，贾盛让人感觉他并不在意别人的处境，给人一种比较难以接近的感觉。"
            },
            "zhangliang": {
                "label": "张亮",
                "content": "张亮：贾盛在工作中反应很快，通常能够在较短时间内做出决策判断，并对我们的工作需求做出及时回应。无论是临时工作安排，还是需要尽快确认的事项，他往往都不会拖延，在协作过程中让人觉得事情推进得比较顺畅。他不仅理解问题快，而且能够很快进入处理状态。即使面对一些节奏比较快、需要尽快拍板的工作情境，他也通常能够保持较高的回应效率。"
            },
            "liuli": {
                "label": "刘莉",
                "content": "刘莉：数据管理和分析是一个优秀销售人员所需具备的专业能力，贾盛在这方面表现突出。对于公司目前使用的销售管理系统，他能够熟练操作各项功能，对系统背后的逻辑和数据处理流程有比较深入的理解。平时我们在系统使用、数据分析或者操作上遇到困难，大家都会先去请教他。即使是比较复杂的技术问题，他也能够耐心地解释。"
            },
            "zhaohong": {
                "label": "赵洪",
                "content": "赵洪：在办公室例会上，贾盛通常很少主动发言，大多数时候倾向于坐在一旁，而不是主动表达自己的想法或推动话题展开。很多时候，即使大家在讨论工作安排或团队协作相关的问题，他也很少主动发表意见。只有当话题涉及他自己比较感兴趣、或和他个人工作联系较紧密的内容时，他才会多说几句。"
            },
            "wuzhou": {
                "label": "吴洲",
                "content": "吴洲：贾盛平时不太喜欢介入和处理人际分歧和矛盾。遇到这类情况，他总是保持距离，很少主动出面协调，也比较少主动提出具体的解决方案。即使问题已经影响到正常工作，他也不会第一时间站出来，而是等待同事去处理。同时，他在工作中比较习惯独来独往，总是按照自己的节奏完成任务。"
            }
        }
    },

    "dufei": {
        "name": "杜飞",
        "title": "杜飞收到的同事评价内容",
        "pages": {
            "summary": {
                "label": "总结报告",
                "content": "总结报告：综合来看，杜飞共收到5条同事评价，其中2条为正面评价（绿色标签），3条为负面评价（红色标签）。该员工在沟通效率和专业能力方面表现较好，但在团队参与、人际支持和冲突处理方面仍存在一定不足。"
            },
            "chenyu": {
                "label": "陈宇",
                "content": "陈宇：杜飞在办公室里一向给人较为友善、随和的印象，与同事相处时态度真诚，也愿意主动与他人沟通交流，他的人缘一直不错。平时如果同事在工作中遇到一些临时性的困难，只要在他能力范围之内，他通常都会主动为同事提供帮助。大家普遍认为他是一个比较容易相处、合作意愿较强、沟通能力较强的人。"
            },
            "zhangliang": {
                "label": "张亮",
                "content": "张亮：杜飞在面对需要作出判断的工作情境时，通常表现得较为果断，能够在较短时间内分析情况并提出相对明确的处理方案。在一些需要快速推进的工作中，这一特点对团队运转是很有帮助的。他对同事需求的回应也比较及时，无论是当面沟通还是通过微信、邮件联系，通常都能够较快给出反馈。与他交流时，不需要花太多时间反复确认意思。"
            },
            "liuli": {
                "label": "刘莉",
                "content": "刘莉：在数据管理相关知识与技术方面，杜飞的掌握程度相对有限，对这些技术在实际工作中的应用也不算熟练。公司目前许多事务已经逐步转向自动化销售流程管理系统，数据管理和分析能力是一个优秀销售人员所需具备的，但他对相关工具和功能的熟悉程度明显不高，一些别人已经能够较熟练完成的操作，他往往仍需要进一步摸索。"
            },
            "zhaohong": {
                "label": "赵洪",
                "content": "赵洪：在会议组织方面，杜飞的表现相对一般。他虽然会参与办公室例会，但通常不会主动承担主持角色。他往往倾向于跟随已有节奏，而不是主动推动会议进程。即便由他负责安排会议，他在议题顺序、讨论重点和时间分配上的把控也不算十分清晰，有时会出现某些内容讨论过多、而关键议题展开不足的情况。他更适合作为参与者发表有用的看法，而不是作为会议的主持者。"
            },
            "wuzhou": {
                "label": "吴洲",
                "content": "吴洲：在处理分歧和矛盾方面，杜飞通常表现得较为积极。很多时候，当讨论陷入僵持或双方表达不够顺畅时，他也会主动提出一些较为务实的建议，帮助大家重新理清问题并寻找可行的解决方式。正因为如此，在遇到一些不太容易处理的团队协调问题或客户问题时，不少同事都愿意先与他交流，听取他的看法。他在面对矛盾时所表现出的介入意愿和协调能力，确实能够增强团队内部的沟通顺畅度。"
            }
        }
    }
}


login_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>登录</title>
</head>
<body>
    <h2>请输入用户ID</h2>

    <form method="POST" action="/login">
        <input type="text" name="user_id" required>
        <button type="submit">确认</button>
    </form>
</body>
</html>
"""


main_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>阅读页面</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            display: flex;
            height: 100vh;
        }

        .sidebar {
            width: 180px;
            background-color: #f2f2f2;
            padding: 20px;
            border-right: 1px solid #ddd;
            box-sizing: border-box;
        }

        .sidebar button {
            display: block;
            width: 100%;
            padding: 12px;
            margin-bottom: 10px;
            cursor: pointer;
            font-size: 16px;
        }
        
        .red-button {
    background-color: #d9534f;
    color: white;
    border: none;
}

.green-button {
    background-color: #5cb85c;
    color: white;
    border: none;
}

.blue-button {
    background-color: #337ab7;
    color: white;
    border: none;
}

       .content {
    flex: 1;
    padding: 50px 70px;
    font-size: 26px;
    line-height: 2.1;
    letter-spacing: 1.2px;
}

#page-content {
    font-size: 28px;
    line-height: 2.2;
    letter-spacing: 1.5px;
    max-width: 1000px;
}

#page-title {
    font-size: 34px;
    letter-spacing: 1px;
}

        .employee-indicator {
            font-size: 18px;
            color: #555;
            margin-bottom: 20px;
        }

        .bottom-button {
            position: fixed;
            right: 30px;
            bottom: 30px;
            padding: 12px 24px;
            background-color: #444;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
        }
        
        .back-button {
    position: fixed;
    left: 30px;
    bottom: 30px;
    padding: 12px 24px;
    background-color: #444;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
}

    </style>
</head>

<body>
<div class="sidebar">
    {% for page_key, page_value in current_employee.pages.items() %}

        {% if page_key == "summary" %}
            <button class="blue-button" onclick="switchPage('{{ page_key }}')">{{ page_value.label }}</button>

        {% elif current_employee_key == "jiasheng" and page_key in ["chenyu", "zhaohong", "wuzhou"] %}
            <button class="red-button" onclick="switchPage('{{ page_key }}')">{{ page_value.label }}</button>

        {% elif current_employee_key == "jiasheng" and page_key in ["zhangliang", "liuli"] %}
            <button class="green-button" onclick="switchPage('{{ page_key }}')">{{ page_value.label }}</button>

        {% elif current_employee_key == "dufei" and page_key in ["liuli", "zhaohong"] %}
            <button class="red-button" onclick="switchPage('{{ page_key }}')">{{ page_value.label }}</button>

        {% elif current_employee_key == "dufei" and page_key in ["chenyu", "zhangliang", "wuzhou"] %}
            <button class="green-button" onclick="switchPage('{{ page_key }}')">{{ page_value.label }}</button>

        {% else %}
            <button onclick="switchPage('{{ page_key }}')">{{ page_value.label }}</button>
        {% endif %}

    {% endfor %}
</div>

    <div class="content">
        <div class="employee-indicator">
            当前阅读对象：{{ current_employee.name }}
        </div>

        <h1 id="page-title">{{ current_employee.title }}</h1>
        <p id="page-content">{{ current_employee.pages["summary"]["content"] }}</p>
    </div>

  {% if is_last_employee %}
    <button class="back-button" onclick="goToPreviousEmployee()">返回上一位候选人</button>
    <button class="bottom-button" onclick="goToResponsePage()">继续</button>
{% else %}
    <button class="bottom-button" onclick="goToNextEmployee()">下一位候选人</button>
{% endif %}

    <script>
        const currentEmployeeKey = "{{ current_employee_key }}";
        const pages = {{ current_employee.pages | tojson }};

        let currentPage = "summary";
        let startTime = Date.now();

       let readingTimes = {
    "summary": 0,
    "chenyu": 0,
    "zhangliang": 0,
    "liuli": 0,
    "zhaohong": 0,
    "wuzhou": 0
};

let readingEvents = [];
let visitOrder = 1;

function recordTime() {
    const now = Date.now();
    const seconds = (now - startTime) / 1000;

    if (readingTimes.hasOwnProperty(currentPage)) {
        readingTimes[currentPage] += seconds;

        readingEvents.push({
            employee_key: currentEmployeeKey,
            page_key: currentPage,
            visit_order: visitOrder,
            duration_seconds: seconds
        });

        visitOrder += 1;
    }

    startTime = now;
}

        function switchPage(pageName) {
            recordTime();

            currentPage = pageName;

            document.getElementById("page-title").innerText = "{{ current_employee.title }}";
            document.getElementById("page-content").innerText = pages[pageName]["content"];

            startTime = Date.now();
        }

        function saveCurrentEmployeeTimes(nextUrl) {
            recordTime();

            fetch("/save_current_employee", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    employee_key: currentEmployeeKey,
                    reading_times: readingTimes,
                    reading_events: readingEvents
                })
            })
            .then(response => response.text())
            .then(data => {
                window.location.href = nextUrl;
            });
        }

        function goToNextEmployee() {
    saveCurrentEmployeeTimes("/next_employee");
}

function goToPreviousEmployee() {
    saveCurrentEmployeeTimes("/previous_employee");
}

function goToResponsePage() {
    saveCurrentEmployeeTimes("/response");
}

    </script>
</body>
</html>
"""

response_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>评价回顾</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 60px;
            line-height: 1.8;
            font-size: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        textarea {
            width: 100%;
            height: 260px;
            font-size: 18px;
            line-height: 1.6;
            padding: 12px;
            box-sizing: border-box;
            margin-top: 20px;
        }

        button {
            margin-top: 30px;
            padding: 12px 28px;
            font-size: 18px;
            background-color: #444;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            float: right;
        }
    </style>
</head>

<body>
    <div class="container">
        <p>
            请回顾刚才的同事评价材料。你在评价判断两名员工时，最关注的是哪些信息？
            请尽量用自己的话写出对你影响最大的信息内容，并说明这些信息是如何影响你的判断的。
        </p>

        <form method="POST" action="/save_response_and_exit">
            <textarea name="text_response" required></textarea>

            <p>
                感谢你已完成实验任务，请点击“保存并退出”后关闭本网页。
            </p>

            <button type="submit">保存并退出</button>
        </form>
    </div>
</body>
</html>
"""

finished_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>结束</title>
</head>
<body>
    <h2>实验已结束，数据已保存。</h2>
    <p>如果页面没有自动关闭，请手动关闭该网页。</p>

    <script>
        window.close();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(login_html)


@app.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id")

    if not user_id:
        return redirect(url_for("index"))

    employee_order = ["jiasheng", "dufei"]
    random.shuffle(employee_order)

    session["user_id"] = user_id
    session["employee_order"] = employee_order
    session["current_index"] = 0
    session["reading_data"] = {}
    session["event_data"] = {}

    return redirect(url_for("main"))


@app.route("/main")
def main():
    if "user_id" not in session:
        return redirect(url_for("index"))

    employee_order = session["employee_order"]
    current_index = session["current_index"]

    current_employee_key = employee_order[current_index]
    current_employee = employees[current_employee_key]

    is_last_employee = current_index == len(employee_order) - 1

    return render_template_string(
        main_html,
        current_employee_key=current_employee_key,
        current_employee=current_employee,
        is_last_employee=is_last_employee
    )

@app.route("/save_current_employee", methods=["POST"])
def save_current_employee():
    if "user_id" not in session:
        return "No user ID", 400

    data = request.get_json()
    employee_key = data.get("employee_key")
    reading_times = data.get("reading_times", {})
    reading_events = data.get("reading_events", [])

    # 累计保存 summary 数据
    reading_data = session.get("reading_data", {})
    existing_times = reading_data.get(employee_key, {})

    for page_key, seconds in reading_times.items():
        existing_times[page_key] = existing_times.get(page_key, 0) + seconds

    reading_data[employee_key] = existing_times
    session["reading_data"] = reading_data

    # 累计保存 event 数据
    event_data = session.get("event_data", {})
    existing_events = event_data.get(employee_key, [])

    current_event_count = len(existing_events)

    for event in reading_events:
        event["visit_order"] = current_event_count + event.get("visit_order", 0)

    existing_events.extend(reading_events)

    event_data[employee_key] = existing_events
    session["event_data"] = event_data

    return "saved"


@app.route("/next_employee")
def next_employee():
    if "user_id" not in session:
        return redirect(url_for("index"))

    current_index = session.get("current_index", 0)
    session["current_index"] = current_index + 1

    return redirect(url_for("main"))

@app.route("/previous_employee")
def previous_employee():
    if "user_id" not in session:
        return redirect(url_for("index"))

    current_index = session.get("current_index", 0)

    if current_index > 0:
        session["current_index"] = current_index - 1

    return redirect(url_for("main"))

@app.route("/response")
def response_page():
    if "user_id" not in session:
        return redirect(url_for("index"))

    return render_template_string(response_html)

@app.route("/save_response_and_exit", methods=["POST"])
def save_response_and_exit():
    if "user_id" not in session:
        return redirect(url_for("index"))

    text_response = request.form.get("text_response", "")

    user_id = session["user_id"]
    employee_order = session["employee_order"]
    reading_data = session.get("reading_data", {})
    event_data = session.get("event_data", {})

    # 保存累计阅读时长
    summary_file_exists = os.path.exists(SUMMARY_FILE)

    with open(SUMMARY_FILE, mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        if not summary_file_exists:
            writer.writerow([
                "timestamp",
                "user_id",
                "employee_order",

                "jiasheng_summary_seconds",
                "jiasheng_chenyu_seconds",
                "jiasheng_zhangliang_seconds",
                "jiasheng_liuli_seconds",
                "jiasheng_zhaohong_seconds",
                "jiasheng_wuzhou_seconds",

                "dufei_summary_seconds",
                "dufei_chenyu_seconds",
                "dufei_zhangliang_seconds",
                "dufei_liuli_seconds",
                "dufei_zhaohong_seconds",
                "dufei_wuzhou_seconds"
            ])

        jiasheng_times = reading_data.get("jiasheng", {})
        dufei_times = reading_data.get("dufei", {})

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id,
            " -> ".join(employee_order),

            round(jiasheng_times.get("summary", 0), 2),
            round(jiasheng_times.get("chenyu", 0), 2),
            round(jiasheng_times.get("zhangliang", 0), 2),
            round(jiasheng_times.get("liuli", 0), 2),
            round(jiasheng_times.get("zhaohong", 0), 2),
            round(jiasheng_times.get("wuzhou", 0), 2),

            round(dufei_times.get("summary", 0), 2),
            round(dufei_times.get("chenyu", 0), 2),
            round(dufei_times.get("zhangliang", 0), 2),
            round(dufei_times.get("liuli", 0), 2),
            round(dufei_times.get("zhaohong", 0), 2),
            round(dufei_times.get("wuzhou", 0), 2),
        ])

    # 保存逐次阅读记录
    event_file_exists = os.path.exists(EVENT_FILE)

    with open(EVENT_FILE, mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        if not event_file_exists:
            writer.writerow([
                "timestamp",
                "user_id",
                "employee_order",
                "employee",
                "page",
                "visit_order",
                "duration_seconds"
            ])

        for employee_key in employee_order:
            events = event_data.get(employee_key, [])

            for event in events:
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    user_id,
                    " -> ".join(employee_order),
                    employee_key,
                    event.get("page_key"),
                    event.get("visit_order"),
                    round(event.get("duration_seconds", 0), 2)
                ])

    # 保存文本回答
    response_file_exists = os.path.exists(RESPONSE_FILE)

    with open(RESPONSE_FILE, mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        if not response_file_exists:
            writer.writerow([
                "timestamp",
                "user_id",
                "employee_order",
                "text_response"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id,
            " -> ".join(employee_order),
            text_response
        ])

    session.clear()
    return redirect(url_for("finished"))


@app.route("/finished")
def finished():
    return render_template_string(finished_html)


if __name__ == "__main__":
    app.run(debug=True, port=5001)