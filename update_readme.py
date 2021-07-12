from datetime import timezone
import git
import pathlib
import re
import sqlite_utils
import sys


ROOT_PATH = pathlib.Path(__file__).parent.resolve()

INDEX_REGEX = re.compile(r"<!\-\- TILs start \-\->.*<!\-\- TILs end \-\->", re.DOTALL)
COUNT_REGEX = re.compile(r"<!\-\- Count starts \-\->.*<!\-\- Count ends \-\->", re.DOTALL)

COUNT_TEMPLATE = "<!-- Count starts -->{}<!-- Count ends -->"


def created_changed_times(repo_path, ref="main"):
    created_changed_times = {}
    repo = git.Repo(repo_path, odbt=git.GitDB)
    commits = reversed(list(repo.iter_commits(ref)))
    for commit in commits:
        dt = commit.committed_datetime
        affected_files = list(commit.stats.files.keys())
        for filepath in affected_files:
            correct_path = ""
            if " => " in filepath:
                chunks = filepath.split("/")
                for chunk in chunks:
                    if " => " in chunk:
                        chunk = chunk.strip("{").strip("}").split(" => ")[1]
                    correct_path += chunk + "/"
                correct_path = correct_path[:-1]
            else:
                correct_path = filepath
            if correct_path not in created_changed_times:
                created_changed_times[correct_path] = {
                    "updated": dt.isoformat(),
                    "updated_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            created_changed_times[correct_path].update(
                {
                    "updated": dt.isoformat(),
                    "updated_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            )
    return created_changed_times


def build_database(repo_path):
    all_times = created_changed_times(repo_path)
    db = sqlite_utils.Database(ROOT_PATH / "til.db")
    table = db.table("til", pk="path")
    for filepath in ROOT_PATH.glob("*/*.md"):
        fp = filepath.open()
        title = fp.readline().lstrip("#").strip()
        body = fp.read().strip()
        path = str(filepath.relative_to(ROOT_PATH))
        url = "https://github.com/fosdickio/til/blob/main/{}".format(path)
        record = {
            "path": path,
            "topic": path.split("/")[0],
            "title": title,
            "url": url,
            "body": body
        }
        if path in all_times:
            record.update(all_times[path])
        else:
            raise RuntimeError("{} not found in all_time.".format(path))
        with db.conn:
            table.upsert(record, alter=True)
    if "til_fts" not in db.table_names():
        table.enable_fts(["title", "body"])


def update_readme():
    db = sqlite_utils.Database(ROOT_PATH / "til.db")
    by_topic = {}
    for row in db["til"].rows_where(order_by="topic"):
        by_topic.setdefault(row["topic"], []).append(row)
    index = ["<!-- TILs start -->"]
    for topic, rows in by_topic.items():
        index.append("## {}\n".format(topic))
        rows.sort()
        for row in rows:
            index.append("- [{}]({}) ({})".format(row["title"], row["url"], row["updated"].split("T")[0]))
        index.append("")
    if index[-1] == "":
        index.pop()
    index.append("<!-- TILs end -->")
    if "--rewrite" in sys.argv:
        readme = ROOT_PATH / "README.md"
        index_txt = "\n".join(index).strip()
        readme_contents = readme.open().read()
        rewritten = INDEX_REGEX.sub(index_txt, readme_contents)
        rewritten = COUNT_REGEX.sub(COUNT_TEMPLATE.format(db["til"].count), rewritten)
        readme.open("w").write(rewritten)
    else:
        print("\n".join(index))


if __name__ == "__main__":
    build_database(ROOT_PATH)
    update_readme()
