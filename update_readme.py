import pathlib
import sqlite_utils
import sys
import re


ROOT_PATH = pathlib.Path(__file__).parent.resolve()

INDEX_REGEX = re.compile(r"<!\-\- TILs start \-\->.*<!\-\- TILs end \-\->", re.DOTALL)
COUNT_REGEX = re.compile(r"<!\-\- Count starts \-\->.*<!\-\- Count ends \-\->", re.DOTALL)

COUNT_TEMPLATE = "<!-- Count starts -->{}<!-- Count ends -->"


def build_database():
    db = sqlite_utils.Database(ROOT_PATH / "til.db")
    table = db.table("til", pk="path")
    for filepath in ROOT_PATH.glob("*/*.md"):
        fp = filepath.open()
        title = fp.readline().lstrip("#").strip()
        body = fp.read().strip()
        path = str(filepath.relative_to(ROOT_PATH))
        url = "https://github.com/fosdickio/til/blob/main/{}".format(path)
        record = {
            "path": path.replace("/", "_"),
            "topic": path.split("/")[0],
            "title": title,
            "url": url,
            "body": body,
        }
        table.insert(record)
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
        for row in rows:
            index.append(
                "- [{title}]({url})".format(
                    date=row["title"].split("T")[0], **row
                )
            )
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
    build_database()
    update_readme()
